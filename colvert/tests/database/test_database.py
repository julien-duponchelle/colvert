from pathlib import Path

import pytest
import pytest_asyncio

from colvert.database import Database, ProgrammingError, Query


class TestDatabase:
    @pytest_asyncio.fixture(scope="class")
    async def db(self):
        db = Database()
        await db.load_files(["./samples/test.csv"])
        return db
    
    def test_init_io_error(self, tmp_path):
        path = Path(tmp_path / "test.db")
        path.touch()
        path.chmod(0o000)
        with pytest.raises(OSError):
            Database(str(path / "test.db"))

    @pytest.mark.asyncio
    async def test_load_file_csv(self):
        db = Database()
        await db.load_files(["./samples/test.csv"])
        assert await db.tables() == ["test"]

    @pytest.mark.asyncio
    async def test_load_file_csv_set_table_name(self):
        db = Database()
        await db.load_files(["./samples/test.csv"], table="world")
        assert await db.tables() == ["world"]

    @pytest.mark.asyncio
    async def test_load_file_csv_starting_with_digit(self, tmpdir):
        with open(tmpdir / "1.csv", "w") as f:
            f.write("a,b,c\n1,2,3\n")
        db = Database()
        await db.load_files([str(tmpdir / "1.csv")])
        assert await db.tables() == ["table_1"]

    @pytest.mark.asyncio
    async def test_load_file_parquet(self):
        db = Database()
        await db.load_files(["./samples/test.parquet"])
        assert await db.tables() == ["test"]

    @pytest.mark.asyncio
    async def test_load_file_json(self):
        db = Database()
        await db.load_files(["./samples/test.json"])
        assert await db.tables() == ["test"]

    @pytest.mark.asyncio
    async def test_load_file_duckdb(self):
        db = Database()
        await db.load_files(["./samples/test.db"])
        assert await db.tables() == ["test"]

    @pytest.mark.asyncio
    async def test_load_file_json_unstructured(self):
        db = Database()
        await db.load_files(["./samples/unstructured.json"])
        assert await db.tables() == ["unstructured"]

    @pytest.mark.asyncio
    async def test_tables(self, db: Database):
        assert await db.tables() == ["test"]

    @pytest.mark.asyncio
    async def test_execute(self, db):
        res = await db._execute("SELECT COUNT(*) FROM test", [])
        assert res.fetchone()[0] == 12

    @pytest.mark.asyncio
    async def test_sql(self, db):
        res = await db.sql(Query("SELECT COUNT(*) FROM test"))
        assert res.fetchone()[0] == 12

    @pytest.mark.asyncio
    async def test_sql_error(self, db):
        with pytest.raises(ProgrammingError):
            await db.sql(Query("SELECT * FROM blal"))

    @pytest.mark.asyncio
    async def test_complete(self, db):
        suggestions = await db.complete("SELECT * FROM te")
        assert suggestions[0] == ('Class', 'test')

        suggestions = await db.complete("SEL")
        assert suggestions[0] == ('Keyword', 'SELECT ')

        suggestions = await db.complete("SELECT * FROM read_csv_auto('sample")
        assert ('File', 'samples/') in suggestions

        suggestions = await db.complete("SELECT * FROM read_csv_auto('samples/te")
        assert ('File', 'test.csv\'') in suggestions

        suggestions = await db.complete('SELECT * FROM test WHERE Fir')
        assert ('Field', '"First Name"') in suggestions

    @pytest.mark.asyncio
    async def test_describe(self, db):
        res = await db.describe("test")
        assert len(res) == 7
        assert res[0]['column_name'] == "Id"

    @pytest.mark.asyncio
    async def test_get_table_name(self, db):
        assert db._get_table_name(["test.csv"]) == "test"
        assert db._get_table_name(["1test.csv"]) == "table_1test"
        assert db._get_table_name(["test_2024.csv", "test_2023.csv"]) == "test"
        assert db._get_table_name(["test_2024_01.csv", "test_2024_02.csv"]) == "test_2024"
        assert db._get_table_name(["test-2024-01.csv", "test-2024-02.csv"]) == "test_2024"
        assert db._get_table_name(["test 2024 01.csv", "test 2024 02.csv"]) == "test_2024"
        assert db._get_table_name(["test 2024.01.02.csv", "test 2024.01.03.csv"]) == "test_2024_01"
        assert db._get_table_name(["test 2024.csv", "test 2024.01.03.csv"]) == "test_2024"

    @pytest.mark.asyncio
    async def test_group_files(self, db):
        assert list(db._group_files(["test.csv", "world.csv"])) == [["test.csv"], ["world.csv"]]
        assert list(db._group_files(["test-001.csv", "test-002.csv"])) == [["test-001.csv", "test-002.csv"]]
        assert list(db._group_files(["user-group.csv", "user-invoice.csv"])) == [["user-group.csv"], ["user-invoice.csv"]]
