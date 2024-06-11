""" Unit tests provision bulks """

import pytest

import sys
import os
import configparser
from pprint import pprint
import pandas as pd
from ....opengate_client import OpenGateClient
from ....provision.bulk.provision_bulk import ProvisionBulkBuilder

@pytest.fixture
def client():
    return OpenGateClient(url="url", api_key="api_password")


class TestSearchingProvisonBulk:
    """Unit tests for the EntitiesBulkProvisionBuilder functionality."""

    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.builder = ProvisionBulkBuilder(client)

    def test_with_organization_name(self):
        self.builder.with_organization_name('test_org')
        assert self.builder.organization_name == 'test_org'
        assert type(self.builder.organization_name) == str

    def test_with_bulk_action(self):
        assert self.builder.bulk_action == 'CREATE'
        self.builder.with_bulk_action('DELETE')
        assert self.builder.bulk_action == 'DELETE'
        assert type(self.builder.bulk_action) == str
        try:
            self.builder.with_bulk_action('NOTVALID')
        except ValueError as e:
            assert str(e) == "Invalid bulk action. Only 'CREATE', 'UPDATE', 'PATCH', 'DELETE' are accepted."
            
        
    def test_with_bulk_type(self):
        assert self.builder.bulk_type == 'ENTITIES'
        self.builder.with_bulk_type('TICKETS')
        assert self.builder.bulk_type == 'TICKETS'
        assert type(self.builder.bulk_type) == str
        try:
            self.builder.with_bulk_type('NOTVALID')
        except ValueError as e:
            assert str(e) == "Invalid bulk type. Only 'ENTITIES','TICKETS' are accepted."
         

    def test_from_file(self):
        self.builder.from_file('ejemplo/camino/a/un/csv.csv')
        assert self.builder.path == 'ejemplo/camino/a/un/csv.csv'
        assert self.builder.file_name == 'csv.csv'
        assert type(self.builder.path) == str
        assert type(self.builder.file_name) == str
        assert f'File not found error:' in self.builder.from_file('ejemplo/camino/a/un/csv.csv')

    def test_from_dataframe_simple(self):
        data = {
            'current_value': [[1,2,3]],
            'other_field': ['a']
        }
        df = pd.DataFrame(data)
        assert self.builder.from_dataframe(df) is self.builder
        assert self.builder.payload['entities'][0]['_current']['value'] == [1,2,3]
        assert self.builder.payload['entities'][0]['other']['field'] == 'a'
    
    def test_from_dataframe_complex(self):
        data = {
            'provision_administration_organization_current_value': ['base_organization','test_organization'],
            'provision_device_location_current_value_position_type': ['Point','Other_Point'],
            'provision_device_location_current_value_position_coordinates': [[-3.7028,40.41675],[-5.7028,47.41675]],
            'provision_device_location_current_value_postal': ['28013','28050']
        }
        df = pd.DataFrame(data)
        assert self.builder.from_dataframe(df) is self.builder
        assert self.builder.payload['entities'][0]['provision']['administration']['organization']['_current']['value'] == 'base_organization'
        assert self.builder.payload['entities'][0]['provision']['device']['location']['_current']['value']['position']['type'] == 'Point'
        assert self.builder.payload['entities'][0]['provision']['device']['location']['_current']['value']['position']['coordinates'] == [-3.7028,40.41675]
        assert self.builder.payload['entities'][0]['provision']['device']['location']['_current']['value']['postal'] == '28013' 
        assert self.builder.payload['entities'][1]['provision']['administration']['organization']['_current']['value'] == 'test_organization'
        assert self.builder.payload['entities'][1]['provision']['device']['location']['_current']['value']['position']['type'] == 'Other_Point'
        assert self.builder.payload['entities'][1]['provision']['device']['location']['_current']['value']['position']['coordinates'] == [-5.7028,47.41675]
        assert self.builder.payload['entities'][1]['provision']['device']['location']['_current']['value']['postal'] == '28050'   
        assert len(self.builder.payload['entities']) == 2

    def test_from_dict(self):
        dct = {'a':1,'b':2,'c':3}
        assert self.builder.from_dict(dct) is self.builder
        assert self.builder.payload['entities'][0] == dct
    
    def test_validate_builds(self):
        try:
            self.builder.build()
        except ValueError as e:
            assert str(e) == "Organization name needed to build the EntitiesBulkProvisionBuilder."
        
        try:
            self.builder.with_organization_name('test').build()
        except ValueError as e:
            assert str(e) == "At least one source of data must be added using the following functions:\n - from_dataframe\n - from_file\n - from_dict"
        
    def test_build_with_build_execute(self):
        self.builder.method_calls = ['build_execute']
        with pytest.raises(Exception):
            self.builder.build()
        assert "You cannot use build() together with build_execute()"

    def test_build_execute_without_build(self):
        self.builder.method_calls = []
        with pytest.raises(Exception):
            self.builder.build_execute()

    def test_build_execute_with_build(self):
        self.builder.method_calls = ['build', 'build_execute']
        self.builder.builder = True
        with pytest.raises(Exception):
            self.builder.build_execute()

    def test_execute_with_incorrect_order(self):
        self.builder.method_calls = ['build', 'with_device_identifier', 'execute']
        with pytest.raises(Exception):
            self.builder.execute()


