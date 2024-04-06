import plotly.graph_objects
from aiohttp.web import Response
from pandas import DataFrame

from ...database import Result


class Base:


    def __init__(self, result: Result) -> None:
        if not hasattr(self, "pattern"):
            self.pattern = ['NUMBER', 'STRING', '*'] 
            raise NotImplementedError("pattern is required")
        if not hasattr(self, "title"):
            self.title = "Title"
            raise NotImplementedError("title is required")
        if not hasattr(self, "example"):
            self.example = "Provide an example here"
            raise NotImplementedError("example is required")
        if not hasattr(self, "limit"):
            self.limit = 10
            raise NotImplementedError("limit is required")
        self._result = result

    def _validate(self):
        """
        Validate if the result can be rendered with this chart.

        Raise ValueError if the result is not valid.
        """
        if len(self._result.column_names) != 2:
            raise ValueError(f"{self.title} need exactly {len(self.pattern)} columns.\nExample: {self.example}")
    
        for i, pattern in enumerate(self.pattern):
            if pattern == "*":
                continue
            elif self._result.column_types[i] != pattern:
                raise ValueError(f"{self.title} need a {pattern} column as column {i+1} got {self._result.column_types[i]}.\nExample: {self.example}")
        
        self._df = self._result.limit(self.limit + 1).df()
        if len(self._df) > self.limit:
            raise ValueError(f"{self.title} need max {self.limit} rows.")
        return True

    def build(self) -> Response:
        self._validate()
        return self.render(self._result, self._df)

    def render(self, result: Result, df: DataFrame) -> Response:
        raise NotImplementedError

    def render_px(self, fig: plotly.graph_objs.Figure) -> Response:
        html = fig.to_html(full_html=False, include_plotlyjs=False)
        return Response(text=html, content_type="text/html")

        