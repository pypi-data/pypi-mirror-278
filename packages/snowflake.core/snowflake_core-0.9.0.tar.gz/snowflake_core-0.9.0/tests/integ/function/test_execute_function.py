import pytest as pytest

from tests.utils import random_string

from .conftest import create_service_function


TRANSLATE_DATA_TYPE_TO_BIND = {
    'INT': 'FIXED'
}


@pytest.mark.skip("Enable when Function is available on prod")
def test_create_service_function_argument(echo_service_name, functions):
    types = [["REAL"], ["INT"], ["BOOLEAN"], ["REAL", "INT"]]
    inputs = [[12.3], [12], [True], [12, 1]]
    outputs = [12.3, 12, True, 12.0]

    for i in range(len(inputs)):
        t = types[i]
        function_name = random_string(5, "test_func_")
        function_name_with_args = f'{function_name}({",".join(t)})'
        endpoint = 'end-point-2' if t == "INT" else "ep1"
        try:
            f = create_service_function(
                function_name, t, t[0], endpoint,
                echo_service_name, functions
            )

            assert f.execute(inputs[i]) == outputs[i]
        finally:
            functions[function_name_with_args].delete()
