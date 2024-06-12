'''  EntitiesBuilder '''

import requests
import pandas as pd
from typing import Callable, Union, List, Dict, Any
from flatten_dict import flatten


class EntitiesBuilder:
    ''' Builder entities'''
    def __init__(self, opengate_client):
        self.client = opengate_client
        self.filter: Dict[str, Any] = {}
        self.format_data: str | None = None
        self.flatten: bool = False
        self.utc: bool = False
        self.summary: bool = False
        self.default_sorted: bool = False
        self.case_sensitive: bool = False
        self.organization_name: str | None = None
        self.bulk_action: str | None = None
        self.bulk_type: str | None = None
        self.csv_data: str | None = None
        self.url: str | None = None
        self.method: str | None = None
        self.requires: Dict[str, Any] = {}
        self.headers: Dict[str, Any] = self.client.headers

    def with_filter(self, filter_data: Dict[str, Any]) -> 'EntitiesBuilder':
        """ Body """
        self.filter = filter_data
        return self

    def with_body(self, filter_data: Dict[str, Any]) -> 'EntitiesBuilder':
        ''' Body '''
        self.filter = filter_data
        return self

    def with_format(self, format_data: str) -> 'EntitiesBuilder':
        ''' Formats the flat entities data based on the specified format ('csv', 'dict', or 'pandas'). '''
        self.format_data = format_data
        if self.format_data == 'csv':
            self.headers['Accept'] = 'text/plain'
        else:
            self.headers['Accept'] = 'application/json'
        return self

    def with_flattened(self):
        self.flatten = True
        return self

    def with_utc(self):
        self.utc = True
        return self

    def with_summary(self):
        self.summary = True
        return self

    def with_default_sorted(self) -> 'EntitiesBuilder':
        """ default sorted"""
        self.default_sorted = True
        return self

    def with_case_sensitive(self) -> 'EntitiesBuilder':
        """ case sensitive """
        self.case_sensitive = True
        return self

    def search(self) -> 'EntitiesBuilder':
        ''' search '''
        self.requires = {
            'default sorted': self.default_sorted
        }
        self.method = 'search'
        if self.format_data == "pandas":
            self.flatten = False

        self.url = f'{self.client.url}/north/v80/search/entities?flattened={self.flatten}&utc={self.utc}&summary={self.summary}&defaultSorted={self.default_sorted}&caseSensitive={self.case_sensitive}'
        print("url", self.url)
        return self

    def with_organization_name(self, organization_name: str) -> 'EntitiesBuilder':
        ''' organization_name '''
        self.organization_name = organization_name
        return self

    def with_bulk_action(self, bulk_action: str) -> 'EntitiesBuilder':
        ''' bulk_action '''
        self.bulk_action = bulk_action
        return self

    def with_bulk_type(self, bulk_type: str) -> 'EntitiesBuilder':
        ''' bulk_type '''
        self.bulk_type = bulk_type
        return self

    def with_csv_data(self, csv_data: str) -> 'EntitiesBuilder':
        ''' csv_data '''
        self.csv_data = csv_data
        return self

    def bulk_provisioning(self) -> 'EntitiesBuilder':
        ''' bulk provisioning '''
        self.requires = {
            'organization_name': self.organization_name,
            'action': self.bulk_action,
            'type': self.bulk_type,
            'data': self.csv_data
        }
        self.method = 'bulk_provisioning'
        self.url = f'{self.client.url}/north/v80/provision/organizations/{self.organization_name}/bulk/async?action={self.bulk_action}&type={self.bulk_type}'
        return self

    def build(self) -> 'EntitiesBuilder':
        """ Check if any parameter is missing. """
        if self.requires is not None:
            for key, value in self.requires.items():
                assert value is not None, f'{key} is required'
        return self

    def execute(self) -> Union[int, List[Dict[str, Any]]]:
        """ Execute and return the responses """
        methods: Dict[str, Callable[[], Union[int, List[Dict[str, Any]]]]] = {
            'search': self._execute_searching,
            'bulk_provisioning': self._execute_bulk_provisioning
        }
        function = methods.get(self.method)
        if function is None:
            raise ValueError(f'Unsupported method: {self.method}')
        return function()

    def _execute_searching(self) -> Union[int, List[Dict[str, Any]]]:
        response = self._send_request()
        if response.status_code == 200:
            if self.format_data == 'csv':
                return response.text
            else:
                data = response.json()
                return self._format_data(data)

        else:
            error_message = response.json().get('message', 'Unknown error')
            error_code = response.status_code
            raise Exception(f"Error: Request failed with status code {error_code}. Message: {error_message}")
        return response

    def _execute_bulk_provisioning(self) -> Union[int, List[Dict[str, Any]]]:
        print(self.csv_data)
        response = requests.post(self.url, headers=self.headers, data=self.csv_data, verify=False, timeout=3000)
        return response

    def _send_request(self) -> requests.Response:
        return requests.post(self.url, headers=self.headers, json=self.filter, verify=False, timeout=3000)

    def _process_entity(self, entity_prefix: str, key_prefix: str, value_dict: Any, flat_entity: Dict[str, Any]) -> None:
        if isinstance(value_dict, list):
            for i, item in enumerate(value_dict):
                for sub_key, sub_value in item.items():
                    new_key = f'{entity_prefix}_{key_prefix}_{i}_{sub_key}'
                    self._assign_value(new_key, sub_value, flat_entity)
        else:
            for sub_key, sub_value in value_dict.items():
                new_key = f'{entity_prefix}_{key_prefix}_{sub_key}'
                self._assign_value(new_key, sub_value, flat_entity)

    def _assign_value(self, key: str, value: Any, flat_entity: Dict[str, Any]) -> None:
        if isinstance(value, dict) and '_current' in value:
            flat_entity[key] = value['_current']['value']
        else:
            flat_entity[key] = value

    def _format_data(self, data: List[Dict[str, Any]]) -> Union[str, List[Dict[str, Any]], pd.DataFrame]:
        if self.format_data == 'dict':
            return data
        elif self.format_data == 'pandas':
            entities_flattened = []
            for entity in data['entities']:
                entities_flattened.append(flatten(entity, reducer='underscore', enumerate_types=(list,)))
            return pd.DataFrame(entities_flattened)
        else:
            raise ValueError('Format not valid')
