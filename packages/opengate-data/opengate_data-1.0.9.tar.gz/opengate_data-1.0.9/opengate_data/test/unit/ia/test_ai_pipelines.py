''' Unit test pipelines '''

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

from ai_pipelines.ai_pipelines import AIPipelinesBuilder
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
    builder = AIPipelinesBuilder(client)
    builder.with_organization('test_org')
    assert builder.organization_name == 'test_org'

def test_with_identifier(client):
    ''' Test identifier '''
    builder = AIPipelinesBuilder(client)
    builder.with_identifier('identifier')
    assert builder.identifier == 'identifier'

def test_with_config_file(client):
    ''' Config file cache transform id '''
    builder = AIPipelinesBuilder(client)
    builder.with_config_file('model_config.ini')
    assert builder.config_file == 'model_config.ini'

def test_with_find_name(client):
    ''' Test find name '''
    builder = AIPipelinesBuilder(client)
    builder.with_find_by_name('name_pipeline')
    assert builder.find_name == 'name_pipeline'

def test_with_prediction(client):
    ''' prediction '''
    prediction = {'X': [{'input_8': [[5002]]}]}
    builder = AIPipelinesBuilder(client)
    builder.with_prediction(prediction)
    assert builder.data_prediction == prediction

def test_with_file_name(client):
    ''' Filename '''
    builder = AIPipelinesBuilder(client)
    builder.with_file_name('file_name')
    assert builder.file_name == 'file_name'

def test_with_collect(client):
    ''' Filename '''
    collect_data = { 'deviceId': 'entity', 'datastream': 'device.identifier' }
    builder = AIPipelinesBuilder(client)
    builder.with_collect(collect_data)
    assert builder.collect == collect_data

def test_with_name(client):
    ''' Test find name '''
    builder = AIPipelinesBuilder(client)
    builder.with_name('name_pipeline')
    assert builder.name == 'name_pipeline'

def test_add_action_transfomer_with_type(client):
    ''' Test find name '''
    builder = AIPipelinesBuilder(client)
    builder.add_action('exittransformer.py', 'TRANSFORMER')
    assert builder.actions ==  [{'name': 'exittransformer.py', 'type': 'TRANSFORMER'}]

def test_add_action_transfomer_without_type(client):
    ''' Test find name '''
    builder = AIPipelinesBuilder(client)
    builder.add_action('exittransformer.py')
    assert builder.actions ==  [{'name': 'exittransformer.py', 'type': 'TRANSFORMER'}]

def test_add_action_model_with_type(client):
    ''' Test find name '''
    builder = AIPipelinesBuilder(client)
    builder.add_action('snow_create.onnx', 'MODEL')
    assert builder.actions ==  [{'name': 'snow_create.onnx', 'type': 'MODEL'}]

def test_add_action_model_without_type(client):
    ''' Test find name '''
    builder = AIPipelinesBuilder(client)
    builder.add_action('snow_create.onnx')
    assert builder.actions ==  [{'name': 'snow_create.onnx', 'type': 'MODEL'}]

def test_add_action_transfomers_and_models(client):
    ''' Test find name '''
    builder = AIPipelinesBuilder(client)
    builder.add_action('exittransformer.py', 'TRANSFORMER')
    builder.add_action('snow_create.onnx', 'MODEL')
    builder.add_action('inittransformer.py')
    builder.add_action('snow_update.onnx')
    assert builder.actions ==  [{'name': 'exittransformer.py', 'type': 'TRANSFORMER'},
                                {'name': 'snow_create.onnx', 'type': 'MODEL'},
                                {'name': 'inittransformer.py', 'type': 'TRANSFORMER'},
                                {'name': 'snow_update.onnx', 'type': 'MODEL'}]

def test_create(client):
    ''' Check create pipeline url '''
    builder = AIPipelinesBuilder(client)
    builder.with_organization(config.get('opengate', 'organization'))
    builder.with_name('create_pipeline')
    builder.add_action('exittransformer.py')
    builder.create()
    builder.build()
    url = f'{config.get("opengate", "url")}/north/ai/{config.get("opengate", "organization")}/pipelines'
    assert builder.url == url and builder.method == 'create'

def test_find_all_url(client):
    ''' Check find all pipeline url '''
    builder = AIPipelinesBuilder(client)
    builder.with_organization(config.get('opengate', 'organization'))
    builder.find_all()
    url = f'{config.get("opengate", "url")}/north/ai/{config.get("opengate", "organization")}/pipelines'
    builder.build()
    assert builder.url == url and builder.method == 'find'

def test_find_one_url(client):
    ''' Check find all pipeline url '''
    builder = AIPipelinesBuilder(client)
    builder.with_organization(config.get('opengate', 'organization'))
    builder.with_identifier('identifier')
    builder.find_one()
    url = f'{config.get("opengate", "url")}/north/ai/{config.get("opengate", "organization")}/pipelines/{builder.identifier}'
    builder.build()
    assert builder.url == url and builder.method == 'find'

def test_update_url(client):
    ''' Check find all pipeline url '''
    builder = AIPipelinesBuilder(client)
    builder.with_organization(config.get('opengate', 'organization'))
    builder.with_identifier('identifier')
    builder.update()
    builder.build()
    url = f'{config.get("opengate", "url")}/north/ai/{config.get("opengate", "organization")}/pipelines/{builder.identifier}'
    assert builder.url == url and builder.method == 'update'

def test_delete_url(client):
    ''' Check find all pipeline url '''
    builder = AIPipelinesBuilder(client)
    builder.with_organization(config.get('opengate', 'organization'))
    builder.with_identifier('identifier')
    builder.delete()
    builder.build()
    url = f'{config.get("opengate", "url")}/north/ai/{config.get("opengate", "organization")}/pipelines/{builder.identifier}'
    assert builder.url == url and builder.method == 'delete'

def test_prediction_url(client):
    ''' Check find all pipeline url '''
    builder = AIPipelinesBuilder(client)
    builder.with_organization(config.get('opengate', 'organization'))
    builder.with_identifier('identifier')
    builder.with_prediction({'X': [{'input_8': [[5002]]}]})
    builder.prediction()
    builder.build()
    url = f'{config.get("opengate", "url")}/north/ai/{config.get("opengate", "organization")}/pipelines/{builder.identifier}/prediction'
    assert builder.url == url and builder.method == 'prediction'

def test_save(client):
    ''' Check test save '''
    builder = AIPipelinesBuilder(client)
    builder.with_organization(config.get('opengate', 'organization'))
    builder.save()
    builder.build()
    assert builder.method == 'save'

def test_set_config_file_identifier(client):
    ''' Check config file'''
    builder = AIPipelinesBuilder(client)
    builder.with_identifier('identifier')
    builder.with_config_file('config_file.ini')
    builder.set_config_file_identifier()
    builder.build()
    assert builder.method == 'set_config_identifier'
