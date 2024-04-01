import typing

import aiohttp_jinja2.helpers
import jinja2
import rocher
from markupsafe import Markup


@jinja2.pass_context
def current_page(
    context,
    route_name: str,
    query: typing.Optional[typing.Dict[str, str]] = None,
    **parts: typing.Union[str, int],
) -> bool:
    """
    Args:
        context jinja2.runtime.Context: The context of the template
        route_name str: The name of the route to check
        query dict: The query parameters to check
        **parts dict: The parts of the URL to check
    Return:
        True if the current page is the one specified by the arguments the arguments are the same as the ones of the url function
    """
    return context["request"].path == str(
        aiohttp_jinja2.helpers.url_for(context, route_name, query, **parts)
    )


def rocher_editor(container, language, content, **kwargs) -> Markup:
    """
    Display a code editor with the given content. It uses the VS Code editor

    Args:
        container str: The CSS container id.
        language str: The programming language.
        content str: The content to display.
        kwargs dict: Additional options to the editor
    Returns:
        The HTML code to display the editor.
    """
    return Markup(
        rocher.editor_html("/static/vs", container, language, content, **kwargs)
    )