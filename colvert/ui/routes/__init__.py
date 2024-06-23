from .completion import routes as completion
from .docs import routes as docs
from .index import routes as index
from .results import routes as results
from .about import routes as about

routes = [*index, *results, *completion, *docs, *about]
