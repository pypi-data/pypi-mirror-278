import time

from contextlib import suppress

import pytest

from snowflake.core import Clone, PointOfTimeOffset
from snowflake.core.dynamic_table import (
    DownstreamLag,
    DynamicTable,
    DynamicTableClone,
    DynamicTableColumn,
    UserDefinedLag,
)
from snowflake.core.exceptions import NotFoundError
from tests.utils import random_string


@pytest.mark.skip("Enable when dynamic table is updated in prod")
def test_create_from_model_create_mode(dynamic_tables, db_parameters, table_handle):
    table_name = '"' + random_string(10, "test_table_ INTEGRATION_") + '"'
    created_handle = dynamic_tables.create(
        DynamicTable(
            name=table_name,
            columns=[
                DynamicTableColumn(name="c1"),
                DynamicTableColumn(name='"cc2"', datatype="varchar"),
            ],
            warehouse=db_parameters["warehouse"],
            target_lag=UserDefinedLag(seconds=60),
            query=f"SELECT * FROM {table_handle.name}",
        ),
        mode="errorifexists",
    )
    try:
        assert created_handle.name == table_name
    finally:
        with suppress(Exception):
            created_handle.delete()


@pytest.mark.skip("Enable when dynamic table is updated in prod")
def test_create_clone(dynamic_tables, dynamic_table_handle):
    table_name = random_string(10, "test_table_")
    created_handle = dynamic_tables.create(
        table_name, clone_table=f"{dynamic_table_handle.name}", copy_grants=True, mode="errorifexists"
    )
    try:
        assert created_handle.name == table_name
        assert created_handle.fetch().target_lag == DownstreamLag()
    finally:
        with suppress(Exception):
            created_handle.delete()

    time.sleep(1)
    table_name = random_string(10, "test_table_")
    created_handle = dynamic_tables.create(
        DynamicTableClone(
            name=table_name,
            target_lag=UserDefinedLag(seconds=120),
        ),
        clone_table=Clone(
            source=f"{dynamic_table_handle.name}", point_of_time=PointOfTimeOffset(reference="before", when="-1")
        ),
        copy_grants=True,
        mode="errorifexists",
    )
    try:
        assert created_handle.name == table_name
        assert created_handle.fetch().target_lag == UserDefinedLag(seconds=120)
    finally:
        with suppress(Exception):
            created_handle.delete()

    table_name = random_string(10, "test_table_")
    with pytest.raises(
        NotFoundError,
    ):
        dynamic_tables.create(table_name, clone_table="non_existant_name", copy_grants=True, mode="errorifexists")
