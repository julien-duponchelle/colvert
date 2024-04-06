import logging

import aiohttp_jinja2
from aiohttp import web
from plotly.offline.offline import get_plotlyjs

from ...database import ParseError
from .. import charts

ROW_LIMIT = 1000

routes = web.RouteTableDef()

@routes.get("/plotly.js")
async def plotly_js(request) -> web.Response:
    return web.Response(
        text=get_plotlyjs(),
        content_type="application/javascript",
    )


@routes.post("/results")
async def index(request: web.Request) -> web.Response:
    post = await request.post()
    query = post.get("q", "")
    chart_type = post.get("chart", "table")
    try:
        result = request.app["db"].sql(query)
    except ParseError as e:
        logging.error(e)
        return aiohttp_jinja2.render_template('error.html.j2', request, {
            "message": str(e),
        })
    if result is None:
        return aiohttp_jinja2.render_template('info.html.j2', request, {
            "message": "No results",
        })
    elif chart_type == "table":
        return table(request, result)
    else:
        try:
            return render_chart(chart_type, result)        
        except ValueError as e:
            logging.error(e)
            return aiohttp_jinja2.render_template('error.html.j2', request, {
                "message": str(e),
            })

def render_chart(chart_type, result):
    for chart in charts.__all__:
        if chart_type == chart.lower():
            return getattr(charts, chart)(result).build()
    raise ValueError(f"Unknown chart type: {chart_type}")

def table(request, result) -> web.Response:
    context = {
        "columns": result.column_names,
        "rows": result.limit(ROW_LIMIT).fetchall(),
    }
    template = "table.html.j2"
    return aiohttp_jinja2.render_template(template, request, context)
