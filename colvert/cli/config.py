
import click

from ..settings import Settings


@click.group()
def config() -> None:
    pass

@config.command()
@click.argument("section", type=click.STRING)
@click.argument("key", type=click.STRING)
@click.argument("value", type=click.STRING)
def set(section, key, value) -> None:
    """
    Set a setting
    """
    settings = Settings()
    settings.set(section, key, value)
    click.echo(f"Set {section}.{key} to {value}")
    settings.save()


@config.command()
def path() -> None:
    """
    Get the path to the settings file
    """
    click.echo(Settings().path())