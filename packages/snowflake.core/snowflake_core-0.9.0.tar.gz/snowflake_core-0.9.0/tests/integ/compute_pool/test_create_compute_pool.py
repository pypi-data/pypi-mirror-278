#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#

import pytest

from snowflake.core._common import CreateMode
from snowflake.core.compute_pool import (
    ComputePool,
)
from snowflake.core.exceptions import APIError
from tests.utils import random_string


def test_create_compute_pool(compute_pools):
    cp_name = random_string(5, "test_cp_case_sensitiv_")
    cp_name = f'"{cp_name}"'
    test_cp = ComputePool(
        name=cp_name, instance_family="CPU_X64_XS", min_nodes=1, max_nodes=1, comment="created by temp_cp"
    )

    # case sensitive name for compute pools is not supported
    with pytest.raises(APIError):
        compute_pools.create(test_cp)

    cp_name = random_string(5, "test_cp_")
    test_cp = ComputePool(
        name=cp_name, instance_family="CPU_X64_XS", min_nodes=1, max_nodes=1, comment="created by temp_cp"
    )
    try:
        cp_ref = compute_pools.create(test_cp)
        cp = cp_ref.fetch()
        assert (
            cp.name == test_cp.name.upper()  # for upper/lower case names
        )
    finally:
        cp_ref.delete()

    # check or replace mode
    test_cp = ComputePool(
        name=cp_name, instance_family="CPU_X64_XS", min_nodes=1, max_nodes=1, comment="created by temp_cp new"
    )
    try:
        cp_ref = compute_pools.create(test_cp, mode=CreateMode.or_replace)
        cp = cp_ref.fetch()
        assert (
            cp.name == test_cp.name.upper()  # for upper/lower case names
        )
        assert cp.comment == "created by temp_cp new"
    finally:
        cp_ref.delete()
