import html


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