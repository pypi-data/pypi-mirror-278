import pytest
from datetime import datetime
import pandas as pd

from ....opengate_client import OpenGateClient
from ....collection.iot_bulk_collection import IotBulkCollectionBuilder

non_type_str = [111, 1.0, True, {"key": "value"}, ["list"]]


@pytest.fixture
def client():
    """Fixture to provide an OpenGateClient instance."""
    return OpenGateClient(url=url, api_key=api_key)


class TestIotBulkCollection:
    """Unit tests for the IotBulkCollectionBuilder functionality."""

    @pytest.fixture(autouse=True)
    def setup(self, client):
        self.builder = IotBulkCollectionBuilder(client)

    def test_add_device_datastream_datapoints_with_empty_datapoints(self):
        with pytest.raises(ValueError):
            self.builder.add_device_datastream_datapoints_with_from('device', 'temperature', [])
        assert "Datastream must contain at least one datapoint"

    def test_add_device_datastream_datapoints_with_valid_data(self):
        datapoints = [(22.5, datetime.now(), None)]
        self.builder.add_device_datastream_datapoints_with_from('device', 'temperature', datapoints)
        assert (len(self.builder.payload['devices']['device']['datastreams']), 1)

    def test_from_dataframe_with_missing_columns(self):
        df = pd.DataFrame({
            'device_id': ['device1'],
            'value': [100]
        })
        with pytest.raises(ValueError, match="Missing required columns: data_stream_id"):
            self.builder.from_dataframe(df)

    def test_from_dataframe_with_valid_data(self):
        data = {
            "device_id": ['device1'],
            "data_stream_id": ["temp"],
            "value": [22],
            "at": [1672531200000],
            "from": [None]
        }
        df = pd.DataFrame(data)
        self.builder.from_dataframe(df)

        device_data = self.builder.payload['devices'].get('device1', {})
        datastreams = device_data.get('datastreams', [])[0]
        assert 'device1' in self.builder.payload['devices']
        assert datastreams['id'] == 'temp'
        assert datastreams['datapoints'][0]['value'] == 22
        assert datastreams['datapoints'][0]['at'] == 1672531200000

    def test_from_dataframe_with_multiple_valid_data(self):
        data = {
            "device_id": ['device1', 'device2'],
            "data_stream_id": ['temp', 'hum'],
            "value": [22, 33],
            "at": [1972531200000, 1672531200000],
            "from": [1972531200000, 1672531200000]
        }
        df = pd.DataFrame(data)
        self.builder.from_dataframe(df)

        device_data = self.builder.payload['devices'].get('device1', {})
        datastreams = device_data.get('datastreams', [])[0]
        assert 'device1' in self.builder.payload['devices']
        assert datastreams['id'] == 'temp'
        assert datastreams['datapoints'][0]['value'] == 22
        assert datastreams['datapoints'][0]['at'] == 1972531200000
        assert datastreams['datapoints'][0]['from'] == 1972531200000

        device_data = self.builder.payload['devices'].get('device2', {})
        datastreams = device_data.get('datastreams', [])[0]
        assert 'device2' in self.builder.payload['devices']
        assert datastreams['id'] == 'hum'
        assert datastreams['datapoints'][0]['value'] == 33
        assert datastreams['datapoints'][0]['at'] == 1672531200000

    def test_from_dataframe_with_invalid_data_device_id_types(self):
        data = {
            "device_id": [12345],
            "data_stream_id": ["temp"],
            "value": ["22"],
            "at": [datetime.now()],
            "from": [datetime.now()]
        }
        df = pd.DataFrame(data)

        with pytest.raises(TypeError, match="Device ID must be of type 'str', but 'int' was provided"):
            self.builder.from_dataframe(df)

    def test_from_dataframe_with_invalid_data_stream_id_types(self):
        data = {
            "device_id": ["device"],
            "data_stream_id": [123],
            "value": ["22"],
            "at": [datetime.now()],
            "from": [datetime.now()]
        }
        df = pd.DataFrame(data)

        with pytest.raises(TypeError, match="Data Stream ID must be of type 'str', but 'int' was provided"):
            self.builder.from_dataframe(df)

    def test_from_dataframe_with_invalid_at_types(self):
        data = {
            "device_id": ["device"],
            "data_stream_id": ["temp"],
            "value": ["22"],
            "at": ["fecha"],
            "from": [datetime.now()]
        }
        df = pd.DataFrame(data)

        with pytest.raises(TypeError, match="At must be of type 'NoneType, datetime, int', but 'str' was provided"):
            self.builder.from_dataframe(df)

    def test_from_dataframe_with_invalid_from_types(self):
        data = {
            "device_id": ["device"],
            "data_stream_id": ["temp"],
            "value": ["22"],
            "at": [datetime.now()],
            "from": ["fecha"]
        }
        df = pd.DataFrame(data)

        with pytest.raises(TypeError, match="From must be of type 'NoneType, datetime, int', but 'str' was provided"):
            self.builder.from_dataframe(df)

    def test_add_device_datastream_datapoints_valid_data(self):
        self.builder.add_device_datastream_datapoints('device', 'temperature', [(22.5, 1609459200)])
        assert 'device' in self.builder.payload['devices']
        assert self.builder.payload['devices']['device']['datastreams'][0]['id'] == 'temperature'
        assert self.builder.payload['devices']['device']['datastreams'][0]['datapoints'][0]['value'] == 22.5
        assert self.builder.payload['devices']['device']['datastreams'][0]['datapoints'][0]['at'] == 1609459200

    def test_add_device_datastream_datapoints_invalid_data_type(self):
        with pytest.raises(TypeError, match="At must be of type 'NoneType, datetime, int', but 'str' was provided"):
            self.builder.add_device_datastream_datapoints('device123', 'temperature', [(24, 'fecha')])

        with pytest.raises(TypeError, match="Device identifier must be of type 'str', but 'int' was provided"):
            self.builder.add_device_datastream_datapoints(1234, 'temperature', [(24, 1609459200)])

        with pytest.raises(TypeError, match="Datastream identifier must be of type 'str', but 'int' was provided"):
            self.builder.add_device_datastream_datapoints("tempe", 1111, [(24, 1609459200)])

    def test_add_device_datastream_datapoints_with_from_invalid_data_type(self):
        with pytest.raises(TypeError, match="At must be of type 'NoneType, datetime, int', but 'str' was provided"):
            self.builder.add_device_datastream_datapoints_with_from('device123', 'temperature',
                                                                    [(24, 'fecha', 1609459200)])

        with pytest.raises(TypeError, match="From must be of type 'NoneType, datetime, int', but 'str' was provided"):
            self.builder.add_device_datastream_datapoints_with_from('device123', 'temperature',
                                                                    [(24, 1609459200, 'fecha')])

        with pytest.raises(TypeError, match="Device identifier must be of type 'str', but 'int' was provided"):
            self.builder.add_device_datastream_datapoints_with_from(1234, 'temperature', [(24, 1609459200, 19459200)])

        with pytest.raises(TypeError, match="Datastream identifier must be of type 'str', but 'int' was provided"):
            self.builder.add_device_datastream_datapoints_with_from("tempe", 1111, [(24, 1609459200, 19459200)])


    def test_to_dict(self):
        data = {
            "device_id": ['device1', 'device2', 'device3'],
            "data_stream_id": ['temp', 'hum', 'temp'],
            "version": ['1.1.0', None, '1.1.3'],
            "value": [25, 30, 10],
            "at": [1431602523123, 1431602523123, 1431602523123],
            "from": [1431602523123, 1431602523123, 1431602523123],
        }
        df = pd.DataFrame(data)
        self.builder.from_dataframe(df)

        # Device 1
        device_data = self.builder.payload['devices'].get('device1', {})
        datastreams = device_data.get('datastreams', [])[0]
        assert 'device1' in self.builder.payload['devices']
        assert device_data.get('version') == '1.1.0'
        assert datastreams['id'] == 'temp'
        assert datastreams['datapoints'][0]['value'] == 25
        assert datastreams['datapoints'][0]['at'] == 1431602523123
        assert datastreams['datapoints'][0]['from'] == 1431602523123

        # Device 2
        device_data = self.builder.payload['devices'].get('device2', {})
        datastreams = device_data.get('datastreams', [])[0]
        assert 'device2' in self.builder.payload['devices']
        assert device_data.get('version') == '1.0.0'
        assert datastreams['id'] == 'hum'
        assert datastreams['datapoints'][0]['value'] == 30
        assert datastreams['datapoints'][0]['at'] == 1431602523123
        assert datastreams['datapoints'][0]['from'] == 1431602523123

        # Device 3
        device_data = self.builder.payload['devices'].get('device3', {})
        datastreams = device_data.get('datastreams', [])[0]
        assert 'device3' in self.builder.payload['devices']
        assert device_data.get('version') == '1.1.3'
        assert datastreams['id'] == 'temp'
        assert datastreams['datapoints'][0]['value'] == 10
        assert datastreams['datapoints'][0]['at'] == 1431602523123
        assert datastreams['datapoints'][0]['from'] == 1431602523123

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
