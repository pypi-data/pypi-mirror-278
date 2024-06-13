import pytest
from datetime import datetime

from searching.datapoints_search import DataPointsSearchBuilder
from opengate_client import OpenGateClient

non_type_str = [111, 1.0, True, {"key": "value"}, ["list"]]
non_type_list = [111, 1.0, True, {"key": "value"}, "str"]


@pytest.fixture
def client():
    """Fixture to provide an OpenGateClient instance."""
    return OpenGateClient(url="None", api_key="api-key")


class TestDatapointsSearch:
    """Unit tests for the datapoints search functionality."""

    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.builder = DataPointsSearchBuilder(client)

    def test_with_transpose(self):
        assert self.transpose

    @pytest.mark.parametrize("invalid_input", non_type_str)
    def test_with_device_identifier_raises_type_error(self, invalid_input):
        with pytest.raises(TypeError):
            self.builder.with_device_identifier(invalid_input)

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
