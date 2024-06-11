"""SearchBuilder"""

import requests
from ..utils import validate_type, set_method_call
from requests import Response
import pandas as pd
from flatten_dict import flatten
from pandas import DataFrame
from typing import Any


class SearchBuilder:
    """ Search Builder """

    def __init__(self):
        self.body_data: dict = {}
        self.format_data: str | None = None
        self.flatten: bool = False
        self.utc: bool = False
        self.summary: bool = False
        self.default_sorted: bool = False
        self.case_sensitive: bool = False
        self.format_data_headers: dict[str, Any] = {}
        self.method_calls: list = []

    def with_filter(self, body_data: dict) -> 'SearchBuilder':
        """
        Filter Body

        Args:
            body_data (dict): The body data to filter.

        Returns:
            SearchBuilder: Returns itself to allow for method chaining.
        """
        validate_type(body_data, dict, "Filter")
        self.body_data = body_data
        return self

    def with_body(self, body_data: dict) -> 'SearchBuilder':
        """
        Filter Body

        Args:
            body_data (dict): The body data to filter.

        Returns:
            SearchBuilder: Returns itself to allow for method chaining.
        """
        validate_type(body_data, dict, "Body")
        self.body_data = body_data
        return self

    @set_method_call
    def with_format(self, format_data: str) -> 'SearchBuilder':
        """
        Formats the flat entities data based on the specified format ('csv', 'dict', or 'pandas').

        Args:
            format_data (str): The format to use for the data.

        Returns:
            SearchBuilder: Returns itself to allow for method chaining.
        """
        validate_type(format_data, str, "Format data")
        self.format_data = format_data
        if self.format_data == 'csv':
            self.format_data_headers = 'text/plain'
        else:
            self.format_data_headers = 'application/json'
        return self

    def with_flattened(self) -> 'SearchBuilder':
        """
        Flatten the data

        Returns:
            SearchBuilder: Returns itself to allow for method chaining.
        """
        self.flatten = True
        return self

    def with_utc(self) -> 'SearchBuilder':
        """
        Set UTC flag

        Returns:
            SearchBuilder: Returns itself to allow for method chaining.
        """
        self.utc = True
        return self

    def with_summary(self) -> 'SearchBuilder':
        """
        Set summary flag

        Returns:
            SearchBuilder: Returns itself to allow for method chaining.
        """
        self.summary = True
        return self

    def with_default_sorted(self) -> 'SearchBuilder':
        """
        Set default sorted flag

        Returns:
            SearchBuilder: Returns itself to allow for method chaining.
        """
        self.default_sorted = True
        return self

    def with_case_sensitive(self) -> 'SearchBuilder':
        """
        Set case-sensitive flag

        Returns:
            SearchBuilder: Returns itself to allow for method chaining.
        """
        self.case_sensitive = True
        return self

    def _send_request(self, type_search: str, headers: dict):
        """
        Send the search request to the server.

        Args:
            type_search (str): The type of search to perform.
            headers (Dict[str, Any]): The headers to send with the request.

        Returns:
            dict: A dictionary containing the execution response which includes the status code and potentially other metadata about the execution.

        Raises:
            Exception: If the build() method was not called before execute().
        """
        if not self.builder or self.method_calls[-2] != 'build':
            raise Exception(
                "The build() function must be called and must be the last method invoked before execute")

        try:
            headers['Accept'] = self.format_data_headers
            url = f'{self.client.url}/north/v80/search/{type_search}?flattened={self.flatten}&utc={self.utc}&summary={self.summary}&defaultSorted={self.default_sorted}&caseSensitive={self.case_sensitive}'
            response = requests.post(url, headers=headers, json=self.body_data, verify=False, timeout=3000)

            if response.status_code != 200:
                return {'status_code': response.status_code, 'error': response.text}

            if self.format_data in ['dict', None]:
                return response.json()

            if self.format_data == 'csv':
                return response.text

            if self.format_data == 'pandas':
                entities_flattened = []
                for entities in response.json()[type_search]:
                    entities_flattened.append(flatten(entities, reducer='underscore', enumerate_types=(list,)))
                return pd.DataFrame(entities_flattened)

            raise ValueError(f"Unsupported format: {self.format_data}")

        except ConnectionError as conn_err:
            return f'Connection error  {str(conn_err)}'
        except Timeout as timeout_err:
            return f'Timeout error  {str(timeout_err)}'
        except RequestException as req_err:
            return f'Request exception  {str(req_err)}'
        except Exception as e:
            return f'Unexpected error {str(e)}'
