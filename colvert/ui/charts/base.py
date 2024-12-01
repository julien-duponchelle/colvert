
from typing import Any, Dict

import aiohttp_jinja2
import plotly.graph_objects
from aiohttp.web import Request
from pandas import DataFrame

from ...database import Result


class Base:
    options = {}

    def __init__(self, request: Request, result: Result, options: Dict[str, Any]) -> None:
        if not hasattr(self, "patterns"):
            self.patterns = ['NUMBER', 'STRING', '*'] 
            raise NotImplementedError("patterns is required")
        if len(self.patterns) == 0:
            raise NotImplementedError("patterns is required")
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
        self._request = request

        self.user_options = {}
        for opt in self.options:
            val = options.get(opt.name)
            if val is not None and val != "":
                self.user_options[opt.name] = opt.convert(val)
            elif opt.default is not None:
                self.user_options[opt.name] = opt.default
                

    def _validate(self):
        """
        Validate if the result can be rendered with this chart.

        Raise ValueError if the result is not valid.
        """
        first_pattern = self.patterns[0]
        if len(self._result.column_names) != 2 and first_pattern[-1:] != ["..."]:
            raise ValueError(f"{self.title} need exactly {len(first_pattern)} columns.\nExample: {self.example}")
    
        error = None
        for pattern in self.patterns:
            error = self._validate_pattern(pattern)
            if not error:
                break
        if error:
            raise ValueError(error)

        self._df = self._result.limit(self.limit + 1).df()
        if len(self._df) > self.limit:
            raise ValueError(f"{self.title} need max {self.limit} rows.")
        return True
    
    def _validate_pattern(self, pattern):
        for i, field in enumerate(pattern):
            if field == "*":
                continue
            elif field == "...":
                break
            elif self._result.column_types[i] != field:
                return f"{self.title} need a {field} column as column {i+1} got {self._result.column_types[i]}.\nExample: {self.example}"
        return None


    async def build(self) -> str:
        self._validate()
        return await self.render(self._result, self._df)

    async def render(self, result: Result, df: DataFrame) -> str:
        raise NotImplementedError
    
    async def render_template(self, template: str, context: dict) -> str:
        return await aiohttp_jinja2.render_string_async(
            template,
            self._request,
            context)

    async def render_px(self, fig: plotly.graph_objs.Figure) -> str:
        out = '<div class="row">'
        

        out += '<div class="col-s-12 col-lg-3" id="form-chart">'
        out += '<div class="card"><div class="card-body">'
        for opt in self.options:
            out += opt.render(self.user_options.get(opt.name), self._result.column_names)
        out += '</div></div>'
        out += '</div>'

        out += '<div class="col-s-12 col-lg-9">'
        out += '<div class="card"><div class="card-body">'
        out += fig.to_html(full_html=False, include_plotlyjs=False)
        out += '</div></div>'
        out += '</div>'
        
        out += '</div>'

        return out
        