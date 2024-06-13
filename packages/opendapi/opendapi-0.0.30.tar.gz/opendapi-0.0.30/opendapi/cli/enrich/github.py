"""Enricher to work from Github as part of `opendapi enrich` CLI command."""

# pylint: disable=unnecessary-pass
import functools
import json
from typing import Callable, List, Optional

import click

from opendapi.adapters.dapi_server import DAPIServerResponse
from opendapi.adapters.git import (
    add_untracked_opendapi_files,
    get_changed_opendapi_filenames,
    run_git_command,
)
from opendapi.adapters.github import GithubAdapter
from opendapi.cli.enrich.local import Enricher
from opendapi.logging import LogCounterKey, increment_counter


class GithubEnricherException(click.ClickException):
    """Exception raised due to errors in the Github enricher."""

    pass


class FailGithubAction(click.ClickException):
    """Exception that will be raised to fail the Github action."""

    pass


class GithubEnricher(Enricher):
    """Enricher to work from Github as part of `opendapi enrich` CLI command."""

    GENERATED_COMMENT_IDENTIFIER = "<!-- OpenDAPI Comment Identifier -->"

    def setup_objects(self):
        """Initialize the adapter."""
        self.github_adapter: GithubAdapter = GithubAdapter(
            self.trigger_event.repo_api_url,
            self.trigger_event.auth_token,
            exception_cls=click.ClickException,
        )
        self.autoupdate_pr_number: Optional[int] = None
        super().setup_objects()

    def should_enrich(self) -> bool:
        """Should we enrich the DAPI files?"""
        return (
            self.dapi_server_config.suggest_changes
            and self.trigger_event.is_pull_request_event
        )

    def should_register(self) -> bool:
        """Should we register the DAPI files?"""
        if (
            self.dapi_server_config.register_on_merge_to_mainline
            and self.trigger_event.is_push_event
            and self.trigger_event.git_ref
            == f"refs/heads/{self.dapi_server_config.mainline_branch_name}"
        ):
            return True

        self.print_markdown_and_text(
            "Registration skipped because the conditions weren't met",
            color="yellow",
        )
        return False

    def should_analyze_impact(self) -> bool:
        return self.trigger_event.is_pull_request_event

    def print_dapi_server_progress(self, progressbar, progress: int):
        """Print the progress bar for validation."""
        progressbar.update(progress)
        self.print_text_message(
            f"\nFinished {round(progressbar.pct * 100)}% with {progressbar.format_eta()} remaining",
            color="green",
            bold=True,
        )

    def get_current_branch_name(self):
        """Get the current branch name."""
        return (
            run_git_command(self.root_dir, ["git", "rev-parse", "--abbrev-ref", "HEAD"])
            .decode("utf-8")
            .strip()
        )

    def get_autoupdate_branch_name(self):
        """Get the autoupdate branch name."""
        return f"opendapi-autoupdate-for-{self.trigger_event.pull_request_number}"

    def add_pull_request_comment(self, message: str):
        """Add a comment to the pull request."""
        message_with_identifier = f"{message}{self.GENERATED_COMMENT_IDENTIFIER}"
        self.github_adapter.add_pull_request_comment(
            self.trigger_event.pull_request_number, message_with_identifier
        )

    def update_pull_request_comment(self, comment_id: int, message: str):
        """Update a comment on the pull request."""
        message_with_identifier = f"{message}{self.GENERATED_COMMENT_IDENTIFIER}"
        self.github_adapter.update_pull_request_comment(
            comment_id, message_with_identifier
        )

    @functools.cached_property
    def existing_opendapi_comment_id(self) -> Optional[int]:
        """Get the existing OpenDAPI comment id."""
        # NOTE: we should create a PR entity on the server, to store things like
        # opendapi comment_id, last checked time, etc. - this is an interim solution

        # the comment user is just github-bot, would not know its Woven related, hack for now
        comment_id_index = -1 * len(self.GENERATED_COMMENT_IDENTIFIER)
        for comment in self.github_adapter.get_pull_request_comments(
            self.trigger_event.pull_request_number
        ):
            if (comment["body"] or "")[
                comment_id_index:
            ] == self.GENERATED_COMMENT_IDENTIFIER:
                return comment["id"]

        return None

    def add_or_update_pull_request_comment(self, message: str):
        """Add or update a comment on the pull request."""
        if comment_id := self.existing_opendapi_comment_id:
            self.update_pull_request_comment(comment_id, message)
        else:
            self.add_pull_request_comment(message)

    def get_base_for_changed_files(self):
        """
        Get the base branch for the changed files.

        On Github and PRs, first check if an earlier autoupdate PR was merged,
        and use that as the base commit
        if not, use the base branch of the current PR.
        """
        if self.trigger_event.is_pull_request_event:
            merged_prs = self.github_adapter.get_merged_pull_requests_cached(
                self.trigger_event.repo_owner,
                self.get_current_branch_name(),
                self.get_autoupdate_branch_name(),
            )
            if merged_prs:
                merge_commit = merged_prs[0]["merge_commit_sha"]
                # check if the merge commit is in the current PR
                try:
                    git_merge_commit = run_git_command(
                        self.root_dir,
                        [
                            "git",
                            "merge-base",
                            merge_commit,
                            self.trigger_event.after_change_sha,
                        ],
                    )
                    if git_merge_commit.decode("utf-8").strip() == merge_commit:
                        return merge_commit
                except RuntimeError:
                    # if the merge commit is not in the current PR, use the base branch
                    pass
        return super().get_base_for_changed_files()

    def create_pull_request_for_changes(self) -> int:
        """
        Create a pull request for any changes made to the DAPI files.
        """

        # if there are no dapi file changes, there is nothing to create a PR for
        if not get_changed_opendapi_filenames(self.root_dir):
            raise GithubEnricherException(
                "No OpenDAPI files found to create a pull request"
            )

        self.print_markdown_and_text(
            "Creating a pull request for the changes...",
            color="green",
        )

        # Set git user and email
        git_config_map = {
            "user.email": self.validate_response.server_meta.github_user_email,
            "user.name": self.validate_response.server_meta.github_user_name,
        }
        for config, value in git_config_map.items():
            run_git_command(self.root_dir, ["git", "config", "--global", config, value])

        # get current branch name
        current_branch_name = self.get_current_branch_name()

        # Unique name for the new branch
        update_branch_name = self.get_autoupdate_branch_name()

        # Checkout new branch. Force reset if branch already exists,
        # including uncommited changes
        run_git_command(self.root_dir, ["git", "checkout", "-B", update_branch_name])

        # Add the relevant files
        add_untracked_opendapi_files(self.root_dir)

        # Commit the changes
        run_git_command(
            self.root_dir,
            [
                "git",
                "commit",
                "-m",
                f"OpenDAPI updates for {self.trigger_event.pull_request_number}",
            ],
        )

        # Push the changes. Force push to overwrite any existing branch
        run_git_command(
            self.root_dir,
            [
                "git",
                "push",
                "-f",
                "origin",
                f"HEAD:refs/heads/{update_branch_name}",
            ],
        )

        # construct the PR body

        # NOTE: current iteration no longer includes Title markdown
        # please reference commits before 2024-06-05 for the previous implementation

        # IMPORTANT section
        body = (
            "> [!IMPORTANT]\n"
            "> **This PR was auto-generated to sync your metadata with "
            f"schema changes in PR #{self.trigger_event.pull_request_number}.** Please review, "
            "revise[^HowToEditDAPI], and merge this PR to your branch.\n"
            ">\n"
            "> Code-synced metadata instills trust[^WhyMetadataMatters] in "
            "data discovery, quality, and compliance. If you have "
            "questions, reach out to Data Engineering.[^Feedback]\n\n"
        )

        # Footer
        body += (
            "[^WhyMetadataMatters]: Learn more about why code-synced metadata matters "
            "[here](https://www.wovencollab.com/docs)\n"
            "[^HowToEditDAPI]: Watch "
            "[a quick video](https://www.wovencollab.com/howto/edit-metadata-in-github) "
            "to see how to revise metadata suggestions\n"
            "[^Feedback]: Did you find this useful? If you found a bug or have an idea to "
            "improve the DevX, [let us know](https://www.wovencollab.com/feedback)"
        )

        self.autoupdate_pr_number = (  # pylint: disable=attribute-defined-outside-init
            self.github_adapter.create_pull_request_if_not_exists(
                self.trigger_event.repo_owner,
                title=(
                    f"Metadata updates for #{self.trigger_event.pull_request_number}"
                ),
                body=body,
                base=current_branch_name,
                head=update_branch_name,
            )
        )

        # ALWAYS Reset by checking out the original branch
        run_git_command(self.root_dir, ["git", "checkout", current_branch_name])
        return self.autoupdate_pr_number

    @staticmethod
    def _create_summary_comment(body: str):
        """Create a summary comment."""
        header = (
            "> [!WARNING]\n"
            "> This PR updates a data schema. You are responsible for keeping schema metadata "
            "in-sync with source code and keeping stakeholders informed.\n\n"
        )
        footer = (
            "<hr>\n\n"
            "<sup>Did you find this useful? If you found a bug or have an idea to improve the "
            "DevX, [let us know](https://www.wovencollab.com/feedback)</sup>"
        )
        return f"{header}{body}{footer}"

    def create_or_update_summary_comment_metadata_merged(self):
        """Create a summary comment on the pull request for when metadata updates merged"""

        pr_comment_md = "# Schema metadata synced! :tada:\n\n"
        merged_prs = self.github_adapter.get_merged_pull_requests_cached(
            self.trigger_event.repo_owner,
            self.get_current_branch_name(),
            self.get_autoupdate_branch_name(),
        )

        # if we are in the else clause, there should be a merged PR, but just in case
        pr_stanza = (
            f"PR #{merged_prs[0]['number']}" if merged_prs else "A Woven-generated PR"
        )

        pr_comment_md += (
            f"This PR contains a schema change. {pr_stanza} was merged into this branch "
            "to keep your metadata in-sync with these changes.\n\n"
        )

        # Impact Response
        if self.analyze_impact_response.compiled_markdown:
            pr_comment_md += self.analyze_impact_response.compiled_markdown
            pr_comment_md += "\n\n"

        self.add_or_update_pull_request_comment(
            self._create_summary_comment(pr_comment_md)
        )

    def create_or_update_summary_comment_metadata_unmerged(
        self,
        autoupdate_pull_request_number: int,
    ):
        """Create a summary comment on the pull request for when metadata updates unmerged"""

        # Update schema section
        pr_comment_md = (
            "# Update your schema metadata\n\n"
            f"This PR contains a schema change. PR #{autoupdate_pull_request_number} "
            "was auto-generated to keep your metadata in-sync with these changes. "
            "Please review, revise, and merge this metadata update into this branch.\n\n"
        )

        # Review suggestion button
        pr_comment_md += (
            f'<a href="{self.trigger_event.repo_html_url}/'
            f'pull/{autoupdate_pull_request_number}">'
            f'<img src="{self.validate_response.server_meta.suggestions_cta_url}" '
            'width="140"/></a>'
            "\n\n"
        )

        # Impact Response
        if self.analyze_impact_response.markdown:
            pr_comment_md += self.analyze_impact_response.markdown
            pr_comment_md += "\n\n"

        self.add_or_update_pull_request_comment(
            self._create_summary_comment(pr_comment_md)
        )

    def functions_to_run(self) -> List[Callable[[], Optional[DAPIServerResponse]]]:
        """Check if we should run the action."""
        # if this is not a pull request event, we only do things if there are files to process
        if self.trigger_event.is_push_event:
            if self._are_there_files_to_process():
                return [
                    *self.base_functions_to_run,
                    self.push_possibly_fail_github_action,
                ]
            return []

        # this is a pull request event

        # if there are files to process, so we run the entire validation and enrichment flow
        if self._are_there_files_to_process():
            return [
                *self.base_functions_to_run,
                self.create_metadata_pr_update_summary_comment,
                self.pr_possiby_fail_github_action,
            ]

        # there are no files to process, but there are schema changes, and so
        # we must comment with impact analysis etc.
        if not self.changed_files_from_base.is_empty:
            self.print_markdown_and_text(
                "\n\nThis PR contains schema changes, continuing with non-metadata analysis.",
                color="yellow",
            )
            return [
                self.maybe_analyze_impact,
                self.create_or_update_summary_comment_metadata_merged,
                self.pr_possiby_fail_github_action,
            ]

        # the PR has no schema changes, we must delete opendapi comments if applicable
        # I.E. the PR had schema changes, but they were reverted, and so comment should be deleted
        if opendapi_comment_id := self.existing_opendapi_comment_id:
            self.print_markdown_and_text(
                "\n\nThis PR no longer contains schema changes, cleaning up PR presence.",
                color="yellow",
            )
            return [lambda: self.github_adapter.delete_comment(opendapi_comment_id)]

        return []

    def push_possibly_fail_github_action(
        self,
    ):
        """Check if we should fail the Github action on a push"""
        error_messages = []
        if not self.changed_files_from_current.is_empty:
            unsynced_dapis = sorted(self.changed_files_from_current.dapis.keys())
            txt = (
                "\n\nThe following DAPIs' metadata is not in sync with schema changes:"
            )
            for dapi in unsynced_dapis:
                txt += f"\n\t- {dapi}"  # pylint: disable=consider-using-join

            self.print_markdown_and_text(
                txt,
                color="red",
            )
            error_messages.append("\n\t- Metadata is not in sync.")

        if self.validate_response and self.validate_response.errors:
            self.print_markdown_and_text(
                "\n\nYour DAPI files have validation errors, as listed "
                f"below:\n{json.dumps(self.validate_response.errors, indent=2)}",
                color="red",
            )
            error_messages.append(
                "\n\t- There are validation errors in the DAPI files."
            )

        if error_messages:
            raise FailGithubAction("".join(error_messages))

    def pr_possiby_fail_github_action(self):
        """Check if we should fail the Github action on a pull request"""
        error_messages = []
        if not self.changed_files.is_empty:
            unsynced_dapis = sorted(self.changed_files.dapis.keys())
            txt = (
                "\n\nThe following DAPIs' metadata is not in sync with schema changes:"
            )
            for dapi in unsynced_dapis:
                txt += f"\n\t- {dapi}"  # pylint: disable=consider-using-join

            if self.autoupdate_pr_number:
                pr_stanza = (
                    f"PR #{self.autoupdate_pr_number}"
                    if self.autoupdate_pr_number
                    else "A Woven-generated PR"
                )
                txt += (
                    f"\n{pr_stanza} with suggested metadata "
                    "updates was created for you to review."
                )

            self.print_markdown_and_text(
                txt,
                color="red",
            )
            error_messages.append("\n\t- Metadata is not in sync.")

        if self.validate_response and self.validate_response.errors:
            self.print_markdown_and_text(
                "\n\nYour DAPI files have validation errors, as listed "
                f"below:\n{json.dumps(self.validate_response.errors, indent=2)}",
                color="red",
            )
            error_messages.append(
                "\n\t- There are validation errors in the DAPI files."
            )

        if error_messages:
            raise FailGithubAction("".join(error_messages))

    def create_metadata_pr_update_summary_comment(self):
        """
        In PRs, spin up another Auto-generated Github PR with new changes
        and leave a comment with that PR number and details on downstream impact
        """

        metrics_tags = {"org_name": self.config.org_name_snakecase}
        increment_counter(LogCounterKey.SUGGESTIONS_PR_CREATED, tags=metrics_tags)
        suggestions_count = len(self.validate_response.suggestions)
        increment_counter(
            LogCounterKey.SUGGESTIONS_FILE_COUNT,
            value=suggestions_count,
            tags=metrics_tags,
        )
        autoupdate_pr_number = self.create_pull_request_for_changes()
        self.create_or_update_summary_comment_metadata_unmerged(autoupdate_pr_number)

    def run(self):
        if self.trigger_event.is_pull_request_event:
            metrics_tags = {"org_name": self.config.org_name_snakecase}
            increment_counter(LogCounterKey.USER_PR_CREATED, tags=metrics_tags)
        super().run()
