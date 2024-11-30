
import plotly.express as px

from .base import Base, DataFrame, Result
from .types import OptionQualitativeColor, OptionTypeResultColumn, OptionTypeString


def _color_choices():
    return [
        k
        for k in px.colors.qualitative.__dict__.keys()
        if not (k.startswith("_") or k.startswith("swatches") or k.endswith("_r"))
    ]


class Line(Base):
    limit = 1000
    example = "SELECT COUNT(*),birthdate FROM table GROUP BY ALL"
    title = "Line Chart"
    pattern = ['NUMBER', '*', '...']
    options = [
        OptionTypeString("title", "Title"),
        OptionTypeResultColumn("color", "Color"),
        OptionTypeResultColumn("facet_row", "Facet Row"),
        OptionTypeResultColumn("facet_col", "Facet Column"),
        OptionQualitativeColor(name="color_discrete_sequence", label="Color theme"),
    ]
    
    async def render(self, result: Result, df: DataFrame) -> str:
        fig = px.line(df, x=result.column_names[1], y=result.column_names[0], **self.user_options)
        return await self.render_px(fig)