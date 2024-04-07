import plotly.express as px

from .base import Base, DataFrame, Result


class Line(Base):
    limit = 1000
    example = "SELECT COUNT(*),birthdate FROM table GROUP BY ALL"
    title = "Line Chart"
    pattern = ['NUMBER', '*']

    def render(self,result: Result, df: DataFrame) -> str:
        fig = px.line(df, x=result.column_names[1], y=result.column_names[0])
        return self.render_px(fig)