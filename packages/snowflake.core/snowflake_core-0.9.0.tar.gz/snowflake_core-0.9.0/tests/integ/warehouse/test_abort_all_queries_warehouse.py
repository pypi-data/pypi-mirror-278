# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.

import time

from contextlib import suppress

import pytest

from snowflake.core.exceptions import NotFoundError
from snowflake.core.warehouse import Warehouse

from ..utils import random_string


pytestmark = pytest.mark.usefixtures("backup_warehouse")


def test_abort_all_queries(warehouses, session):
    warehouse_name = random_string(5, "test_abort_all_queries_warehouse_")
    test_warehouse = Warehouse(name=warehouse_name)

    warehouse_ref = None
    try:
        warehouse_ref = warehouses.create(test_warehouse)
        result = next(warehouses.iter(like=warehouse_name))
        time.sleep(5)
        warehouse_ref.abort_all_queries()
        time.sleep(5)
        result = next(warehouses.iter(like=warehouse_name))
        assert result.running == 0 and result.queued == 0

    finally:
        with suppress(NotFoundError):
            warehouse_ref.delete()
