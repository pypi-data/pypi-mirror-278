"""Common utilities for the OpenDAPI CLI."""

import os
from typing import List, Optional

import click

from opendapi.config import OpenDAPIConfig
from opendapi.defs import CONFIG_FILEPATH_FROM_ROOT_DIR


def check_command_invocation_in_root():
    """Check if the `opendapi` CLI command is invoked from the root of the repository."""
    if not (os.path.isdir(".github") or os.path.isdir(".git")):
        click.secho(
            "  This command must be run from the root of your repository. Exiting...",
            fg="red",
        )
        raise click.Abort()
    click.secho(
        "  We are in the root of the repository. Proceeding...",
        fg="green",
    )
    return True


def get_opendapi_config(
    root_dir: str, local_spec_path: Optional[str] = None
) -> OpenDAPIConfig:
    """Get the OpenDAPI configuration object."""
    try:
        config = OpenDAPIConfig(root_dir, local_spec_path=local_spec_path)
        click.secho(
            f"  Found the {CONFIG_FILEPATH_FROM_ROOT_DIR} file. Proceeding...",
            fg="green",
        )
        return config
    except FileNotFoundError as exc:
        click.secho(
            f"  The {CONFIG_FILEPATH_FROM_ROOT_DIR} file does not exist. "
            "Please run `opendapi init` first. Exiting...",
            fg="red",
        )
        raise click.Abort() from exc


def check_if_opendapi_config_is_valid(config: OpenDAPIConfig) -> bool:
    """Check if the `opendapi.config.yaml` file is valid."""
    try:
        config.validate()
    except Exception as exc:
        click.secho(
            f"  The `{CONFIG_FILEPATH_FROM_ROOT_DIR}` file is not valid. "
            f"`opendapi init` may rectify. {exc}. Exiting...",
            fg="red",
        )
        raise click.Abort()
    click.secho(
        f"  The {CONFIG_FILEPATH_FROM_ROOT_DIR} file is valid. Proceeding...",
        fg="green",
    )
    return True


def pretty_print_errors(errors: List[Exception]):
    """Prints all the errors"""
    if errors:
        click.secho("\n\n")
        click.secho(
            "OpenDAPI: Encountered validation errors",
            fg="red",
            bold=True,
        )

    for error in errors:
        click.secho("\n")
        click.secho("OpenDAPI: ", nl=False, fg="green", bold=True)
        click.secho(error.prefix_message, fg="red")
        for err in error.errors:
            click.secho(err)
    click.secho("\n\n")


def common_options(func: click.core.Command) -> click.core.Command:
    """Set of click options required for most commands."""
    options = [
        click.option(
            "--local-spec-path",
            default=None,
            envvar="LOCAL_SPEC_PATH",
            help="Use specs in the local path instead of the DAPI server",
            show_envvar=False,
        ),
    ]
    for option in reversed(options):
        func = option(func)
    return func
