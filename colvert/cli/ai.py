import asyncio

import click

from ..ai import AI, AIError


@click.group()
def ai() -> None:
    pass

@ai.command()
def models() -> None:
    """
    List supported AI models
    """
    for model in AI().list_models():
        click.echo(model)


@ai.command()
def test() -> None:
    """
    Test the connection to the AI model
    """
    loop = asyncio.new_event_loop()
    ai = AI()
    result = None
    try:
        result = loop.run_until_complete(ai.test())
        click.echo(result)
    except AIError as e:
        click.echo(e, err=True)
    finally:
        loop.close()