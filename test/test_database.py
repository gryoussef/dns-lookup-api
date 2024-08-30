import pytest
from mock_database import MockDatabase

@pytest.mark.asyncio
async def test_database():
    db = MockDatabase()
    await db.connect()
    await db.create_tables()
    await db.save_query("example.com", ["93.184.216.34"])
    queries = await db.get_latest_queries(1)
    assert len(queries) == 1
    assert queries[0]["domain"] == "example.com"
    await db.disconnect()