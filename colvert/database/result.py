import duckdb
import pandas

from .error import ProgrammingError


class Result:
    """
    Wrapper around duckdb result
    """
    def __init__(self, result) -> None:
        self.result = result
        if result is None:
            self.column_names = []
            self.column_types = []
        else:
            self.column_names = [d[0] for d in result.description]
            self.column_types = [d[1] for d in result.description]
    
    def fetchall(self):
        if self.result is None:
            return []
        return self.result.fetchall()

    def fetchone(self):
        if self.result is None: 
            return None
        return self.result.fetchone()
    
    def limit(self, limit: int) -> "Result":
        if self.result is None:
            return self
        return Result(self.result.limit(limit))
    
    def df(self) -> pandas.DataFrame:
        if self.result is None:
            return pandas.DataFrame()
        try:
            return self.result.df()
        except duckdb.ConversionException as e:
            raise ProgrammingError(e)