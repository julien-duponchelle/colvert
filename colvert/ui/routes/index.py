import aiohttp_jinja2
from aiohttp import web

routes = web.RouteTableDef()

@routes.get("/")
@aiohttp_jinja2.template("index.html.j2")
async def index(request):
    query = request.query.get("q", "")
    first_table = request.app["db"].tables()[0]
    if query == "":
        query = f"SELECT *\nFROM '{first_table}'\nLIMIT 10"
    return {
        "query": query,
    }