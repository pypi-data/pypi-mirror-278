#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#
import copy
import time

import pytest

from snowflake.core import Clone, PointOfTimeOffset
from snowflake.core.database import Database, DatabaseCollection
from snowflake.core.exceptions import APIError, ConflictError

from ..utils import random_string


pytestmark = pytest.mark.usefixtures("backup_database_schema")


def test_create_database(databases: DatabaseCollection):
    new_db_def = Database(name=random_string(3, "test_database_$12create_"))
    new_db_def.comment = "database first"
    database = databases.create(new_db_def, kind="TRANSIENT")
    try:
        created_database = database.fetch()
        assert created_database.name == new_db_def.name.upper()
        assert created_database.comment == new_db_def.comment

        with pytest.raises(
            ConflictError,
        ):
            databases.create(new_db_def, mode="error_if_exists")

        new_db_def_1 = copy.deepcopy(new_db_def)
        new_db_def_1.comment = "databse second"
        database = databases.create(new_db_def_1, mode="if_not_exists")

        created_database = database.fetch()
        assert created_database.name == new_db_def.name.upper()
        assert created_database.comment == new_db_def.comment
    finally:
        database.delete()

    try:
        database = databases.create(new_db_def_1, mode="or_replace")

        created_database = database.fetch()
        assert created_database.name == new_db_def_1.name.upper()
        assert created_database.comment == new_db_def_1.comment
    finally:
        database.delete()

    try:
        database_name = random_string(10, "test_database_INT_test_")
        database_name_case_sensitive = '"' + database_name + '"'
        new_db_def = Database(name=database_name_case_sensitive)
        database = databases.create(new_db_def)
        # TODO(SNOW-1354988) - Please uncomment this once you have this bug resolved
        # created_database = database.fetch()
        # assert created_database.name == new_db_def.name
    finally:
        database.delete()

    try:
        database_name = random_string(10, 'test_database_""INT""_test_#_')
        database_name_case_sensitive = '"' + database_name + '"'
        new_db_def = Database(name=database_name_case_sensitive)
        database = databases.create(new_db_def)
        # TODO(SNOW-1354988) - Please uncomment this once you have this bug resolved
        # created_database = database.fetch()
        # assert created_database.name == new_db_def.name
    finally:
        database.delete()


@pytest.mark.skip("Temporarily disabled. TODO: Investigate why this is flaky.")
@pytest.mark.jenkins
def test_create_clone(databases: DatabaseCollection):
    database_name = random_string(3, "test_database_create_clone_")
    new_db_def = Database(name=database_name)

    # error because Schema does not exist
    with pytest.raises(APIError):
        db = databases.create(
            new_db_def,
            clone=Clone(source=database_name, point_of_time=PointOfTimeOffset(reference="before", when="-1")),
            mode="orreplace",
        )

    databases.create(new_db_def, kind="TRANSIENT")

    # error because transient database cannot be cloned
    with pytest.raises(APIError):
        db = databases.create(
            new_db_def,
            clone=Clone(source=database_name, point_of_time=PointOfTimeOffset(reference="before", when="-1")),
            mode="orreplace",
        )

    # replaced transient to permanent schema
    databases.create(new_db_def, mode="or_replace")

    time.sleep(2)
    db = databases.create(
        new_db_def,
        clone=Clone(source=database_name, point_of_time=PointOfTimeOffset(reference="before", when="-1")),
        mode="orreplace",
    )
    try:
        db.fetch()
    finally:
        db.delete()


@pytest.mark.skip("Temporarily disabled. TODO: Investigate why this is flaky.")
@pytest.mark.env("online")
@pytest.mark.jenkins
def test_create_from_share(databases: DatabaseCollection):
    new_db_name = random_string(3, "test_db_from_share_")
    db = databases._create_from_share(
        new_db_name,
        share='SFSALESSHARED.SFC_SAMPLES_PROD3."SAMPLE_DATA"',
    )
    try:
        assert db.fetch().is_current
    finally:
        db.delete()
