"""  RulesSearchBuilder """

import requests
import os
import configparser
import json
import urllib3
import re
from dotenv import load_dotenv, set_key, dotenv_values
from typing import Any
from ..utils import validate_type, send_request, set_method_call

from requests import Response


class RulesSearchBuilder:
    """ Class rules builder"""

    def __init__(self, opengate_client):
        self.client = opengate_client
        self.headers = self.client.headers
        self.url: str | None = None
        self.body_data: dict = {}
        self.builder: bool = False
        self.method_calls: list = []

    def with_filter(self, body_data: dict) -> 'RulesSearchBuilder':
        """
        Filter Body

        Args:
            body_data (dict): The body data to filter.

        Returns:
            RulesSearchBuilder: Returns itself to allow for method chaining.
        """
        validate_type(format_data, dict, "Filter")
        self.body_data = body_data
        return self

    def with_body(self, body_data: dict) -> 'RulesSearchBuilder':
        """
        Filter Body

        Args:
            body_data (dict): The body data to filter.

        Returns:
            RulesSearchBuilder: Returns itself to allow for method chaining.
        """
        validate_type(body_data, dict, "Body")
        self.body_data = body_data
        return self

    @set_method_call
    def build(self) -> 'RulesSearchBuilder':
        """
        Finalizes the construction of the datapoints search configuration.

        This method prepares the builder to execute the collection by ensuring all necessary configurations are set and validates the overall integrity of the build. It should be called before executing the collection to ensure that the configuration is complete and valid.

        Returns:
            DataPointsSearchBuilder: Returns itself to allow for method chaining.

        Raises:
            ValueError: If required configurations are missing or if incompatible methods are used together.
        """
        self.builder = True
        self._validate_builds()

        if self.method_calls.count('build_execute') > 0:
            raise Exception("You cannot use build() together with build_execute()")

        return self

    def build_execute(self):
        """
        Executes the datapoints search immediately after building the configuration.

        This method is a shortcut that combines building and executing in a single step.

        Returns:
            dict: A dictionary containing the execution response which includes the status code and potentially other metadata about the execution.

        Raises:
            ValueError: If `build` has already been called on this builder instance.
        """
        if self.method_calls.count('build') > 0:
            raise ValueError("You cannot use build_execute() together with build()")

        if self.method_calls.count('execute') > 0:
            raise ValueError("You cannot use build_execute() together with execute()")

        self._validate_builds()
        return self.execute()

    def execute(self):
        """
        Executes the operations search based on the built configuration.

        Returns:
            dict: The response data.

        Raises:
            Exception: If the build() method was not called before execute().
        """
        if not self.builder or self.method_calls[-2] != 'build':
            raise Exception(
                "The build() function must be called and must be the last method invoked before execute")
        try:
            url = f'{self.client.url}/north/v80/rules/search'
            response = requests.post(url, headers=headers, json=self.body_data, verify=False, timeout=3000)
            if response.status_code == 200:
                return response
            else:
                return {'status_code': response.status_code, 'error': response.text}

        except ConnectionError as conn_err:
            return f'Connection error  {str(conn_err)}'

        except Timeout as timeout_err:
            return f'Timeout error  {str(timeout_err)}'

        except RequestException as req_err:
            return f'Request exception  {str(req_err)}'

        except Exception as e:
            return f'Unexpected error {str(e)}'

    def _validate_builds(self):
        if self.method_calls.count('with_filter') > 0 and self.method_calls.count('with_body') > 0:
            raise Exception("You cannot use with_filter() together with with_body()")
