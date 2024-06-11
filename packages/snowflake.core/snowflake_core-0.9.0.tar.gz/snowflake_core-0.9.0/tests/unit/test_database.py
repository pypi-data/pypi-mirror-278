from collections import defaultdict
from contextlib import suppress
from unittest import mock

import pytest

from snowflake.core.database import Database
from snowflake.core.version import __version__ as VERSION


pytestmark = pytest.mark.jenkins


SNOWPY_USER_AGENT_VAL = "python_api/" + VERSION

def test_fetch(fake_root, db):
    with suppress(Exception):
        with mock.patch("snowflake.core.database._generated.api_client.ApiClient.request") as mocked_request:
            db.fetch()
    mocked_request.assert_called_once_with(
        fake_root,
        "GET",
        "http://localhost:80/api/v2/databases/my_db",
        query_params=[],
        headers={"Accept": "application/json", "User-Agent": SNOWPY_USER_AGENT_VAL},
        post_params=[],
        body=None,
        _preload_content=True,
        _request_timeout=None,
    )


def test_delete(fake_root, db):
    with mock.patch("snowflake.core.database._generated.api_client.ApiClient.request") as mocked_request:
        db.delete()
    mocked_request.assert_called_once_with(
        fake_root,
        "DELETE",
        "http://localhost:80/api/v2/databases/my_db",
        query_params=[],
        headers={"Accept": "application/json", "User-Agent": SNOWPY_USER_AGENT_VAL},
        post_params=[],
        body=None,
        _preload_content=True,
        _request_timeout=None,
    )


def test_create(fake_root, dbs):
    with mock.patch("snowflake.core.database._generated.api_client.ApiClient.request") as mocked_request:
        dbs.create(
            Database(
                name="sophie_db",
                comment="This is Sophie's database",
                trace_level="always",
            ),
            kind="transient",
        )
    mocked_request.assert_called_once_with(
        fake_root,
        "POST",
        "http://localhost:80/api/v2/databases?createMode=errorIfExists&kind=transient",
        query_params=[
            ("createMode", "errorIfExists"),
            ("kind", "transient"),
        ],
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": SNOWPY_USER_AGENT_VAL,
        },
        post_params=[],
        body={"name": "sophie_db", "comment": "This is Sophie's database", "trace_level": "always", "dropped_on": None},
        _preload_content=True,
        _request_timeout=None,
    )


def test_create_from_share(fake_root, dbs):
    with mock.patch("snowflake.core.database._generated.api_client.ApiClient.request") as mocked_request:
        dbs._create_from_share(
            name="name",
            share="share",
        )
    mocked_request.assert_called_once_with(
        fake_root,
        "POST",
        "http://localhost:80/api/v2/databases/name:from_share?createMode=errorIfExists&share=share&kind=",
        query_params=[
            ("createMode", "errorIfExists"),
            ("share", "share"),
            ("kind", ""),
        ],
        headers={"Accept": "application/json", "User-Agent": SNOWPY_USER_AGENT_VAL},
        post_params=[],
        body=None,
        _preload_content=True,
        _request_timeout=None,
    )


def test_enable_replication(fake_root, db):
    with mock.patch("snowflake.core.database._generated.api_client.ApiClient.request") as mocked_request:
        db.enable_replication(["fake_identifier1", "fake_identifier2"])
    mocked_request.assert_called_once_with(
        fake_root,
        "POST",
        "http://localhost:80/api/v2/databases/my_db/replication:enable?ignore_edition_check=False",
        query_params=[
            ("ignore_edition_check", False),
        ],
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": SNOWPY_USER_AGENT_VAL,
        },
        post_params=[],
        body={"accounts": ["fake_identifier1", "fake_identifier2"]},
        _preload_content=True,
        _request_timeout=None,
    )


