
import html
from typing import Any, Dict

import aiohttp_jinja2
import plotly.graph_objects
from aiohttp.web import Request
from pandas import DataFrame

from ...database import Result


class BaseOptionType:
    def __init__(self, name: str, label: str, default=None) -> None:
        self.name = name
        self.label = label
        self.default = default

    def render(self, value):
        return f'<label for="{self.name}" class="form-label">{self.label}</label>'

    def input(self, value=None, **kwargs):
        out = "<input"
        if value is not None and (not isinstance(value, str) or len(value) > 0):
            value = html.escape(str(value), quote=True)
            out += f' value="{value}"'
        elif self.default is not None:
            out += f' value="{html.escape(str(self.default), quote=True)}"'
        for key, val in kwargs.items():
            val = str(val)
            out += f' {key}="{html.escape(val, quote=True)}"'
        out += f' id="{self.name}"'
        out += f' name="{self.name}"'
        out += ' class="form-control"'
        out += ' onchange="document.getElementById(\'results\').dispatchEvent(new Event(\'sql-change\'))"'
        out += ">"
        return out
    
    def convert(self, value):
        return value


class OptionTypeString(BaseOptionType):
    def render(self, value):
        out = super().render(value)
        out += self.input(
            value=value,
            type="text",
        )
        return out


class OptionTypeFloat(BaseOptionType):
    def __init__(self, name: str, label: str, step: float=0.01, min=None, max=None, **kwargs) -> None:
        self.step = step
        self.min = min
        self.max = max
        super().__init__(name, label, **kwargs)

    def render(self, value):
        out = super().render(value)
        out += self.input(
            value=value,
            type="number",
            min=self.min,
            max=self.max,
            step=self.step,
        )
        return out

    def convert(self, value):
        return float(value)


class Base:
    options = {}

    def __init__(self, request: Request, result: Result, options: Dict[str, Any]) -> None:
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
        self._request = request

        self.user_options = {}
        for opt in self.options:
            val = options.get(opt.name)
            if val is not None:
                self.user_options[opt.name] = opt.convert(val)

    def _validate(self):
        """
        Validate if the result can be rendered with this chart.

        Raise ValueError if the result is not valid.
        """
        if len(self._result.column_names) != 2 and self.pattern[-1:] != ["..."]:
            raise ValueError(f"{self.title} need exactly {len(self.pattern)} columns.\nExample: {self.example}")
    
        for i, pattern in enumerate(self.pattern):
            if pattern == "*":
                continue
            elif pattern == "...":
                break
            elif self._result.column_types[i] != pattern:
                raise ValueError(f"{self.title} need a {pattern} column as column {i+1} got {self._result.column_types[i]}.\nExample: {self.example}")
        
        self._df = self._result.limit(self.limit + 1).df()
        if len(self._df) > self.limit:
            raise ValueError(f"{self.title} need max {self.limit} rows.")
        return True

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
        out = '<div class="card"><div class="card-body">'
        
        out += '<div class="col-s-12 col-lg-3" id="form-chart">'
        for opt in self.options:
            out += opt.render(self.user_options.get(opt.name))
        out += '</div>'

        out += '<div class="col-s-12 col-lg-9">'
        out += fig.to_html(full_html=False, include_plotlyjs=False)
        out += '</div>'
        
        out += '</div></div>'

        return out
        