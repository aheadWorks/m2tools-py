from m2tools import extension
import pytest
import os
import zipfile
import io


@pytest.fixture()
def composer_json():
    here = os.path.dirname(__file__)
    fp = os.path.join(here, 'composer.json')
    with open(fp) as f:
        yield f


@pytest.fixture()
def zip_package(composer_json):
    fp = io.BytesIO()
    with zipfile.ZipFile(fp, 'w') as zip_ref:
        zip_ref.writestr('/composer.json', composer_json.read())
        zip_ref.writestr('/registration.php', '<?php')

        yield zip_ref


def test_metadata_types():
    m = extension.Metadata()
    m2 = extension.Metadata()

    m.version = '1.2.3'
    m2.version = '3.4.5'

    assert m.version != m2.version
    assert m.version == '1.2.3'

    with pytest.raises(ValueError):
        m.version = '1.2.3.4.4.3'

    m.name = 'vendor/cool-name'
    with pytest.raises(ValueError):
        m.name = 'justsomename'

    m.type = 'magento2-module'
    with pytest.raises(ValueError):
        m.type = 'some-code'


def test_metadata_from_composer(composer_json):
    m = extension.Metadata()
    m.init_from_file(composer_json)
    assert m.name == 'vendor/test-module'
    assert m.version == '1.2.3'
    assert m.description == 'N/A'

