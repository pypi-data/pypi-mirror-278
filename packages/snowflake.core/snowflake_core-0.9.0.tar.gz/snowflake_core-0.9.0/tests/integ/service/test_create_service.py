#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#
from io import BytesIO
from textwrap import dedent

import pytest

from tests.utils import random_string

from snowflake.core._common import CreateMode
from snowflake.core.exceptions import APIError, ConflictError
from snowflake.core.service import Service, ServiceSpecStageFile
from snowflake.core.service._generated.models.service_spec_inline_text import ServiceSpecInlineText


def test_create(services, session, imagerepo):
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
    s = services.create(test_service)

    fetched_service = s.fetch()
    assert fetched_service.name == service_name.upper()

    with pytest.raises(
        ConflictError,
    ):
        services.create(test_service)

    s = services.create(test_service, mode=CreateMode.if_not_exists)

    s.delete()

    service_name = random_string(5, "test_service_")
    service_name = f'"{service_name}"'
    test_service = Service(
        name=service_name,
        compute_pool="ci_compute_pool",
        spec=ServiceSpecStageFile(stage=stage_name, spec_file=spec_file),
        min_instances=1,
        max_instances=1,
    )

    with pytest.raises(APIError):
        services.create(test_service)


def test_create_or_replace(services, session, imagerepo):
    service_name = random_string(5, "test_service_")
    stage_name = random_string(5, "test_stage_")
    spec_file = "spec.yaml"
    test_service = Service(
        name=service_name,
        compute_pool="ci_compute_pool",
        spec=ServiceSpecStageFile(stage=stage_name, spec_file=spec_file),
        min_instances=1,
        max_instances=1,
    )
    with pytest.raises(ValueError):
        services.create(test_service, mode=CreateMode.or_replace)


def test_create_with_spec_inline(services, temp_service_from_spec_inline, database):
    service = services[temp_service_from_spec_inline.name].fetch()
    assert (
        service.name == temp_service_from_spec_inline.name  # for mixed case names
        or service.name.upper() == temp_service_from_spec_inline.name.upper()  # for upper/lower case names
    )
    assert 'name: "hello-world"' in service.spec.spec_text
    assert service.comment == "created by temp_service_from_spec_inline"


@pytest.mark.skip(reason="put isn't supported be Image repository OAS")
@pytest.mark.parametrize("comment", (None, "ThIs Is A cOmMeNt"))
@pytest.mark.skip
def test_update_comment(services, comment, temp_cp, imagerepo):
    new_s_name = random_string(3, "test_update_comment_")
    new_s = Service(
        name=new_s_name,
        compute_pool=temp_cp.name,
        min_instances=1,
        max_instances=1,
        spec=ServiceSpecInlineText(
            spec_text=dedent(
                f"""
                spec:
                  containers:
                  - name: hello-world
                    image: {imagerepo}/hello-world:latest
                """
            )
        ),
    )
    s = services.create(new_s)
    try:
        s.comment = comment
        s.create_or_update(new_s)
        assert s.fetch().comment == comment
    finally:
        s.delete()
