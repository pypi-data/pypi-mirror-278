import pytest as pytest

from snowflake.core.exceptions import NotFoundError


@pytest.mark.skip("TODO: undelete is not part of our OAS")
def test_delete_and_undelete(tables, table_handle):
    table_handle.delete()
    with pytest.raises(NotFoundError):
        table_handle.fetch()
    table_handle.undelete()
    assert table_handle.fetch() is not None
