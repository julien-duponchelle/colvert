import logging

import aiohttp_jinja2
from aiohttp import web
from plotly.offline.offline import get_plotlyjs

from ...database import ParseError
from .. import charts

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
    side_by_side = post.get("side-by-side", False)
    try:
        result = request.app["db"].sql(query)
    except ParseError as e:
        logging.error(e)
        return await aiohttp_jinja2.render_template_async('error.html.j2', request, {
            "message": str(e),
        })
    if result is None:
        return await aiohttp_jinja2.render_template_async('info.html.j2', request, {
            "message": "No results",
        })
    try:
        if side_by_side and chart_type != "table":
            return await render_side_by_side(chart_type, request, result)
        else:
            return await render_full(chart_type, request, result, )
    except ValueError as e:
        logging.error(e)
        return await aiohttp_jinja2.render_template_async('error.html.j2', request, {
            "message": str(e),
        })

async def render_side_by_side(chart_type, request, result)-> web.Response:
    body_table = await render_chart("table", request, result, col=6)
    body_chart = await render_chart( chart_type, request, result, col=6)
    return web.Response(text=body_table + body_chart, content_type="text/html")


async def render_full(chart_type, request, result) -> web.Response:
    body = await render_chart( chart_type, request, result, col=12)
    return web.Response(text=body, content_type="text/html")


async def render_chart(chart_type, request, result, col: int):# -> Any:
    for chart in charts.__all__:
        if chart_type == chart.lower():
            body = await getattr(charts, chart)(request, result).build()
            return f'<div class="col-{col}">' + body + '</div>'
    raise ValueError(f"Unknown chart type: {chart_type}")