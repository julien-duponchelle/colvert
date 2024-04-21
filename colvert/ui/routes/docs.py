import os.path
import re

import aiohttp_jinja2
import markdown
from aiohttp import web
from markdown.extensions.admonition import AdmonitionExtension, AdmonitionProcessor
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.toc import TocExtension

routes = web.RouteTableDef()


class ColvertAdmonitionProcessor(AdmonitionProcessor):
    """
    Override the AdmonitionProcessor to use bootstrap classes.

    Example:
    !!! note
        This is a note.
    """
    def get_class_and_title(self, match: re.Match[str]) -> tuple[str, str | None]:
        klass = match.group(1).lower()
        # We don't want to use the title as it's already visible via the color coded box.
        return f"alert alert-{klass}", None


class ColvertAdmonitionExtension(AdmonitionExtension):
    def extendMarkdown(self, md):
        """ Add Admonition to Markdown instance. """
        md.registerExtension(self)
        md.parser.blockprocessors.register(ColvertAdmonitionProcessor(md.parser), 'admonition', 105)


def path(file: str) -> str:
    
    return os.path.join(os.path.dirname(__file__), "..", "..", "docs", file)

def render(file: str) -> str:
    with open(path(file)) as f:
        return markdown.markdown(f.read(), extensions=[
            TocExtension(),
            FencedCodeExtension(),
            CodeHiliteExtension(),
            ColvertAdmonitionExtension()
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

