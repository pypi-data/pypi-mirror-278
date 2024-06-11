# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.

import os
import uuid

from contextlib import contextmanager
from io import BytesIO
from textwrap import dedent
from typing import Dict, Generator, Iterator, List, NamedTuple

import pytest

from pydantic import StrictStr

import snowflake.connector

from snowflake.core import Root
from snowflake.core.compute_pool import (
    ComputePool,
    ComputePoolCollection,
)
from snowflake.core.cortex.search_service import CortexSearchServiceCollection
from snowflake.core.database import (
    Database,
    DatabaseCollection,
    DatabaseResource,
)
from snowflake.core.function import FunctionCollection
from snowflake.core.grant._grants import Grants
from snowflake.core.image_repository import (
    ImageRepository,
    ImageRepositoryCollection,
)
from snowflake.core.role import RoleCollection
from snowflake.core.schema import (
    Schema,
    SchemaCollection,
    SchemaResource,
)
from snowflake.core.service import (
    Service,
    ServiceCollection,
    ServiceResource,
    ServiceSpecInlineText,
    ServiceSpecStageFile,
)
from snowflake.core.user import UserCollection
from snowflake.core.warehouse import WarehouseCollection
from snowflake.snowpark import Session

from .utils import random_string


RUNNING_ON_GHA = os.getenv("GITHUB_ACTIONS") == "true"
RUNNING_ON_JENKINS = "JENKINS_URL" in os.environ
JENKINS_RUN_ALL_TESTS = "SF_JENKINS_RUN_ALL_TESTS" in os.environ
TEST_SCHEMA = "GH_JOB_{}".format(str(uuid.uuid4()).replace("-", "_"))


@pytest.fixture(scope="session")
def running_on_public_ci() -> bool:
    return RUNNING_ON_GHA


@pytest.fixture(scope="session")
def running_on_private_ci():
    return RUNNING_ON_JENKINS


def print_help() -> None:
    print(
        """Connection parameter must be specified in parameters.py,
    for example:
CONNECTION_PARAMETERS = {
    'account': 'testaccount',
    'user': 'user1',
    'password': 'test',
    'database': 'testdb',
    'schema': 'public',
}
"""
    )


def pytest_runtest_setup(item):
    # Skip online tests when not running on GHA
    # TODO: make the naming of this marker consistent with the other skip_xzy markers
    envnames = [mark.args[0] for mark in item.iter_markers(name="env")]
    if envnames:
        if "online" in envnames:
            if not RUNNING_ON_GHA:
                pytest.skip(f"local test skip {envnames!r} tests")
    # Skip any test not marked for Jenkins when running on Jenkins
    if RUNNING_ON_JENKINS and not JENKINS_RUN_ALL_TESTS:
        jenkins_marker = list(item.iter_markers(name="jenkins"))
        if not jenkins_marker:
            pytest.skip("this test is not supposed to run on Jenkins")


@pytest.fixture(scope="session")
def db_parameters() -> Dict[str, str]:
    # If its running on our public CI, replace the schema
    # If its running on our public CI, replace the schema
    #
    # For legacy purposes, look to see if there's a parameters.py file and if
    # so, use its credentials.  To use the newer ~/.snowflake/config.toml file
    # credentials, delete parameters.py.
    try:
        from ..parameters import CONNECTION_PARAMETERS
    except ImportError:
        CONNECTION_PARAMETERS = None
        from snowflake.connector.config_manager import CONFIG_MANAGER

    # 2023-06-23(warsaw): By default, we read out of the [connections.snowflake] section in the config.toml file, but by
    # setting the environment variable SNOWFLAKE_DEFAULT_CONNECTION_NAME you can read out of a different section.
    # For example SNOWFLAKE_DEFAULT_CONNECTION_NAME='test' reads out of [connections.test]

    level0, level1 = ("connections", CONFIG_MANAGER["default_connection_name"])

    if CONNECTION_PARAMETERS is None:
        config = CONFIG_MANAGER[level0][level1]
    else:
        config = CONNECTION_PARAMETERS

    config["schema"] = TEST_SCHEMA
    config["database"] = "TESTDB_PYTHON_AUTO"
    return config


# 2023-06-21(warsaw): WARNING!  If any of these fixtures fail, they will print
# db_parameters in the traceback, and that **will** leak the password.  pytest
# doesn't seem to have any way to suppress the password, and I've tried lots
# of things to get that to work, to no avail.


@pytest.fixture(scope="session")
def connection(db_parameters):
    _keys = ["user", "password", "host", "port", "database", "account", "protocol", "role", "warehouse"]
    with snowflake.connector.connect(
        # This works around SNOW-998521, by forcing JSON results
        **{k: db_parameters[k] for k in _keys if k in db_parameters}
    ) as con:
        yield con


@pytest.fixture(scope="session")
def session(connection):
    return Session.builder.config("connection", connection).create()


@pytest.fixture(scope="session")
def root(connection) -> Root:
    return Root(connection)


@pytest.fixture(scope="session")
def database(root, db_parameters) -> DatabaseResource:
    return root.databases[db_parameters["database"]]


