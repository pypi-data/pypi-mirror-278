from contextlib import suppress

import pytest as pytest

from snowflake.core.exceptions import NotFoundError
from snowflake.core.table import Table, TableColumn
from tests.utils import random_string


def test_swap(tables):
    table1_name = random_string(10, "test_table_")
    table2_name = random_string(10, "test_table_")
    test_table1_handle = tables[table1_name]
    test_table2_handle = tables[table2_name]

    test_table1 = Table(
        name=table1_name,
        columns=[
            TableColumn(name="c1", datatype="int"),
        ],
    )
    try:
        _ = tables.create(test_table1)
        test_table2 = Table(
            name=table2_name,
            columns=[
                TableColumn(name="c2", datatype="int"),
            ],
        )
        _ = tables.create(test_table2)
        test_table1_handle.swap_with(table2_name)
        fetched_table1 = test_table1_handle.fetch()
        fetched_table2 = test_table2_handle.fetch()
        assert fetched_table1.columns[0].name == "C2"
        assert fetched_table2.columns[0].name == "C1"
    finally:
        with suppress(NotFoundError):
            test_table1_handle.delete()
        with suppress(NotFoundError):
            test_table2_handle.delete()
