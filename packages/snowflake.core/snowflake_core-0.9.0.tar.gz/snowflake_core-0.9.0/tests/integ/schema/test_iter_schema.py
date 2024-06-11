from operator import attrgetter

import pytest

from snowflake.core.exceptions import APIError


pytestmark = pytest.mark.usefixtures("backup_database_schema")


def test_iter(schemas, temp_schema, temp_schema_case_sensitive):
    schema_names = tuple(
        map(
            attrgetter("name"),
            schemas.iter(),
        )
    )
    assert any(
        map(
            lambda e: e in schema_names,
            (
                temp_schema.name.upper(),  # for upper/lower case names
            ),
        )
    )

    # TODO(SNOW-1354988) - Please uncomment this once you have this bug resolved
    # assert any(
    #     map(
    #         lambda e: e in schema_names,
    #         (
    #             temp_schema_case_sensitive.name,  # for mixed case names
    #         ),
    #     )
    # )


def test_iter_like(schemas, temp_schema, temp_schema_case_sensitive):
    schema_names = tuple(
        map(
            attrgetter("name"),
            schemas.iter(like="test_schema%"),
        )
    )
    assert any(
        map(
            lambda e: e in schema_names,
            (
                temp_schema.name.upper(),  # for upper/lower case names
            ),
        )
    )

    # TODO(SNOW-1354988) - Please uncomment this once you have this bug resolved
    # assert any(
    #     map(
    #         lambda e: e in schema_names,
    #         (
    #             temp_schema_case_sensitive.name,  # for mixed case names
    #         ),
    #     )
    # )


def test_iter_starts_with(schemas, temp_schema, temp_schema_case_sensitive):
    schema_names = tuple(
        map(
            attrgetter("name"),
            schemas.iter(starts_with="Test_schema"),
        )
    )
    assert not any(
        map(
            lambda e: e in schema_names,
            (
                temp_schema.name.upper(),  # for upper/lower case names
            ),
        )
    )

    assert not any(
        map(
            lambda e: e in schema_names,
            (
                temp_schema_case_sensitive.name,  # for mixed case names
            ),
        )
    )

    schema_names = tuple(
        map(
            attrgetter("name"),
            schemas.iter(starts_with="TEST_SCHEMA"),
        )
    )
    assert any(
        map(
            lambda e: e in schema_names,
            (
                temp_schema.name.upper(),  # for upper/lower case names
            ),
        )
    )

    assert not any(
        map(
            lambda e: e in schema_names,
            (
                temp_schema_case_sensitive.name,  # for mixed case names
            ),
        )
    )


# TODO(SNOW-1355013) - Please uncomment this once you have this bug resolved
# def test_iter_from_name(schemas, temp_schema, temp_schema_case_sensitive):
#     schema_names = tuple(
#         map(
#             attrgetter("name"),
#             schemas.iter(from_name="test_schema"),
#         )
#     )
#     assert not any(
#         map(
#             lambda e: e in schema_names,
#             (
#                 temp_schema.name.upper(),  # for upper/lower case names
#             ),
#         )
#     )
#     # TODO(SNOW-1354988) - Please uncomment this once you have this bug resolved
#     # assert any(
#     #     map(
#     #         lambda e: e in schema_names,
#     #         (
#     #             temp_schema_case_sensitive.name,  # for mixed case names
#     #         ),
#     #     )
#     # )


@pytest.mark.jenkins
def test_iter_limit(schemas):
    data = list(schemas.iter(limit=10))
    assert len(data) <= 10

    with pytest.raises(
        APIError,
    ):
        data = list(schemas.iter(limit=10001))
