import aiohttp_jinja2
from aiohttp.web import Request, Response


async def info_box(message: str, request: Request) -> Response:
    return await aiohttp_jinja2.render_template_async('info.html.j2', request, {
            "message": message,
    })

async def error_box(message: str, request: Request) -> Response:
    return await aiohttp_jinja2.render_template_async('error.html.j2', request, {
        "message": message,
    })

async def warning_box(message: str, request: Request) -> Response:
    return await aiohttp_jinja2.render_template_async('warning.html.j2', request, {
        "message": message,
    })