import pytest


@pytest.mark.jenkins
@pytest.mark.skip
def test_fetch(temp_stage, temp_stage_case_sensitive):
    stage = temp_stage.fetch()
    assert stage.name.upper() == temp_stage.name.upper()

    # TODO(SNOW-1354988) - Please uncomment this once you have this bug resolved
    # stage = temp_stage_case_sensitive.fetch()
    # assert stage.name == temp_stage_case_sensitive.name
    # assert stage.comment == temp_stage_case_sensitive.comment
