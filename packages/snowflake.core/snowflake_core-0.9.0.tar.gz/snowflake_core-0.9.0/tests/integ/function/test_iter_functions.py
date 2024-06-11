import pytest as pytest

from tests.utils import random_string

from .conftest import create_service_function


@pytest.mark.skip("Enable when Function is available on prod")
def test_iter_services(echo_service_name, functions):
    funcs = []

    try:
        function_name_prefix = random_string(5, "test_func_")
        for i in range(5):
            function_name = f"{function_name_prefix}_foofunc_{str(i)}"
            function_name_with_args = f'{function_name}(REAL)'
            endpoint = "ep1"

            create_service_function(
                function_name, ["REAL"], "REAL", endpoint,
                echo_service_name, functions
            )

            funcs.append(function_name_with_args)

        for i in range(3):
            function_name = f"{function_name_prefix}_woofunc_{str(i)}"
            function_name_with_args = f'{function_name}(REAL)'
            endpoint = "end-point-2"

            create_service_function(
                function_name, ["REAL"], "REAL", endpoint,
                echo_service_name, functions
            )

            funcs.append(function_name_with_args)

        assert len([func.name for func in functions.iter()]) == 8

    finally:
        for i in funcs:
            functions[i].delete()
