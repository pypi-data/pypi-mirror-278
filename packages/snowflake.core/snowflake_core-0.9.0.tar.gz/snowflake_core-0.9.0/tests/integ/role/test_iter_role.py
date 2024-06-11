import pytest

from tests.utils import random_string

from snowflake.core.role import Role


@pytest.mark.skip("Enable when manage role permission is granted to the test user")
def test_iter(roles, session):
    session.sql("USE ROLE SYSADMIN")
    role_name_1 = random_string(5, "test_role_1")
    role_name_2 = random_string(5, "test_role_2")
    try:
        test_role = Role(name=role_name_1)
        test_role_1 = roles.create(test_role)
        test_role = Role(name=role_name_2)
        test_role_2 = roles.create(test_role)

        test_roles = [role.name for role in roles.iter()]

        assert test_role_1.name.upper() in test_roles
        assert test_role_2.name.upper() in test_roles

        test_roles = [role.name for role in roles.iter(like="TEST_ROLE_%")]

        assert test_role_1.name.upper() in test_roles
        assert test_role_2.name.upper() in test_roles

        test_roles = [role.name for role in roles.iter(like="TEST_ROLE_1%")]

        assert test_role_1.name.upper() in test_roles
        assert test_role_2.name.upper() not in test_roles

        test_roles = roles.iter(limit=1)
        assert len(list(test_roles)) == 1

        # show roles starts_with has a bug and isn't filtering the output as expected.
        # test_roles = roles.iter(starts_with="TEST_ROLE")
        # assert len(list(test_roles)) == 1

    finally:
        session.sql(f"DROP ROLE IF EXISTS {role_name_1}")
        session.sql(f"DROP ROLE IF EXISTS {role_name_2}")
