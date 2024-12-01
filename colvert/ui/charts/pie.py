
import pandas
import plotly.express as px

from .base import Base, Result
from .types import OptionQualitativeColor, OptionTypeFloat, OptionTypeString


class Pie(Base):
    limit = 10
    example = "SELECT COUNT(*) as score, column FROM table GROUP BY ALL"
    title = "Pie Chart"
    patterns = [
        ['NUMBER', '*'],
        ['*', 'NUMBER'],
    ]
    options = [
        OptionTypeString("title", "Title"),
        OptionTypeFloat("hole", "Hole", default=0, step=0.1, min=0, max=1),
        OptionQualitativeColor(name="color_discrete_sequence", label="Color theme"),
    ]

    async def render(self,result: Result, df: pandas.DataFrame) -> str:
        values, names = result.column_names[0], result.column_names[1]
        # Swap the values if provided as
        # SELECT name ,COUNT(*) as score FROM table
        # Instead of
        # SELECT COUNT(*) as score,name FROM table
        # This is to improve user experience
        if self._result.column_types[0] != "NUMBER":
            values, names = result.column_names[1], result.column_names[0]

        fig = px.pie(df, values=values, names=names, **self.user_options)
        return await self.render_px(fig)