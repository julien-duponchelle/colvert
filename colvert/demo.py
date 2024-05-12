#
# This file is use to run the project in demo/develoment mode.
# 

import asyncio
import logging

import aiohttp.web

from .database import Database
from .ui import setup_app


def create_app() -> aiohttp.web.Application:
    # Log on console
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting colvert development server")
    app = setup_app()
    app["db"] = Database()
    logging.info("Loading sample data")
    loop = asyncio.get_running_loop()
    loop.create_task(app["db"].load_files(["samples/test.csv"]))
    return app
