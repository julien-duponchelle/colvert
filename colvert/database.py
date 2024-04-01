import logging
import os
import re

import duckdb


class ParseError(duckdb.ParserException):
    pass


class Database:
    def __init__(self) -> None:
        self._db = duckdb.connect(":memory:")

    def load_file(self, file: str) -> None:
        # TODO: Add support for other file types
        # TODO: handle unknown file types
        if file.endswith(".csv"):
            filename = os.path.basename(file)
            table_name = os.path.splitext(filename)[0]
            table_name = re.sub(r"[^a-zA-Z0-9_]", "_", table_name)
            self.execute(f"CREATE TABLE {table_name} AS SELECT * FROM read_csv_auto(?)", [file])
            self.sql(f"SELECT * FROM {table_name}")
    
    def tables(self):
        tables = self.sql("SELECT table_name FROM information_schema.tables WHERE table_schema = 'main'")
        tables = tables.fetchall()
        return [table[0] for table in tables]

    def execute(self, sql: str, params: list):
        logging.info(sql)
        try:
            result = self._db.execute(sql, params)
        except duckdb.ParserException as e:
            raise ParseError(e)
        return result

    def sql(self, sql: str):
        logging.info(sql)
        try:
            result = self._db.sql(sql)
        except duckdb.ParserException as e:
            raise ParseError(e)
        return result
            