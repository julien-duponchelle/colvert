import logging

from aiohttp import web
from plotly.offline.offline import get_plotlyjs

from ...database import ParseError, Query
from .. import charts
from ..components import error_box, info_box, warning_box

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
    query = Query(str(post.get("q", "")))
    chart_type = str(post.get("chart", "table"))
    side_by_side = post.get("side-by-side", False)
    auto_run = post.get("auto-run", False)

    if auto_run and not query.auto_runnable():
        response = await warning_box("Query is not auto-runnable because it's not read only. Disabling auto-run.", request)
        response.headers["HX-Reswap"] = "afterbegin"
        response.headers["HX-Trigger"] = "disableAutoRun"
        return response

    try:
        result = await request.app["db"].sql(query)
    except ParseError as e:
        logging.error(e)
        return await error_box(str(e), request)
    if result is None:
        return await info_box("No results", request)
    
    options = {}
    for key, value in post.items():
        if key not in ["q", "chart", "side-by-side"]:
            options[key] = value
    try:
        if side_by_side and chart_type != "table":
            return await render_side_by_side(chart_type, request, result, options)
        else:
            return await render_full(chart_type, request, result, options)
    except ValueError as e:
        logging.error(e)
        return await error_box(str(e), request)
    

async def render_side_by_side(chart_type, request, result, options)-> web.Response:
    body_table = await render_chart("table", request, result, options, col=6)
    body_chart = await render_chart(chart_type, request, result, options, col=6)
    return web.Response(text='<div class="row">'+ body_table + body_chart + '</div>', content_type="text/html")


async def render_full(chart_type, request, result, options) -> web.Response:
    body = await render_chart( chart_type, request, result,options, col=12)
    return web.Response(text=body, content_type="text/html")


async def render_chart(chart_type, request, result, options, col: int):# -> Any:
    for chart in charts.__all__:
        if chart_type == chart.lower():
            body = await getattr(charts, chart)(request, result, options).build()
            return f'<div class="col-{col}">' + body + '</div>'
    raise ValueError(f"Unknown chart type: {chart_type}")