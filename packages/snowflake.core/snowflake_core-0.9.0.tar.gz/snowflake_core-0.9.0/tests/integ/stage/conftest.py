# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.

import os
import uuid

from typing import Iterator

import pytest

from snowflake.core import Root
from snowflake.core.stage import Stage, StageCollection, StageResource

from ..utils import random_string


RUNNING_ON_GH = os.getenv("GITHUB_ACTIONS") == "true"
TEST_SCHEMA = "GH_JOB_{}".format(str(uuid.uuid4()).replace("-", "_"))


@pytest.fixture(scope="module")
def stages(root: Root, db_parameters, test_schema) -> StageCollection:
    return root.databases[db_parameters["database"]].schemas[test_schema].stages

@pytest.fixture(scope="module")
def temp_stage(stages) -> Iterator[StageResource]:
    stage_name = random_string(5, "test_stage_")
    test_stage = Stage(
        name=stage_name,
        comment="created by temp_stage",
    )
    st = stages.create(test_stage)
    try:
        yield st
    finally:
        st.delete()

@pytest.fixture(scope="module")
def temp_stage_case_sensitive(stages) -> Iterator[StageResource]:
    stage_name = random_string(5, "test_stage_case_sensitive_")
    stage_name_case_sensitive = '"' + stage_name + '"'
    test_stage = Stage(
        name=stage_name_case_sensitive,
        comment="created by temp_stage",
    )
    st = stages.create(test_stage)
    try:
        yield st
    finally:
        st.delete()
