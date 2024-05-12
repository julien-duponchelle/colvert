from aiohttp import web

routes = web.RouteTableDef()

@routes.post("/completion")
async def completion(request):
    body = await request.json()
    query = body.get("q", "")

    completions = await request.app["db"].complete(query)

    result = []
    for kind, completion in completions:
        result.append(
            {
                "kind": kind,
                "text": completion,
                "label": completion,
            }
        )
    return web.json_response(result)