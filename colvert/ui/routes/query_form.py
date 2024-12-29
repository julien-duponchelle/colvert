import aiohttp_jinja2
from aiohttp import web

from colvert.ai import AIError, prompt_to_sql, sql_to_prompt

routes = web.RouteTableDef()


@routes.post("/sql-to-prompt")
async def to_prompt(request):
    post = await request.post()
    query = post.get("q", "")
    error = None
    try:
        prompt = await sql_to_prompt(query)
    except AIError as e:
        prompt = ""
        error = f"Error generating prompt: {e}"

    return await aiohttp_jinja2.render_template_async(
        "_query_form.html.j2",
        request,
        {
            "prompt": prompt,
            "query": query,
            "tab": "tab-prompt",
            "error": error,
        },
    )


@routes.post("/prompt-to-sql")
async def to_sql(request):
    post = await request.post()
    prompt = post.get("prompt", "")
    error = None
    try:
        query = await prompt_to_sql(request.app["db"], prompt)
    except AIError as e:
        query = ""
        error = f"Error generating SQL query: {e}"

    return await aiohttp_jinja2.render_template_async(
        "_query_form.html.j2",
        request,
        {
            "prompt": prompt,
            "query": query,
            "tab": "tab-sql",
            "error": error,
        },
    )
