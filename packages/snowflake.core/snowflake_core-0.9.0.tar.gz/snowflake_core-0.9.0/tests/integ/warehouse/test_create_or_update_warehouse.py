# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.

from contextlib import suppress

import pytest

from snowflake.core._common import CreateMode
from snowflake.core.exceptions import NotFoundError
from snowflake.core.warehouse import Warehouse

from ..utils import random_string


pytestmark = pytest.mark.usefixtures("backup_warehouse")


@pytest.mark.skip
def test_create_or_update(warehouses, session):
    warehouse_name = random_string(5, "test_create_or_update_warehouse_")
    test_warehouse = Warehouse(name=warehouse_name)
    warehouse_ref = None
    try:
        # Test create when the warehouse does not exist.
        warehouse_ref = warehouses[warehouse_name]
        warehouse_ref.create_or_update(test_warehouse)
        warehouse_list = warehouses.iter(like=warehouse_name)
        result = next(warehouse_list)
        assert warehouse_name.upper() == result.name

        # Make sure that issuing an empty alter doesn't create a malformed SQL
        warehouse_ref.create_or_update(test_warehouse)

        # Test introducing property which was not set before
        test_warehouse_new_1 = Warehouse(
            name=warehouse_name,
            warehouse_size="SMALL",
        )
        warehouse_ref.create_or_update(test_warehouse_new_1)
        warehouse_list = warehouses.iter(like=warehouse_name)
        result = next(warehouse_list)
        assert warehouse_name.upper() == result.name
        assert result.warehouse_size.upper() == "SMALL"

        # Test altering the property which we set before
        test_warehouse_new_2 = Warehouse(name=warehouse_name, warehouse_size="LARGE", comment="Hey")
        warehouse_ref.create_or_update(test_warehouse_new_2)
        warehouse_list = warehouses.iter(like=warehouse_name)
        result = next(warehouse_list)
        assert warehouse_name.upper() == result.name
        assert result.warehouse_size.upper() == "LARGE"
        assert result.comment == "Hey"

        # Test not providing the property and checking that it is unset now and adding a new property at the same time
        test_warehouse_new_3 = Warehouse(name=warehouse_name, warehouse_type="STANDARD")
        warehouse_ref.create_or_update(test_warehouse_new_3)
        warehouse_list = warehouses.iter(like=warehouse_name)
        result = next(warehouse_list)
        assert warehouse_name.upper() == result.name
        assert result.comment is None
        assert result.warehouse_type.upper() == "STANDARD"

        # Test providing functionality which is not eligible for alter and it does not throw an error and ignore it
        test_warehouse_new_4 = Warehouse(name=warehouse_name, initially_suspended="true")
        warehouse_ref.create_or_update(test_warehouse_new_4)
        warehouse_list = warehouses.iter(like=warehouse_name)
        result = next(warehouse_list)
        assert warehouse_name.upper() == result.name
        assert result.warehouse_size.upper() == "LARGE"
    finally:
        with suppress(NotFoundError):
            warehouse_ref.delete()


@pytest.mark.skip
def test_create_or_update_with_fetch(warehouses):
    warehouse_name = random_string(5, "test_create_or_update_warehouse_")
    test_warehouse = Warehouse(
        name=warehouse_name, comment="Hello 1", warehouse_size="SMALL", initially_suspended="true"
    )
    warehouse_ref = None
    try:
        # Test create when the warehouse does not exist.
        warehouse_ref = warehouses.create(test_warehouse, mode=CreateMode.error_if_exists)
        warehouse_list = warehouses.iter(like=warehouse_name)
        result = next(warehouse_list)
        assert warehouse_name.upper() == result.name
        assert result.warehouse_size.upper() == "SMALL"
        assert result.comment == "Hello 1"

        warehouse_fetched = warehouse_ref.fetch()
        warehouse_fetched.size = "LARGE"
        # updating the size is not a alterable paramter
        warehouse_ref.create_or_update(warehouse_fetched)
        assert result.warehouse_size.upper() == "SMALL"

        warehouse_fetched.warehouse_size = "LARGE"
        warehouse_ref.create_or_update(warehouse_fetched)
        warehouse_fetched = warehouse_ref.fetch()
        assert warehouse_name.upper() == warehouse_fetched.name
        assert warehouse_fetched.warehouse_size.upper() == "LARGE"
    finally:
        with suppress(NotFoundError):
            warehouse_ref.delete()


@pytest.mark.parametrize("comment", (None, "ThIs Is A cOmMeNt"))
@pytest.mark.skip
def test_update_comment(warehouses, comment):
    new_w_name = random_string(3, "test_update_comment_")
    new_w = Warehouse(name=new_w_name)
    w = warehouses.create(new_w)
    try:
        new_w.comment = comment
        w.create_or_update(new_w)
        assert w.fetch().comment == comment
    finally:
        w.delete()


@pytest.mark.skip
def test_create_or_update_with_wildcardish_name(warehouses, session):
    # 2023-10-20(bwarsaw): Don't forget we have to filter out pre-existing warehouses, since we do not
    # have a clean test environment.

    # Create multiple warehouses with similar names.  Because the underscore is a wildcard character, and SHOW
    # WAREHOUSE does not support ILIKE or RLIKE, names can overlap.
    warehouse1_name = random_string(5, "warehouseXabcdef_")
    warehouse2_name = random_string(5, "warehouse_abcdef_")

    warehouse_refs = []
    try:
        test1_warehouse = Warehouse(name=warehouse1_name)
        test2_warehouse = Warehouse(name=warehouse2_name)
        w1_ref = warehouses[warehouse1_name]
        w2_ref = warehouses[warehouse2_name]
        w1_ref.create_or_update(test1_warehouse)
        w2_ref.create_or_update(test2_warehouse)
        warehouse_refs.append(w1_ref)
        warehouse_refs.append(w2_ref)
        warehouse_names = set(warehouse.name for warehouse in warehouses.iter())
        assert warehouse1_name.upper() in warehouse_names
        assert warehouse2_name.upper() in warehouse_names
    finally:
        for warehouse_ref in warehouse_refs:
            with suppress(NotFoundError):
                warehouse_ref.delete()
