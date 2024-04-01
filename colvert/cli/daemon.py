import logging
import webbrowser

import aiohttp.web
import click

from ..database import Database
from ..ui import setup_app


def create_app() -> aiohttp.web.Application:
    # Log on console
    logging.basicConfig(level=logging.INFO)
    app = setup_app()
    return app

async def open_browser(app: aiohttp.web.Application):
    webbrowser.open_new_tab(f"http://{app['host']}:{app['port']}")


@click.command()
@click.option(
    "--port", default=9999, type=int, help="Port to listen on", show_default=True
)
@click.option(
    "--host", default="127.0.0.1", help="Host to listen on", show_default=True
)
@click.option(
    "--no-browser",
    is_flag=True,
    help="Do not open the browser",
)
@click.argument("file", type=click.File("rb"))
def open(port: int, host: str, file: click.File, no_browser: bool):
    """
    Load a file and start the UI
    """
    app = create_app()
    app["db"] = Database()
    app["db"].load_file(file.name)
    app["host"] = host
    app["port"] = port
    logging.info(f"UI listening on http://{host}:{port}")
    if not no_browser:
        app.on_startup.append(open_browser)
    aiohttp.web.run_app(
        app, host=host, port=port, print=None, access_log=None
    )
