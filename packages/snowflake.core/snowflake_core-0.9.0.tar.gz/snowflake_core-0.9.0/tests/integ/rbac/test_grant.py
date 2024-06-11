import pytest

from tests.utils import random_string

from snowflake.core.exceptions import NotFoundError
from snowflake.core.grant._grant import Grant
from snowflake.core.grant._grantee import Grantees
from snowflake.core.grant._privileges import Privileges
from snowflake.core.grant._securables import Securables
from snowflake.core.role import Role


@pytest.mark.skip("Enable when Role is available on prod")
def test_apply_grant(roles, grants, session):
    role_name = random_string(4, "test_grant_role_")
    try:
        test_role = Role(
            name=role_name,
            comment="test_comment"
        )
        roles.create(test_role)
        grants.grant(Grant(
            grantee=Grantees.role(name=role_name),
            securable=Securables.current_account,
            privileges=[Privileges.create_database, Privileges.create_compute_pool, Privileges.create_warehouse]
        ))
    finally:
        session.sql(f"DROP ROLE IF EXISTS {role_name}")


@pytest.mark.skip("Enable when Role is available on prod")
def test_apply_grant_with_grant_opt(roles, grants, session):
    role_name = random_string(4, "test_grant_role_")
    try:
        test_role = Role(
            name=role_name,
            comment="test_comment"
        )
        roles.create(test_role)
        grants.grant(Grant(
            grantee=Grantees.role(name=role_name),
            securable=Securables.current_account,
            privileges=[Privileges.create_database],
            grant_option=False
        ))
    finally:
        session.sql(f"DROP ROLE IF EXISTS {role_name}")


@pytest.mark.skip("Enable when Role is available on prod")
def test_grant_role_to_another_role(roles, grants, session):
    role_one = random_string(4, "test_grant_role_")
    role_two = random_string(4, "test_grant_role_")

    try:
        for role in [role_one, role_two]:
            roles.create(Role(
                name=role,
                comment="test_comment"
            ))

        grants.grant(Grant(
            grantee=Grantees.role(role_one),
            securable=Securables.role(role_two)
        ))

    finally:
        session.sql(f"DROP ROLE IF EXISTS {role_one}")
        session.sql(f"DROP ROLE IF EXISTS {role_two}")


@pytest.mark.skip("Enable when Role is available on prod")
def test_grants_for_invalid_role_names(roles, grants, session):
    with pytest.raises(NotFoundError):
        grants.grant(Grant(
            grantee=Grantees.role(name="\"some-random-role\""),
            securable=Securables.current_account,
            privileges=[Privileges.create_database],
            grant_option=False
        ))


@pytest.mark.skip("Enable when Role is available on prod")
def test_grants_for_invalid_db_securable(roles, grants, session):
    with pytest.raises(NotFoundError):
        grants.grant(Grant(
            grantee=Grantees.role(name="public"),
            securable=Securables.database("invaliddb123"),
            privileges=[Privileges.create_database],
            grant_option=False
        ))
