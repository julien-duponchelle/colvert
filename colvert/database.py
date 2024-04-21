import logging
import os
import re
from typing import List, Optional

import duckdb
import pandas


class ParseError(duckdb.ParserException):
    pass


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
        return self.result.df()


class Database:
    def __init__(self) -> None:
        self._db = duckdb.connect(":memory:")
        self._db.install_extension("autocomplete")
        self._db.load_extension("autocomplete")

    def load_files(self, files: List[str], table: Optional[str] = None) -> None:
        # TODO: Add support for other file types
        if table is None:
            table = self._get_table_name(files[0])
        table = self._escape(table)
        if files[0].endswith(".csv"):    
            self.execute(f"CREATE TABLE {table} AS SELECT * FROM read_csv_auto(?)", [files])
        elif files[0].endswith(".parquet"):
            self.execute(f"CREATE TABLE {table} AS SELECT * FROM read_parquet(?)", [files])
        else:
            raise ValueError(f"Unknown file type: {', '.join(files)}")

    def _get_table_name(self, file):
        filename = os.path.basename(file)
        table = os.path.splitext(filename)[0]
        if table[0].isdigit(): # Table names cannot start with a digit
            table = f"table_{table}"

    def _escape(self, value: str) -> str:
        """
        Brutally escape a string for use in SQL as a table or column name

        For paremeters, use prepared statements
        """
        return re.sub(r"[^a-zA-Z0-9_]", "_", value)

    def describe(self, table: str):
        table = self._escape(table)
        result =  self.sql(f"DESCRIBE {table}")
        rows = []
        for row in result.fetchall():
            field = {}
            for idx, col in enumerate(result.column_names):
                field[col] = row[idx]
            rows.append(field)
        return rows

    def tables(self):
        tables = self._db.sql("SELECT table_name FROM information_schema.tables WHERE table_schema = 'main' ORDER BY table_name ASC")
        tables = tables.fetchall()
        return [table[0] for table in tables]

    def execute(self, sql: str, params: list):
        logging.info(sql)
        try:
            result = self._db.execute(sql, params)
        except duckdb.ProgrammingError as e:
            raise ParseError(e)
        return Result(result)

    def sql(self, sql: str):
        logging.info(sql)
        try:
            result = self._db.sql(sql)
        except (duckdb.ProgrammingError, duckdb.IOException, duckdb.NotImplementedException) as e:
            raise ParseError(e)
        return Result(result)
    
    def complete(self, query: str) -> list[tuple[str, str]]:
        result = self._db.execute("SELECT * FROM sql_auto_complete(?)", [query])
        completions = []
        for row in result.fetchall():
            kind = "Text"
            val = row[0]
            if re.match("^[A-Z ]+$", val):
                kind = "Keyword"
            elif val in self.tables():
                kind = "Class"
            elif val[-1:] == "/":
                kind = "File"
            elif val[-1:] == "'":
                kind = "File"

            # Prevent double quotes from being if double quotes are
            # already present in the query
            if val[0] == '"' and val[-1:] == '"':
                kind = "Field"
                if re.search(r'"[^"]*$', query):
                    val = val[1:-1]
            completions.append((kind, val))
        return completions