from contextlib import suppress
from unittest import mock

import pytest

from snowflake.core.version import __version__ as VERSION


pytestmark = pytest.mark.jenkins


SNOWPY_USER_AGENT_VAL = "python_api/" + VERSION

def test_create_dynamic_table(fake_root, dynamic_tables, dynamic_table):
    with suppress(Exception):
        with mock.patch("snowflake.core.dynamic_table._generated.api_client.ApiClient.request") as mocked_request:
            dynamic_tables.create(dynamic_table)
    mocked_request.assert_called_once_with(
        fake_root,
        "POST",
        "http://localhost:80/api/v2/databases/my_db/schemas/my_schema/dynamic-tables?createMode=errorIfExists",
        query_params=[("createMode", "errorIfExists")],
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": SNOWPY_USER_AGENT_VAL,
        },
        post_params=[],
        body={
            "name": "my_table",
            "kind": "PERMANENT",
            "target_lag": {"type": "DOWNSTREAM"},
            "warehouse": "wh",
            "columns": [{"name": "c1", "datatype": "int"}],
            "query": "SELECT * FROM foo",
        },
        _preload_content=True,
        _request_timeout=None,
    )


def test_create_dynamic_table_clone(fake_root, dynamic_tables):
    with suppress(Exception):
        with mock.patch("snowflake.core.dynamic_table._generated.api_client.ApiClient.request") as mocked_request:
            dynamic_tables.create("my_table", clone_table="temp_clone_table")
    mocked_request.assert_called_once_with(
        fake_root,
        "POST",
        "http://localhost:80/api/v2/databases/my_db/schemas/my_schema/dynamic-tables/temp_clone_table:clone?createMode=errorIfExists&copyGrants=False",
        query_params=[("createMode", "errorIfExists"), ("copyGrants", False)],
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": SNOWPY_USER_AGENT_VAL,
        },
        post_params=[],
        body={"name": "my_table"},
        _preload_content=True,
        _request_timeout=None,
    )
