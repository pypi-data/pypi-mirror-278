import pytest as pytest

from tests.utils import random_string

from .conftest import create_service_function


TRANSLATE_DATA_TYPE_TO_BIND = {
    'INT': 'FIXED'
}


@pytest.mark.skip("Enable when Function is available on prod")
def test_create_service_function_argument(echo_service_name, functions):
    for t in [["REAL"], ["INT"], ["BOOLEAN"], ["TIME"], ["REAL", "INT"]]:
        function_name = random_string(5, "test_func_")
        function_name_with_args = f'{function_name}({",".join(t)})'
        endpoint = 'end-point-2' if t == "INT" else "ep1"
        try:
            f = create_service_function(
                function_name, t, t[0], endpoint,
                echo_service_name, functions
            )


            assert f.fetch().to_dict().items() >= {
                'function_type': 'service-function',
                'name': function_name.upper(),
                'arguments': [{
                    'name': f'V_{i}',
                    'datatype': TRANSLATE_DATA_TYPE_TO_BIND.get(v, v),
                    'value': None
                    } for i , v in enumerate(t)
                ],
                'returns': TRANSLATE_DATA_TYPE_TO_BIND.get(t[0], t[0]),
                'max_batch_rows': 5,
                'body': '/path/to/myapp',
                'endpoint': endpoint,
                'path': '/path/to/myapp'
            }.items()
        finally:
            functions[function_name_with_args].delete()
