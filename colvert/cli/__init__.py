import click

from .. import __version__
from .daemon import open


@click.group()
@click.version_option(version=__version__)
def cli():
    pass


cli.add_command(open)

if __name__ == "__main__":
    cli()