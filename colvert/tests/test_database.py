import pytest

from colvert.database import Database


class TestDatabase:
    @pytest.fixture(scope="class")
    def db(self):
        db = Database()
        db.load_file("./samples/test.csv")
        return db

    def test_load_file_csv(self):
        db = Database()
        db.load_file("./samples/test.csv")
        assert db is not None
        assert db.tables() == ["test"]

    def test_load_file_parquet(self):
        db = Database()
        db.load_file("./samples/test.parquet")
        assert db is not None
        assert db.tables() == ["test"]

    def test_tables(self, db: Database):
        assert db.tables() == ["test"]

    def test_execute(self, db):
        assert db.execute("SELECT COUNT(*) FROM test", []).fetchone()[0] == 12

    def test_sql(self, db):
        assert db.execute("SELECT COUNT(*) FROM test", []).fetchone()[0] == 12

    def test_complete(self, db):
        suggestions = db.complete("SELECT * FROM te")
        assert suggestions[0] == ('Class', 'test')

        suggestions = db.complete("SEL")
        assert suggestions[0] == ('Keyword', 'SELECT ')

        suggestions = db.complete("SELECT * FROM read_csv_auto('sample")
        assert ('File', 'samples/') in suggestions

        suggestions = db.complete("SELECT * FROM read_csv_auto('samples/te")
        assert ('File', 'test.csv\'') in suggestions

        suggestions = db.complete('SELECT * FROM test WHERE Fir')
        assert ('Field', '"First Name"') in suggestions