import copy

from time import sleep

import pytest

from snowflake.core import Clone, PointOfTimeOffset
from snowflake.core.exceptions import APIError, ConflictError
from snowflake.core.schema import Schema, SchemaCollection
from tests.utils import random_string


pytestmark = pytest.mark.usefixtures("backup_database_schema")


def test_create_schema(schemas: SchemaCollection):
    new_schema_def = Schema(name=random_string(10, "test_schema_int_test_"))
    new_schema_def.comment = "schema first"
    schema = schemas.create(new_schema_def, kind="TRANSIENT")
    try:
        created_schema = schema.fetch()
        assert created_schema.name == new_schema_def.name.upper()
        assert created_schema.comment == new_schema_def.comment
        assert created_schema.options != 'MANAGED ACCESS'

        with pytest.raises(
            ConflictError,
        ):
            schemas.create(new_schema_def, mode="error_if_exists")

        new_schema_def_1 = copy.deepcopy(new_schema_def)
        new_schema_def_1.comment = "schema second"
        schema = schemas.create(new_schema_def_1, mode="if_not_exists")

        created_schema = schema.fetch()
        assert created_schema.name == new_schema_def.name.upper()
        assert created_schema.comment == new_schema_def.comment
        assert created_schema.options != 'MANAGED ACCESS'
    finally:
        schema.delete()

    try:
        schema = schemas.create(new_schema_def_1, mode="or_replace")

        created_schema = schema.fetch()
        assert created_schema.name == new_schema_def_1.name.upper()
        assert created_schema.comment == new_schema_def_1.comment
    finally:
        schema.delete()

    try:
        schema_name = random_string(10, "test_schema_INT_test_")
        schema_name_case_sensitive = '"' + schema_name + '"'
        new_schema_def = Schema(name=schema_name_case_sensitive)
        schema = schemas.create(new_schema_def)
        # TODO(SNOW-1354988) - Please uncomment this once you have this bug resolved
        # created_schema = schema.fetch()
        # assert created_schema.name == new_schema_def.name
    finally:
        schema.delete()

@pytest.mark.skip("Enable when the schema managed access changes make it to prod")
def test_create_with_managed_access(schemas: SchemaCollection):
    new_schema_def = Schema(name=random_string(10, "test_schema_int_test_"), managed_access=True)
    try:
        schema = schemas.create(new_schema_def, mode="or_replace")

        created_schema = schema.fetch()
        assert created_schema.name == new_schema_def.name.upper()
        assert created_schema.managed_access is True
        assert created_schema.options == 'MANAGED ACCESS'
    finally:
        schema.delete()

@pytest.mark.jenkins
@pytest.mark.skip("Temporarily disabled. TODO: Investigate why this is flaky.")
def test_create_clone(schemas: SchemaCollection):
    schema_name = random_string(10, "test_schema_clone")
    new_schema_def = Schema(name=schema_name)

    # error because Schema does not exist
    with pytest.raises(APIError):
        schema = schemas.create(
            new_schema_def,
            clone=Clone(source=schema_name, point_of_time=PointOfTimeOffset(reference="at", when="-5")),
            mode="orreplace",
        )

    schemas.create(new_schema_def, kind="TRANSIENT")
    # error because transient schema cannot be cloned
    with pytest.raises(APIError):
        schema = schemas.create(
            new_schema_def,
            clone=Clone(source=schema_name, point_of_time=PointOfTimeOffset(reference="at", when="-5")),
            mode="orreplace",
        )

    # replaced transient to permanent schema
    schemas.create(new_schema_def, mode="or_replace")
    sleep(2)
    schema = schemas.create(
        new_schema_def,
        clone=Clone(source=schema_name, point_of_time=PointOfTimeOffset(reference="at", when="-1")),
        mode="orreplace",
    )
    try:
        schema.fetch()
    finally:
        schema.delete()
