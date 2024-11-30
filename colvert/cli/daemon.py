import asyncio
import logging
import signal
import webbrowser
from typing import List

import aiohttp.web
import click

from ..database import Database
from ..ui import setup_app


def create_app() -> aiohttp.web.Application:
    # Log on console
    logging.basicConfig(level=logging.INFO)
    app = setup_app()
    return app


async def open_browser_schedule(app: aiohttp.web.Application):
    """
    This is run in the context of the aiohttp event loop.

    We need to create a task to open the browser and add it to the background tasks.
    We can directly call webbrowser.open_new_tab(url) because the server is not yet started.
    and wait for this task to finish before starting the server.
    """
    browser_task = asyncio.create_task(open_browser(app))
    app["background_tasks"].add(browser_task)
    browser_task.add_done_callback(app["background_tasks"].discard)


async def open_browser(app: aiohttp.web.Application):
    await asyncio.sleep(
        0.3
    )  # Limit chance a race condition where the server is not yet started

    # Call the url with aiohttp.web
    url = f"http://{app['host']}:{app['port']}"
    async with aiohttp.ClientSession() as session:
        tries = 0
        while True:
            try:
                async with session.get(url):
                    logging.info(f"Opening browser at {url}")
                    webbrowser.open_new_tab(url)
                    break
            except aiohttp.ClientConnectorError as e:
                print(e)
                tries += 1
                if tries > 3:
                    logging.error(f"Could not connect to {url}")
                    break
                await asyncio.sleep(1)


@click.group(invoke_without_command=True)
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
@click.option(
    "--table",
    type=str,
    help="Table to load the file into",
)
@click.option("--database", type=str, help="Database file to use, by default it's in-memory", default=":memory:")
@click.argument("files", type=str, nargs=-1)
def open(port: int, host: str, files: List[str], no_browser: bool, table: str, database: str):
    """
    Load a file and start the UI
    """
    app = create_app()
    try:
        app["db"] = Database(database)
    except OSError as e:
        logging.error(e)
        return
    app["host"] = host
    app["port"] = port
    app["background_tasks"] = set()
    logging.info(f"UI listening on http://{host}:{port}")

    async def load_files(app: aiohttp.web.Application):
        logging.info(f"Loading files {', '.join(file for file in files)}")
        try:
            await app["db"].load_files([file for file in files], table=table)
        except ValueError as e:
            logging.error(e)
            # Send a signal to ourselves to stop the server
            signal.raise_signal(signal.SIGTERM)


    app.on_startup.append(load_files)
    if not no_browser:
        app.on_startup.append(open_browser_schedule)

    runner = aiohttp.web.AppRunner(app)
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(runner.setup())
        site = aiohttp.web.TCPSite(runner, host, port)
        loop.run_until_complete(site.start())
        loop.run_forever()
    except OSError as e:
        logging.error(e)
    except KeyboardInterrupt:
        pass
