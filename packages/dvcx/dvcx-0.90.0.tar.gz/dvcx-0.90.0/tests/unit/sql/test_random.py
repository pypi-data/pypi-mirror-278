from dvcx.sql import select
from dvcx.sql.functions import rand


def test_rand(warehouse):
    query = select(rand())
    result = tuple(warehouse.db.execute(query))
    assert isinstance(result[0][0], int)
