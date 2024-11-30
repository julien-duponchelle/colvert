import html
from typing import List

from plotly.express.colors import qualitative


class BaseOptionType:
    def __init__(self, name: str, label: str, default=None) -> None:
        self.name = name
        self.label = label
        self.default = default

    def render(self, value, _result_columns: List[str]):
        return f'<label for="{self.name}" class="form-label">{self.label}</label>'

    def input(self, value=None, **kwargs):
        out = "<input"
        if value is not None and (not isinstance(value, str) or len(value) > 0):
            value = html.escape(str(value), quote=True)
            out += f' value="{value}"'
        elif self.default is not None:
            out += f' value="{html.escape(str(self.default), quote=True)}"'
        for key, val in kwargs.items():
            if val is not None:
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
    def render(self, value, result_columns: List[str]):
        out = super().render(value, result_columns)
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

    def render(self, value, result_columns: List[str]):
        out = super().render(value, result_columns)
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
    

class OptionTypeResultColumn(BaseOptionType):
    """
    This option type is used to select a column from the SQL result.

    Example:
    SELECT COUNT(*) as score,name FROM table

    Is going to display a select with the columns name and score.
    """
    def render(self, value, result_columns: List[str]) -> str:
        out = super().render(value, result_columns)
        
        out += '<select autocomplete="on"'
        out += f' id="{self.name}"'
        out += f' name="{self.name}"'
        out += ' class="form-control"'
        out += ' onchange="document.getElementById(\'results\').dispatchEvent(new Event(\'sql-change\'))"'
        out += ">"

        out += '<option value=""></option>'
        for result_column in result_columns:
            if value == result_column:
                selected = "selected"
            else:
                selected = ""
            out += f"<option value=\"{result_column}\" {selected}>{result_column}</option>"

        out += "</select>"

        return out
    

class OptionTypeSelect(BaseOptionType):
    """
    And html <select>
    """
    def __init__(self, name: str, label: str, choices: List[str], default=None, allow_empty_value=False) -> None:
        super().__init__(name, label, default)
        self._choices = choices
        self._allow_empty_value = allow_empty_value
        if self._allow_empty_value is False and self.default is None:
            raise ValueError("The default value must be set if allow_empty_value is False")

    def render(self, value, result_columns: List[str]):
        out = super().render(value, result_columns)
        out += '<select autocomplete="on"'
        out += f' id="{self.name}"'
        out += f' name="{self.name}"'
        out += ' class="form-control"'
        out += ' onchange="document.getElementById(\'results\').dispatchEvent(new Event(\'sql-change\'))"'
        out += ">"

        if self.default and (value is None or len(value) == 0):
            value = self.default

        if self._allow_empty_value:
            out += '<option value=""></option>'            
        for choice in self._choices:
            if value == choice:
                selected = "selected"
            else:
                selected = ""
            out += f"<option value=\"{choice}\" {selected}>{choice}</option>"

        out += "</select>"

        return out


class OptionQualitativeColor(OptionTypeSelect):
    def __init__(self, name: str, label: str) -> None:
        choices = sorted([
            k
            for k in qualitative.__dict__.keys()
            if not (k.startswith("_") or k.startswith("swatches") or k.endswith("_r"))
        ])
        super().__init__(name, label, choices, default=qualitative.Vivid, allow_empty_value=False)

    def render(self, value, result_columns: List[str]):
        for k,v in qualitative.__dict__.items():
            if value == v:
                value = k
        return super().render(value, result_columns)

    def convert(self, value: str) -> str:
        return qualitative.__dict__[value]