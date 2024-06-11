from pathlib import Path

import pytest

from snowflake.core.function import FunctionArgument, ServiceFunction
from tests.utils import random_string


@pytest.fixture(scope="session")
def echo_service_name(session):
    stage_name = random_string(5, "testfunc_stage_")
    session.sql(f"create or replace stage {stage_name};").collect()

    session.sql(
        """
        alter session set
        qa_mode = true,
        qa_mode_mock_external_function_remote_calls = true;
        """
    ).collect()
    session.sql("""
                alter session set snowservices_mock_server_endpoints =
                  '{"ep1":["mockhost1", "mockhost2"],"end-point-2":["mockhost3"]}';
                """).collect()

    print(session.sql(f"""put file://{Path(__file__).resolve().parent.parent.parent
                      / "resources"
                      / "fake_spec_single_container.yaml"
                } @{stage_name} auto_compress=false;
            """).collect())

    service_name = random_string(5, "testfunc_service_")
    session.sql(f"""
            create service {service_name}
            in compute pool mypool
            from @{stage_name}
            spec='/fake_spec_single_container.yaml';
            """
    ).collect()

    return service_name

def create_service_function(
        name,
        arg_types,
        returns,
        endpoint,
        echo_service_name,
        functions
        ):
    return functions.create(
        ServiceFunction(
            name=name,
            arguments=[
                FunctionArgument(name=f"v_{str(i)}", datatype=v)
                    for i , v in enumerate(arg_types)
            ],
            returns=returns,
            service=echo_service_name,
            endpoint=endpoint,
            path="/path/to/myapp",
            max_batch_rows=5,
            )
    )
