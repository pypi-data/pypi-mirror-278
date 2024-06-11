#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#
from io import BytesIO
from textwrap import dedent
from time import sleep

import pytest

from tests.utils import random_string

from snowflake.core.service import Service, ServiceSpecStageFile


@pytest.fixture(scope="session")
def seed_temp_service_data():
    return


@pytest.mark.skip(reason="very flaky, need investigation")
def test_suspend_resume(root, services, session, imagerepo):
    stage_name = random_string(5, "test_stage_")
    s_name = random_string(5, "test_service_")
    session.sql(f"create temp stage {stage_name};").collect()
    spec_file = "spec.yaml"
    stage_file = f"@{stage_name}"
    spec = f"{stage_file}/{spec_file}"
    session.file.put_stream(
        BytesIO(
            dedent(
                f"""
                spec:
                  containers:
                  - name: web-server
                    image: {imagerepo}/nginx:latest
                 """
            ).encode()
        ),
        spec,
    )
    test_s = Service(
        name=s_name,
        compute_pool="ci_compute_pool",
        spec=ServiceSpecStageFile(stage=stage_name, spec_file=spec_file),
        min_instances=1,
        max_instances=1,
    )
    s = services.create(test_s)
    try:
        for _ in range(10):
            web_server = s.get_service_status(1)[0]
            if web_server["status"] in ("READY",):
                break
            sleep(1)
        else:
            pytest.fail("web_server never came online")
        services[test_s.name].suspend()
        for _ in range(10):
            web_server = s.get_service_status(1)[0]
            if web_server["status"] in ("SUSPENDED",):
                break
            sleep(1)
        else:
            pytest.fail("web_server never went to sleep")
        services[test_s.name].resume()
        for _ in range(60):
            web_server = s.get_service_status(1)[0]
            if web_server["status"] in ("READY",):
                break
            print(f"{web_server['status']}")
            sleep(1)
        else:
            pytest.fail("web_server never resumed")
    finally:
        s.delete()
