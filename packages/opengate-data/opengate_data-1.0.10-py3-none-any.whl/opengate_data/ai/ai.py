"""  AIBuilder """
import json
import os
import configparser
import requests
import urllib3
from dotenv import load_dotenv, set_key, dotenv_values
from typing import Any
from requests import Response


class AIBaseBuilder:
    """ Class AIBaseBuilder """

    def __init__(self):
        self.client = client
        self.organization_name: str | None = None
        self.identifier: str | None = None
        self.data_env: str | None = None
        self.find_name: str | None = None
        self.identifier: str | None = None
        self.config_file: str | None = None
        self.section: str | None = None
        self.config_key: str | None = None
        self.find_name: str | None = None

    def with_organization_name(self, organization_name: str) -> 'AIBuilder':
        """
        Specify the organization name.

        Args:
            organization_name (str): The name of the organization.

        Returns:
            AIBuilder: Returns self for chaining.
        """
        self.organization_name = organization_name
        return self

    def with_identifier(self, identifier: str) -> 'AIBuilder':
        """
         Specify the identifier for the pipeline.

         Args:
             identifier (str): The identifier for the pipeline.

         Returns:
             AIBuilder: Returns self for chaining.
         """
        self.identifier = identifier
        return self

    def with_env(self, data_env: str) -> 'AIBuilder':
        """
        Specify the environment variable.

        Args:
            data_env (str): The environment variable.

        Returns:
            AIBuilder: Returns self for chaining.
        """
        self.data_env = data_env
        return self

    def with_find_by_name(self, find_name: str) -> 'AIBuilder':
        """
        Specify the name to find.

        Args:
            find_name (str): The name of the model, pipeline or transformer.

        Returns:
            AIBuilder: Returns self for chaining.
        """
        self.find_name = find_name
        return self

    def _get_identifier(self) -> str:
        # Obtiene el identificador por identifier, data_env y config_file
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
            all_identifiers = self.find_all().build().execute().json()
            name_identifier = [item['identifier'] for item in all_identifiers if item['name'] == self.find_name]

            if not name_identifier:
                raise ValueError(f'File name "{self.find_name}" does not exist')

            return name_identifier[0]

        raise ValueError('A configuration file with identifier, config file, or a find by name is required.')


