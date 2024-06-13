import pytest
import sys
import os
import configparser
from ....opengate_client import OpenGateClient
from ....rules.rules import RulesBuilder

non_type_str = [111, 1.0, True, {"key": "value"}, ["list"]]


@pytest.fixture
def client():
    return OpenGateClient(url="url", api_key="api_password")


class TestRules:
    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.builder = RulesBuilder(client)

    def test_with_organization_name(self):
        organization = "organization_name"
        self.builder.with_organization_name(organization)
        assert self.builder.rule_data["organization"] == organization

    def test_with_identifier(self):
        identifier = "identifier"
        self.builder.with_identifier(identifier)
        assert self.builder.rule_data["identifier"] == identifier

    def test_with_actions(self):
        actions = {
            "actions": {"open": [{"name": "name", "enabled": False, "severity": "INFORMATIVE", "priority": "LOW"}]}}
        self.builder.with_actions(actions)
        assert self.builder.rule_data['actions'] == actions

    def test_with_actions_delay(self):
        self.builder.with_actions_delay(1000)
        assert self.builder.rule_data['actionsDelay'] == 1000

    def test_with_active(self):
        self.builder.with_active(False)
        assert self.builder.rule_data['active'] is False

    def test_with_channel(self):
        self.builder.with_channel('channel')
        assert self.builder.rule_data['channel'] == 'channel'

    def test_with_condition(self):
        condition = {"condition": {
            "filter": {"eq": {"device.cpu.usage._current.value": "$datastream:device.cpu.usage._current.value"}}}}
        self.builder.with_condition(condition)
        assert self.builder.rule_data['condition'] == condition

    def test_with_mode(self):
        self.builder.with_mode('ADVANCED')
        assert self.builder.rule_data["mode"] == 'ADVANCED'
        self.builder.with_mode('EASY')
        assert self.builder.rule_data["mode"] == 'EASY'

    def test_with_name(self):
        self.builder.with_name('name')
        assert self.builder.rule_data["name"] == 'name'

    def test_with_type(self):
        type_rule = {"type": {"name": "DATASTREAM", "datastreams": [
            {"name": "device.cpu.usage", "fields": [{"field": "value", "alias": "CPU usage"}], "prefilter": False}]}}
        self.builder.with_type(type_rule)
        assert self.builder.rule_data["type"] == type_rule

    def test_with_parameters(self):
        parameters = [{"name": "name", "schema": "string", "value": "2"}]
        self.builder.with_parameters(parameters)
        assert self.builder.rule_data["parameters"] == parameters

    def test_create(self):
        self.builder.with_organization_name("organization_name")
        self.builder.with_channel("channel")
        self.builder.create()
        assert self.builder.rule_data["organization"] == "organization_name"
        assert self.builder.rule_data['channel'] == 'channel'
        assert self.builder.method == "create"

    def test_find_all(self):
        self.builder.find_all()
        assert self.builder.method == "find_all"

    def test_find_one(self):
        self.builder.with_identifier("identifier")
        self.builder.with_organization_name("organization_name")
        self.builder.with_channel("channel")
        self.builder.find_one()
        assert self.builder.rule_data["organization"] == "organization_name"
        assert self.builder.rule_data['channel'] == 'channel'
        assert self.builder.rule_data["identifier"] == "identifier"
        assert self.builder.method == "find_one"

    def test_update(self):
        self.builder.with_identifier("identifier")
        self.builder.with_organization_name("organization_name")
        self.builder.with_channel("channel")
        self.builder.update()
        assert self.builder.rule_data["organization"] == "organization_name"
        assert self.builder.rule_data['channel'] == 'channel'
        assert self.builder.rule_data["identifier"] == "identifier"
        assert self.builder.method == "update"

    def test_update_parameters(self):
        self.builder.with_identifier("identifier")
        self.builder.with_organization_name("organization_name")
        self.builder.with_channel("channel")
        self.builder.with_parameters([{"parameter1": "value1", "parameter2": "value2"}])
        self.builder.update_parameters()
        assert self.builder.rule_data["organization"] == "organization_name"
        assert self.builder.rule_data['channel'] == 'channel'
        assert self.builder.rule_data["identifier"] == "identifier"
        assert self.builder.method == "update_parameters"

    def test_delete(self):
        self.builder.with_identifier("identifier")
        self.builder.with_organization_name("organization_name")
        self.builder.with_channel("channel")
        self.builder.delete()
        assert self.builder.rule_data["organization"] == "organization_name"
        assert self.builder.rule_data['channel'] == 'channel'
        assert self.builder.rule_data["identifier"] == "identifier"
        assert self.builder.method == "delete"

    def test_catalog(self):
        self.builder.catalog()
        assert self.builder.method == "catalog"

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
