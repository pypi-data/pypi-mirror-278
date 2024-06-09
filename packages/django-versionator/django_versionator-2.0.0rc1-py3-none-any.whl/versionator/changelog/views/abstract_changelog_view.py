from django.views.generic import TemplateView

from versionator.changelog.new_changelog import Changelog


class AbstractChangelogView(TemplateView):

    def get_graphql_variables(self):
        page_num = self.kwargs.get("page_num", 1)
        return {
            "page_num": page_num,
        }

    def get_changelog_config(self):
        if not hasattr(self, "changelog_config"):
            raise NotImplementedError(
                "You must define a `changelog_config` attribute on your view or override `get_changelog_config` method"
            )

    def get_changelog_data(self):
        changelog = Changelog(self.get_changelog_config())
        page_num = self.kwargs.get("page_num", 1)
        entries = changelog.get_entries(page_num)

        num_pages = changelog.get_num_pages()

        has_next_page = page_num < num_pages

        entries_without_diffs = [entry for entry in entries if not entry.diffs]

        prev_page = None
        next_page = None

        if page_num > 1:
            prev_page = page_num - 1

        if has_next_page:
            next_page = page_num + 1

        return {
            "entries_without_diffs": entries_without_diffs,
            "entries": entries,
            "prev_page_num": prev_page,
            "next_page_num": next_page,
            "num_pages": num_pages,
            "page_num": page_num,
        }

    def get_context_data(self, *args, **kwargs):
        changelog_context_data = self.get_changelog_data()
        return {
            **super().get_context_data(*args, **kwargs),
            **changelog_context_data,
        }
