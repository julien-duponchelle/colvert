import os.path

import aiohttp_jinja2
import markdown
from aiohttp import web
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.toc import TocExtension

routes = web.RouteTableDef()


def path(file: str) -> str:
    
    return os.path.join(os.path.dirname(__file__), "..", "..", "docs", file)

def render(file: str) -> str:
    with open(path(file)) as f:
        return markdown.markdown(f.read(), extensions=[
            TocExtension(),
            FencedCodeExtension(),
            CodeHiliteExtension(),
        ])

@routes.get("/docs")
@aiohttp_jinja2.template("docs.html.j2")
async def index(request) -> dict[str, str]:
    return {"html": render("index.md")}


@routes.get("/docs/{file:[a-z-/]+}.png")
async def get_png(request) -> web.Response:
    file = request.match_info["file"]
    return web.Response(body=open(path(file + ".png"), "rb").read(), content_type="image/png")


@routes.get("/docs/{file:[a-z-/]+}")
@aiohttp_jinja2.template("docs.html.j2")
async def get(request) -> dict[str, str]:
    file = request.match_info["file"]
    if file.endswith("/"):
        file += "index"
    return {"html": render(file + ".md")}

