import pandas

from .base import Base, Result


class Table(Base):
    limit = 1000
    example = "SELECT * FROM table"
    title = "Table"
    pattern = ['...']

    def _row_iterator(self, df):
        for _, row in df.iterrows():
            yield row

    async def render(self,result: Result, df: pandas.DataFrame) -> str:
        context = {
            "columns": df.columns,
            "rows": self._row_iterator(df),
            "length": len(df),
        }
        template = "table.html.j2"
        return await self.render_template(template, context)