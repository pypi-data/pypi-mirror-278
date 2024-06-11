#
# Copyright (c) 2012-2023 Snowflake Computing Inc. All rights reserved.
#


import pytest

from tests.utils import random_string

from snowflake.core.image_repository import ImageRepository


def test_iter(image_repositories):
    ir_name = random_string(5, "test_ir_1")
    test_ir = ImageRepository(name=ir_name)
    image_repo_1 = image_repositories.create(test_ir)

    ir_name = random_string(5, "test_ir_2")
    test_ir = ImageRepository(name=ir_name)
    image_repo_2 = image_repositories.create(test_ir)

    image_repo_names = [image_repo.name for image_repo in image_repositories.iter()]

    assert image_repo_1.name.upper() in image_repo_names
    assert image_repo_2.name.upper() in image_repo_names

    image_repo_names = [image_repo.name for image_repo in image_repositories.iter(like="TEst_Ir_%")]

    assert image_repo_1.name.upper() in image_repo_names
    assert image_repo_2.name.upper() in image_repo_names

    image_repo_names = [image_repo.name for image_repo in image_repositories.iter(like="TEst_Ir_2%")]

    assert image_repo_1.name.upper() not in image_repo_names
    assert image_repo_2.name.upper() in image_repo_names

    image_repo_names = [image_repo.name for image_repo in image_repositories.iter(like="TEst_Ir_3%")]

    assert image_repo_1.name.upper() not in image_repo_names
    assert image_repo_2.name.upper() not in image_repo_names

    image_repo_1.delete()
    image_repo_2.delete()


@pytest.mark.skip("TODO: investigate flakiness")
def test_list_images(image_repositories):
    ir_name = random_string(5, "test_ir_3")
    test_ir = ImageRepository(name=ir_name)
    image_repo_1 = image_repositories.create(test_ir)

    images = image_repo_1.list_images_in_repository()

    assert len(list(images)) == 0

    image_repo_1.delete()
