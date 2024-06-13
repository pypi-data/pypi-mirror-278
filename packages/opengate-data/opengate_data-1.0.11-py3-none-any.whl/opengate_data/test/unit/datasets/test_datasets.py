""" Unit tests datasets """

import pytest
import sys
import os
import configparser
from ....opengate_client import OpenGateClient
from ....datasets.search_dataset import DatasetsSearchBuilder

non_type_str = [111, 1.0, True, {"key": "value"}, ["list"]]


@pytest.fixture
def client():
    return OpenGateClient(url="url", api_key="api_password")


class TestSearchingDatasets:
    """Unit tests for the DatasetsSearchingBuilder functionality."""

    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.builder = DatasetsSearchBuilder(client)

    def test_with_organization_name(self):
        self.builder.with_organization_name('test_org')
        assert self.builder.organization_name == 'test_org'

    def test_with_identifier(self):
        self.builder.with_identifier('identifier')
        assert self.builder.identifier == 'identifier'

    def test_with_utc(self):
        self.builder.with_utc()
        assert self.builder.utc is True

    def test_with_format_csv(self):
        self.builder.with_format('csv')
        assert self.builder.format_data == 'csv'
        assert self.builder.headers['Accept'] == 'text/plain'

    def test_with_format_dict(self):
        self.builder.with_format('dict')
        assert self.builder.format_data == 'dict'
        assert self.builder.headers['Accept'] == 'application/json'
        self.builder.with_format('pandas')
        assert self.builder.format_data == 'pandas'
        assert self.builder.headers['Accept'] == 'application/json'



