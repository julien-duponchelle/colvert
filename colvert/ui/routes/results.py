import aiohttp_jinja2
from aiohttp import web

routes = web.RouteTableDef()

@routes.get("/results")
@aiohttp_jinja2.template("results.html.j2")
async def index(request):
    query = request.query.get("q", "")
    result = request.app["db"].sql(query)
    return {
        "columns": [ d[0] for d in result.description ],
        "rows": result.fetchall(),
    }