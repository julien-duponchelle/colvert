import pandas
import plotly.express as px

from .base import Base, Response, Result


class Pie(Base):
    limit = 10
    example = "SELECT COUNT(*) as score, column FROM table GROUP BY ALL"
    title = "Pie Chart"
    pattern = ['NUMBER', '*']

    def render(self,result: Result, df: pandas.DataFrame) -> Response:
        fig = px.pie(df, values=result.column_names[0], names=result.column_names[1])
        return self.render_px(fig)