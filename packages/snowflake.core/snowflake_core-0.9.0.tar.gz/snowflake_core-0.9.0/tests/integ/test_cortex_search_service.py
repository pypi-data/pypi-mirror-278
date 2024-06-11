#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#

import pytest

from snowflake.core.cortex.search_service import QueryRequest


TEST_SERVICE_NAME = "SNOWPY_TEST_SERVICE"

@pytest.fixture
def setup_cortex_search_service(connection):
    with connection.cursor() as cursor:
        warehouse_name = cursor.execute(
            "SELECT /* setup_basic */ CURRENT_WAREHOUSE()"
        ).fetchone()[0]

        test_table_name = "SNOWPY_TEST_TABLE"
        # Base Table
        cursor.execute(
            f"CREATE OR REPLACE TABLE {test_table_name} (col1 VARCHAR, col2 VARCHAR)",
        )

        rows = ",".join(["('hi', 'hello')"] * 20)
        cursor.execute(
            f"INSERT INTO {test_table_name} VALUES {rows}",
        )

        # Cortex Search Service
        cursor.execute(
            f"CREATE OR REPLACE CORTEX SEARCH SERVICE {TEST_SERVICE_NAME} "
            f"ON col1 TARGET_LAG='1 minute' WAREHOUSE={warehouse_name} "
            f"AS SELECT col1, col2 FROM {test_table_name}",
        )

        try:
            yield
        finally:
            cursor.execute(f"DROP CORTEX SEARCH SERVICE {TEST_SERVICE_NAME}")
            cursor.execute(f"DROP TABLE {test_table_name}")


pytestmark = pytest.mark.usefixtures("setup_cortex_search_service")


@pytest.mark.skip(
    "This requires an account which has the Cortex Search feature enabled."
)
def test_search(cortex_search_services):
    resp = cortex_search_services[TEST_SERVICE_NAME].search(
        "hi", ["col1", "col2"], limit=5
    )
    assert len(resp.results) == 5
    for row in resp.results:
        assert row["col1"] is not None
        assert row["col2"] is not None


@pytest.mark.skip(
    "This requires an account which has the Cortex Search feature enabled."
)
def test_search_collection(cortex_search_services):
    resp = cortex_search_services.search(
        TEST_SERVICE_NAME,
        QueryRequest.from_dict(
            {"query": "hi", "columns": ["col1", "col2"], "limit": 5}
        ),
    )
    assert len(resp.results) == 5
    for row in resp.results:
        assert row["col1"] is not None
        assert row["col2"] is not None
