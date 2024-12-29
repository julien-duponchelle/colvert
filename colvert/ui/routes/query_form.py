import aiohttp_jinja2
from aiohttp import web

from colvert.ai import AI, AIError

routes = web.RouteTableDef()

ai = AI()


@routes.post("/sql-to-prompt")
async def to_prompt(request):
    post = await request.post()
    query = post.get("q", "")
    try:
        prompt = await ai.sql_to_prompt(query)
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
    query = await ai.prompt_to_sql(request.app["db"], prompt)

    return await aiohttp_jinja2.render_template_async(
        "_query_form.html.j2",
        request,
        {"prompt": prompt, "query": query, "tab": "tab-sql"},
    )
