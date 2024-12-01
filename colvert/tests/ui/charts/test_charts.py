import pytest

from ....ui.charts import Pie, Table


@pytest.mark.asyncio
async def test_validate_pie(get_request, sample_db):
    """
    Pie Chart is use to test the common functionality of the charts
    """
    await Pie(
        get_request,
        await sample_db.sql("SELECT COUNT(*),'First Name' FROM test GROUP BY ALL"),
        {},
    ).build()
    with pytest.raises(expected_exception=ValueError, match="2 columns"):
        await Pie(get_request, await sample_db.sql("SELECT COUNT(*) FROM test"), {}).build()
    with pytest.raises(ValueError, match="NUMBER"):
        await Pie(
            get_request, await sample_db.sql("SELECT 'First Name','Last Name' FROM test"), {}
        ).build()
    with pytest.raises(ValueError, match="need max 10 rows"):
        await Pie(
            get_request, await sample_db.sql("SELECT 1,'First Name' FROM test"), {}
        ).build()


@pytest.mark.asyncio
async def test_validate_table(get_request, sample_db):
    await Table(
        get_request,
        await sample_db.sql("SELECT COUNT(*),'First Name' FROM test GROUP BY ALL"),
        {},
    ).build()
    # Test empty result
    await Table(
        get_request,
        await sample_db.sql("CREATE TABLE t1 (id INTEGER PRIMARY KEY, j VARCHAR)"),
        {},
    ).build()


