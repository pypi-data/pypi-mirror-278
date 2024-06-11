import copy

import pytest

from snowflake.core.exceptions import ConflictError
from snowflake.core.stage import Stage, StageCollection
from tests.utils import random_string


@pytest.mark.skip
@pytest.mark.jenkins
def test_create_stage(stages: StageCollection):
    new_stage_def = Stage(name=random_string(10, "test_stage_int_test_"))
    new_stage_def.comment = "stage first"
    stage = stages.create(new_stage_def)
    try:
        created_stage = stage.fetch()
        assert created_stage.name == new_stage_def.name.upper()
        assert created_stage.comment == new_stage_def.comment

        with pytest.raises(
            ConflictError,
        ):
            stages.create(new_stage_def, mode="error_if_exists")

        new_stage_def_1 = copy.deepcopy(new_stage_def)
        new_stage_def_1.comment = "stage second"
        stage = stages.create(new_stage_def_1, mode="if_not_exists")

        created_stage = stage.fetch()
        assert created_stage.name == new_stage_def.name.upper()
        assert created_stage.comment == new_stage_def.comment
    finally:
        stage.delete()

    try:
        stage = stages.create(new_stage_def_1, mode="or_replace")

        created_stage = stage.fetch()
        assert created_stage.name == new_stage_def_1.name.upper()
        assert created_stage.comment == new_stage_def_1.comment
    finally:
        stage.delete()

    try:
        stage_name = random_string(10, "test_stage_INT_test_")
        stage_name_case_sensitive = '"' + stage_name + '"'
        new_stage_def = Stage(name=stage_name_case_sensitive)
        stage = stages.create(new_stage_def)

        # TODO(SNOW-1354988) - Please uncomment this once you have this bug resolved
        # created_stage = stage.fetch()
        # assert created_stage.name == new_stage_def.name
    finally:
        stage.delete()
