import asyncio
import logging
import os
import re
from typing import Generator, List, Optional

import duckdb

from .error import ProgrammingError
from .query import Query
from .result import Result


class Database:
    def __init__(self, database=":memory:") -> None:
        try:
            self._db = duckdb.connect(database)
        except duckdb.IOException as e:
            raise OSError(e)
        self._db.install_extension("autocomplete")
        self._db.load_extension("autocomplete")
        self._db.install_extension("httpfs")
        self._db.load_extension("httpfs")

    async def load_files(self, files: List[str], table: Optional[str] = None) -> None:
        if len(files) == 0:
            return
        if table is not None:
            await self._load_files_to_table(files, table)
        else:
            for files in self._group_files(files):
                table = self._get_table_name(files)
                await self._load_files_to_table(files, table)

    async def _load_files_to_table(self, files: List[str], table: str):
        table = self._escape(table)
        if files[0].endswith(".csv") or files[0].endswith(".tsv"):
            await self._execute(f"CREATE TABLE {table} AS SELECT * FROM read_csv_auto(?)", [files])
        elif files[0].endswith(".json"):    
            await self._execute(f"CREATE TABLE {table} AS SELECT * FROM read_json_auto(?)", [files])
        elif files[0].endswith(".parquet"):
            await self._execute(f"CREATE TABLE {table} AS SELECT * FROM read_parquet(?)", [files])
        elif files[0].endswith(".db") or files[0].endswith(".duckdb"):
            self._db = duckdb.connect(files[0])
        else:
            raise ValueError(f"Unknown file type: {', '.join(files)}")

    def _group_files(self, files: List[str]) -> Generator[List[str], None, None]:
        """
        Group files that belong to the same table

        Example: 
        [user-001.csv, user-002.csv, user-003.csv], [order-001.csv, order-002.csv], [product.csv]
        """
        current_group = []
        file_name_pattern = re.compile(r"[\s_-][0-9]")
        
        for file in sorted(files):
            if len(current_group) == 0:
                current_group.append(file)
            else:
                if re.split(file_name_pattern, current_group[0])[0] == re.split(file_name_pattern, file)[0]:
                    current_group.append(file)
                else:
                    yield current_group
                    current_group = [file]
        if len(current_group) > 0:
            yield current_group


    def _get_table_name(self, files: List[str]):
        """
        Compute a table name from a list of files
        """

        filenames = [os.path.basename(file) for file in files]
        tables = [re.sub(r'[ -\.]', '_', os.path.splitext(filename)[0]) for filename in filenames]

        # We want to find the common prefix of the tables
        # using the underscore as a separator
        # Example 2024-01, 2024-02, 2024-03 -> 2024
        parts = [table.split("_") for table in tables]
        common = []
        for idx in range(0, len(parts[0])):
            if len(set(part[idx] for part in parts)) == 1:
                common.append(parts[0][idx])
            else:
                break
        if len(common) == 0:
            table = tables[0]
        else:
            table = "_".join(common)
        if table[0].isdigit(): # Table names cannot start with a digit
            table = f"table_{table}"
        return table

    def _escape(self, value: str) -> str:
        """
        Brutally escape a string for use in SQL as a table or column name

        For paremeters, use prepared statements
        """
        return re.sub(r"[^a-zA-Z0-9_]", "_", value)

    async def describe(self, table: str):
        table = self._escape(table)
        result = await self._execute(f"DESCRIBE {table}")
        rows = []
        for row in result.fetchall():
            field = {}
            for idx, col in enumerate(result.column_names):
                field[col] = row[idx]
            rows.append(field)
        return rows

    async def tables(self) -> list[str]:
        tables = await self._execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'main' ORDER BY table_name ASC")
        tables = tables.fetchall()
        return [table[0] for table in tables]

    async def _execute(self, sql: str, params: list = [], log: bool = True) -> Result:
        """
        Internal method to execute a query

        :param sql: SQL query
        :param params: Parameters for prepared statements
        :param log: Log the query to the console

        :return: Result object
        """
        if log:
            logging.info(sql)
        try:
            result = await asyncio.get_event_loop().run_in_executor(None, self._db.execute, str(sql), params)
        except duckdb.ProgrammingError as e:
            raise ProgrammingError(e)
        return Result(result)

    async def sql(self, sql: Query) -> Result:
        """
        External method to execute a query
        """
        logging.info(sql)
        try:
            result = await asyncio.get_event_loop().run_in_executor(None, self._db.sql, str(sql))
        except (duckdb.ProgrammingError, duckdb.IOException, duckdb.NotImplementedException, duckdb.ConversionException) as e:
            raise ProgrammingError(e)
        return Result(result)
    
    async def complete(self, query: str) -> list[tuple[str, str]]:
        result = await self._execute("SELECT * FROM sql_auto_complete(?)", [query], log=False)
        completions = []
        for row in result.fetchall():
            kind = "Text"
            val = row[0]
            if re.match("^[A-Z ]+$", val):
                kind = "Keyword"
            elif val in await self.tables():
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
    
    async def schema(self) -> str:
        """
        Return the current database schema
        """
        schema = ""

        for table in await self.tables():
            schema += f"CREATE TABLE {table} (\n"
            for col in await self.describe(table):
                schema += f"\t\"{col['column_name']}\" {col['column_type']}"
                if col['null'] != 'YES':
                    schema += " NOT NULL"
                schema += ",\n"
            schema += ");\n\n"
        return schema
