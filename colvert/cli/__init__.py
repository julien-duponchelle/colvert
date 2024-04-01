import click

from .daemon import open


@click.group()
def cli():
    pass


cli.add_command(open)

if __name__ == "__main__":
    cli()