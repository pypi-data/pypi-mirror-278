import pytest
import sys
import os
import configparser
from ....opengate_client import OpenGateClient
from ....rules.rules_searching import RulesSearchBuilder

non_type_str = [111, 1.0, True, {"key": "value"}, ["list"]]

@pytest.fixture
def client():
    return OpenGateClient(url="url", api_key="api_password")


class TestRulesSearching:
    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.builder = RulesSearchBuilder(client)

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
