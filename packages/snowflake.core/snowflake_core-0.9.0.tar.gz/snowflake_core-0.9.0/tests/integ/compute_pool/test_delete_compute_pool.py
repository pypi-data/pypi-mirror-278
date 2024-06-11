#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#

import pytest

from snowflake.core.compute_pool import ComputePool
from snowflake.core.exceptions import NotFoundError

from ..utils import random_string


def test_delete(compute_pools):
    cp_name = random_string(5, "test_cp_")
    test_cp = ComputePool(
        name=cp_name,
        instance_family="CPU_X64_XS",
        min_nodes=1,
        max_nodes=1,
    )
    compute_pools.create(test_cp)
    compute_pools[test_cp.name].delete()
    with pytest.raises(
        NotFoundError,
    ):
        compute_pools[test_cp.name].fetch()

    compute_pools.create(test_cp)
    compute_pools[test_cp.name].delete()
