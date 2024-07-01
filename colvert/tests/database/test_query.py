from colvert.database.query import Query


def test_query_auto_runnable():
    # Test when query does not contain disallowed words
    query = Query("SELECT * FROM users")
    assert query.auto_runnable()

    query = Query("SELECT *\nFROM users")
    assert query.auto_runnable()

    # Test when query contains disallowed words
    query = Query("INSERT INTO users (name) VALUES ('John')")
    assert not query.auto_runnable()

    query = Query(query="insert into users (name) VALUES ('John')")
    assert not query.auto_runnable()

    query = Query("UPDATE users SET name = 'John' WHERE id = 1")
    assert not query.auto_runnable()

    query = Query("UPDATE\nusers SET name = 'John' WHERE id = 1")
    assert not query.auto_runnable()


def test_query_str():
    query = Query("SELECT * FROM users")
    assert str(query) == "SELECT * FROM users"