def test_disable_replication(fake_root, db):
    with mock.patch("snowflake.core.database._generated.api_client.ApiClient.request") as mocked_request:
        db.disable_replication()
    mocked_request.assert_called_once_with(
        fake_root,
        "POST",
        "http://localhost:80/api/v2/databases/my_db/replication:disable",
        query_params=[],
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": SNOWPY_USER_AGENT_VAL,
        },
        post_params=[],
        body={"accounts": []},
        _preload_content=True,
        _request_timeout=None,
    )


def test_refresh_replication(fake_root, db):
    with mock.patch("snowflake.core.database._generated.api_client.ApiClient.request") as mocked_request:
        db.refresh_replication()
    mocked_request.assert_called_once_with(
        fake_root,
        "POST",
        "http://localhost:80/api/v2/databases/my_db/replication:refresh",
        query_params=[],
        headers={"Accept": "application/json", "User-Agent": SNOWPY_USER_AGENT_VAL},
        post_params=[],
        body=None,
        _preload_content=True,
        _request_timeout=None,
    )


def test_enable_failover(fake_root, db):
    with mock.patch("snowflake.core.database._generated.api_client.ApiClient.request") as mocked_request:
        db.enable_failover(["fake_identifier1", "fake_identifier2"])
    mocked_request.assert_called_once_with(
        fake_root,
        "POST",
        "http://localhost:80/api/v2/databases/my_db/failover:enable",
        query_params=[],
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": SNOWPY_USER_AGENT_VAL,
        },
        post_params=[],
        body={"accounts": ["fake_identifier1", "fake_identifier2"]},
        _preload_content=True,
        _request_timeout=None,
    )


def test_disable_failover(fake_root, db):
    with mock.patch("snowflake.core.database._generated.api_client.ApiClient.request") as mocked_request:
        db.disable_failover()
    mocked_request.assert_called_once_with(
        fake_root,
        "POST",
        "http://localhost:80/api/v2/databases/my_db/failover:disable",
        query_params=[],
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": SNOWPY_USER_AGENT_VAL,
        },
        post_params=[],
        body={"accounts": []},
        _preload_content=True,
        _request_timeout=None,
    )


def test_promote_to_primary_failover(fake_root, db):
    with mock.patch("snowflake.core.database._generated.api_client.ApiClient.request") as mocked_request:
        db.promote_to_primary_failover()
    mocked_request.assert_called_once_with(
        fake_root,
        "POST",
        "http://localhost:80/api/v2/databases/my_db/failover:primary",
        query_params=[],
        headers={"Accept": "application/json", "User-Agent": SNOWPY_USER_AGENT_VAL},
        post_params=[],
        body=None,
        _preload_content=True,
        _request_timeout=None,
    )


request_called_count_for_long_running = defaultdict(int)


def mocked_request_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, data, status):
            self.data = data
            self.status = status

        def getheader(self, param):
            return {"Location": "/api/v2/results/XXXX"}.get(param, None)

    url = args[2]

    global request_called_count_for_long_running
    if "api/v2/databases" in url:
        request_called_count_for_long_running["database"] += 1
        return MockResponse(None, 202)

    assert "api/v2/result" in url
    request_called_count_for_long_running["result"] += 1
    if request_called_count_for_long_running.get("result", 0) < 2:
        return MockResponse(None, 202)
    return None


# def test_fetch_with_long_running(fake_root, setup_enable_rest_api_with_long_running):
#     dbs = DatabaseCollection(fake_root)
#     with setup_enable_rest_api_with_long_running(dbs._ref_class):
#         with mock.patch(
#             "snowflake.core.database._generated.api_client.ApiClient.request",
#             side_effect=mocked_request_get,
#         ):
#             # TODO: Improve fetch results instead of error
#             try:
#                 dbs["my_db"].fetch()
#             except AttributeError:
#                 # TODO: The AttributeError message is not reliable, so we just catch it and
#                 # pass for now. Make this better
#                 # assert e.args[0] == "'NoneType' object has no attribute 'status'"
#                 pass
#         global request_called_count_for_long_running
#         assert request_called_count_for_long_running['database'] == 1
#         assert request_called_count_for_long_running['result'] == 2
