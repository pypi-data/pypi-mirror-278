'''  AIModelsBuilder '''
import json
import os
import configparser
from configparser import ConfigParser

import requests
import urllib3
from dotenv import load_dotenv, set_key, dotenv_values
from typing import Any, Dict
from .ai import AIBaseBuilder
from requests import Response

from ..utils import validate_type, send_request, set_method_call


class AIModelsBuilder:
    """ Class ai Model builder """

    def __init__(self, opengate_client):
        self.client = opengate_client
        self.base_url: str = f'{self.client.url}/north/ai'
        self.organization_name: str | None = None
        self.identifier: str | None = None
        self.config_key: str | None = None
        self.data_env: str | None = None
        self.section: str | None = None
        self.config_file: str | None = None
        self.file_name: str | None = None
        self.full_file_path: str | None = None
        self.data_prediction: dict = {}
        self.output_file_path: str | None = None
        self.builder: bool = False
        self.method_calls: list = []
        self.url: str | None = None
        self.method: str | None = None
        self.method_calls: list = []


    @set_method_call
    def with_organization_name(self, organization_name: str) -> 'AIModelsBuilder':
        """
        Set organization name

        Args:
            organization_name (str): Organization name

        Example:
            builder.with_organization('organization_name')

        Returns:
            AIModelsBuilder: Returns itself to allow for method chaining.
        """
        validate_type(organization_name, str, "Organization")
        self.organization_name = organization_name
        return self

    @set_method_call
    def with_identifier(self, identifier: str) -> 'AIModelsBuilder':
        """
        Set identifier

        Args:
            identifier (str): Identifier model

        Raises:
            TypeError: If the provided identifier is not a string.

        Returns:
            AIModelsBuilder: Returns itself to allow for method chaining.
        """
        self.identifier = identifier
        return self

    def with_config_file(self, config_file: str, section: str, config_key: str) -> 'AIModelsBuilder':
        """
        Sets up the configuration file (.ini).

        This method allows specifying a configuration file, a section within that file, and a key to retrieve a specific value from the section.

        Args:
            config_file (str): The path to the.ini configuration file.
            section (str): The section name within the.ini file where the desired configuration is located.
            config_key (str): The key within the specified section whose value will be retrieved.

        Raises:
            TypeError: If the provided config_file is not a string.
            TypeError: If the provided section is not a string.
            TypeError: If the provided config_key is not a string.

        Example:
            Given a configuration file named `model_config.ini` with the following example content:

            [id]
            model_id = afe07216-14ec-4134-97ae-c483b11d965a

            builder.with_config_file('model_config.ini', 'id', 'model_id')

        Returns:
            AIModelsBuilder: Returns itself to allow for method chaining.
        """
        validate_type(config_file, str, "Config file")
        validate_type(section, str, "Section")
        validate_type(config_key, str, "Config Key")

        config = configparser.ConfigParser().read(config_file)
        self.identifier = config.get(self.section, self.config_key)
        return self

    @set_method_call
    def add_file(self, file: str) -> 'AIModelsBuilder':
        """
        Model file

        Args:
            file (str): The path to the file to be added.

        Raises:
            TypeError: If the provided file path is not a string.

        Example:
            builder.add_file('test.onnx')

        Returns:
            AIModelsBuilder: Returns itself to allow for method chaining.
        """

        validate_type(file, str, "File")

        self.file_name = os.path.basename(file)
        self.full_file_path = os.path.abspath(file)
        return self

    def with_prediction(self, data_prediction: dict) -> 'AIModelsBuilder':
        """
        Prediction with model

        Args:
            data_prediction (dict): Prediction

        Raises:
            TypeError: If the prediction is not a dict.

        Example:
            prediction = {
              "X": [
                {
                  "input_8": [
                    [
                      -0.5391107438074961,
                      -0.15950019784171535,
                    ]
                  ]
                }
              ]
            }
            builder.with_prediction(prediction)

        Returns:
            AIModelsBuilder: Returns itself to allow for method chaining.
        """

        validate_type(data_prediction, dict, "Data prediction")

        self.data_prediction = data_prediction
        return self

    def with_output_file_path(self, output_file_path: str) -> 'AIModelsBuilder':
        """
        Sets the output file path for the model.

        This method allows you to specify the path where the output file will be saved.
        It is particularly useful for operations that involve downloading or saving files.

        Args:
            output_file_path (str): The path where the output file will be saved.

        Example:
            builder.with_output_file_path("rute/prueba.onnx")

        Returns:
            AIModelsBuilder: The instance of the AIModelsBuilder class.
        """
        validate_type(output_file_path, str, "Output file path")

        self.output_file_path = output_file_path
        return self

    @set_method_call
    def create(self) -> 'AIModelsBuilder':
        """
        Initiates the creation process of a new model within the organization.

        This method prepares the AIModelsBuilder instance to create a new model by setting up the necessary parameters such as the organization name and the file to be associated with the model. It also specifies the URL endpoint for creating the model and sets the operation type to 'create'.


        Returns:
            AIModelsBuilder: The instance of the AIModelsBuilder class itself, allowing for method chaining.

        Example:
            builder.with_organization_name("MyOrganization").add_file("/path/to/model/file").create().build().execute()
        """
        self.url = f'{self.base_url}/{self.organization_name}/models'
        self.method = 'create'
        return self

    @set_method_call
    def find_one(self) -> 'AIModelsBuilder':
        identifier = self._get_identifier()
        self.url = f'{self.base_url}/{self.organization_name}/models/{identifier}'
        self.method = 'find'
        return self

    @set_method_call
    def find_all(self) -> 'AIModelsBuilder':
        self.url = f'{self.base_url}/{self.organization_name}/models'
        self.method = 'find'
        return self

    def update(self) -> 'AIModelsBuilder':
        identifier = self._get_identifier()
        self.url = f'{self.base_url}/{self.organization_name}/models/{identifier}'
        self.method = 'update'
        return self

    def delete(self) -> 'AIModelsBuilder':
        identifier = self._get_identifier()
        self.url = f'{self.base_url}/{self.organization_name}/models/{identifier}'
        self.method = 'delete'
        return self

    def validate(self) -> 'AIModelsBuilder':
        self.url = f'{self.base_url}/{self.organization_name}/models/validate'
        self.method = 'validate'
        return self

    def download(self) -> 'AIModelsBuilder':
        identifier = self._get_identifier()
        self.url = f'{self.base_url}/{self.organization_name}/models/{identifier}/file'
        self.method = 'download'
        return self

    def prediction(self) -> 'AIModelsBuilder':
        identifier = self._get_identifier()
        self.url = f'{self.base_url}/{self.organization_name}/models/{identifier}/prediction'
        self.method = 'prediction'
        return self

    def save(self) -> 'AIModelsBuilder':
        self.method = 'save'
        return self

    def set_config_file_identifier(self) -> 'AIModelsBuilder':
        self.method = 'set_config_file_identifier'
        return self

    def set_env_identifier(self) -> 'AIModelsBuilder':
        self.method = 'set_env_identifier'
        return self

    @set_method_call
    def build(self) -> 'AIModelsBuilder':
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

        self._validate_builds()
        return self.execute()

    def execute(self) -> requests.Response:
        """ Execute and return the responses """
        print("self.method_calls", self.method_calls)
        if not self.builder or self.method_calls[-1] != 'build':
            raise Exception(
                "The build() function must be called and must be the last method invoked before execute")

        methods = {
            'create': self._execute_create,
            'find': self._execute_find,
            'update': self._execute_update,
            'delete': self._execute_delete,
            'validate': self._execute_validate,
            'download': self._execute_download,
            'prediction': self._execute_prediction,
            'save': self._execute_save,
            'set_config_file_identifier': self._execute_set_identifier,
            'set_env_identifier': self._execute_env_identifier,
        }

        function = methods.get(self.method)
        if function is None:
            raise ValueError(f'Unsupported method: {self.method}')
        return function()

    def _execute_create(self) -> dict[str, Any]:
        files = self._get_file_data()
        payload = {}
        file_config = self._read_config_file()
        response = send_request('post', self.client.headers, self.url, payload, files)
        print(response)
        if response.status_code == 201:
            all_identifiers = self.find_all().build().execute().json()
            identifiers = [item['identifier'] for item in all_identifiers if item['name'] == self.file_name]
            if file_config:
                try:
                    self._read_config_file().get(self.section, self.config_key)
                    file_config.set(self.section, self.config_key, identifiers[0])
                    with open(self.config_file, 'w', encoding='utf-8') as configfile:
                        file_config.write(configfile)

                except configparser.NoOptionError:
                    raise Exception('The "model_id" parameter was not found in the configuration file.')
            elif self.data_env is not None:
                try:
                    env_vars = dotenv_values('.env')
                    if self.data_env not in env_vars:
                        raise Exception('The environment variable was not found in the .env file.')

                    set_key('.env', self.data_env, identifiers[0])

                except KeyError as error:
                    raise Exception('The environment variable was not found in the .env file.') from error

        else:
            return {'status_code': response.status_code, 'error': response.text}

    def _execute_find(self) -> requests.Response | dict[str, Any]:
        response = send_request('get', self.client.headers, self.url)
        if response.status_code == 200:
            return response
        else:
            return {'status_code': response.status_code, 'error': response.text}

    def _execute_update(self) -> dict[str, Any]:
        files = self._get_file_data()
        payload: dict[str, Any] = {}
        response = send_request('put', self.client.headers, self.url, payload, files)
        if response.status_code == 200:
            return {'status_code': response.status_code}
        else:
            return {'status_code': response.status_code, 'error': response.text}

    def _execute_delete(self) -> dict[str, Any]:
        response = send_request('delete', self.client.headers, self.url)
        if response.status_code == 200:
            return {'status_code': response.status_code}
        else:
            return {'status_code': response.status_code, 'error': response.text}

    def _execute_validate(self) -> dict[str, Any]:
        files = self._get_file_data()
        payload: dict[str, Any] = {}
        response = send_request('post', self.client.headers, self.url, payload, files)
        if response.status_code == 200:
            return {'status_code': response.status_code}
        else:
            return {'status_code': response.status_code, 'error': response.text}

    def _execute_download(self) -> dict[str, Any]:
        response = send_request('get', self.client.headers, self.url)
        if response.status_code == 200:
            with open(self.output_file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
        else:
            return {'status_code': response.status_code, 'error': response.text}

    def _execute_prediction(self) -> dict[str, Any] | dict[str, Any]:
        self.client.headers['Content-Type'] = 'application/json'
        payload = json.dumps(self.data_prediction)
        response = send_request('post', self.client.headers, self.url, payload)
        if response.status_code == 200:
            return {'status_code': response.status_code}
        else:
            return {'status_code': response.status_code, 'error': response.text}

    def _execute_save(self) -> Response | ValueError:
        if self.data_env is not None or self.config_file is not None:
            if self.data_env is not None:
                identifier = dotenv_values('.env')[self.data_env]
                self.identifier = identifier

            elif self.config_file is not None:
                config = configparser.ConfigParser()
                config.read(self.config_file)
                model_id = config.get(self.section, self.config_key, fallback=None)
                self.identifier = model_id

            response = self.find_one().build().execute()
            if response.status_code == 200:
                #Update
                return self.update().build().execute()

            # Create
            return self.create().build().execute()

        return ValueError('The "config file" or env parameter was not found')

    def _execute_set_identifier(self):
        try:
            file_config = self._read_config_file()
            self._read_config_file().get(self.section, self.config_key)
            file_config.set(self.section, self.config_key, self.identifier)
            with open(self.config_file, 'w', encoding='utf-8') as configfile:
                file_config.write(configfile)

        except configparser.NoOptionError as error:
            raise ValueError('The "model_id" parameter was not found in the configuration file.') from error

    def _execute_env_identifier(self):
        try:
            env_vars = dotenv_values('.env')
            if self.data_env not in env_vars:
                raise KeyError('The environment variable was not found in the .env file.')

            set_key('.env', self.data_env, self.identifier)

        except KeyError as error:
            raise ValueError('The environment variable was not found in the .env file.') from error

    def _read_config_file(self) -> ConfigParser | None:
        if self.config_file is not None:
            if os.path.exists(self.config_file):
                config = configparser.ConfigParser()
                config.read(self.config_file)
                return config
            raise ValueError('The configuration file does not exist.')
        return None

    def _get_file_data(self):
        with open(self.full_file_path, 'rb') as file:
            file_data = file.read()
        files = [('modelFile', (self.file_name, file_data, 'application/octet-stream'))]
        return files

    def _validate_builds(self):
        if self.method_calls.count('create') > 0:
            if "with_organization_name" not in self.method_calls and "add_file" not in self.method_calls:
                raise Exception(
                    "It is mandatory to use the with_organization_name() and add_file() methods in create()")

        if self.method_calls.count('find_one') > 0:
            if "with_organization_name" not in self.method_calls:
                raise Exception(
                    "It is mandatory to use the with_organization_name() method in find_one()")

        if self.method_calls.count('find_all') > 0:
            if "with_organization_name" not in self.method_calls:
                raise Exception("It is mandatory to use the with_organization_name() methods")

        return self
