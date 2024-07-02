import duckdb


class ProgrammingError(duckdb.ParserException):
    """
    A user error occurred
    """
    pass