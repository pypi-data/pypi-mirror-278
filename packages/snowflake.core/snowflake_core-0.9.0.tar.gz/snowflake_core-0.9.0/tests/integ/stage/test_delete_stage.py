import pytest

from snowflake.core.exceptions import NotFoundError
from snowflake.core.stage import Stage
from tests.utils import random_string


@pytest.mark.skip
@pytest.mark.jenkins
def test_delete(stages):
    comment = "my comment"
    new_stage = Stage(
        name=random_string(5, "test_stage_"),
        comment=comment,
    )
    s = stages.create(new_stage)
    try:
        assert s.fetch().comment == comment
    finally:
        s.delete()

    with pytest.raises(
        NotFoundError,
    ):
        s.fetch()

    s = stages.create(new_stage)
    try:
        assert s.fetch().comment == comment
    finally:
        s.delete()
