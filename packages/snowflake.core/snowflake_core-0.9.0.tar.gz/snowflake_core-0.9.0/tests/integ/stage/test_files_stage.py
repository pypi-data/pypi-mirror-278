import filecmp
import os.path
import tempfile

import pytest

from snowflake.core.stage import Stage, StageDirectoryTable, StageEncryption
from tests.utils import random_string


@pytest.mark.skip
@pytest.mark.jenkins
def test_files(stages):
    comment = "my comment"
    new_stage = Stage(
        name=random_string(5, "test_stage_"),
        encryption=StageEncryption(type="SNOWFLAKE_SSE"),
        directory_table=StageDirectoryTable(enable=True),
        comment=comment,
    )
    s = stages.create(new_stage)
    try:
        assert s.fetch().comment == comment
        # upload file
        s.upload_file("./tests/resources/schema.yaml", "/", auto_compress=False)

        # list file
        files = list(s.list_files())
        assert len(files) == 1, files
        assert "schema.yaml" in files[0].name

        # download file
        temp_dir = tempfile.mkdtemp()
        s.download_file("/schema.yaml", temp_dir)

        # compare files
        assert filecmp.cmp("./tests/resources/schema.yaml", os.path.join(temp_dir, "schema.yaml"))
    finally:
        s.delete()
