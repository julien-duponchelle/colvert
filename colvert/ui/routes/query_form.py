import aiohttp_jinja2
from aiohttp import web

routes = web.RouteTableDef()


@routes.post("/sql-to-prompt")
async def to_prompt(request):
    post = await request.post()
    prompt = post.get("prompt", "")
    query = post.get("q", "")
    prompt = "Mon prompt" + prompt

    return await aiohttp_jinja2.render_template_async(
        "_query_form.html.j2", request, {"prompt": prompt, "query": query, "tab": "tab-prompt"}
    )


@routes.post("/prompt-to-sql")
async def to_sql(request):
    post = await request.post()
    prompt = post.get("prompt", "")
    query = "SELECT * FROM blala"

    return await aiohttp_jinja2.render_template_async(
        "_query_form.html.j2", request, {"prompt": prompt, "query": query, "tab": "tab-sql"}
    )