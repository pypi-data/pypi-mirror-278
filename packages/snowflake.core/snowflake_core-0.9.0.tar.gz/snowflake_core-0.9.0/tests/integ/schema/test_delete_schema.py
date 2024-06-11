import pytest

from snowflake.core.exceptions import NotFoundError
from snowflake.core.schema import Schema
from tests.utils import random_string


pytestmark = pytest.mark.usefixtures("backup_database_schema")


@pytest.mark.jenkins
def test_delete(schemas):
    comment = "my comment"
    new_schema = Schema(
        name=random_string(5, "test_schema_"),
        comment=comment,
    )
    s = schemas.create(new_schema)
    try:
        assert s.fetch().comment == comment
    finally:
        s.delete()

    with pytest.raises(
        NotFoundError,
    ):
        s.fetch()

    s = schemas.create(new_schema)
    try:
        assert s.fetch().comment == comment
    finally:
        s.delete()
