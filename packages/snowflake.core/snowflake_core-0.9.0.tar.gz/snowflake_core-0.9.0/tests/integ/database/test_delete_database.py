#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#


import pytest

from snowflake.core.database import Database
from snowflake.core.exceptions import NotFoundError

from ..utils import random_string


pytestmark = pytest.mark.usefixtures("backup_database_schema")


@pytest.mark.jenkins
def test_delete(databases):
    new_database = Database(name=random_string(5, "test_db_"))
    new_db = databases.create(new_database)

    # delete a database which exists
    new_db.delete()
    with pytest.raises(
        NotFoundError,
    ):
        new_db.fetch()

    # delete a database which does not exists
    with pytest.raises(
        NotFoundError,
    ):
        new_db.delete()
