''' Unit test tra '''

# pylint: disable=E0401
# pylint: disable=C0413
# pylint: disable=W0621
# pylint: disable=C0301

import sys
import os
import configparser
import pytest

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.join(current_dir, '..', '..', '..')
sys.path.append(project_dir)

from ai_transformers.ai_transformers import AITransformersBuilder
from manuelharo.opengate_client.opengate_client import OpenGateClient

config = configparser.ConfigParser()
config_file_path = os.path.join(current_dir, '..', '..', 'config_test.ini')
config.read(config_file_path)

@pytest.fixture
def client():
    ''' Fixture opengate client '''
    api_url = config.get('opengate', 'url')
    api_user = config.get('opengate', 'user')
    api_password = config.get('opengate', 'password')
    return OpenGateClient(url=api_url, user=api_user, password=api_password)

def test_with_organization(client):
    ''' Test organization '''
    builder = AITransformersBuilder(client)
    builder.with_organization('test_org')
    assert builder.organization_name == 'test_org'

def test_with_identifier(client):
    ''' Test identifier '''
    builder = AITransformersBuilder(client)
    builder.with_identifier('identifier')
    assert builder.identifier == 'identifier'

def test_with_config_file(client):
    ''' Config file cache transform id '''
    builder = AITransformersBuilder(client)
    builder.with_config_file('model_config.ini')
    assert builder.config_file == 'model_config.ini'

def test_add_file_plk_with_type(client):
    ''' Config file cache transform id '''
    builder = AITransformersBuilder(client)
    builder.add_file('/opengate_py/test/utils/pkl_encoder.pkl', 'application/octet-stream')
    assert builder.files == [('/opengate_py/test/utils/pkl_encoder.pkl', 'application/octet-stream')]

def test_add_file_plk_without_type(client):
    ''' Config file cache transform id '''
    builder = AITransformersBuilder(client)
    builder.add_file('/opengate_py/test/utils/pkl_encoder.pkl')
    assert builder.files == [('/opengate_py/test/utils/pkl_encoder.pkl', 'application/octet-stream')]

def test_add_file_python_with_type(client):
    ''' Config file cache transform id '''
    builder = AITransformersBuilder(client)
    builder.add_file('/opengate_py/test/utils/inittransformer.py')
    assert builder.files == [('/opengate_py/test/utils/inittransformer.py', 'text/python')]

def test_add_file_python_without_type(client):
    ''' Config file cache transform id '''
    builder = AITransformersBuilder(client)
    builder.add_file('/opengate_py/test/utils/inittransformer.py')
    assert builder.files == [('/opengate_py/test/utils/inittransformer.py', 'text/python')]

def test_with_find_name(client):
    ''' Test find name '''
    builder = AITransformersBuilder(client)
    builder.with_find_by_name('name_transform')
    assert builder.find_name == 'name_transform'

def test_with_evaluate(client):
    ''' evaluate '''
    data_evaluate = {"data": {"PPLast12H": 0,},"date": "2022-06-13T13:59:34.779+02:00"}
    builder = AITransformersBuilder(client)
    builder.with_evaluate(data_evaluate)
    assert builder.data_evaluate == data_evaluate

def test_with_output_file_path(client):
    ''' Test output_file_download '''
    builder = AITransformersBuilder(client)
    builder.with_output_file_path('opengate_py/test/unit/ia/test_ai_transformers.py')
    assert builder.output_file_path == 'opengate_py/test/unit/ia/test_ai_transformers.py'

def test_with_file_name(client):
    ''' Filename '''
    builder = AITransformersBuilder(client)
    builder.with_file_name('file_name')
    assert builder.file_name == 'file_name'

def test_create(client):
    ''' Check create transformer url '''
    builder = AITransformersBuilder(client)
    builder.with_organization(config.get('opengate', 'organization'))
    builder.add_file('create_transformer')
    builder.create()
    builder.build()
    url = f'{config.get("opengate", "url")}/north/ai/{config.get("opengate", "organization")}/transformers'
    assert builder.url == url and builder.method == 'create'

def test_find_all_url(client):
    ''' Check find all transformer url '''
    builder = AITransformersBuilder(client)
    builder.with_organization(config.get('opengate', 'organization'))
    builder.find_all()
    url = f'{config.get("opengate", "url")}/north/ai/{config.get("opengate", "organization")}/transformers'
    builder.build()
    assert builder.url == url and builder.method == 'find_all'

def test_find_one_url(client):
    ''' Check find one transformer url '''
    builder = AITransformersBuilder(client)
    builder.with_organization(config.get('opengate', 'organization'))
    builder.with_identifier('identifier')
    builder.find_one()
    url = f'{config.get("opengate", "url")}/north/ai/{config.get("opengate", "organization")}/transformers/{builder.identifier}'
    builder.build()
    print('builder.url', builder.url)
    assert builder.url == url and builder.method == 'find_one'

def test_update_url(client):
    ''' Check find all transformer url '''
    builder = AITransformersBuilder(client)
    builder.with_organization(config.get('opengate', 'organization'))
    builder.with_identifier('identifier')
    builder.add_file('create_transformer')
    builder.update()
    builder.build()
    url = f'{config.get("opengate", "url")}/north/ai/{config.get("opengate", "organization")}/transformers/{builder.identifier}'
    assert builder.url == url and builder.method == 'update'

def test_delete(client):
    ''' Check find one transformer url '''
    builder = AITransformersBuilder(client)
    builder.with_organization(config.get('opengate', 'organization'))
    builder.with_identifier('identifier')
    builder.delete()
    url = f'{config.get("opengate", "url")}/north/ai/{config.get("opengate", "organization")}/transformers/{builder.identifier}'
    builder.build()
    print('builder.url', builder.url)
    assert builder.url == url and builder.method == 'delete'

def test_download_url(client):
    ''' Check download transformer url '''
    builder = AITransformersBuilder(client)
    builder.with_organization(config.get('opengate', 'organization'))
    builder.with_identifier('identifier')
    builder.add_file('create_transformer')
    builder.with_output_file_path('output_file')
    builder.with_file_name('file_name')
    builder.download()
    builder.build()
    url = f'{config.get("opengate", "url")}/north/ai/{config.get("opengate", "organization")}/transformers/{builder.identifier}/{builder.file_name}'
    assert builder.url == url and builder.method == 'download'

def test_evaluate_url(client):
    ''' Check evaluate transformer url '''
    builder = AITransformersBuilder(client)
    data_evaluate = {"data": {"PPLast12H": 0,},"date": "2022-06-13T13:59:34.779+02:00"}
    builder.with_organization(config.get('opengate', 'organization'))
    builder.with_identifier('identifier')
    builder.with_evaluate(data_evaluate)
    builder.evaluate()
    builder.build()
    url = f'{config.get("opengate", "url")}/north/ai/{config.get("opengate", "organization")}/transformers/{builder.identifier}/transform'
    assert builder.url == url and builder.method == 'evaluate'

def test_save(client):
    ''' Check test save '''
    builder = AITransformersBuilder(client)
    builder.with_organization(config.get('opengate', 'organization'))
    builder.save()
    builder.build()
    assert builder.method == 'save'

def test_set_config_file_identifier(client):
    ''' Check config file'''
    builder = AITransformersBuilder(client)
    builder.with_identifier('identifier')
    builder.with_config_file('config_file.ini')
    builder.set_config_file_identifier()
    builder.build()
    assert builder.method == 'set_config_identifier'