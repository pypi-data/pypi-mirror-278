import pytest

from snowflake.core.schema import Schema, SchemaResource
from tests.utils import random_string


pytestmark = pytest.mark.usefixtures("backup_database_schema")


# Enable for REST once 8.22 GS in production with native CoA support.
@pytest.mark.skip
def test_update_all_params(schemas, temp_schema: SchemaResource):
    new_sc_def = temp_schema.fetch()
    new_sc_def.comment = "my new comment"
    new_sc_def.data_retention_time_in_days = 0
    new_sc_def.default_ddl_collation = "en_US-trim"
#    new_sc_def.log_level = "INFO"
#    new_sc_def.pipe_execution_paused = True
    new_sc_def.max_data_extension_time_in_days = 7
    new_sc_def.suspend_task_after_num_failures = 1
 #   new_sc_def.trace_level = "ALWAYS"
    new_sc_def.user_task_managed_initial_warehouse_size = "SMALL"
    new_sc_def.user_task_timeout_ms = 3600001
    temp_schema.create_or_update(new_sc_def)
    new_sc = schemas[temp_schema.name].fetch()
    assert new_sc.name == new_sc_def.name
    assert new_sc.comment == new_sc_def.comment
    assert new_sc.data_retention_time_in_days == new_sc_def.data_retention_time_in_days
    assert new_sc.default_ddl_collation == new_sc_def.default_ddl_collation
    assert new_sc.options != 'MANAGED ACCESS'
   # assert new_sc.log_level == new_sc_def.log_level
   # assert new_sc.pipe_execution_paused == new_sc_def.pipe_execution_paused
    assert new_sc.max_data_extension_time_in_days == new_sc_def.max_data_extension_time_in_days
    assert new_sc.suspend_task_after_num_failures == new_sc_def.suspend_task_after_num_failures
  #  assert new_sc.trace_level == new_sc_def.trace_level
    assert new_sc.user_task_managed_initial_warehouse_size == new_sc_def.user_task_managed_initial_warehouse_size
    assert new_sc.user_task_timeout_ms == new_sc_def.user_task_timeout_ms

@pytest.mark.skip(reason="Priviledge issue")
def test_update_with_managed_access(temp_schema: SchemaResource):
    new_sc_def = temp_schema.fetch()
    original_options = new_sc_def.options
    assert original_options != 'MANAGED ACCESS'

    # Test with_managed_access = True
    temp_schema.create_or_update(new_sc_def, with_managed_access = True)
    new_sc_def = temp_schema.fetch()
    assert new_sc_def.options == 'MANAGED ACCESS'

    # Test WITH MANAGEMENT ACCESS + WITH MANAGEMENT ACCESS = WITH MANAGEMENT ACCESS
    temp_schema.create_or_update(new_sc_def, with_managed_access = True)
    new_sc_def = temp_schema.fetch()
    assert new_sc_def.options == 'MANAGED ACCESS'

    # Test WITH MANAGEMENT ACCESS + do nothing = WITH MANAGEMENT ACCESS
    temp_schema.create_or_update(new_sc_def)
    new_sc_def = temp_schema.fetch()
    assert new_sc_def.options == 'MANAGED ACCESS'

    # Test with_managed_access = False
    temp_schema.create_or_update(new_sc_def, with_managed_access = False)
    new_sc_def = temp_schema.fetch()
    assert new_sc_def.options == original_options

    # Test False + False = False
    temp_schema.create_or_update(new_sc_def, with_managed_access = False)
    new_sc_def = temp_schema.fetch()
    assert new_sc_def.options == original_options

    # Test False + do nothing = False
    # Test False + False = False
    temp_schema.create_or_update(new_sc_def)
    new_sc_def = temp_schema.fetch()
    assert new_sc_def.options == original_options

# Enable for REST once 8.22 GS in production with native CoA support.
@pytest.mark.skip
@pytest.mark.parametrize("comment", (None, "ThIs Is A cOmMeNt"))
@pytest.mark.jenkins
def test_update_comment(schemas, comment):
    new_s_name = random_string(3, "test_update_comment_")
    new_s = Schema(name=new_s_name)
    s = schemas.create(new_s)
    try:
        new_s.comment = comment
        s.create_or_update(new_s)
        assert s.fetch().comment == comment
    finally:
        s.delete()
