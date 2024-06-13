import pytest
from datetime import datetime

from ....opengate_client import OpenGateClient
from ....collection.iot_collection import IotCollectionBuilder

non_type_str = [111, 1.0, True, {"key": "value"}, ["list"]]
non_type_list = [111, 1.0, True, {"key": "value"}, "str"]


@pytest.fixture
def client():
    """ Fixture to provide an OpenGateClient instance."""
    return OpenGateClient(url="url", api_key="api_key")


class TestIotCollection:
    """Unit tests for the IotCollection functionality."""

    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.builder = IotCollectionBuilder(client)

    def test_with_device_identifier(self):
        device_id = "device"
        self.builder.with_device_identifier(device_id)
        assert self.builder.device_identifier == device_id

    @pytest.mark.parametrize("invalid_input", non_type_str)
    def test_with_device_identifier_raises_type_error(self, invalid_input):
        with pytest.raises(TypeError):
            self.builder.with_device_identifier(invalid_input)

    def test_with_origin_device_identifier(self):
        origin_id = "origin_device_identifier"
        self.builder.with_origin_device_identifier(origin_id)
        assert self.builder.payload['device'] == origin_id

    @pytest.mark.parametrize("invalid_input", non_type_str)
    def test_with_origin_device_identifier_raises_type_error(self, invalid_input):
        with pytest.raises(TypeError):
            self.builder.with_origin_device_identifier(invalid_input)

    def test_with_version(self):
        version = "1.0.0"
        self.builder.with_version(version)
        assert self.builder.version == version
        assert self.builder.payload['version'] == version

    @pytest.mark.parametrize("invalid_input", non_type_str)
    def test_with_version_raises_type_error(self, invalid_input):
        with pytest.raises(TypeError):
            self.builder.with_version(invalid_input)

    def test_with_path(self):
        path = ["prueba1", "prueba2"]
        self.builder.with_path(path)
        assert self.builder.payload['path'] == path

    @pytest.mark.parametrize("invalid_input", non_type_list)
    def test_with_path_raises_type_error(self, invalid_input):
        with pytest.raises(TypeError):
            self.builder.with_path(invalid_input)

    def test_with_trustedboot(self):
        trustedboot = "enabled"
        self.builder.with_trustedboot(trustedboot)
        assert self.builder.payload['trustedBoot'] == trustedboot

    @pytest.mark.parametrize("invalid_input", non_type_str)
    def test_with_trustedboot_raises_type_error(self, invalid_input):
        with pytest.raises(TypeError):
            self.builder.with_trustedboot(invalid_input)

    def test_add_datastream_datapoints(self):
        datastream_id = "temperature"
        datapoints = [(22.5, datetime.now()), (23.0, None)]
        self.builder.add_datastream_datapoints(datastream_id, datapoints)
        found_datastream = next((ds for ds in self.builder.payload['datastreams'] if ds['id'] == datastream_id), None)
        assert len(found_datastream['datapoints']) == 2

    def test_add_datastream_datapoints_empty_list(self):
        datastream_id = "temperature"
        datapoints = []
        with pytest.raises(ValueError, match="Datastream must contain at least one datapoint"):
            self.builder.add_datastream_datapoints(datastream_id, datapoints)

    def test_add_datastream_datapoints_invalid_datapoints(self):
        datastream_id = "temperature"
        datapoints = "string"
        with pytest.raises(TypeError):
            self.builder.add_datastream_datapoints(datastream_id, datapoints)

    def test_add_datapoints_from_with_invalid_value_type(self):
        datastream_id = "temperature"
        datapoints = [(None, datetime.now(), datetime.now())]
        with pytest.raises(TypeError) as context:
            self.builder.add_datastream_datapoints_with_from(datastream_id, datapoints)
        assert "Value" in str(context.value)

    def test_add_datapoints_from_with_invalid_at(self):
        datastream_id = "humidity"
        datapoints = [(55.0, "string", datetime.now())]
        with pytest.raises(TypeError) as context:
            self.builder.add_datastream_datapoints_with_from(datastream_id, datapoints)
        assert "At" in str(context.value)

    def test_add_datapoints_from_with_invalid_from(self):
        datastream_id = "humidity"
        datapoints = [(55.0, datetime.now(), "test")]
        with pytest.raises(TypeError) as context:
            self.builder.add_datastream_datapoints_with_from(datastream_id, datapoints)
        assert "From" in str(context.value)

    def test_from_dict(self):
        payload = {
            'version': '1.1.2',
            'device': 'device123',
            'path': ["111"],
            'trustedBoot': 'enabled',
            "datastreams": [
                {
                    "id": "device.temperature.value",
                    "datapoints": [
                        {
                            "at": 1431602523123,
                            "value": 25
                        },
                        {
                            "at": 1431602523123,
                            "value": 26
                        },
                        {
                            "at": 1431602523123,
                            "value": 27
                        }
                    ]
                },
            ]
        }
        self.builder.from_dict(payload)
        assert self.builder.payload['version'] == payload['version']
        assert self.builder.payload['device'] == payload['device']
        assert self.builder.payload['path'] == payload['path']
        assert self.builder.payload['trustedBoot'] == payload['trustedBoot']
        assert self.builder.payload['datastreams'][0]['id'] == payload['datastreams'][0]['id']

    def test_from_dict_missing_datastreams(self):
        payload = {'version': '1.0.0'}
        with pytest.raises(ValueError,
                           match="The 'datastreams' field must be present and contain at least one element."):
            self.builder.from_dict(payload)

    def test_from_dict_unsupported_key(self):
        payload = {
            'version': '1.1.2',
            'unsupported_key': 'key',
            "datastreams": [
                {
                    "id": "device.temperature.value",
                    "datapoints": [
                        {
                            "at": 1431602523123,
                            "value": 25
                        },
                        {
                            "at": 1431602523123,
                            "value": 26
                        },
                        {
                            "at": 1431602523123,
                            "value": 27
                        }
                    ]
                },
            ]
        }
        with pytest.raises(ValueError, match="Unsupported key 'unsupported_key' in payload"):
            self.builder.from_dict(payload)

    def test_to_dict(self):
        payload = {
            'version': '1.1.2',
            "datastreams": [
                {
                    "id": "device.temperature.value",
                    "datapoints": [
                        {
                            "at": 1431602523123,
                            "value": 25
                        },
                        {
                            "at": 1431602523123,
                            "value": 26
                        },
                        {
                            "at": 1431602523123,
                            "value": 27
                        }
                    ]
                },
            ]
        }
        expected_payload = {
            'version': '1.1.2',
            "datastreams": [
                {
                    "id": "device.temperature.value",
                    "datapoints": [
                        {
                            "at": 1431602523123,
                            "value": 25
                        },
                        {
                            "at": 1431602523123,
                            "value": 26
                        },
                        {
                            "at": 1431602523123,
                            "value": 27
                        }
                    ]
                },
            ]
        }
        self.builder.from_dict(payload)
        self.builder.with_device_identifier('device')
        assert self.builder.build().to_dict() == expected_payload

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
