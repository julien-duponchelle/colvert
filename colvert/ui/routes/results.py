import logging

import aiohttp_jinja2
import plotly.express as px
from aiohttp import web
from plotly.offline.offline import get_plotlyjs

from ...database import ParseError

routes = web.RouteTableDef()

@routes.get("/plotly.js")
async def plotly_js(request):

    return web.Response(
        text=get_plotlyjs(),
        content_type="application/javascript",
    )


@routes.get("/results")
async def index(request):
    query = request.query.get("q", "")
    chart_type = request.query.get("chart", "table")
    try:
        result = request.app["db"].sql(query)
    except ParseError as e:
        logging.error(e)
        return aiohttp_jinja2.render_template('error.html.j2', request, {
            "error": str(e),
        })
    if chart_type == "table":
        return table(request, result)
    elif chart_type == "pie":
        return pie_chart(result)
    else:
        raise web.HTTPBadRequest(reason="Invalid chart type")

def table(request, result) -> web.Response:
    context = {
        "columns": [ d[0] for d in result.description ],
        "rows": result.fetchall(),
    }
    template = "table.html.j2"
    return aiohttp_jinja2.render_template(template, request, context)

def pie_chart(result) -> web.Response:
    fig = px.pie(result.df(), values='c', names='region')
    return render(fig)

def render(fig) -> web.Response:
    html = fig.to_html(full_html=False, include_plotlyjs=False)
    return web.Response(text=html, content_type="text/html")
    