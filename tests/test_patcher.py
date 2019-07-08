import pytest
import os
from m2tools import patcher
from unittest import mock


@pytest.fixture
def php():
    here = os.path.dirname(__file__)
    fp = os.path.join(here, 'File.php')
    with open(fp) as f:
        yield f.read()


@pytest.fixture
def js():
    here = os.path.dirname(__file__)
    fp = os.path.join(here, 'File.js')
    with open(fp) as f:
        yield f.read()


@pytest.fixture
def xml():
    here = os.path.dirname(__file__)
    fp = os.path.join(here, 'File.xml')
    with open(fp) as f:
        yield f.read()


@pytest.fixture
def folder():
    return [('test', [], ['Test.php'])]


def test_walk(folder, php):
    with mock.patch('m2tools.patcher.os.walk') as mock_walk:
        mock_walk.return_value = folder
        p = patcher.Patcher('test')
        for fname in p.walk(match=lambda x: x.endswith('.php')):
            assert 'test' in fname
            assert fname.endswith('Test.php')


def test_sign_php(php):
    p = patcher.PhpCode(php)
    patched = p.sign('test\nmultiline')
    assert patched.startswith("<?php\n/**\n * test\n * multiline\n */")


def test_sign_js(js):
    p = patcher.JsCode(php)
    patched = p.sign('test\nmultiline')
    assert patched.startswith("/**\n * test\n * multiline\n */")


def test_sign_xml(xml):
    p = patcher.XmlCode(xml)
    patched = p.sign('test\nmultiline')
    assert patched.startswith('<?xml version="1.0"?>')
    assert '<!--\n/**\n* test\n* multiline\n*/\n-->' in patched