@pytest.fixture(scope="session")
def schema(schemas, db_parameters) -> SchemaResource:
    return schemas[db_parameters["schema"]]


@pytest.fixture(scope="module")
def image_repositories(schema) -> ImageRepositoryCollection:
    return schema.image_repositories


@pytest.fixture(scope="module")
def compute_pools(root) -> ComputePoolCollection:
    return root.compute_pools


@pytest.fixture(scope="module")
def warehouses(root) -> WarehouseCollection:
    return root.warehouses


@pytest.fixture(scope="session")
def services(schema) -> ServiceCollection:
    return schema.services


@pytest.fixture(scope="session")
def functions(schema) -> FunctionCollection:
    return schema.functions


@pytest.fixture(scope="session")
def databases(root, db_parameters) -> DatabaseCollection:
    return root.databases


@pytest.fixture(scope="session")
def schemas(database) -> SchemaCollection:
    return database.schemas


@pytest.fixture(scope="module")
def roles(root) -> RoleCollection:
    return root.roles


@pytest.fixture(scope="module")
def users(root) -> UserCollection:
    return root.users

@pytest.fixture(scope="module")
def grants(root) -> Grants:
    return root.grants


@pytest.fixture(scope="session")
def cortex_search_services(schema) -> CortexSearchServiceCollection:
    return schema.cortex_search_services


@pytest.fixture(scope="session", autouse=True)
def test_schema(connection) -> Generator[str, None, None]:
    """Set up and tear down the test schema. This is automatically called per test session."""
    with connection.cursor() as cursor:
        database = cursor.execute("SELECT CURRENT_DATABASE()").fetchone()[0]
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {TEST_SCHEMA}")
        try:
            yield TEST_SCHEMA
        finally:
            cursor.execute(f"USE DATABASE {database}")
            cursor.execute(f"DROP SCHEMA IF EXISTS {TEST_SCHEMA}")


@pytest.fixture
def temp_ir(image_repositories) -> Generator[ImageRepository, None, None]:
    ir_name = random_string(5, "test_ir_")
    test_ir = ImageRepository(
        name=ir_name,
        # TODO: comment is not supported by image repositories?
        # comment="created by temp_ir",
    )
    image_repositories.create(test_ir)
    yield test_ir
    image_repositories[test_ir.name].delete()


@pytest.fixture
def temp_cp(compute_pools) -> Generator[ComputePool, None, None]:
    cp_name = random_string(5, "test_cp_")
    test_cp = ComputePool(
        name=cp_name, instance_family="CPU_X64_XS", min_nodes=1, max_nodes=1, comment="created by temp_cp"
    )
    compute_pools.create(test_cp)
    yield test_cp
    compute_pools[test_cp.name].delete()


@pytest.fixture
def temp_service(root, services, session, imagerepo) -> Iterator[ServiceResource]:
    stage_name = random_string(5, "test_stage_")
    s_name = random_string(5, "test_service_")
    session.sql(f"create temp stage {stage_name};").collect()
    spec_file = "spec.yaml"
    spec = f"@{stage_name}/{spec_file}"
    session.file.put_stream(
        BytesIO(
            dedent(
                f"""
                spec:
                  containers:
                  - name: hello-world
                    image: {imagerepo}/hello-world:latest
                 """
            ).encode()
        ),
        spec,
    )
    test_s = Service(
        name=s_name,
        compute_pool="ci_compute_pool",
        spec=ServiceSpecStageFile(stage=stage_name, spec_file=spec_file),
        min_instances=1,
        max_instances=1,
        comment="created by temp_service",
    )
    s = services.create(test_s)
    yield test_s
    s.delete()


@pytest.fixture
def temp_service_from_spec_inline(root, services, session, imagerepo) -> Iterator[ServiceResource]:
    s_name = random_string(5, "test_service_")
    inline_spec = dedent(
        f"""
        spec:
          containers:
          - name: hello-world
            image: {imagerepo}/hello-world:latest
         """
    )
    test_s = Service(
        name=s_name,
        compute_pool="ci_compute_pool",
        spec=ServiceSpecInlineText(spec_text=inline_spec),
        min_instances=1,
        max_instances=1,
        comment="created by temp_service_from_spec_inline",
    )
    s = services.create(test_s)
    yield test_s
    s.delete()


@pytest.fixture
def backup_database_schema(connection):
    """Reset the current database and schema after a test is complete.

    These 2 resources go hand-in-hand, so they should be backed up together.
    This fixture should be used when a database, or schema is created,
    or used in a test.
    """
    with connection.cursor() as cursor:
        database_name = cursor.execute("SELECT /* backup_database_schema */ CURRENT_DATABASE()").fetchone()[0]
        schema_name = cursor.execute("SELECT /* backup_database_schema */ CURRENT_SCHEMA()").fetchone()[0]
        try:
            yield
        finally:
            if schema_name is not None:
                cursor.execute(f"USE SCHEMA /* backup_database_schema */ {database_name}.{schema_name}")
            elif database_name is not None:
                cursor.execute(f"USE DATABASE /* backup_database_schema */ {database_name}")


