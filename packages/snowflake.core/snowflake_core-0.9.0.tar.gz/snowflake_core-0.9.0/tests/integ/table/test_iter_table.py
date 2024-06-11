from contextlib import suppress

import pytest as pytest

from snowflake.core.exceptions import APIError
from tests.integ.table.conftest import (
    assert_table,
)
from tests.utils import random_string


def test_iter_like(tables, table_handle, table_handle_case_senstitive, database, schema):
    listed_tables_deep = list(tables.iter(like=table_handle.name, deep=True))
    assert_table(listed_tables_deep[0], table_handle.name, database, schema, True)

    listed_tables_not_deep = list(tables.iter(like=table_handle.name, deep=False))
    assert_table(listed_tables_not_deep[0], table_handle.name, database, schema, False)

    listed_tables_deep = list(tables.iter(like="test_table_ca%", deep=True))
    assert_table(
        listed_tables_deep[0], table_handle_case_senstitive.name, database, schema, True
    )

    listed_tables_deep = list(tables.iter(like="test_table%", deep=True))
    assert len(listed_tables_deep) == 2


def test_iter_starts_with(tables, table_handle, table_handle_case_senstitive, database, schema):
    listed_tables_deep = list(tables.iter(starts_with="test_table", deep=True))
    assert len(listed_tables_deep) == 1
    assert_table(
        listed_tables_deep[0], table_handle_case_senstitive.name, database, schema, True
    )

    listed_tables_deep = list(tables.iter(starts_with="TEST_TABLE", deep=True))
    assert len(listed_tables_deep) == 1
    assert_table(listed_tables_deep[0], table_handle.name, database, schema, True)


# TODO(SNOW-1359464) - Please uncomment this once you have this bug resolved
# @pytest.mark.skip
# def test_iter_from_name(tables, table_handle, table_handle_case_senstitive, database, schema):
#     listed_tables_deep = list(tables.iter(from_name="test_table", deep=True))
#     assert len(listed_tables_deep) == 1
#     assert_table(
#         listed_tables_deep[0], table_handle_case_senstitive.name, database, schema, True
#     )

#     listed_tables_deep = list(tables.iter(from_name="TEST_TABLE", deep=True))
#     assert len(listed_tables_deep) == 1
#     assert_table(listed_tables_deep[0], table_handle.name, database, schema, True)


def test_iter_limit(tables):
    data = list(tables.iter(limit=10))
    assert len(data) <= 10

    with pytest.raises(
        APIError,
    ):
        data = list(tables.iter(limit=10001))


def test_iter_history(tables, table_handle):
    table_name = random_string(10, "test_table_")
    created_handle = tables.create(
        table_name, like_table=f"{table_handle.name}", copy_grants=True, mode="errorifexists"
    )
    try:
        assert created_handle.name == table_name
    finally:
        with suppress(Exception):
            created_handle.delete()

    data = list(tables.iter(history=True))
    assert len(data) >= 3
