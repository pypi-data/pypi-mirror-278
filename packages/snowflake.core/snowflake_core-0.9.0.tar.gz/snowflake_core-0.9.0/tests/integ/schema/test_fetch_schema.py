import pytest


pytestmark = pytest.mark.usefixtures("backup_database_schema")


@pytest.mark.skip
@pytest.mark.jenkins
def test_fetch(temp_schema, temp_schema_case_sensitive):
    schema = temp_schema.fetch()
    assert schema.name.upper() == temp_schema.name.upper()

    # TODO(SNOW-1354988) - Please uncomment this once you have this bug resolved
    # schema = temp_schema_case_sensitive.fetch()
    # assert schema.name == temp_schema_case_sensitive.name
    # assert schema.comment == temp_schema_case_sensitive.comment
