from datetime import datetime
from typing import Any
import time
import openpyxl
import pandas as pd
import json
import os
import requests
from ..utils import validate_type, set_method_call, parse_json
from dateutil import parser
from functools import wraps
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException


class IotBulkCollectionBuilder:
    """Collection Builder"""

    def __init__(self, opengate_client):
        self.client = opengate_client
        self.headers = self.client.headers
        self.requires: dict[str, Any] = {}
        self.device_identifier: str | None = None
        self.version: str | None = None
        self.payload: dict = {"devices": {}}
        self.method_calls: list = []
        self.builder: bool = False

    @set_method_call
    def add_device_datastream_datapoints(self, device_id: str, datastream_id: str, datapoints: list[
        tuple[int | float | bool | dict, None | datetime | int]]) -> "IotBulkCollectionBuilder":
        """
        Add device identifier with the datastream identifier and a list of datapoints with their value and at for data collection.
        Parameters:
            device_id (str): The identifier for the device.
            datastream_id (str): The identifier for the datastream within the device.
            datapoints (list): A list of tuples, where each tuple contains the data value and the timestamp
                               at which the data was recorded. The tuple structure is (value, at).

        Returns:
            IotBulkCollectionBuilder: Returns itself to allow for method chaining.

        Example:
            builder.add_device_datastream_datapoints('device123', 'temperature', [(22.5, 1609459200)])
        """

        dp = [(dp[0], dp[1], None) for dp in datapoints]
        return self.add_device_datastream_datapoints_with_from(device_id, datastream_id, dp)

    @set_method_call
    def add_device_datastream_datapoints_with_from(self, device_id: str, datastream_id: str, datapoints: list[
        tuple[int | float | bool | dict, None | datetime | int, None | datetime | int]]):
        """
        Add device identifier with the datastream identifier and a list of datapoints with their value with at and from for data collection.
        they are created. This method also handles the inclusion of timestamps for when the data was recorded
        ('at') and when it was transmitted ('from').

        Parameters:
            device_id (str): The identifier for the device.
            datastream_id (str): The identifier for the datastream within the device.
            datapoints (list): A list of tuples, where each tuple contains the data value, the timestamp
                               at which the data was recorded, and the timestamp from which the data was sent.
                               The tuple structure is (value, at, from).

        Raises:
            ValueError: If the datapoints list is empty, indicating that no data is being added.

        Returns:
            self: Returns the instance of the class to allow for method chaining.

        Example:
            builder.add_device_datastream_datapoints_with_from('device123', 'temperature', [(22.5, 1609459200, 1609459300)])
        """
        validate_type(device_id, str, "Device identifier")
        validate_type(datastream_id, str, "Datastream identifier")
        validate_type(datapoints, list, "Datastreams")
        if not datapoints:
            raise ValueError("Datastream must contain at least one datapoint")

        if device_id not in self.payload['devices']:
            self.payload['devices'][device_id] = {
                "datastreams": [],
                "version": None,
                "origin_device": None
            }

        if self.payload['devices'][device_id]['version'] is None:
            self.payload['devices'][device_id]['version'] = "1.0.0"

        device_data = self.payload['devices'][device_id]
        datastream = next((ds for ds in device_data['datastreams'] if ds['id'] == datastream_id), None)
        if not datastream:
            datastream = {"id": datastream_id, "datapoints": []}
            device_data['datastreams'].append(datastream)

        for value, at, from_ in datapoints:
            validate_type(at, (type(None), datetime, int), "At")

            validate_type(from_, (type(None), datetime, int), "From")

            datapoint = {"value": value}
            if at is not None:
                datapoint["at"] = int(at.timestamp() * 1000) if isinstance(at, datetime) else at
            if from_ is not None:
                datapoint["from"] = int(from_.timestamp() * 1000) if isinstance(from_, datetime) else from_
            datastream['datapoints'].append(datapoint)

        return self

    @set_method_call
    def from_dataframe(self, df: pd.DataFrame) -> "IotBulkCollectionBuilder":
        """
        Processes a DataFrame to extract device, data and datapoints, and adds them to the payload.

        Parameters:
            df (pd.DataFrame): The DataFrame containing the device data and datapoints. The DataFrame
                               is expected to have columns that match the expected structure for device
                               datastreams and datapoints.

        Returns:
            IotBulkCollectionBuilder: Returns itself to allow for method chaining.

        Example:
            df = pd.DataFrame({
                 'device_id': ['device'], ['device2'],
                 'datastream_id': ['datastream'],['datastream2'],
                 'value': [value, value2],
                 'at': [datetime.now(), 2000]
            })
            builder.from_dataframe(df)
        """
        validate_type(df, pd.DataFrame, "Dataframe")
        self._process_dataframe(df)
        return self

    @set_method_call
    def from_spreadsheet(self, path: str, sheet_name_index: int | str) -> "IotBulkCollectionBuilder":
        """
        Loads data from a spreadsheet, processes it, and adds the resulting device data and datapoints
        to the payload. This method is particularly useful for bulk data operations where data is
        stored in spreadsheet format.

        Parameters:
            path (str): The file path to the spreadsheet to load.
            sheet_name_index (int | str): The sheet name or index to load from the spreadsheet.

        Returns:
            IotBulkCollectionBuilder: Returns itself to allow for method chaining.
        """
        validate_type(path, str, "Path")
        validate_type(sheet_name_index, (int, str), "Sheet name index")

        df = pd.read_excel(path, sheet_name=sheet_name_index)
        df.columns = df.columns.str.lower().str.replace(' ', '_')

        df['value'] = df['value'].apply(parse_json)

        if 'at' in df.columns:
            df['at'] = pd.to_datetime(df['at'], errors='coerce', utc=True)
        if 'from' in df.columns:
            df['from'] = pd.to_datetime(df['from'], errors='coerce', utc=True)

        if 'path' in df.columns:
            df['path'] = df['path'].apply(lambda x: [str(item) for item in json.loads(x)] if isinstance(x, str) else x)

        self._process_dataframe(df)
        return self

    @set_method_call
    def build(self):
        self.builder = True
        self._validate_builds()

        if self.method_calls.count('build_execute') > 0:
            raise ValueError("You cannot use build() together with build_execute()")

        return self

    @set_method_call
    def build_execute(self, include_payload=False):

        self.builder = True

        if self.method_calls.count('build') > 0:
            raise ValueError("You cannot use build_execute() together with build()")

        # if not self.builder or self.method_calls[-1] != 'build_execute':
        #    raise Exception("The build_execute() must be the last method")

        self._validate_builds()
        self._execute_bulk_iot_collection()

        return self._execute_bulk_iot_collection(include_payload)

    def to_dict(self) -> dict:
        """
        This method is used to retrieve the entire payload that has been constructed by the builder. The payload
        includes all devices, their respective datastreams, and the datapoints that have been added to each datastream.
        This is particularly useful for inspecting the current state of the payload after all configurations and
        additions have been made, but before any execution actions (like sending data to a server) are taken.

        Returns:
            dict: A dictionary representing the current state of the payload within the IotBulkCollectionBuilder.
                  This dictionary includes all devices, datastreams, and datapoints that have been configured.

        Example:
            builder.to_dict()

        Raises:
            Exception: If the build method was not called before this method.
        """
        if not self.builder:
            raise Exception("The build() method must be called before calling to_dict().")

        return self.payload

    @set_method_call
    def execute(self, include_payload=False):
        """
        Executes the IoT collection based on the current configuration of the builder.

        Parameters:
            include_payload (bool): Determine if the payload should be included in the response.

        Example:
            builder.build()
            response = builder.execute(True)

        Returns:
            dict: A dictionary containing the results of the execution, including success messages for each device ID
                  if the data was successfully sent, or error messages detailing what went wrong.


        Raises:
            Exception: If `build()` has not been called before `execute()`, or if it was not the last method invoked prior to `execute()`.
        """

        if not self.builder or self.method_calls[-2] != 'build':
            raise Exception("The build() function must be called and must be the last method invoked before execute")

        results = self._execute_bulk_iot_collection(include_payload)
        return results

    def _execute_bulk_iot_collection(self, include_payload):
        results = {}
        errors = {}
        for device_id, device_data in self.payload.get('devices', {}).items():
            try:
                response = requests.post(f'{self.client.url}/south/v80/devices/{device_id}/collect/iot',
                                         headers=self.headers, json=device_data, verify=False, timeout=3000)
                if response.status_code == 201:
                    result = {'status_code': response.status_code}
                    if include_payload:
                        result['payload'] = device_data
                    results[device_id] = result
                else:
                    errors[device_id] = {'error': 'HTTP error', 'code': response.status_code, 'message': response.text}

            except HTTPError as http_err:
                errors[device_id] = {'error': 'HTTP error', 'code': http_err.response.status_code,
                                     'message': http_err.response.text}
            except ConnectionError as conn_err:
                errors[device_id] = {'error': 'Connection error', 'message': str(conn_err)}
            except Timeout as timeout_err:
                errors[device_id] = {'error': 'Timeout error', 'message': str(timeout_err)}
            except RequestException as req_err:
                errors[device_id] = {'error': 'Request exception', 'message': str(req_err)}
            except Exception as e:
                errors[device_id] = {'error': 'Unexpected error', 'message': str(e)}

        if errors:
            error_messages = "; ".join(
                f"{key}: (Error: {value['error']}, Status code: {value['code']}), {value['message']}" for key, value in
                errors.items()
            )
            if results:
                results.items()
                raise Exception(
                    f"The following entities were executed successfully: {results}. However, errors occurred for these entities: {error_messages}.")
            else:
                raise Exception(f"Errors occurred for these entities: {error_messages}")
        else:
            return results

    def _process_dataframe(self, df: pd.DataFrame):
        required_columns = ['device_id', 'data_stream_id', 'value']
        optional_columns = ['origin_device_identifier', 'version', 'path', 'trustedboot', 'at', 'from']

        if not set(required_columns).issubset(df.columns):
            missing_cols = set(required_columns) - set(df.columns)
            raise ValueError(f"Missing required columns: {', '.join(missing_cols)}")

        for index, row in df.iterrows():
            device_id = row['device_id']
            datastream_id = row['data_stream_id']
            value = row['value']
            at = row.get('at', None)
            from_ = row.get('from', None)

            validate_type(device_id, str, "Device ID")
            validate_type(datastream_id, str, "Data Stream ID")
            validate_type(value, (int, str, float, bool, dict, list), "Value")

            if device_id not in self.payload['devices']:
                device_config = {
                    "datastreams": []
                }
                for field in optional_columns:
                    if field in df.columns and (
                            pd.Series(row[field]).notna().any() if isinstance(row[field], list) else pd.notna(
                                row[field])):
                        if field != 'at' and field != 'from':
                            device_config[field] = row[field]

                self.payload['devices'][device_id] = device_config

                if 'version' not in device_config or device_config['version'] is None:
                    device_config['version'] = "1.0.0"

            if 'origin_device_identifier' in df.columns and pd.notna(row['origin_device_identifier']):
                self.payload['devices'][device_id]['device'] = row['origin_device_identifier']
                if 'origin_device_identifier' in self.payload['devices'][device_id]:
                    del self.payload['devices'][device_id]['origin_device_identifier']

            datapoint = {"value": value}

            if pd.notna(at):
                if isinstance(at, float):
                    at = int(at)
                validate_type(at, (type(None), datetime, int), "At")
                if isinstance(at, datetime):
                    datapoint["at"] = int(at.timestamp() * 1000)
                else:
                    datapoint["at"] = at
            if pd.notna(from_):
                if isinstance(from_, float):
                    from_ = int(from_)
                validate_type(from_, (type(None), datetime, int), "From")
                if isinstance(from_, datetime):
                    datapoint["from"] = int(from_.timestamp() * 1000)
                else:
                    datapoint["from"] = from_

            existing_ds = next(
                (ds for ds in self.payload['devices'][device_id]['datastreams'] if ds['id'] == datastream_id), None)
            if existing_ds:
                existing_ds['datapoints'].append(datapoint)
            else:
                new_ds = {"id": datastream_id, "datapoints": [datapoint]}
                self.payload['devices'][device_id]['datastreams'].append(new_ds)

        return self

    def _ensure_build_is_last_method(self):
        if not self.builder or self.method_calls[-2] != 'build':
            raise Exception("The build() function must be called and must be the last method invoked before execute")

    def _validate_builds(self):
        if self.method_calls.count('from_spreadsheet') == 0 and self.method_calls.count(
                'from_dataframe') == 0 and self.method_calls.count(
            'add_device_datastream_datapoints_with_from') == 0 and self.method_calls.count(
            'add_device_datastream_datapoints') == 0:
            raise ValueError(
                "The from_dict() or add_device_datastream_datapoints or add_device_datastream_datapoints_with_from() from_add method must be called")
