from m2tools.package import zipdir
import io
from unittest import mock
import zipfile
import pytest


@pytest.fixture
def extension_path():
    return [('/path/to/dir', ['Api'], ['registration.php', 'composer.json'])]

@pytest.mark.skip
def test_zipdir(extension_path):
    zh = zipfile.ZipFile(io.BytesIO(), 'w', zipfile.ZIP_DEFLATED)
    with mock.patch('m2tools.package.os.walk') as mock_walk:
        mock_walk.return_value = extension_path

        with mock.patch('m2tools.package.open') as mock_open:

            mock_open.return_value = '111'

            with mock.patch('m2tools.package.zipfile.ZipFile.write') as mock_write:

                def side_effect(file_to_add, arcname):
                    assert arcname.startswith('dir')
                    assert file_to_add.endswith(arcname)
                    assert file_to_add == 'aaa'

                mock_write.side_effect = side_effect
                zipdir('/path/to/', zh)

