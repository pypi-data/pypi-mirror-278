
from pathlib import Path

import pytest

from snowflake.core._common import CreateMode
from snowflake.core.function import FunctionArgument, ServiceFunction


@pytest.mark.skip("Enable when Function is available on prod")
def test_demo(functions, session):
    session.sql("create or replace stage mystage;").collect()

    session.sql(
        """
        alter session set
        qa_mode = true,
        qa_mode_mock_external_function_remote_calls = true;
        """
    ).collect()
    session.sql("""
                alter session set snowservices_mock_server_endpoints = '{"ep1":["mockhost1", "mockhost2"]}';
                """).collect()

    print(session.sql(f"""put file://{Path(__file__).resolve().parent.parent.parent
                      / "resources"
                      / "fake_spec_single_container.yaml"
                } @mystage auto_compress=false;
            """).collect())

    session.sql(            """
            create service my_service
            in compute pool mypool
            from @mystage
            spec='/fake_spec_single_container.yaml';
            """
    ).collect()

    functions.create(
        ServiceFunction(
            name="service_func",
            arguments=[
                FunctionArgument(name="input", datatype="REAL")
            ],
            returns="REAL",
            service="my_service",
            endpoint="ep1",
            path="/path/to/myapp",
            max_batch_rows=5,
            ),
            mode=CreateMode.or_replace
    )

    sf = functions["service_func(REAL)"].fetch()
    assert sf.to_dict().items() >= {
        'function_type': 'service-function',
        'name': 'SERVICE_FUNC',
        'arguments': [{'name': 'INPUT', 'datatype': 'REAL', 'value': None}],
        'returns': 'REAL',
        'max_batch_rows': 5,
        'signature': '(INPUT FLOAT)',
        'language': 'EXTERNAL',
        'body': '/path/to/myapp',
        'service': 'MY_SERVICE',
        'endpoint':'ep1',
        'path': '/path/to/myapp'
    }.items()

    assert functions["service_func(REAL)"].execute([12]) == 12.0
    functions["service_func(REAL)"].delete()

