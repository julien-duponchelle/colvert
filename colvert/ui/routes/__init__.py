from .completion import routes as completion
from .index import routes as index
from .results import routes as results

routes = [*index, *results, *completion]