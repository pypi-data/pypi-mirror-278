#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#
from io import BytesIO
from textwrap import dedent

from tests.utils import random_string

from snowflake.core.service import Service, ServiceSpecStageFile


def test_iter(services, temp_service, session, imagerepo):
    service_name = random_string(5, "test_service_")
    stage_name = random_string(5, "test_stage_")
    session.sql(f"create temp stage {stage_name};").collect()
    spec_file = "spec.yaml"
    stage_file = f"@{stage_name}"
    spec = f"{stage_file}/{spec_file}"
    session.file.put_stream(
        BytesIO(
            dedent(f"""
                spec:
                  containers:
                  - name: hello-world
                    image: {imagerepo}/hello-world:latest
                """).encode()
        ),
        spec,
    )
    test_service = Service(
        name=service_name,
        compute_pool="ci_compute_pool",
        spec=ServiceSpecStageFile(stage=stage_name, spec_file=spec_file),
        min_instances=1,
        max_instances=1,
    )

    s = None
    try:
        s = services.create(test_service)

        service_names = [sr.name for sr in services.iter()]
        assert temp_service.name.upper() in service_names

        service_names = [sr.name for sr in services.iter(like="TESt_Serv%")]
        assert temp_service.name.upper() in service_names
        assert service_name.upper() in service_names
        service_names = [sr.name for sr in services.iter(starts_with="TESt_Serv")]
        assert temp_service.name.upper() not in service_names
        assert service_name.upper() not in service_names

        service_names = [sr.name for sr in services.iter(starts_with="TEST_SERVICE")]
        assert temp_service.name.upper() in service_names
        assert service_name.upper() in service_names

        service_names = [sr.name for sr in services.iter(starts_with="test_service")]
        assert temp_service.name.upper() not in service_names
        assert service_name.upper() not in service_names
    finally:
        s.delete()
