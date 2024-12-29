import click

from .. import __version__
from .ai import ai
from .daemon import open
from .sample import sample


@click.group()
@click.version_option(version=__version__)
def cli():
    pass


cli.add_command(open)
cli.add_command(sample)
cli.add_command(ai)

if __name__ == "__main__":
    cli()