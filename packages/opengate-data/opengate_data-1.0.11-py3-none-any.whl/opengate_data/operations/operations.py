'''  OperationsBuilder '''

import requests
from typing import Callable, Union, List, Dict, Any
import pandas as pd
from requests import Response
from ..searching.search import SearchBuilder
from ..utils import validate_type, set_method_call


class OperationsBuilder(SearchBuilder):
    def __init__(self, opengate_client):
        super().__init__()
        self.client = opengate_client
        self.default_sorted = False
        self.body_data = {}
        self.format_data = None
        self.method = None
        self.requires = {}
        self.method_calls: list = []

        self.headers = self.client.headers

    @set_method_call
    def build(self) -> 'OperationsBuilder':
        """ Check if any parameter is missing. """
        if self.requires is not None:
            for key, value in self.requires.items():
                assert value is not None, f'{key} is required'
        return self

    @set_method_call
    def build_execute(self):
        """ build_execute """
        if self.method_calls.count('build') > 0:
            raise ValueError("You cannot use build_execute() together with build()")
        self._validate_builds()
        return self.execute()

    def execute(self):
        self.headers.update(self.format_data_headers)
        url = f'{self.client.url}/north/v80/search/entities/operations/history?flattened={self.flatten}&utc={self.utc}&summary={self.summary}&defaultSorted={self.default_sorted}&caseSensitive={self.case_sensitive}'
        response = requests.post(url, headers=self.headers, json=self.body_data, verify=False, timeout=3000)
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

    def _format_data(self, data: List[Dict[str, Any]]) -> Union[str, List[Dict[str, Any]], pd.DataFrame]:
        if self.format_data == 'dict':
            return data
        elif self.format_data == 'pandas':
            # Ver como manda las operaciones en formato pandas!!!
            return pd.DataFrame(data)
        else:
            raise ValueError('Format not valid')
