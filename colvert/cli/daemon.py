import logging

import aiohttp.web
import click

from ..database import Database
from ..ui import setup_app


def create_app() -> aiohttp.web.Application:
    # Log on console
    logging.basicConfig(level=logging.INFO)
    app = setup_app()
    return app


@click.command()
@click.option(
    "--port", default=9999, type=int, help="Port to listen on", show_default=True
)
@click.option(
    "--host", default="127.0.0.1", help="Host to listen on", show_default=True
)
@click.argument("file", type=click.File("rb"))
def open(port: int, host: str, file: click.File):
    """
    Load a file and start the UI
    """
    app = create_app()
    app["db"] = Database()
    app["db"].load_file(file.name)
    logging.info(f"UI listening on http://{host}:{port}")
    aiohttp.web.run_app(
        app, host=host, port=port, print=None, access_log=None
    )