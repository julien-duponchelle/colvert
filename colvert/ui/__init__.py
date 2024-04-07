import os.path

import aiohttp_jinja2
import jinja2
import rocher
from aiohttp import web

from .helpers import current_page, rocher_editor
from .routes import routes


def setup_app():
    app = web.Application()
    jinja = aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(
            os.path.join(os.path.dirname(__file__), "templates")
        ),
        enable_async=True,
        context_processors=[aiohttp_jinja2.request_processor],
    )
    jinja.globals["current_page"] = current_page
    jinja.globals["rocher_editor"] = rocher_editor
    app.add_routes(routes)
    app.add_routes(
        [
            web.static("/static/vs", rocher.path()),
            web.static("/static", os.path.join(os.path.dirname(__file__), "static")),
        ]
    )
    return app