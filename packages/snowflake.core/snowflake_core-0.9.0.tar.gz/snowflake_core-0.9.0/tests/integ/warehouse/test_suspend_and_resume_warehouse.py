# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.

from contextlib import suppress

import pytest

from snowflake.core.exceptions import APIError, NotFoundError
from snowflake.core.warehouse import Warehouse

from ..utils import random_string


pytestmark = pytest.mark.usefixtures("backup_warehouse")


def test_suspend_and_resume(warehouses):
    warehouse_name = random_string(5, "test_suspend_and_resume_warehouse_")
    test_warehouse = Warehouse(name=warehouse_name)

    warehouse_ref = None
    try:
        warehouse_ref = warehouses.create(test_warehouse)
        # Test warehouse suspend from default state
        warehouse_ref.suspend()
        result = next(warehouses.iter(like=warehouse_name))
        assert result.state in ("SUSPENDED", "SUSPENDING")

        # Test warehouse resume from suspended state
        warehouse_ref.resume()
        result = next(warehouses.iter(like=warehouse_name))
        assert result.state in ("STARTED", "RESUMING")

        # suspend again from resumed state
        warehouse_ref.suspend()
        result = next(warehouses.iter(like=warehouse_name))
        assert result.state in ("SUSPENDED", "SUSPENDING")

        # suspend when it is already suspended
        with pytest.raises(APIError):
            warehouse_ref.suspend()

        warehouse_ref.delete()
        warehouse_ref = warehouses.create(test_warehouse)
        result = next(warehouses.iter(like=warehouse_name))
        assert result.state in ("STARTED", "RESUMING")

        # resume from default state - a warehoue cannot be resumed if it is not in suspended state
        # TODO(SNOW-1362454) - Please uncomment this once you have this bug resolved
        # with pytest.raises(APIError):
        #     warehouse_ref.resume()

    finally:
        with suppress(NotFoundError):
            warehouse_ref.delete()
