# pylint: disable=too-many-arguments, too-many-locals
"""CLI for validating and enriching DAPI files: `opendapi enrich`."""
import os
from typing import Optional

import click

from opendapi.adapters.dapi_server import DAPIServerConfig
from opendapi.adapters.git import ChangeTriggerEvent
from opendapi.cli.common import (
    check_command_invocation_in_root,
    common_options,
    get_opendapi_config,
)
from opendapi.cli.enrich.github import GithubEnricher
from opendapi.cli.enrich.local import Enricher
from opendapi.logging import LogDistKey, Timer
from opendapi.utils import read_yaml_or_json


def enrich_options(func: click.core.Command) -> click.core.Command:
    """Set of click options required for the enrich command."""
    options = [
        click.option(
            "--github-event-name",
            type=click.Choice(["push", "pull_request"], case_sensitive=True),
            envvar="GITHUB_EVENT_NAME",
            show_envvar=False,
        ),
        click.option(
            "--github-workspace", envvar="GITHUB_WORKSPACE", show_envvar=False
        ),
        click.option(
            "--github-step-summary", envvar="GITHUB_STEP_SUMMARY", show_envvar=False
        ),
        click.option(
            "--github-event-path",
            envvar="GITHUB_EVENT_PATH",
            show_envvar=False,
        ),
        click.option("--github-token", envvar="GITHUB_TOKEN", show_envvar=False),
        click.option(
            "--dapi-server-host",
            envvar="DAPI_SERVER_HOST",
            show_envvar=True,
            default="https://api.wovencollab.com",
            help="The host of the DAPI server",
        ),
        click.option(
            "--dapi-server-api-key",
            envvar="DAPI_SERVER_API_KEY",
            show_envvar=True,
            help="The API key for the DAPI server",
        ),
        click.option(
            "--mainline-branch-name",
            default="main",
            envvar="MAINLINE_BRANCH_NAME",
            show_envvar=True,
            help="The name of the mainline branch to compare against",
        ),
        click.option(
            "--suggest-changes",
            is_flag=True,
            default=True,
            envvar="SUGGEST_CHANGES",
            show_envvar=True,
            help="Suggest changes to the DAPI files",
        ),
        click.option(
            "--enrich-batch-size",
            default=5,
            envvar="ENRICH_BATCH_SIZE",
            help="Batch size for validating and enriching DAPI files",
            show_envvar=True,
        ),
        click.option(
            "--register-batch-size",
            default=30,
            envvar="REGISTER_BATCH_SIZE",
            help="Batch size for validating and enriching DAPI files",
            show_envvar=False,
        ),
        click.option(
            "--revalidate-all-files",
            is_flag=True,
            default=False,
            envvar="REVALIDATE_ALL_FILES",
            help="Revalidate all files, not just the ones that have changed",
            show_envvar=True,
        ),
        click.option(
            "--require-committed-changes",
            is_flag=True,
            default=False,
            envvar="REQUIRE_COMMITTED_CHANGES",
            help="Do not Overwrite uncommitted DAPI files with server suggestions",
            show_envvar=True,
        ),
        click.option(
            "--ignore-suggestions-cache",
            is_flag=True,
            default=False,
            envvar="IGNORE_SUGGESTIONS_CACHE",
            help="Ignore suggestions cache and fetch fresh suggestions",
            show_envvar=False,
        ),
    ]
    for option in reversed(options):
        func = option(func)
    return func


def _should_use_github_enricher(
    github_event_name: Optional[str],
    github_event_path: Optional[str],
    github_token: Optional[str],
) -> bool:
    return (
        github_event_name is not None
        and github_event_path is not None
        and github_token is not None
    )


@click.command()
@common_options
@enrich_options
def cli(
    github_event_name: Optional[str],
    github_workspace: Optional[str],  # pylint: disable=unused-argument
    github_step_summary: Optional[str],
    github_event_path: Optional[str],
    github_token: Optional[str],
    dapi_server_host: str,
    dapi_server_api_key: str,
    mainline_branch_name: str,
    suggest_changes: bool,
    enrich_batch_size: int,
    register_batch_size: int,
    revalidate_all_files: bool,
    require_committed_changes: bool,
    ignore_suggestions_cache: bool,
    local_spec_path: Optional[str],
):
    """
    This command will find all the DAPI files in the repository to
        1. validate them for compliance with the company policies
        2. enrich data semantics and classification using AI.
        3. pull forward downstream impact of the changes.
        4. register the DAPI files with the DAPI server when appropriate

    This interacts with the DAPI server, and thus needs
    the server host and API key as environment variables or CLI options.
    """
    root_dir = os.getcwd()

    # Setup the DAPI server configuration
    dapi_server_config = DAPIServerConfig(
        server_host=dapi_server_host,
        api_key=dapi_server_api_key,
        mainline_branch_name=mainline_branch_name,
        suggest_changes=suggest_changes,
        enrich_batch_size=enrich_batch_size,
        ignore_suggestions_cache=ignore_suggestions_cache,
        register_batch_size=register_batch_size,
    )
    check_command_invocation_in_root()
    config = get_opendapi_config(root_dir, local_spec_path=local_spec_path)

    # Construct the Enricher
    if not _should_use_github_enricher(
        github_event_name,
        github_event_path,
        github_token,
    ):
        # This is a non-GitHub environment
        enricher_cls = Enricher
        change_trigger_event = ChangeTriggerEvent(
            where="local",
            before_change_sha=mainline_branch_name,
        )
    else:
        enricher_cls = GithubEnricher
        github_event = read_yaml_or_json(github_event_path)
        change_trigger_event = ChangeTriggerEvent(
            where="github",
            event_type=github_event_name,
            repo_api_url=github_event["repository"]["url"],
            repo_html_url=github_event["repository"]["html_url"],
            repo_owner=github_event["repository"]["owner"]["login"],
            before_change_sha=(
                github_event["before"]
                if github_event_name == "push"
                else github_event["pull_request"]["base"]["sha"]
            ),
            after_change_sha=(
                github_event["after"]
                if github_event_name == "push"
                else github_event["pull_request"]["head"]["sha"]
            ),
            git_ref=(
                github_event["ref"]
                if github_event_name == "push"
                else github_event["pull_request"]["head"]["ref"]
            ),
            pull_request_number=(
                github_event["pull_request"]["number"]
                if github_event_name == "pull_request"
                else None
            ),
            auth_token=github_token,
            markdown_file=github_step_summary,
        )

    enricher = enricher_cls(
        config=config,
        dapi_server_config=dapi_server_config,
        trigger_event=change_trigger_event,
        revalidate_all_files=revalidate_all_files,
        require_committed_changes=require_committed_changes,
    )

    enricher.print_text_message(
        "\nGetting ready to validate and enrich your DAPI files...",
        color="green",
        bold=True,
    )
    enricher.print_text_message(
        "\n\nChecking if we are in the right repository...",
        color="yellow",
    )
    metrics_tags = {
        "org_name": config.org_name_snakecase,
        "where": change_trigger_event.where,
        "event_type": change_trigger_event.event_type,
    }
    with Timer(dist_key=LogDistKey.CLI_ENRICH, tags=metrics_tags):
        enricher.run()
