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
        if file.endswith(".csv"):
            filename = os.path.basename(file)
            table_name = os.path.splitext(filename)[0]
            table_name = re.sub(r"[^a-zA-Z0-9_]", "_", table_name)
            self.execute(f"CREATE TABLE {table_name} AS SELECT * FROM read_csv_auto(?)", [file])
    
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
        except duckdb.ProgrammingError as e:
            raise ParseError(e)
        return result
    
    def complete(self, query: str) -> list[tuple[str, str]]:
        result = self._db.execute("SELECT * FROM sql_auto_complete(?)", [query])
        completions = []
        for row in result.fetchall():
            kind = "Text"
            if re.match("^[A-Z ]+$", row[0]):
                kind = "Keyword"
            elif row[0] in self.tables():
                kind = "Class"
            elif row[0][-1:] == "/":
                kind = "File"
            elif row[0][-1:] == "'":
                kind = "File"
            completions.append((kind, row[0]))
        print(completions)
        return completions