"""Entrypoint for the OpenDAPI CLI."""

import click
import sentry_sdk

from opendapi.cli.enrich.main import cli as enrich_cli
from opendapi.cli.generate import cli as generate_cli
from opendapi.cli.init import cli as init_cli
from opendapi.cli.run import cli as run_cli
from opendapi.logging import sentry_init


@click.group()
@click.option(
    "--dapi-server-host",
    envvar="DAPI_SERVER_HOST",
    show_envvar=True,
    default="https://api.wovencollab.com",
    help="The host of the DAPI server",
)
@click.option(
    "--dapi-server-api-key",
    envvar="DAPI_SERVER_API_KEY",
    show_envvar=True,
    help="The API key for the DAPI server",
)
def cli(dapi_server_host: str = None, dapi_server_api_key: str = None):
    """
    OpenDAPI CLI is a command-line interface to initialize and run OpenDAPI projects.\n\n

    This tool helps autogenerate DAPI files and associated configuration files,
    and interacts with DAPI servers to bring the power of AI to your data documentation.\n\n

    Use `opendapi [COMMAND] --help` for more information about a command.
    """

    # Initialize sentry (this function fails silently)
    sentry_init(dapi_server_host, dapi_server_api_key)


def cli_wrapper():
    """A wrapper for all commands so we can capture exceptions and log them"""
    try:
        cli()
    except Exception as exp:  # pylint: disable=broad-except
        # This catches all the exceptions that are uncaught by click.
        # For eg: If an application developer raises click.Abort(), click handles
        # it and exits the program. This is expected behavior and we will not send
        # these to sentry. However, if the application fails due to an internal
        # error, we will catch it and log it.
        sentry_sdk.capture_exception(exp)
        raise exp


# Add commands to the CLI
cli.add_command(init_cli, name="init")
cli.add_command(generate_cli, name="generate")
cli.add_command(enrich_cli, name="enrich")
cli.add_command(run_cli, name="run")
