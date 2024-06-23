from aiohttp import web
import aiohttp_jinja2

routes = web.RouteTableDef()

@routes.get('/about')
@aiohttp_jinja2.template('about.html.j2')
async def about(request):
    return {}
