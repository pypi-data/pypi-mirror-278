"""CLI for generating, validating and enriching DAPI files: `opendapi run`."""

import click

from opendapi.cli.common import common_options
from opendapi.cli.enrich.main import cli as enrich_cli
from opendapi.cli.enrich.main import enrich_options
from opendapi.cli.generate import cli as generate_cli


@click.command()
@common_options
@enrich_options
def cli(**kwargs):
    """
    This command combines the `opendapi generate` and `opendapi enrich` commands.

    This interacts with the DAPI server, and thus needs
    the server host and API key as environment variables or CLI options.
    """
    click.secho(
        'Running "opendapi generate" to generate DAPI files...',
        fg="green",
        bold=True,
    )

    generate_params = generate_cli.params
    generate_kwargs = {key.name: kwargs.get(key.name) for key in generate_params}
    with click.Context(generate_cli) as ctx:
        ctx.invoke(generate_cli, **generate_kwargs)

    click.secho(
        'Running "opendapi enrich" to validate and enrich DAPI files...',
        fg="green",
        bold=True,
    )
    enrich_params = enrich_cli.params
    enrich_kwargs = {key.name: kwargs.get(key.name) for key in enrich_params}

    # Invoke enrich_cli using the click.Context.invoke method
    with click.Context(enrich_cli) as ctx:
        ctx.invoke(enrich_cli, **enrich_kwargs)
