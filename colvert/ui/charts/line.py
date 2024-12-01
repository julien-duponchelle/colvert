import plotly.graph_objects as go

from .base import Base, DataFrame, Result
from .types import OptionQualitativeColor, OptionTypeResultColumn, OptionTypeString


class Line(Base):
    limit = 1000
    max_facet = 10
    example = "SELECT COUNT(*),birthdate FROM table GROUP BY ALL"
    title = "Line Chart"
    patterns = [["*", "NUMBER", "..."]]
    options = [
        OptionTypeString("title", "Title"),
        OptionTypeResultColumn(name="facet", label="Facet"),
        OptionQualitativeColor(name="color_discrete_sequence", label="Color theme"),
    ]

    def _get_x_y_column_names(self, result: Result) -> tuple[str, list[str]]:
        """
        Compute the column names of the x and y columns.

        :return: Tuple[str, list[str]] with name of x colum and y columns
        in the result dataframe
        """
        facet = self.user_options.get("facet")
        x = result.column_names[0]
        y = [c for c in result.column_names[1:] if c != facet]
        return x, y

    def _traces(self, df: DataFrame, y_names: list[str]):
        facet = self.user_options.get("facet")

        for y_name in y_names:
            if not facet:
                yield y_name, df, None
            else:
                for facet_value in df[facet].unique():
                    yield y_name, df[df[facet] == facet_value], facet_value

    async def render(self, result: Result, df: DataFrame) -> str:
        x_name, y_names = self._get_x_y_column_names(result)

        fig = go.Figure()
        index = 0

        for y_name, dataframe, facet_value in self._traces(df, y_names):
            color = self.user_options["color_discrete_sequence"][
                index % len(self.user_options["color_discrete_sequence"])
            ]
            if facet_value and len(y_names) > 1:
                name = f"{facet_value} - {y_name}"
            elif facet_value:
                name = facet_value
            else:
                name = y_name

            fig.add_trace(
                go.Scatter(
                    x = dataframe[x_name],
                    y = dataframe[y_name],
                    mode = "lines",
                    name = name,
                    marker = {"color": color},
                )
            )
            index += 1
            if index == self.max_facet:
                fig.add_annotation(
                    text = f"Too many facets, only showing first {self.max_facet}",
                    showarrow = False,
                    font = dict(size = 15, color="white"),
                    xref = "paper",
                    yref = "paper",
                    x = 0,
                    y = 1,
                    bgcolor="red",
                    align = "left",
                    xanchor = "left",
                    yanchor = "top",
                )

        if len(result.column_names) == 2:
            fig.update_layout(
                title=self.user_options.get("title"),
                xaxis_title=x_name,
                yaxis_title=y_names[0],
            )
        else:
            fig.update_layout(
                title=self.user_options.get("title"),
                xaxis_title=x_name,
            )

        return await self.render_px(fig)
