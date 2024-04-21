
import pandas
import plotly.express as px

from .base import Base, Result
from .types import OptionTypeFloat, OptionTypeString


class Pie(Base):
    limit = 10
    example = "SELECT COUNT(*) as score, column FROM table GROUP BY ALL"
    title = "Pie Chart"
    pattern = ['NUMBER', '*']
    options = [
        OptionTypeString("title", "Title"),
        OptionTypeFloat("hole", "Hole", default=0, step=0.1, min=0, max=1),
    ]

    async def render(self,result: Result, df: pandas.DataFrame) -> str:
        fig = px.pie(df, values=result.column_names[0], names=result.column_names[1], **self.user_options)
        return await self.render_px(fig)