@pytest.fixture
def backup_warehouse(connection):
    """Reset the current warehouse after a test is complete.

    This fixture should be used when a warehouse is created, or used in a test.
    """
    with connection.cursor() as cursor:
        warehouse_name = cursor.execute("SELECT /* backup_warehouse */ CURRENT_WAREHOUSE()").fetchone()[0]
        try:
            yield
        finally:
            if warehouse_name is not None:
                cursor.execute(f"USE WAREHOUSE /* backup_warehouse */ {warehouse_name};")


@pytest.fixture
@pytest.mark.usefixtures("backup_database_schema")
def temp_db(databases: DatabaseCollection) -> Iterator[DatabaseResource]:
    # create temp database
    db_name = random_string(5, "test_database_")
    test_db = Database(name=db_name, comment="created by temp_db")
    db = databases.create(test_db)
    try:
        yield db
    finally:
        db.delete()


@pytest.fixture
@pytest.mark.usefixtures("backup_database_schema")
def temp_db_case_sensitive(databases: DatabaseCollection) -> Iterator[DatabaseResource]:
    # create temp database
    db_name = random_string(5, "test_database_case_sensitive_")
    db_name_case_sensitive = '"' + db_name + '"'
    test_db = Database(name=db_name_case_sensitive, comment="created by temp_case_sensitive_db")
    db = databases.create(test_db)
    try:
        yield db
    finally:
        db.delete()


@pytest.fixture
@pytest.mark.usefixtures("backup_database_schema")
def temp_schema(schemas) -> Iterator[SchemaResource]:
    schema_name = random_string(5, "test_schema_")
    test_schema = Schema(
        name=schema_name,
        comment="created by temp_schema",
    )
    sc = schemas.create(test_schema)
    try:
        yield sc
    finally:
        sc.delete()


@pytest.fixture
@pytest.mark.usefixtures("backup_database_schema")
def temp_schema_case_sensitive(schemas) -> Iterator[SchemaResource]:
    schema_name = random_string(5, "test_schema_case_sensitive_")
    schema_name_case_sensitive = '"' + schema_name + '"'
    test_schema = Schema(
        name=schema_name_case_sensitive,
        comment="created by temp_schema_case_sensitive",
    )
    sc = schemas.create(test_schema)
    try:
        yield sc
    finally:
        sc.delete()


# TODO: SNOW-1297234 Organize NamedTuples in stack
class Tuple_database(NamedTuple):
    name: str
    param: str


AUTO_database = Tuple_database(name="TESTDB_PYTHON_AUTO", param="DATA_RETENTION_TIME_IN_DAYS=1")


class Tuple_schema(NamedTuple):
    name: str
    db: str


AUTO_schema = Tuple_schema(name=TEST_SCHEMA, db="TESTDB_PYTHON_AUTO")


@pytest.fixture(scope="session", autouse=True)
def setup_basic(connection):
    with connection.cursor() as cursor:
        # Like backup_database_schema, but scope of this fixture is session
        database_name = cursor.execute("SELECT /* setup_basic */ CURRENT_DATABASE()").fetchone()[0]
        schema_name = cursor.execute("SELECT /* setup_basic */ CURRENT_SCHEMA()").fetchone()[0]

        # Database
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS /* setup_basic */ " f"{AUTO_database.name} {AUTO_database.param}",
        )

        # Schema
        cursor.execute(f"USE DATABASE {AUTO_schema.db}")
        cursor.execute(f"CREATE SCHEMA IF NOT EXISTS {AUTO_schema.name}")

        cursor.execute("USE DATABASE TESTDB_PYTHON_AUTO")
        cursor.execute(f"USE SCHEMA {TEST_SCHEMA}")

        try:
            yield
        finally:
            if schema_name is not None:
                cursor.execute(f"USE SCHEMA /* backup_database_schema */ {database_name}.{schema_name}")
            elif database_name is not None:
                cursor.execute(f"USE DATABASE /* backup_database_schema */ {database_name}")


@pytest.fixture
def imagerepo() -> str:
    # When adding an inlined image repository YAML file, don't hard code the path to the test image
    # repository.  Instead, use this fixture and f-string this value in for the `{imagrepo}` substitution.
    # This way, there's only one thing to change across the entire test suite.
    # Legacy: return 'sfengineering-ss-lprpr-test2.registry
    #    .snowflakecomputing.com/testdb_python/public/ci_image_repository'
    return (
        "sfengineering-ss-lprpr-test2.registry.snowflakecomputing.com/"
        + "testdb_python_auto/testschema_auto/test_image_repo_auto"
    )


@pytest.fixture
def setup_with_connector_execution(connection):
    @contextmanager
    def _setup(sqls_to_enable: List[StrictStr], sqls_to_disable: List[StrictStr]):
        with connection.cursor() as cursor:
            for sql in sqls_to_enable:
                cursor.execute(sql)

            try:
                yield
            finally:
                for sql in sqls_to_disable:
                    cursor.execute(sql)

    return _setup
