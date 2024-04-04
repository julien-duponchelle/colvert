import logging
import os
import re

import duckdb


class ParseError(duckdb.ParserException):
    pass


class Database:
    def __init__(self) -> None:
        self._db = duckdb.connect(":memory:")
        self._db.install_extension("autocomplete")
        self._db.load_extension("autocomplete")

    def load_file(self, file: str) -> None:
        # TODO: Add support for other file types
        # TODO: handle unknown file types
        filename = os.path.basename(file)
        table_name = os.path.splitext(filename)[0]
        table_name = re.sub(r"[^a-zA-Z0-9_]", "_", table_name)
        if file.endswith(".csv"):    
            self.execute(f"CREATE TABLE {table_name} AS SELECT * FROM read_csv_auto(?)", [file])
        elif file.endswith(".parquet"):
            self.execute(f"CREATE TABLE {table_name} AS SELECT * FROM read_parquet(?)", [file])
        else:
            raise ValueError(f"Unknown file type: {file}")
    
    def tables(self):
        tables = self._db.sql("SELECT table_name FROM information_schema.tables WHERE table_schema = 'main'")
        tables = tables.fetchall()
        return [table[0] for table in tables]

    def execute(self, sql: str, params: list):
        logging.info(sql)
        try:
            result = self._db.execute(sql, params)
        except duckdb.ProgrammingError as e:
            raise ParseError(e)
        return result

    def sql(self, sql: str):
        logging.info(sql)
        try:
            result = self._db.sql(sql)
        except (duckdb.ProgrammingError, duckdb.IOException, duckdb.NotImplementedException) as e:
            raise ParseError(e)
        return result
    
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