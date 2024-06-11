"""  RulesBuilder """

import requests
import os
import configparser
import json
import urllib3
import re
from dotenv import load_dotenv, set_key, dotenv_values
from typing import Any, Dict
from ..utils import validate_type, send_request, set_method_call, handle_basic_response, parse_json
from requests import Response


def _convert_to_one_line(input_code: str) -> str:
    """ Convert a multi-line code into a single line """
    comments: List[str] = re.findall(r'\/\/.*|\/\*[\s\S]*?\*\/', input_code)
    input_code: str = re.sub(r'\/\/.*', '', input_code)
    input_code: str = re.sub(r'\/\*[\s\S]*?\*\/', '', input_code)
    one_line_code: str = re.sub(r'\n', ' ', input_code)
    one_line_code: str = re.sub(r'\s+', ' ', one_line_code)
    one_line_code: str = one_line_code.strip()

    for comment in comments:
        one_line_code = one_line_code.replace(' ', comment, 1)
    return one_line_code


class RulesBuilder:
    """ Class rules builder"""

    def __init__(self, opengate_client):
        self.client = opengate_client
        self.rule_data: dict[str, Any] = {}
        self.method: str | None = None
        self.url: str | None = None
        self.body_data: dict[str, Any] = {}
        self.requires: dict[str, Any] = {}
        self.config_file: str | None = None
        self.section: str | None = None
        self.config_key: str | None = None
        self.find_name: str | None = None
        self.data_env: str | None = None
        self.builder: str | None = None
        self.method_calls: list = []

    @set_method_call
    def with_organization_name(self, organization_name: str) -> 'RulesBuilder':
        """
        Specify the organization name.

        Args:
            organization_name (str): The name of the organization.


        Example:
            builder.with_organization_name('organization_name')

        Returns:
            RulesBuilder: Returns self for chaining.
        """
        validate_type(organization_name, str, "Organization")
        self.rule_data['organization'] = organization_name
        return self

    @set_method_call
    def with_identifier(self, identifier: str) -> 'RulesBuilder':
        """
         Specify the identifier for the rule.

         Args:
             identifier (str): The identifier for the rules.

        Example:
            builder.with_identifier('identifier')

         Returns:
             RulesBuilder: Returns self for chaining.
         """
        validate_type(identifier, str, "Identifier")
        self.rule_data['identifier'] = identifier
        return self

    @set_method_call
    def with_actions(self, actions: dict[str, Any]) -> 'RulesBuilder':
        """
        Specify the actions in rules.

        Args:
            actions (dict): Actions

        Example:
            rule = {
                "actions": {
                    "close": [
                        {
                            "enabled": False,
                            "ruleToClose": "rule_name",
                            "alarmToClose": "alarmToClose"
                        }
                    ]
                }
            }
            with_actions = rule["actions"]
            builder.with_actions(with_actions)
        Returns:
            RulesBuilder: Returns self for chaining.
        """

        validate_type(actions, dict, "Actions")
        self.rule_data['actions'] = actions
        return self

    @set_method_call
    def with_actions_delay(self, actions_delay: int) -> 'RulesBuilder':
        """
        Waiting threshold before actions are executed. Allows cancellation of the execution of actions if another rule exists with a subsequent delay cancellation action.

        Args:
            actions_delay (int): Delay option in milliseconds

        Example:
            builder.with_actions(1000)

        Returns:
            RulesBuilder: Returns self for chaining.
        """
        validate_type(actions_delay, int, "Actions delay")
        self.rule_data['actionsDelay'] = actions_delay
        return self

    @set_method_call
    def with_active(self, active: bool) -> 'RulesBuilder':
        """
        Specify the active in rules.

        Args:
            active (bool): Activate or deactivate action

        Example:
            builder.with_active(False)

        Returns:
            RulesBuilder: Returns self for chaining.
        """
        validate_type(active, bool, "Active")
        self.rule_data['active'] = active
        return self

    @set_method_call
    def with_channel(self, channel: str) -> 'RulesBuilder':
        """
        Specify the channel in rules.

        Args:
            channel (str): Channel

        Example:
            builder.with_channel('default_channel')

        Returns:
            RulesBuilder: Returns self for chaining.
        """
        validate_type(channel, str, "Channel")
        self.rule_data['channel'] = channel
        return self

    @set_method_call
    def with_condition(self, condition: dict[str, Any]) -> 'RulesBuilder':
        """
        Specify the condition for the rule.

        Args:
            condition (dict): Specify the identifier for the rule.

        Example:
            condition = "filter": {
                "eq": {
                    "device.cpu.usage._current.value": "$datastream:device.cpu.usage._current.value"
                }
            }
            builder.with_condition('default_channel')

        Returns:
            RulesBuilder: Returns self for chaining.
        """

        validate_type(condition, dict, "Condition")
        self.rule_data['condition'] = condition
        return self

    @set_method_call
    def with_mode(self, mode: str) -> 'RulesBuilder':
        """
        Specify rule type mode

         Args:
             mode (str): Advanced or basic.

        Example:
            builder.with_mode('EASY')
            builder.with_mode('ADVANCED')

         Returns:
             RulesBuilder: Returns self for chaining.
         """
        validate_type(mode, str, "Mode")
        if mode in {"EASY", "ADVANCED"}:
            self.rule_data['mode'] = mode
        else:
            raise Exception('It is necessary to introduce a type of rule "EASY" or "ADVANCED"')

        return self

    @set_method_call
    def with_name(self, name: str) -> 'RulesBuilder':
        """
         Specify the name for the rule.

         Args:
             name (str): The identifier for the rules.

        Example:
            builder.with_mode('EASY')
            builder.with_mode('ADVANCED')

         Returns:
             RulesBuilder: Returns self for chaining.
         """
        validate_type(name, str, "Name")
        self.rule_data['name'] = name
        return self

    @set_method_call
    def with_description(self, description: str) -> 'RulesBuilder':
        """
        Specify the description.

        Args:
            description (str): The description for the rules.

        Example:
            builder.with_organization_name('organization_name')

        Returns:
            RulesBuilder: Returns self for chaining.
        """
        validate_type(description, str, "Description")
        self.rule_data['description'] = description
        return self

    @set_method_call
    def with_type(self, rule_type: dict[str, Any]) -> 'RulesBuilder':
        """
        Specify the description.

        Args:
            rule_type (dict): The description for the rules.

        Example:
            "rule": {
                "type": {
                    "datastreams": [
                        {
                            "name": "device.cpu.usage",
                            "fields": [
                                {
                                    "field": "value",
                                    "alias": "CPU usage"
                                }
                            ],
                            "prefilter": False
                        }
                    ],
                    "name": "DATASTREAM"
                }
            }
            type = rule["type"]
            builder.with_type(type)

        Returns:
            RulesBuilder: Returns self for chaining.
        """
        validate_type(rule_type, dict, "Type")
        self.rule_data['type'] = rule_type
        return self

    @set_method_call
    def with_parameters(self, parameters: list[dict[str, str]]) -> 'RulesBuilder':
        """
        Specify the parameters for rules.

        Args:
            parameters (dict): The parameters for the rules.

        Example:
            parameters = [
                {
                    "name": "name",
                    "schema": "string",
                    "value": "2"
                }
            ]
            builder.with_parameters(parameters).\

        Returns:
            RulesBuilder: Returns self for chaining.
        """
        validate_type(parameters, list, "Parameters")
        self.rule_data['parameters'] = parameters
        return self

    @set_method_call
    def with_code(self, code: str) -> 'RulesBuilder':
        """
        Specify the JavaScript code for advanced rules.

        Args:
            code (str): The JavaScript code to be used in the rule.

        Example:
            builder.with_mode('ADVANCED')
            builder.with_code('function execute() { return true; }')

        Returns:
            RulesBuilder: Returns self for chaining.

        Raises:
            Exception: If the mode is not set to 'ADVANCED'.
        """
        validate_type(code, str, "Code")
        if self.rule_data['mode'] is not None and self.rule_data['mode'] == "ADVANCED":
            self.rule_data['javascript'] = _convert_to_one_line(code)
        else:
            raise Exception('It is necessary to introduce a mode of rule and that it be advanced')
        return self

    @set_method_call
    def with_code_file(self, code_file: str) -> 'RulesBuilder':
        """
        Specify the JavaScript code for advanced rules from a file.

        This method reads the JavaScript code from a specified file and converts it into a single line to be used in the rule.

        Args:
            code_file (str): The path to the file containing the JavaScript code.

        Example:
            builder.with_mode('ADVANCED')
            builder.with_code_file('path/to/code.js')

        Returns:
            RulesBuilder: Returns self for chaining.

        Raises:
            ValueError: If the file does not exist or is not a valid file.
            ValueError: If the mode is not set to 'ADVANCED'.
        """
        validate_type(code_file, str, "Code File")
        if self.rule_data['mode'] is not None and self.rule_data['mode'] == "ADVANCED":
            if os.path.exists(code_file):
                if os.path.isfile(code_file):
                    with open(code_file, 'r', encoding="utf-8") as file:
                        code_file = file.read()
                        self.rule_data['javascript'] = _convert_to_one_line(code_file)
            else:
                raise ValueError(f"{code_file} is not a valid file")
        else:
            raise ValueError('It is necessary to introduce a mode EASY or ADVANCED')
        return self

    @set_method_call
    def with_env(self, data_env: str) -> 'RulesBuilder':
        """
        Specify the environment variable.

        Args:
            data_env (str): The environment variable.

        Returns:
            RulesBuilder: Returns self for chaining.
        """
        validate_type(data_env, str, "Data env")
        self.data_env = data_env
        return self

    @set_method_call
    def with_config_file(self, config_file: str, section: str, config_key: str) -> 'RulesBuilder':
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
            rule_id = afe07216-14ec-4134-97ae-c483b11d965a

            builder.with_config_file('model_config.ini', 'id', 'rule_id')

        Returns:
            RulesBuilder: Returns itself to allow for method chaining.
        """
        validate_type(config_file, str, "Config file")
        validate_type(section, str, "Section")
        validate_type(config_key, str, "Config Key")

        self.config_file = config_file
        self.section = section
        self.config_key = config_key

        config = configparser.ConfigParser()
        config.read(config_file)
        self.rule_data['identifier'] = config.get(section, config_key)
        return self

    @set_method_call
    def with_find_by_name(self, find_name: str) -> 'RulesBuilder':
        """
        Specify the name to find.

        Args:
            find_name (str): The name of the pipeline.

        Returns:
            RulesBuilder: Returns self for chaining.
        """
        validate_type(find_name, str, "Find Name")
        self.find_name = find_name
        return self

    @set_method_call
    def find_all(self) -> 'RulesBuilder':
        """
        Retrieve all models.

        This method sets up the RulesBuilder instance to retrieve all rules associated with the specified organization.

        Example:
            builder.with_organization_name("MyOrganization").find_all()

        Returns:
            RulesBuilder: The instance of the RulesBuilder class itself, allowing for method chaining.
        """
        self.url = f'{self.client.url}/north/v80/rules/search'
        self.method = 'find_all'
        return self

    @set_method_call
    def find_one(self) -> 'RulesBuilder':
        """
        Retrieve all models.

        This method sets up the RulesBuilder instance to retrieve all rules associated with the specified organization.

        Example:
            builder().with_organization('ManuCorp').with_channel('default_channel').\
                with_identifier('4ae733b0-2dc6-4ad4-9d2c-9ab426c9f32d').find_one()

        Returns:
            RulesBuilder: The instance of the RulesBuilder class itself, allowing for method chaining.
        """
        identifier = self._get_identifier()
        self.url = f'{self.client.url}/north/v80/rules/provision/organizations/{self.rule_data["organization"]}/channels/{self.rule_data["channel"]}/{identifier}'
        self.method = 'find_one'
        return self

    @set_method_call
    def create(self) -> 'RulesBuilder':
        """
        Initiates the creation process of a new model.

        This method prepares the AIModelsBuilder instance to create a new model by setting up the necessary parameters such as the organization name and the file to be associated with the model. It also specifies the URL endpoint for creating the model and sets the operation type to 'create'.

        Example:
            builder.with_organization_name("MyOrganization").add_file("example.onnx").create()

        Returns:
            AIModelsBuilder: The instance of the AIModelsBuilder class itself, allowing for method chaining.
        """
        self.url = f'{self.client.url}/north/v80/rules/provision/organizations/{self.rule_data["organization"]}/channels/{self.rule_data["channel"]}'
        self.method = 'create'
        return self

    @set_method_call
    def update(self) -> 'RulesBuilder':
        """
        Update an existing rule.

        This method sets up the RulesBuilder instance to update a specific rule associated with the specified organization and identifier.

        Example:
            rule = {
                "identifier": "9482a13d-ade5-46ec-b6c9-1cfc23f1f2c6",
                "name": "avanzado22",
                "active": False,
                "mode": "ADVANCED",
                "type": {
                    "datastreams": [
                        {
                            "name": "device.cpu.usage",
                            "fields": [
                                {
                                    "field": "value",
                                    "alias": "CPU usage"
                                }
                            ],
                            "prefilter": False
                        }
                    ],
                    "name": "DATASTREAM"
                },
                "actionsDelay": 1000
            }

            with_type = rule["type"]
                with_type(with_type).\
                with_actions_delay(rule["actionsDelay"]).\
                with_code_file('reglas_update.js').\
                update()
        Returns:
            RulesBuilder: The instance of the AIModelsBuilder class itself, allowing for method chaining.
        """
        identifier = self._get_identifier()
        self.url = f'{self.client.url}/north/v80/rules/provision/organizations/{self.rule_data["organization"]}/channels/{self.rule_data["channel"]}/{identifier}'
        self.method = 'update'
        return self

    @set_method_call
    def delete(self) -> 'RulesBuilder':
        """
       builder().with_organization('ManuCorp').\
            with_channel('default_channel').\
            with_identifier("45ddc1a9-4de2-4d5f-a9fe-7972aa4555a4").\
            delete().\
            build().\
            execute()
        """
        identifier = self._get_identifier()
        self.url = f'{self.client.url}/north/v80/rules/provision/organizations/{self.rule_data["organization"]}/channels/{self.rule_data["channel"]}/{identifier}'
        self.method = 'delete'
        return self

    @set_method_call
    def update_parameters(self) -> 'RulesBuilder':
        """
        Updates the parameters of an existing rule.

        This function prepares the RulesBuilder instance to update the parameters of a specific rule associated with the specified organization and channel.

        Example:
            builder.with_organization_name("MyOrganization").with_channel("default_channel").\
                with_name("rule_name").with_active(True).with_mode("ADVANCED").\
                with_parameters({"parameter1": "value1", "parameter2": "value2"}).update_parameters()

        Returns:
            RulesBuilder: The RulesBuilder instance itself, allowing method chaining.
        """
        identifier = self._get_identifier()
        self.url = f'{self.client.url}/north/v80/rules/provision/organizations/{self.rule_data["organization"]}/channels/{self.rule_data["channel"]}/{identifier}/parameters'
        self.method = 'update_parameters'
        return self

    @set_method_call
    def catalog(self) -> 'RulesBuilder':
        """
        Retrieves the rules catalog.

        This function prepares the RulesBuilder instance to retrieve the catalog of rules associated with the specified organization.

        Example:
            builder.with_organization_name("MyOrganization").catalog()

        Returns:
            RulesBuilder: The RulesBuilder instance itself, allowing method chaining.
        """
        self.url = f'{self.client.url}/north/v80/rules/catalog'
        self.method = 'catalog'
        return self

    @set_method_call
    def save(self) -> 'RulesBuilder':

        self.method = 'save'
        return self

    @set_method_call
    def set_config_file_identifier(self) -> 'RulesBuilder':
        """
        Set the rule identifier from a configuration file.

        This method sets up the AIModelsBuilder instance to retrieve the model identifier from a specified configuration file. It reads the identifier from the given section and key within the configuration file and sets it for the builder instance.

        Example:
            builder.with_config_file('model_config.ini', 'id', 'model_id').set_config_file_identifier()

        Returns:
            RulesBuilder: The instance of the AIModelsBuilder class itself, allowing for method chaining.
        """
        self.method = 'set_config_identifier'
        return self

    @set_method_call
    def set_env_identifier(self) -> 'RulesBuilder':
        """
        Set the rule identifier from an environment variable.

        This method sets up the RulesBuilder instance to retrieve the model identifier from a specified environment variable. It reads the identifier from the environment variable and sets it for the builder instance.

        Example:
            builder.with_env("MODEL_ENV_VAR").set_env_identifier()

        Returns:
            RulesBuilder: The instance of the AIModelsBuilder class itself, allowing for method chaining.
        """
        self.method = 'set_env_identifier'
        return self

    @set_method_call
    def build(self) -> 'AIModelsBuilder':
        """
        Finalizes the construction of the IoT collection configuration.

        This method prepares the builder to execute the collection by ensuring all necessary configurations are set and validates the overall integrity of the build. It should be called before executing the collection to ensure that the configuration is complete and valid.

        The build process involves checking that mandatory fields such as the device identifier are set. It also ensures that method calls that are incompatible with each other (like `build` and `build_execute`) are not both used.

        Example:
            builder.build()

        Returns:
            AIModelsBuilder: Returns itself to allow for method chaining, enabling further actions like `execute`.

        Raises:
            ValueError: If required configurations are missing or if incompatible methods are used together.

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

    @set_method_call
    def execute(self) -> requests.Response:
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
            'find_all': self._execute_find_all,
            'find_one': self._execute_find_one,
            'update': self._execute_update,
            'delete': self._execute_delete,
            'update_parameters': self._execute_update_parameters,
            'catalog': self._execute_catalog,
            'save': self._execute_save,
            'set_config_identifier': self._execute_set_identifier
        }

        function = methods.get(self.method)
        if function is None:
            raise ValueError(f'Unsupported method: {self.method}')
        return function()

    def _get_identifier(self) -> str:
        identifier = self.rule_data.get('identifier')
        if identifier:
            return identifier

        # Check if identifier is available in environment variables
        if self.data_env:
            identifier = dotenv_values().get(self.data_env)
            if identifier:
                return identifier
            raise KeyError(f'The parameter "{self.data_env}" was not found in the configuration env')

        # Check if identifier can be found by name
        if self.find_name:
            response = self.find_all().build().execute()
            all_identifiers = parse_json(response)

            if not isinstance(all_identifiers, dict) or 'rules' not in all_identifiers:
                raise Exception('Unexpected response format from the server.')

            identifier_list = all_identifiers['rules']
            name_identifier = next(
                (item['identifier'] for item in identifier_list if item.get('name') == self.find_name), None)
            if name_identifier:
                return name_identifier
            raise Exception(f'No rule with the name "{self.find_name}" was found.')

        # Raise error if no valid source for identifier is provided
        raise ValueError('A configuration file, a model identifier, or a name is required.')

    def _read_config_file(self):
        if self.config_file is not None:
            if os.path.exists(self.config_file):
                config = configparser.ConfigParser()
                config.read(self.config_file)
                return config
            raise ValueError('The configuration file does not exist.')
        return None

    def _execute_create(self):
        response = requests.post(self.url, headers=self.client.headers, json=self.rule_data, verify=False, timeout=3000)
        if response.status_code == 201:
            identifier = self._get_created_rule_identifier()
            if self.config_file:
                file_config = self._read_config_file()
                if file_config:
                    try:
                        self._read_config_file().get(self.section, self.config_key)
                        file_config.set(self.section, self.config_key, identifier)
                        with open(self.config_file, 'w', encoding='utf-8') as configfile:
                            file_config.write(configfile)
                    except configparser.NoOptionError:
                        return ValueError('The "rule_id" parameter was not found in the configuration file.')

                elif self.data_env is not None:
                    try:
                        env_vars = dotenv_values('.env')
                        if self.data_env not in env_vars:
                            raise KeyError('The environment variable was not found in the .env file.')

                        set_key('.env', self.data_env, identifier)

                    except KeyError as error:
                        raise ValueError('The environment variable was not found in the .env file.') from error
            return {'status_code': response.status_code}
        else:
            return {'status_code': response.status_code, 'error': response.text}

    def _get_created_rule_identifier(self):
        name = self.rule_data.get('name')
        if not name:
            raise ValueError('The "name" attribute is missing or empty.')
        response = self.find_all().build().execute()
        all_identifiers = parse_json(response)
        if 'rules' in all_identifiers:
            for rule in all_identifiers['rules']:
                if 'name' in rule and rule['name'] == name:
                    return rule['identifier']

        raise ValueError(f'No rule with the name "{name}" was found.')

    def _execute_find_all(self) -> str | dict[str, str | int]:
        # El limite no debería de tenerlo es decir un bucle for en cada response hasta que no tenga mas datos
        body_data = {
            "filter": {"and": [{"eq": {"rule.organization": self.rule_data['organization']}}]},
            "limit": {"size": 1000, "start": 1}
        }
        url = f'{self.client.url}/north/v80/rules/search'
        response = requests.post(url, headers=self.client.headers, json=body_data, verify=False, timeout=3000)
        if response.status_code == 200:
            return response.text
        else:
            return {'status_code': response.status_code, 'error': response.text}

    def _execute_find_one(self) -> str | dict[str, str | int]:
        response = send_request('get', self.client.headers, self.url)
        if response.status_code == 200:
            return response.text
        else:
            return {'status_code': response.status_code, 'error': response.text}

    def _execute_update(self) -> Response | dict[str, str | int]:
        response = requests.put(self.url, headers=self.client.headers, json=self.rule_data, verify=False, timeout=3000)
        return handle_basic_response(response)

    def _execute_delete(self) -> Response | dict[str, str | int]:
        response = requests.delete(self.url, headers=self.client.headers, json=self.rule_data, verify=False,
                                   timeout=3000)
        return handle_basic_response(response)

    def _execute_update_parameters(self) -> dict[str, Any]:
        response = requests.put(self.url, headers=self.client.headers, json=self.rule_data['parameters'], verify=False,
                                timeout=3000)
        return handle_basic_response(response)

    def _execute_catalog(self) -> str | dict[str, str | int]:
        response = send_request('get', self.client.headers, self.url)
        if response.status_code == 200:
            return response.text
        else:
            return {'status_code': response.status_code, 'error': response.text}

    def _execute_save(self):
        if self.data_env is not None or self.config_file is not None:
            if self.data_env is not None:
                identifier = dotenv_values('.env')[self.data_env]
                self.rule_data['identifier'] = identifier

            elif self.config_file is not None:
                config = configparser.ConfigParser()
                config.read(self.config_file)
                rule_id = config.get(self.section, self.config_key, fallback=None)
                self.rule_data["identifier"] = rule_id
                response = self.find_one().build().execute().json()
                if response is not None and isinstance(response, dict):
                    # Update
                    return self.update().build().execute()
                # Create
                return self.create().build().execute()
        return ValueError('The "rule_id" parameter was not found in the configuration file.')

    def _execute_set_identifier(self):
        try:
            file_config = self._read_config_file()
            self._read_config_file().get(self.section, self.config_key)
            file_config.set(self.section, self.config_key, self.rule_data['identifier'])
            with open(self.config_file, 'w', encoding='utf-8') as configfile:
                file_config.write(configfile)
            return None

        except configparser.NoOptionError:
            return Exception('The "rule_id" parameter was not found in the configuration file.')

    def _execute_env_identifier(self) -> None:
        try:
            env_vars = dotenv_values('.env')
            if self.data_env not in env_vars:
                raise KeyError('The environment variable was not found in the .env file.')

            set_key('.env', self.data_env, self.rule_data['identifier'])

        except KeyError as error:
            raise Exception('The environment variable was not found in the .env file.') from error

    def _validate_builds(self):
        required_methods = {
            'create': ['with_organization_name', 'with_name', 'with_mode', 'with_actions_delay', 'with_channel'],
            'update': ['with_organization_name', 'with_name', 'with_mode', 'with_actions_delay', 'with_channel'],
            'find_one': ['with_organization_name', 'with_channel'],
            'find_all': ['with_organization_name'],
            'delete': ['with_organization_name', 'with_channel'],
            'update_parameters': ['with_organization_name', 'with_channel', 'with_parameters'],
            'save': ['with_organization_name'],
            'set_config_file_identifier': ['with_config_file'],
            'set_env_identifier': ['with_env']
        }

        for method, required in required_methods.items():
            if self.method_calls.count(method) > 0:
                missing_methods = [req for req in required if req not in self.method_calls]
                if missing_methods:
                    raise Exception(f"It is mandatory to use the {', '.join(missing_methods)} method(s) in {method}()")

        return self
