'''  ProvisionProcessorBuilder '''

import requests
from typing import Callable, Union, List, Dict, Any


class ProvisionProcessorBuilder:
    ''' Provision Processor operations'''
    def __init__(self, opengate_client):
        self.client = opengate_client
        self.organization_name: str = None
        self.provision_processor_id: str = None
        self.provision_processor_name: str = None
        self.bulk_process_id: str = None
        self.bulk_file: Dict = None
        self.url: str = None
        self.method: str = None
        self.requires: Dict[str, Any] = {}
        self.headers: Dict[str, Any] = self.client.headers


    def __str__(self):
        ''' String representation of the object '''
        return f"Url: {self.url}, headers: {self.headers}, requires: {self.requires}, organization_name: {self.organization_name}, provision_processor_id: {self.provision_processor_id}, bulk_file: {self.bulk_file}, method: {self.method}"


    def with_organization_name(self, organization_name: str) -> 'ProvisionProcessorBuilder':
        ''' organization_name '''
        self.organization_name = organization_name
        return self
      
    def with_provision_processor_id(self, provision_processor_id: str) -> 'ProvisionProcessorBuilder':
        ''' provision_processor_id '''
        self.provision_processor_id = provision_processor_id
        return self
      
    def with_provision_processor_name(self, provision_processor_name: str) -> 'ProvisionProcessorBuilder':
        ''' provision_processor_name '''
        self.provision_processor_name = provision_processor_name
        return self
      
    def with_bulk_file(self, bulk_file: Dict) -> 'ProvisionProcessorBuilder':
        ''' bulk_file '''
        self.bulk_file = {'file': ('salida.xlsx', open(bulk_file, 'rb'), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')}
        return self
      
    def with_bulk_process_id(self, bulk_process_id: Dict) -> 'ProvisionProcessorBuilder':
        ''' bulk_file '''
        self.bulk_process_id = bulk_process_id
        return self
    
        
    def bulk(self) -> 'ProvisionProcessorBuilder':
        ''' bulk_provision_processor '''
        self.requires = {
            'organization_name': self.organization_name,
            'provision_processor_id': self.provision_processor_id,
            'bulk_file': self.bulk_file
        }
        self.method = 'bulk_provision_processor'
        self.headers['Accept'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        self.url = f'{self.client.url}/north/v80/provisionProcessors/provision/organizations/{self.organization_name}/{self.provision_processor_id}/bulk'
        return self
    
        
    def search_by_name(self) -> 'ProvisionProcessorBuilder':
        ''' search_provision_processor '''
        self.requires = {
            'organization_name': self.organization_name,
            'provision_processor_name': self.provision_processor_name,
            
        }
        self.method = 'search_provision_processor'
        self.headers['Accept'] = 'application/json'
        self.url = f'{self.client.url}/north/v80/provisionProcessors/provision/organizations/{self.organization_name}'
        return self
    
        
    def bulk_status(self) -> 'ProvisionProcessorBuilder':
        ''' bulk_status '''
        self.requires = {
            'organization_name': self.organization_name,
            'bulk_process_id': self.bulk_process_id,
            
        }
        self.method = 'bulk_status'
        self.headers['Accept'] = 'application/json'
        self.url = f'{self.client.url}/north/v80/provisionProcessors/provision/organizations/{self.organization_name}/bulk/{self.bulk_process_id}'
        return self
    
        
    def bulk_details(self) -> 'ProvisionProcessorBuilder':
        ''' bulk_details '''
        self.requires = {
            'organization_name': self.organization_name,
            'bulk_process_id': self.bulk_process_id,
            
        }
        self.method = 'bulk_details'
        self.headers['Accept'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        self.url = f'{self.client.url}/north/v80/provisionProcessors/provision/organizations/{self.organization_name}/bulk/{self.bulk_process_id}/details'
        return self
    
    def build(self) -> 'ProvisionProcessorBuilder':
        ''' Check if any parameter is missing. '''
        if self.requires is not None:
            for key, value in self.requires.items():
                assert value is not None, f'{key} is required'
        return self
    

    def execute(self) -> Union[int, List[Dict[str, Any]]]:
        ''' Execute and return the responses '''
        methods: Dict[str, Callable[[], Union[int, List[Dict[str, Any]]]]] = {
            'bulk_provision_processor': self._execute_bulk,
            'search_provision_processor': self._execute_searching,
            'bulk_status': self._execute_bulk_status,
            'bulk_details': self._execute_bulk_details,
        }
        function = methods.get(self.method)
        if function is None:
            raise ValueError(f'Unsupported method: {self.method}')
        return function()

    def _execute_bulk(self) -> Union[int, List[Dict[str, Any]]]:
        return requests.post(self.url, headers=self.headers, files=self.bulk_file, verify=False, timeout=3000)


    def _execute_searching(self) -> Union[int, List[Dict[str, Any]]]:
        request_response = requests.get(self.url, headers=self.headers, verify=False, timeout=3000)
        data = request_response.json()
        provision_procesor = {}
        for item in data.get("provisionProcessors", []):
            if item.get("name") == self.provision_processor_name:
                provision_procesor = item    
        return provision_procesor
    

    def _execute_bulk_status(self) -> Union[int, List[Dict[str, Any]]]:
        return requests.get(self.url, headers=self.headers, verify=False, timeout=3000)    
    
    
    def _execute_bulk_details(self) -> Union[int, List[Dict[str, Any]]]:
        return requests.get(self.url, headers=self.headers, verify=False, timeout=3000)
        