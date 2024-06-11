import pytest
from datetime import datetime

from ....searching.datapoints_search import DataPointsSearchBuilder
from ....opengate_client import OpenGateClient

non_type_str = [111, 1.0, True, {"key": "value"}, ["list"]]


@pytest.fixture
def client():
    """Fixture to provide an OpenGateClient instance."""
    return OpenGateClient(url="None", api_key="api-key")


class TestDatapointsSearch:
    """Unit tests for the datapoints search functionality."""

    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.builder = DataPointsSearchBuilder(client)

    def test_with_body(self):
        filter_datapoints = {"filter": {},
                             "select": [{"name": "entityIdentifier", "fields": [{"field": "entityIdentifier"}]},
                                        {"name": "subEntityIdentifier", "fields": [{"field": "subEntityIdentifier"}]}]}
        self.builder.with_body(filter_datapoints)
        assert self.builder.body_data == filter_datapoints

    def test_with_format_csv(self):
        self.builder.with_format("csv")
        assert self.builder.format_data == "csv"
        assert self.builder.format_data_headers == "text/plain"

    def test_with_format_csv_check_header(self):
        self.builder.with_format("csv")
        assert self.builder.format_data_headers != "application/json"

    def test_with_format_dict(self):
        self.builder.with_format("dict")
        assert self.builder.format_data == "dict"
        assert self.builder.format_data_headers == "application/json"

    def test_with_format_dict_check_format_header(self):
        self.builder.with_format("dict")
        assert self.builder.format_data_headers != "text/plain"

    def test_with_flattened(self):
        self.builder.with_flattened()
        assert self.builder.flatten is True

    def test_with_summary(self):
        self.builder.with_summary()
        assert self.builder.summary is True

    def test_with_default_sorted(self):
        self.builder.with_default_sorted()
        assert self.builder.default_sorted is True

    def test_with_case_sensitive(self):
        self.builder.with_case_sensitive()
        assert self.builder.case_sensitive is True

    @pytest.mark.parametrize("invalid_input", non_type_str)
    def test_with_format_raises_type_error(self, invalid_input):
        with pytest.raises(TypeError):
            self.builder.with_format(invalid_input)

    def test_with_transpose(self):
        self.builder.with_transpose()
        assert self.builder.transpose is True

    def test_with_mapped_mapping(self):
        mapping = {'device.communicationModules[].subscription.address': {'type': 'type', 'IP': 'value'},
                   'entity.location': {'latitud': 'position.coordinates[0]', 'longitud': 'position.coordinates[1]'}}
        self.builder.with_mapped_transpose(mapping)
        assert self.builder.mapping == mapping

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
        self.builder.method_calls = ['build', 'some_other_method', 'execute']
        with pytest.raises(Exception):
            self.builder.execute()
        assert "The build() function must be called and must be the last method invoked before execute"

