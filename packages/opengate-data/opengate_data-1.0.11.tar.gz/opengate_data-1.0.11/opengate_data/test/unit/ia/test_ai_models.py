""" Unit test tra """

import sys
import os
import configparser
import pytest

from ....opengate_client import OpenGateClient
from ....ai_models.ai_models import AIModelsBuilder

non_type_str = [111, 1.0, True, {"key": "value"}, ["list"]]
non_type_list = [111, 1.0, True, {"key": "value"}, "str"]


@pytest.fixture
def client():
    """ Fixture to provide an OpenGateClient instance."""
    return OpenGateClient(url="url", api_key="api_key")


class TestAIModel:
    """Unit tests for the AIMODEL functionality."""

    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.builder = AIModelsBuilder(client)

    def test_with_organization_name(self):
        organization = "organization_name"
        self.builder.with_organization_name(organization)
        assert self.builder.organization_name == organization

    def test_with_identifier(self):
        identifier = "identifier"
        self.builder.with_identifier(identifier)
        assert self.builder.identifier == identifier

    def test_with_find_by_name(self):
        find_name = "find_name"
        self.builder.with_find_by_name(find_name)
        assert self.builder.find_name == find_name

    def test_with_prediction(self):
        data_prediction = {"X": [{"input_8": [[-0.5391107438074961]]}]}
        self.builder.with_prediction(data_prediction)
        assert self.builder.data_prediction == data_prediction

    def test_with_output_file_path(self):
        self.builder.with_output_file_path('opengate_py/test/unit/ia/snow_create.py')
        assert self.builder.output_file_path == 'opengate_py/test/unit/ia/snow_create.py'

    def test_create(self):
        self.builder.with_organization_name("organization_name")
        self.builder.create()
        assert self.builder.base_url == "url/north/ai"
        assert self.builder.organization_name == "organization_name"
        assert self.builder.method == "create"

    def test_find_one(self):
        self.builder.with_identifier("identifier")
        self.builder.with_organization_name("organization_name")
        self.builder.find_one()
        assert self.builder.base_url == "url/north/ai"
        assert self.builder.organization_name == "organization_name"
        assert self.builder.method == "find"

    def test_find_all(self):
        self.builder.with_organization_name("organization_name")
        self.builder.find_all()
        assert self.builder.base_url == "url/north/ai"
        assert self.builder.organization_name == "organization_name"
        assert self.builder.method == "find"

    def test_update(self):
        self.builder.with_organization_name("organization_name")
        self.builder.with_identifier("identifier")
        self.builder.update()
        assert self.builder.base_url == "url/north/ai"
        assert self.builder.organization_name == "organization_name"
        assert self.builder.method == "update"

    def test_delete(self):
        self.builder.with_organization_name("organization_name")
        self.builder.with_identifier("identifier")
        self.builder.delete()
        assert self.builder.base_url == "url/north/ai"
        assert self.builder.organization_name == "organization_name"
        assert self.builder.method == "delete"

    def test_validate(self):
        self.builder.with_organization_name("organization_name")
        self.builder.validate()
        assert self.builder.base_url == "url/north/ai"
        assert self.builder.organization_name == "organization_name"
        assert self.builder.method == "validate"

    def test_download(self):
        self.builder.with_identifier("identifier")
        self.builder.with_organization_name("organization_name")
        self.builder.download()
        assert self.builder.base_url == "url/north/ai"
        assert self.builder.organization_name == "organization_name"
        assert self.builder.method == "download"

    def test_prediction(self):
        self.builder.with_identifier("identifier")
        self.builder.with_organization_name("organization_name")
        self.builder.prediction()
        assert self.builder.base_url == "url/north/ai"
        assert self.builder.organization_name == "organization_name"
        assert self.builder.method == "prediction"

    def test_save(self):
        self.builder.save()
        assert self.builder.method == "save"

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



