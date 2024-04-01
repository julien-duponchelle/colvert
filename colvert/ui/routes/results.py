import logging

import aiohttp_jinja2
from aiohttp import web

from ...database import ParseError

routes = web.RouteTableDef()

@routes.get("/results")
async def index(request):
    query = request.query.get("q", "")
    try:
        result = request.app["db"].sql(query)
    except ParseError as e:
        logging.error(e)
        return aiohttp_jinja2.render_template('error.html.j2', request, {
            "error": str(e),
        })
    context = {
        "columns": [ d[0] for d in result.description ],
        "rows": result.fetchall(),
    }
    template = "results.html.j2"
    return aiohttp_jinja2.render_template(template, request, context)
