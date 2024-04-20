import pandas
import plotly.express as px

from .base import Base, Result


class Pie(Base):
    limit = 10
    example = "SELECT COUNT(*) as score, column FROM table GROUP BY ALL"
    title = "Pie Chart"
    pattern = ['NUMBER', '*']

    async def render(self,result: Result, df: pandas.DataFrame) -> str:
        fig = px.pie(df, values=result.column_names[0], names=result.column_names[1])
        return await self.render_px(fig)