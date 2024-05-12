import pytest
import pytest_asyncio

from colvert.database import Database


class TestDatabase:
    @pytest_asyncio.fixture(scope="class")
    async def db(self):
        db = Database()
        await db.load_files(["./samples/test.csv"])
        return db

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
    async def test_load_file_json_unstructured(self):
        db = Database()
        await db.load_files(["./samples/unstructured.json"])
        assert await db.tables() == ["test"]

    @pytest.mark.asyncio
    async def test_tables(self, db: Database):
        assert await db.tables() == ["test"]

    @pytest.mark.asyncio
    async def test_execute(self, db):
        res = await db.execute("SELECT COUNT(*) FROM test", [])
        assert res.fetchone()[0] == 12

    @pytest.mark.asyncio
    async def test_sql(self, db):
        res = await db.execute("SELECT COUNT(*) FROM test", [])
        assert res.fetchone()[0] == 12

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
        assert len(res) == 5
        assert res[0]['column_name'] == "Id"
