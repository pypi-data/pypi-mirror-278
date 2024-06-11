#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#


import pytest


pytestmark = pytest.mark.usefixtures("backup_database_schema")


@pytest.mark.skip
@pytest.mark.jenkins
def test_fetch(databases, temp_db):
    database = databases[temp_db.name].fetch()
    assert database.name.upper() == temp_db.name.upper()
    assert database.comment == "created by temp_db"


@pytest.mark.skip("This could only test in local dev-vm when set qa_mode = true")
@pytest.mark.jenkins
def test_fetch_with_long_running(
    databases,
    temp_db,
    setup_with_connector_execution,
):
    alter_prefix = "alter session "
    with setup_with_connector_execution(
        [
            alter_prefix + "set TEST_SNOWAPI_TIME_OUT_REQUEST_ASYNC = true",
        ],
        [
            alter_prefix + "unset TEST_SNOWAPI_TIME_OUT_REQUEST_ASYNC",
        ],
    ):
        database = databases[temp_db.name].fetch()
        assert database.name.upper() == temp_db.name.upper()
