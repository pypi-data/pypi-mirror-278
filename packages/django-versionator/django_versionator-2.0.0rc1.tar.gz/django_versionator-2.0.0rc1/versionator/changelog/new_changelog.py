from functools import lru_cache
from typing import List

from django.db.models import Model
from django.utils.functional import cached_property

from versionator.changelog.util import get_diffable_fields_for_model
from versionator.core import VersionModel

from .diff import CreateDiff, DeleteDiff, get_field_diff_for_version_pair

EXCLUDE_CREATES = "exlude_creates"
INCLUDE_CREATES = "include_creates"
ONLY_CREATES = "only_creates"

CREATE_MODES = [EXCLUDE_CREATES, INCLUDE_CREATES, ONLY_CREATES]


class ChangelogConfig:
    models = None
    page_size = 50
    start_date = None
    end_date = None
    fetcher_class = None
    create_mode = INCLUDE_CREATES

    def __init__(
        self, models=None, start_date=None, end_date=None, page_size=None
    ):
        if models:
            self.models = models
        if start_date:
            self.start_date = start_date
        if end_date:
            self.end_date = end_date
        if page_size:
            self.page_size = page_size

    def get_models(self) -> List[type]:
        if self.models:
            return self.models

        raise NotImplementedError(
            "You must implement get_models or define a models iterable"
        )

    def get_fields(self):
        if not hasattr(self, "fields"):
            return None

    def get_page_size(self) -> int:
        return self.page_size

    def get_user_ids(self):
        if not hasattr(self, "user_ids"):
            return None

    def get_create_mode(self) -> str:
        return self.create_mode

    def get_fetcher_class(self) -> type:
        from versionator.changelog.consecutive_versions_fetcher import (
            ConsecutiveVersionsFetcher,
        )

        return ConsecutiveVersionsFetcher

    def get_start_date(self):
        return self.start_date

    def get_end_date(self):
        return self.end_date


class ChangelogEntry:
    def __init__(
        self,
        left_version: VersionModel,
        right_version: VersionModel,
        eternal: Model,
        config: ChangelogConfig,
    ):
        self.left_version = left_version
        self.right_version = right_version
        self.eternal = eternal
        self.config = config

    def get_diffs(self) -> List:

        if self.left_version is None and self.right_version is not None:
            return [CreateDiff()]

        if self.left_version is not None and self.right_version is None:
            return [DeleteDiff()]

        specified_fields = self.config.get_fields()
        diffable_fields = get_diffable_fields_for_model(self.eternal.__class__)
        fields_to_diff = diffable_fields
        if specified_fields:
            fields_to_diff = [
                field for field in diffable_fields if field in specified_fields
            ]

        diffs = []
        for field in fields_to_diff:
            diff_obj = get_field_diff_for_version_pair(
                self.right_version,
                self.left_version,
                field,
            )
            if diff_obj is not None:
                diffs.append(diff_obj)

        return diffs

    @cached_property
    def diffs(self):
        return self.get_diffs()

    def queue_deps(self):
        # TODO: return promised diffs and live names ??
        # maybe this is just taken care of by the fetcher
        pass

    @cached_property
    def live_name(self):
        live_obj = self.eternal

        if hasattr(live_obj, "changelog_live_name_fetcher_class"):
            fetcher = live_obj.changelog_live_name_fetcher_class.get_instance()
            return fetcher.get(live_obj.id)

        if hasattr(live_obj, "name"):
            return live_obj.name

        return live_obj.__str__()


class Changelog:
    def __init__(self, config: ChangelogConfig):
        self.config = config
        self._get_fetcher = lru_cache(maxsize=None)(self._get_fetcher)

    def _get_fetcher(self, page_num):
        #  FETCHER API REFACTOR TODO
        FetcherCls = self.config.get_fetcher_class()
        fetcher = FetcherCls(
            page_size=self.config.get_page_size(),
            page_num=page_num,
            models=self.config.get_models(),
            user_ids=self.config.get_user_ids(),
            exclude_create=self.config.get_create_mode() == EXCLUDE_CREATES,
            only_creates=self.config.get_create_mode() == ONLY_CREATES,
            fields_by_model=self.config.get_fields(),
            start_date=self.config.get_start_date(),
            end_date=self.config.get_end_date(),
            # TODO: replace all of these kwargs with a single config object
            config=self.config,
        )
        return fetcher

    def get_entries(self, page_num: int) -> List[ChangelogEntry]:
        fetcher = self._get_fetcher(page_num)
        fetcher.prefetch_entries_and_diff_dependencies()
        return fetcher.get_fully_fetched_edit_entries()

    def get_num_pages(self) -> int:
        fetcher = self._get_fetcher(1)
        return fetcher.get_total_page_count()

    def get_total_entry_count(self) -> int:
        fetcher = self._get_fetcher(1)
        return fetcher.get_total_entry_count()
