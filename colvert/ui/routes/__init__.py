from .about import routes as about
from .completion import routes as completion
from .docs import routes as docs
from .index import routes as index
from .query_form import routes as query_form
from .results import routes as results

routes = [*index, *results, *completion, *docs, *about, *query_form]
