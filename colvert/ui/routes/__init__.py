from .completion import routes as completion
from .docs import routes as docs
from .index import routes as index
from .results import routes as results

routes = [*index, *results, *completion, *docs]