import asyncio

import click

from ..ai import AIError, test_model


@click.group()
def ai() -> None:
    pass


@ai.command()
def test() -> None:
    """
    Test the connection to the AI model
    """
    loop = asyncio.new_event_loop()
    result = None
    try:
        result = loop.run_until_complete(test_model())
        click.echo(result)
    except AIError as e:
        click.echo(e, err=True)
    finally:
        loop.close()