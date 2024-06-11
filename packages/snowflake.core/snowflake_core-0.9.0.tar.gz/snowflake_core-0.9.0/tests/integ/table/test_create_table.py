import time

from contextlib import suppress

import pytest as pytest

from snowflake.core import Clone, PointOfTimeOffset
from snowflake.core.exceptions import NotFoundError
from snowflake.core.table import Table, TableColumn
from tests.utils import random_string


pytestmark = pytest.mark.jenkins


def test_create_from_model_create_mode(tables):
    table_name = random_string(10, "test_table_ INTEGRATION_")
    table_name_case_sensitive = '"' + table_name + '"'
    column_name_case_sensitive = '"cc2"'
    created_handle = tables.create(
        Table(
            name=table_name_case_sensitive,
            columns=[
                TableColumn(name="c1", datatype="varchar"),
                TableColumn(name=column_name_case_sensitive, datatype="varchar"),
            ],
        ),
        mode="errorifexists",
    )
    try:
        assert created_handle.name == table_name_case_sensitive
    finally:
        with suppress(Exception):
            created_handle.delete()

    table_name = random_string(10, '"test_table_INTEGRATION_"')
    # TODO(SNOW-1357278) - Please uncomment this once you have this bug resolved
    # with pytest.raises(
    #     APIError,
    # ):
    #     created_handle = tables.create(
    #         Table(
    #             name=table_name,
    #             columns=[
    #                 TableColumn(name="c1", datatype="varchar"),
    #             ],
    #         ),
    #         mode="errorifexists",
    #     )


def test_create_using_template(session, tables):
    session.sql("create or replace temp stage table_test_stage").collect()
    table_name = random_string(10, "test_table_")
    try:
        session.sql("CREATE or replace temp FILE FORMAT table_test_csv_format TYPE = csv parse_header=true").collect()
        session.file.put("./tests/resources/testCSVheader.csv", "@table_test_stage", auto_compress=False)
        handle = tables.create(
            table_name,
            template="select array_agg(object_construct(*)) "
            "from table(infer_schema(location=>'@table_test_stage', "
            "file_format=>'table_test_csv_format', "
            "files=>'testCSVheader.csv'))",
        )
        table = handle.fetch()
        assert table.columns[0].name == "id"
        assert table.columns[1].name == "name"
        assert table.columns[2].name == "rating"
        assert table.rows == 0

    finally:
        with suppress(Exception):
            session.sql("drop file format if exists table_test_csv_file_format")
        with suppress(Exception):
            session.sql("drop stage if exists @table_test_stage").collect()
        with suppress(Exception):
            tables[table_name].delete()


@pytest.mark.parametrize("create_mode", ["errorifexists", "orreplace", "ifnotexists"])
def test_create_like(tables, table_handle, create_mode):
    table_name = random_string(10, "test_table_")
    created_handle = tables.create(table_name, like_table=f"{table_handle.name}", copy_grants=True, mode=create_mode)
    try:
        assert created_handle.name == table_name
    finally:
        with suppress(Exception):
            created_handle.delete()


def test_create_clone(tables, table_handle):
    table_name = random_string(10, "test_table_")
    created_handle = tables.create(
        table_name, clone_table=f"{table_handle.name}", copy_grants=True, mode="errorifexists"
    )
    try:
        assert created_handle.name == table_name
        assert created_handle.fetch().rows == 2
    finally:
        with suppress(Exception):
            created_handle.delete()

    time.sleep(1)
    table_name = random_string(10, "test_table_")
    created_handle = tables.create(
        table_name,
        clone_table=Clone(
            source=f"{table_handle.name}", point_of_time=PointOfTimeOffset(reference="before", when="-1")
        ),
        copy_grants=True,
        mode="errorifexists",
    )
    try:
        assert created_handle.name == table_name
        assert created_handle.fetch().rows == 2
    finally:
        with suppress(Exception):
            created_handle.delete()

    table_name = random_string(10, "test_table_")
    with pytest.raises(
        NotFoundError,
    ):
        tables.create(table_name, clone_table="non_existant_name", copy_grants=True, mode="errorifexists")


@pytest.mark.parametrize("create_mode", ["errorifexists", "orreplace", "ifnotexists"])
@pytest.mark.skip
def test_create_as_select(tables, table_handle, create_mode):
    table_name = random_string(10, "test_table_")
    copy_grants = True if create_mode == "orreplace" else False
    created_handle = tables.create(
        table_name,
        as_select=f"select * from {table_handle.database.name}.{table_handle.schema.name}.{table_handle.name}"
        " where c1 = 1",
        copy_grants=copy_grants,
        mode=create_mode,
    )
    try:
        table = created_handle.fetch()
        assert created_handle.name == table_name
        assert table.rows == 1
    finally:
        with suppress(Exception):
            created_handle.delete()
