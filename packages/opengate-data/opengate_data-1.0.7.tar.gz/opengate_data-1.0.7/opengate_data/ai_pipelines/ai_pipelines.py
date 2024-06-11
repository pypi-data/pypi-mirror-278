"""  AIPipelinesBuilder """

import requests
from requests import Response
import os
import configparser
import json
import urllib3
import re
from dotenv import load_dotenv, dotenv_values, set_key
from typing import Any
from ..utils import validate_type, send_request, set_method_call, handle_basic_response


class AIPipelinesBuilder:
    """ Builder pipelines """

    def __init__(self, opengate_client):
        self.client: str = opengate_client
        self.builder: bool = False
        self.base_url: str = f'{self.client.url}/north/ai'
        self.organization_name: str | None = None
        self.identifier = None
        self.config_file: str | None = None
        self.section: str | None = None
        self.config_key: str | None = None
        self.new_file: str | None = None
        self.data_prediction: dict = {}
        self.url: str | None = None
        self.requires: Dict[str, Any] = None
        self.method: str | None = None
        self.name: str | None = None
        self.output_file_path: str | None = None
        self.collect = None
        self.action = None
        self.type = None
        self.actions = []
        self.data_env: str | None = None
        self.method_calls: list = []
        self.find_name: str | None = None

    def with_organization_name(self, organization_name: str) -> 'AIPipelinesBuilder':
        """
        Specify the organization name.

        Args:
            organization_name (str): The name of the organization.

        Returns:
            AIModelsBuilder: Returns self for chaining.
        """
        validate_type(organization_name, str, "Organization Name")
        self.organization_name = organization_name
        return self

    def with_identifier(self, identifier: str) -> 'AIPipelinesBuilder':
        """
         Specify the identifier for the pipeline.

         Args:
             identifier (str): The identifier for the pipeline.

         Returns:
             AIModelsBuilder: Returns self for chaining.
         """
        validate_type(identifier, str, "Identifier")
        self.identifier = identifier
        return self

    def with_env(self, data_env: str) -> 'AIPipelinesBuilder':
        """
        Specify the environment variable.

        Args:
            data_env (str): The environment variable.

        Returns:
            AIModelsBuilder: Returns self for chaining.
        """
        validate_type(data_env, str, "Data env")
        self.data_env = data_env
        return self

    @set_method_call
    def with_find_by_name(self, find_name: str) -> 'AIPipelinesBuilder':
        """
        Specify the name to find.

        Args:
            find_name (str): The name of the pipeline.

        Returns:
            AIPipelinesBuilder: Returns self for chaining.
        """
        validate_type(find_name, str, "Find Name")
        self.find_name = find_name
        return self

    def with_config_file(self, config_file: str, section: str, config_key: str) -> 'AIPipelinesBuilder':
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
            pipeline_id = afe07216-14ec-4134-97ae-c483b11d965a

            builder.with_config_file('model_config.ini', 'id', 'pipeline_id')

        Returns:
            AIPipelinesBuilder: Returns itself to allow for method chaining.
        """
        validate_type(config_file, str, "Config file")
        validate_type(section, str, "Section")
        validate_type(config_key, str, "Config Key")

        self.config_file = config_file
        self.section = section
        self.config_key = config_key

        config = configparser.ConfigParser()
        config.read(config_file)
        self.identifier = config.get(section, config_key)
        return self

    def with_prediction(self, data_prediction: dict) -> 'AIPipelinesBuilder':
        """
        Prediction with model

        Args:
            data_prediction (dict): Prediction

        Raises:
            TypeError: If the prediction is not a dict.

        Example:
            {
              "input": {},
              "collect": {
                "deviceId": "123456",
                "datastream": "PredictionDatastream"
              }
            }
            builder.with_prediction(prediction)

        Returns:
            AIPipelinesBuilder: Returns itself to allow for method chaining.
        """
        validate_type(data_prediction, dict, "Data prediction")
        self.data_prediction = data_prediction
        return self

    def with_name(self, name: str) -> 'AIPipelinesBuilder':
        """
        Name new pipeline

        Args:
            name (str): Name new pipeline

        Raises:
            TypeError: If the name is not a string.

        Example:
            builder.with_name(name_prediction)

        Returns:
            AIPipelinesBuilder: Returns itself to allow for method chaining.
        """

        validate_type(name, str, "Name")
        self.name = name
        return self

    def with_actions(self, actions: list[dict[str, any]]) -> 'AIPipelinesBuilder':
        """
        Set actions for the pipeline.

        Args:
            actions (list[dict[str, any]]): A list of dictionaries where each dictionary represents an action with string keys.

        Raises:
            TypeError: If actions is not a list of dictionaries with string keys.

        Example:
            builder.with_actions([{"action1": "value1"}, {"action2": "value2"}])

        Returns:
            AIPipelinesBuilder: Returns itself to allow for method chaining.
        """

        validate_type(actions, list, "Actions")

        for action in actions:
            validate_type(action, dict, "Each action in Actions")
            for key in action:
                validate_type(key, str, "Each key in the dictionaries of Actions")

        self.actions = actions
        return self

    def add_action(self, file_name: str, type_action: str | None) -> 'AIPipelinesBuilder':
        """
        Add action name and type of model or transform exist.

        Args:
            file_name (str): The name of the file representing the action.
            type_action (str | None): The type of the action, either 'MODEL' or 'TRANSFORMER'. If None, it will be inferred from the file extension.

        Raises:
            TypeError: If file_name is not a string.
            TypeError: If type_action is not a string or None.

        Example:
            builder.add_action('transform.py', 'TRANSFORMER')

        Returns:
            AIPipelinesBuilder: Returns itself to allow for method chaining.
        """

        validate_type(file_name, str, "File Name")
        validate_type(type_action, (str, type(None)), "Type action")

        if os.path.dirname(file_name):
            file_name = os.path.basename(file_name)

        _, file_extension = os.path.splitext(file_name)
        if file_extension == '.py':
            default_type = 'TRANSFORMER'
        else:
            default_type = 'MODEL'

        action_type = type_action if type_action is not None else default_type

        action = {
            'name': file_name,
            'type': action_type
        }
        self.actions.append(action)

        return self

    @set_method_call
    def build(self) -> 'AIPipelinesBuilder':
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

    def create(self) -> 'AIPipelinesBuilder':
        """
        Creates a new pipeline.

        This method prepares the request to create a new pipeline using the specified configuration in the object. It is necessary to define the name (`with_name`) and actions (`with_actions`) before calling this method.

        Example:
            builder.with_name('MyPipeline').with_actions([{'action1': 'value1'}, {'action2': 'value2'}]).create()

        Returns:
            AIPipelinesBuilder: Returns the same object to allow method chaining.

        """
        self.url = f'{self.base_url}/{self.organization_name}/pipelines'
        self.method = 'create'
        return self

    def find_all(self) -> 'AIPipelinesBuilder':
        """
        Retrieves all available pipelines.

        Example:
            builder.with_organization_name('MyOrganization').find_all()

        Returns:
            AIPipelinesBuilder: Returns the same object to allow method chaining.
        """
        self.requires = {
            'organization': self.organization_name
        }
        self.url = f'{self.base_url}/{self.organization_name}/pipelines'
        self.method = 'find'
        return self

    def find_one(self) -> 'AIPipelinesBuilder':
        """
        Finds a specific pipeline by its identifier.

        This method prepares the request to find a specific pipeline based on its identifier. The identifier is obtained automatically if not explicitly defined or can be obtained from a configuration file or environment variables.

        Example:
            builder.with_organization_name('my_organization').with_identifier('identifier').find_one()

        Returns:
            AIPipelinesBuilder: Returns the same object to allow method chaining.

        """
        identifier = self._get_identifier()
        self.url = f'{self.base_url}/{self.organization_name}/pipelines/{identifier}'
        self.method = 'find'
        return self

    def update(self) -> 'AIPipelinesBuilder':
        """
        Updates an existing pipeline.

        This method prepares the request to update an existing pipeline. It is necessary to define the organization's name (`with_organization_name`) and the pipeline's name (`with_name`) before calling this method.

        Example:
            builder.with_organization_name('MyOrganization').with_identifier("pipeline_identifier").with_name('MyPipeline').update()
            builder.with_organization_name('MyOrganization').with_find_by_name("pipeline_name").with_config_file('model_config.ini', 'id', 'model').with_name('MyPipeline').update()
            builder.with_organization_name('MyOrganization').with_name('MyPipeline').update()

        Returns:
            AIPipelinesBuilder: Returns the same object to allow method chaining.
        """

        identifier = self._get_identifier()
        self.url = f'{self.base_url}/{self.organization_name}/pipelines/{identifier}'
        self.method = 'update'
        return self

    def delete(self) -> 'AIPipelinesBuilder':
        """
        Deletes an existing pipeline.

        This method prepares the request to delete an existing pipeline. It is necessary to define the organization's name (`with_organization_name`) and the pipeline's identifier (`with_identifier`) before calling this method.

        Example:
            builder.with_organization_name('MyOrganization').with_identifier('pipeline_identifier').delete()

        Returns:
            AIPipelinesBuilder: Returns the same object to allow method chaining.
        """
        identifier = self._get_identifier()
        self.url = f'{self.base_url}/{self.organization_name}/pipelines/{identifier}'
        self.method = 'delete'
        return self

    def prediction(self) -> 'AIPipelinesBuilder':
        """
        Performs a prediction with a model.

        This method prepares the request to perform a prediction using the model associated with the specified pipeline. It is necessary to define the organization's name (`with_organization_name`), the pipeline's identifier (`with_identifier`), and provide prediction data (`with_prediction`) before calling this method.

        Example:
            builder.with_organization_name('MyOrganization').with_identifier('pipeline_identifier').with_prediction({'input': {}, 'collect': {'deviceId': '123456', 'datastream': 'PredictionDatastream'}}).prediction()

        Returns:
            AIPipelinesBuilder: Returns the same object to allow method chaining.
        """
        identifier = self._get_identifier()
        self.url = f'{self.base_url}/{self.organization_name}/pipelines/{identifier}/prediction'
        self.method = 'prediction'
        return self

    def save(self) -> 'AIPipelinesBuilder':
        """
        Save the model configuration.

        This method sets up the AIPipelinesBuilder instance to save the configuration of a model associated with the specified organization. It configures the URL endpoint for the save operation and sets the operation type to 'save'.

        Example:
            builder.with_organization_name("MyOrganization").with_env("MODEL_ENV_VAR").save().build().execute()
            builder.with_organization_name("MyOrganization").with_config_file('model_config.ini', 'id', 'model').save().build().execute()

        Returns:
            AIPipelinesBuilder: The instance of the AIModelsBuilder class itself, allowing for method chaining.
        """
        self.method = 'save'
        return self

    def set_config_file_identifier(self) -> 'AIPipelinesBuilder':
        """
        Set the model identifier from a configuration file.

        This method sets up the AIModelsBuilder instance to retrieve the model identifier from a specified configuration file. It reads the identifier from the given section and key within the configuration file and sets it for the builder instance.

        Example:
            builder.with_config_file('model_config.ini', 'id', 'model_id').set_config_file_identifier().build().execute()

        Returns:
            AIPipelinesBuilder: The instance of the AIModelsBuilder class itself, allowing for method chaining.
        """
        self.method = 'set_config_identifier'
        return self

    def set_env_identifier(self) -> 'AIPipelinesBuilder':
        """
        Set the model identifier from an environment variable.

        This method sets up the AIModelsBuilder instance to retrieve the model identifier from a specified environment variable. It reads the identifier from the environment variable and sets it for the builder instance.

        Example:
            builder.with_env("MODEL_ENV_VAR").set_env_identifier().build().execute()

        Returns:
            AIPipelinesBuilder: The instance of the AIModelsBuilder class itself, allowing for method chaining.
        """
        self.method = 'set_env_identifier'
        return self

    @set_method_call
    def build(self) -> 'AIPipelinesBuilder':
        """
         Finalizes the construction of the IoT collection configuration.

         This method prepares the builder to execute the collection by ensuring all necessary configurations are set and validates the overall integrity of the build. It should be called before executing the collection to ensure that the configuration is complete and valid.

         The build process involves checking that mandatory fields such as the device identifier are set. It also ensures that method calls that are incompatible with each other (like `build` and `build_execute`) are not both used.

         Example:
             builder.build()

         Returns:
             AIPipelinesBuilder: Returns itself to allow for method chaining, enabling further actions like `execute`.

         Raises:
             ValueError: If required configurations are missing or if incompatible methods are used together.

         Note:
             This method should be used as a final step before `execute` to prepare the IoT collection configuration. It does not modify the state but ensures that the builder's state is ready for execution.
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

        self._validate_builds()
        return self.execute()

    def execute(self):
        """
         Execute the configured operation and return the response.

         This method executes the operation that has been configured using the builder pattern. It ensures that the `build` method has been called and that it is the last method invoked before `execute`. Depending on the configured method (e.g., create, find, update, delete), it calls the appropriate internal execution method.

         Returns:
             requests.Response: The response object from the executed request.

         Raises:
             Exception: If the `build` method has not been called or if it is not the last method invoked before `execute`.
             ValueError: If the configured method is unsupported.
         """
        methods = {
            'create': self._execute_create,
            'find': self._execute_find,
            'update': self._execute_update,
            'delete': self._execute_delete,
            'prediction': self._execute_prediction,
            'save': self._execute_save,
            'set_config_identifier': self._execute_set_identifier,
            'set_env_identifier': self._execute_env_identifier,
        }

        function = methods.get(self.method)
        if function is None:
            raise ValueError(f'Unsupported method: {self.method}')
        return function()

    def _execute_create(self):
        name = self.name
        actions = self.actions

        if not name:
            raise ValueError('The "with_name" is required.')

        if not actions:
            raise ValueError('The "add_action is required.')

        data = {
            "name": name,
            "actions": actions
        }
        response = send_request('post', self.client.headers, self.url, data)
        if response.status_code != 201:
            raise ValueError(response.text)

        if response.status_code == 201:
            file_config = self._read_config_file()
            all_identifiers = self.find_all().build().execute().json()
            for item in all_identifiers:
                if item['name'] == name:
                    result = item['identifier']
                    break

            if file_config:
                try:
                    # file_config.get(self.section, self.config_key)
                    file_config.set(self.section, self.config_key, result)
                    with open(self.config_file, 'w', encoding='utf-8') as configfile:
                        file_config.write(configfile)

                except configparser.NoOptionError as error:
                    raise ValueError('The "pipeline_id" parameter was not found in the configuration file.') from error

            elif self.data_env is not None:
                try:
                    env_vars = dotenv_values('.env')
                    if self.data_env not in env_vars:
                        raise KeyError('The environment variable was not found in the .env file.')

                    set_key('.env', self.data_env, result)

                except KeyError as error:
                    raise ValueError('The environment variable was not found in the .env file.') from error

        else:
            return {'status_code': response.status_code, 'error': response.text}

    def _execute_find(self) -> requests.Response | dict[str, Any]:
        response = send_request('get', self.client.headers, self.url)
        if response.status_code == 200:
            return response
        else:
            return {'status_code': response.status_code, 'error': response.text}

    def _execute_update(self):
        name = self.name
        actions = self.actions

        data = {
            "name": name,
            "actions": actions
        }
        response = send_request('put', self.client.headers, self.url, data)
        return handle_basic_response(response)

    def _execute_delete(self):
        response = send_request('delete', self.client.headers, self.url)
        return handle_basic_response(response)

    def _execute_prediction(self):
        self.client.headers['Content-Type'] = 'application/json'
        response = send_request('post', self.client.headers, self.url, self.data_prediction)
        return handle_basic_response(response)

    def _execute_save(self) -> Response | ValueError:
        if self.data_env is not None or self.config_file is not None:
            if self.data_env is not None:
                identifier = dotenv_values('.env')[self.data_env]
                self.identifier = identifier

            elif self.config_file is not None:
                config = configparser.ConfigParser()
                config.read(self.config_file)
                pipeline_id = config.get(self.section, self.config_key, fallback=None)
                self.identifier = pipeline_id

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
            return None

        except configparser.NoOptionError:
            return ValueError('The "pipeline_id" parameter was not found in the configuration file.')

    def _execute_env_identifier(self) -> None:
        try:
            env_vars = dotenv_values('.env')
            if self.data_env not in env_vars:
                raise KeyError('The environment variable was not found in the .env file.')

            set_key('.env', self.data_env, self.identifier)

        except KeyError as error:
            raise ValueError('The environment variable was not found in the .env file.') from error

    def _read_config_file(self):
        if self.config_file is not None:
            if os.path.exists(self.config_file):
                config = configparser.ConfigParser()
                config.read(self.config_file)
                return config
            raise ValueError('The configuration file does not exist.')
        return None

    def _validate_builds(self):
        if self.method_calls.count('create') > 0:
            if "with_organization_name" not in self.method_calls and "with_name" not in self.method_calls and "with_actions" not in self.method_calls:
                raise Exception(
                    "It is mandatory to use the with_organization_name() and with_name() with_actions() methods in create()")

        if self.method_calls.count('find_one') > 0:
            if "with_organization_name" not in self.method_calls:
                raise Exception(
                    "It is mandatory to use the with_organization_name() method in find_one()")

        if self.method_calls.count('find_all') > 0:
            if "with_organization_name" not in self.method_calls:
                raise Exception("It is mandatory to use the with_organization_name() methods")

        if self.method_calls.count('update') > 0:
            if "with_organization_name" not in self.method_calls and "with_name" not in self.method_calls:
                raise Exception(
                    "It is mandatory to use the with_organization_name() and with_name() method in update()")

        if self.method_calls.count('delete') > 0:
            if "with_organization_name" not in self.method_calls:
                raise Exception("It is mandatory to use the with_organization_name()")

        if self.method_calls.count('prediction') > 0:
            if "with_organization_name" not in self.method_calls and "with_prediction" not in self.method_calls:
                raise Exception(
                    "It is mandatory to use the with_organization_name() and with_output_file_path () methods in download()")

        if self.method_calls.count('save') > 0:
            if "with_organization_name" not in self.method_calls:
                raise Exception("It is mandatory to use the with_organization_name() method in update()")

        if self.method_calls.count('set_config_file_identifier') > 0:
            if "with_config_file" not in self.method_calls:
                raise Exception("It is mandatory to use the with_config_file() method in set_config_file_identifier()")

        if self.method_calls.count('set_env_identifier') > 0:
            if "with_env" not in self.method_calls:
                raise Exception("It is mandatory to use the with_env() method in set_env_identifier()")

        return self

    def _get_identifier(self) -> str:
        if self.identifier is not None:
            return self.identifier

        if self.data_env is not None:
            config = dotenv_values()
            identifier = config.get(self.data_env)
            if identifier is None:
                raise KeyError(f'The parameter "{self.data_env}" was not found in the configuration env')
            return identifier

        if self.config_file is not None and self.section is not None and self.config_key is not None:
            config = configparser.ConfigParser()
            config.read(self.config_file)
            try:
                return config.get(self.section, self.config_key)
            except (configparser.NoOptionError, configparser.NoSectionError) as e:
                raise ValueError(f'The "{self.config_key}" parameter was not found in the configuration file: {e}')

        if self.find_name is not None:
            response = self.find_all().build().execute()
            all_identifiers = parse_json(response)
            name_identifier = [item['identifier'] for item in all_identifiers if item['name'] == self.find_name]

            if not name_identifier:
                raise Exception(f'File name "{self.find_name}" does not exist')

            return name_identifier[0]

        raise ValueError('A configuration file with identifier, config file, or a find by name is required.')
