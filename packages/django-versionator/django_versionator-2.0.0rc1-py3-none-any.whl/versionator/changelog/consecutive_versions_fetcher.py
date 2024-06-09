import operator
from collections import defaultdict
from functools import reduce

from django.core.paginator import Paginator
from django.db.models import CharField, F, OuterRef, Q, Subquery, Value
from django.utils.functional import cached_property

from data_fetcher import PrimaryKeyFetcherFactory

from versionator.changelog.diff import get_field_diff_for_version_pair
from versionator.changelog.new_changelog import ChangelogEntry
from versionator.changelog.util import get_diffable_fields_for_model

neverQ = Q(pk=None)
anyQ = ~neverQ

from .util import get_diffable_fields_for_model


# this class is used by the parent resolver. should we move it elsewhere ?
class ConsecutiveVersionsFetcher:
    def __init__(
        self,
        page_size,
        page_num,
        models,
        user_ids=None,
        exclude_create=False,
        only_creates=False,
        fields_by_model=None,
        start_date=None,
        end_date=None,
        config=None,
    ):
        if only_creates and (fields_by_model or exclude_create):
            raise Exception(
                "cant only show creations while excluding them or comparing specific fields"
            )

        self.page_num = page_num
        self.models = models
        self.page_size = page_size

        self.user_ids = user_ids
        self.fields_by_model = fields_by_model
        self.exclude_create = exclude_create or fields_by_model is not None
        self.only_creates = only_creates
        self.start_date = start_date
        self.end_date = end_date
        self.config = config

    @staticmethod
    def unionize_querysets(qs1, qs2):
        return qs1.union(qs2)

    def get_base_version_qs_for_single_model(self, live_model):
        """
        You can override this to allow for custom extra filtering
        """
        history_model = live_model._history_class
        return history_model.objects.all()

    def _get_values_qs_for_single_model(self, live_model):
        history_model = live_model._history_class

        base_qs = self.get_base_version_qs_for_single_model(live_model)

        user_filter = anyQ
        if self.user_ids:
            user_filter = Q(edited_by_id__in=self.user_ids)
        qs = base_qs.with_previous_version_id().filter(user_filter)

        if self.exclude_create:
            qs = qs.filter(previous_version_id__isnull=False)

        if self.only_creates:
            qs = qs.filter(previous_version_id__isnull=True)

        if self.start_date:
            qs = qs.filter(timestamp__gte=self.start_date)

        if self.end_date:
            qs = qs.filter(timestamp__lte=self.end_date)

        if self.fields_by_model and self.fields_by_model.get(live_model, None):
            field_names = self.fields_by_model[live_model]
            # also filter out creations when comparing specific fields
            qs = qs.filter(previous_version_id__isnull=False)

            field_objs = [
                f
                for f in get_diffable_fields_for_model(live_model)
                if f.name in field_names
            ]

            get_annotation_name = lambda field: f"_previous_{field.name}"
            for f in field_objs:
                prev_field_value_subquery = Subquery(
                    history_model.objects.filter(
                        id=OuterRef("previous_version_id")
                    ).values(f.attname)[:1]
                )

                qs = qs.annotate(
                    **{get_annotation_name(f): prev_field_value_subquery}
                )

            # once annotated, we can filter on any OR differences
            # the difference doesn't seem to check for nulls vs. values, so we check that manually
            field_difference_filters = [
                (
                    ~Q(**{get_annotation_name(field): F(field.attname)})
                    | (
                        Q(**{f"{get_annotation_name(field)}__isnull": False})
                        & Q(**{f"{field.attname}__isnull": True})
                    )
                    | (
                        Q(**{f"{get_annotation_name(field)}__isnull": True})
                        & Q(**{f"{field.attname}__isnull": False})
                    )
                )
                for field in field_objs
            ]
            combined_filter = reduce(
                operator.__or__, field_difference_filters, neverQ
            )

            qs = qs.filter(combined_filter)

        qs = (
            qs.annotate(model_name=Value(live_model.__name__, CharField()))
            .only(
                "timestamp",
                "id",
                "eternal_id",
                "model_name",
                "previous_version_id",
            )
            .order_by("-timestamp")
            .values(
                "timestamp",
                "id",
                "eternal_id",
                "model_name",
                "previous_version_id",
            )
        )

        return qs

    @cached_property
    def _page_obj(self):

        if self.fields_by_model:
            history_querysets = [
                self._get_values_qs_for_single_model(m)
                for m in self.fields_by_model.keys()
            ]
        else:
            history_querysets = [
                self._get_values_qs_for_single_model(m) for m in self.models
            ]

        qs_values_union = reduce(self.unionize_querysets, history_querysets)
        sorted_union = qs_values_union.order_by("-timestamp")
        paginated_qs = Paginator(sorted_union, self.page_size)
        page = paginated_qs.page(self.page_num)

        return page

    def get_total_entry_count(self):
        return self._page_obj.paginator.count

    def get_total_page_count(self):
        return self._page_obj.paginator.num_pages

    def get_fully_fetched_edit_entries(self):
        self.prefetch_entries_and_diff_dependencies()
        return self._fully_fetched_entries

    @cached_property
    def _fully_fetched_entries(self):
        """
        our paginated qs only hold id, previous_version_id, eternal_id and model_name in dicts
        """
        slim_versions = self._page_obj.object_list
        models_by_name = {m.__name__: m for m in self.models}

        eternal_ids_to_fetch_by_model = defaultdict(list)
        version_ids_to_fetch_by_model = defaultdict(list)

        for slim_ver in slim_versions:
            eternal_model = models_by_name[slim_ver["model_name"]]
            hist_model = eternal_model._history_class
            eternal_ids_to_fetch_by_model[eternal_model].append(
                slim_ver["eternal_id"]
            )
            version_ids_to_fetch_by_model[hist_model].append(slim_ver["id"])
            if slim_ver.get("previous_version_id", None):
                version_ids_to_fetch_by_model[hist_model].append(
                    slim_ver["previous_version_id"]
                )

        eternal_records_by_pair_id = {}
        version_records_by_pair_id = {}

        for model, ids in eternal_ids_to_fetch_by_model.items():
            for record in model.objects.filter(id__in=ids):
                eternal_records_by_pair_id[(model, record.id)] = record

        for model, ids in version_ids_to_fetch_by_model.items():
            for record in model.objects.filter(id__in=ids):
                version_records_by_pair_id[(model, record.id)] = record

        resolved_list = []
        for slim_ver in slim_versions:
            eternal_model = models_by_name[slim_ver["model_name"]]
            hist_model = eternal_model._history_class
            resolved = {}

            resolved["eternal"] = eternal_records_by_pair_id[
                (eternal_model, slim_ver["eternal_id"])
            ]

            resolved["version"] = version_records_by_pair_id[
                (hist_model, slim_ver["id"])
            ]

            if slim_ver.get("previous_version_id", None):
                resolved["previous_version"] = version_records_by_pair_id[
                    (hist_model, slim_ver["previous_version_id"])
                ]
            else:
                resolved["previous_version"] = None

            resolved_list.append(
                ChangelogEntry(
                    left_version=resolved["previous_version"],
                    right_version=resolved["version"],
                    eternal=resolved["eternal"],
                    config=self.config,
                )
            )

        return resolved_list

    def prefetch_entries_and_diff_dependencies(self):
        entries = self._fully_fetched_entries

        # fetch live names
        live_name_fetcher_dependencies = defaultdict(list)
        for entry in entries:
            eternal_instance = entry.eternal
            if hasattr(eternal_instance, "changelog_live_name_fetcher_class"):
                live_name_fetcher_dependencies[
                    eternal_instance.changelog_live_name_fetcher_class
                ].append(eternal_instance.id)

        for fetcher_cls, ids in live_name_fetcher_dependencies.items():
            fetcher = fetcher_cls.get_instance()
            fetcher.get_many(ids)

        # fetch authors
        author_ids = set()
        from django.contrib.auth import get_user_model

        for entry in entries:
            if getattr(entry.right_version, "edited_by_id", None):
                author_ids.add(entry.right_version.edited_by_id)

        user_fetcher = PrimaryKeyFetcherFactory.get_model_by_id_fetcher(
            get_user_model()
        ).get_instance()
        user_fetcher.get_many_lazy(author_ids)

        # fetch diffs
        # now we fetch diffs, much more challenging, different fetchers are used in different cases
        # we will need some kind of polymorphism here so that different field-configs
        # can expose their dependencies
        for entry in entries:
            model = entry.eternal.__class__
            # TODO: we need to filter the fields being diffed based on arguments
            # rather than look into GQL query info
            # this will be fixed later when we change the API
            prev_version = entry.left_version
            this_version = entry.right_version
            if not prev_version:
                continue

            fields_to_diff = get_diffable_fields_for_model(
                this_version.live_model
            )
            for f in fields_to_diff:
                diff_obj = get_field_diff_for_version_pair(
                    this_version, prev_version, f
                )
                if diff_obj and hasattr(diff_obj, "queue_dependencies"):
                    diff_obj.queue_dependencies()


class SingleRecordConsecutiveVersionsFetcher(ConsecutiveVersionsFetcher):
    def __init__(self, page_size, page_num, model, primary_key=None):
        super().__init__(
            page_num=page_num,
            page_size=page_size,
            models=[model],
        )
        self.primary_key = primary_key

    def get_base_version_qs_for_single_model(self, live_model):
        history_model = live_model._history_class
        return history_model.objects.filter(eternal_id=self.primary_key)
