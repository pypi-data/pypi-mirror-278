"""  DatasetsSearchBuilder """

import requests
import pandas as pd
from typing import Any
from ..utils import validate_type, set_method_call
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException


class DatasetsSearchBuilder:
    """ Dataset Builder """

    def __init__(self, opengate_client):
        self.client = opengate_client
        self.headers = self.client.headers
        self.organization_name: str | None = None
        self.identifier: str | None = None
        self.body_data: dict[str, Any] = {}
        self.format_data: str | None = None
        self.utc: bool = False
        self.builder: bool = False
        self.method_calls: list = []

    @set_method_call
    def with_organization_name(self, organization_name: str) -> 'DatasetsSearchBuilder':
        """
        Set organization name

        Args:
            organization_name (str):

        Returns:
            DatasetsSearchBuilder: Returns itself to allow for method chaining.
        """
        validate_type(organization_name, str, "Organization")
        self.organization_name = organization_name
        return self

    @set_method_call
    def with_identifier(self, identifier: str) -> 'DatasetsSearchBuilder':
        """
        Set identifier

        Returns:
            DatasetsSearchBuilder: Returns itself to allow for method chaining.
        """
        validate_type(identifier, str, "Identifier")
        self.identifier = identifier
        return self

    def with_utc(self) -> 'DatasetsSearchBuilder':
        """
        Set UTC

        Returns:
            DatasetsSearchBuilder: Returns itself to allow for method chaining.
        """
        self.utc = True
        return self

    def with_body(self, body_data: dict[str, Any]) -> 'DatasetsSearchBuilder':
        """ Sets the body data """
        validate_type(body_data, dict, "With Body")
        self.body_data = body_data
        return self

    @set_method_call
    def with_format(self, format_data: str) -> 'DatasetsSearchBuilder':
        """
        Formats the flat entities data based on the specified format ('csv', 'dict', or 'pandas').

        Args:
            format_data (str): The format to use for the data.

        Returns:
            DatasetsSearchBuilder: Returns itself to allow for method chaining.
        """
        validate_type(format_data, str, "Format data")
        self.format_data = format_data
        if self.format_data == 'csv':
            self.headers['Accept'] = 'text/plain'
        else:
            self.headers['Accept'] = 'application/json'
        return self

    @set_method_call
    def build(self) -> 'DatasetsSearchBuilder':
        """
        Finalizes the construction of the operations search configuration.

        This method prepares the builder to execute the collection by ensuring all necessary configurations are set and validates the overall integrity of the build. It should be called before executing the collection to ensure that the configuration is complete and valid.

        The build process involves checking that mandatory fields such as the device identifier are set. It also ensures that method calls that are incompatible with each other (like `build` and `build_execute`) are not both used.

        Example:
            builder.build()

        Returns:
            OperationsSearchBuilder: Returns itself to allow for method chaining, enabling further actions like `execute`.

        Raises:
            ValueError: If required configurations are missing or if incompatible methods are used together.

        Note:
            This method should be used as a final step before `execute` to prepare the operations search configuration. It does not modify the state but ensures that the builder's state is ready for execution.
        """
        self.builder = True
        self._validate_builds()

        if self.method_calls.count('build_execute') > 0:
            raise Exception("You cannot use build() together with build_execute()")

        return self

    @set_method_call
    def build_execute(self):
        """
        Executes the data sets search immediately after building the configuration.

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

    def _validate_builds(self):
        if self.method_calls.count('with_format') > 1:
            raise Exception("You cannot use more than one with_format() method")

        if "with_organization_name" not in self.method_calls and "with_identifier" not in self.method_calls:
            raise Exception("It is mandatory to use the with_organization_name() and with_identifier() methods")

        return self

    def execute(self):
        url = f'{self.client.url}/north/v80/datasets/provision/organizations/{self.organization_name}/{self.identifier}/data?utc={self.utc}'
        response = requests.post(url, headers=self.client.headers, json=self.body_data, verify=False, timeout=3000)
        data = response.json()

        try:
            if response.status_code != 200:
                result = {'status_code': response.status_code}
                if response.text:
                    result['error'] = response.text
                return result

            if self.format_data == 'csv':
                return response.text

            if self.format_data in ['dict', None]:
                dict_data = []
                for fila in data['data']:
                    fila_dict = {data['columns'][i]: fila[i] for i in range(len(data['columns']))}
                    dict_data.append(fila_dict)
                return dict_data

            elif self.format_data == 'pandas':
                data_frame = pd.DataFrame(data['data'], columns=data['columns'])
                return data_frame
            raise ValueError(f"Unsupported format: {self.format_data}")

        except ConnectionError as conn_err:
            return f'Connection error  {str(conn_err)}'
        except Timeout as timeout_err:
            return f'Timeout error  {str(timeout_err)}'
        except RequestException as req_err:
            return f'Request exception  {str(req_err)}'
        except Exception as e:
            return f'Unexpected error {str(e)}'



