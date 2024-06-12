""" Class representing the OpenGateClient """

import requests
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings


from .searching.entities_search import EntitiesSearchBuilder
from .searching.operations_search import OperationsSearchBuilder
from .searching.datapoints_search import DataPointsSearchBuilder
from .datasets.search_dataset import DatasetsSearchBuilder
from .timeseries.search_timeseries import TimeseriesSearchBuilder
from .ai_models.ai_models import AIModelsBuilder
from .ai_pipelines.ai_pipelines import AIPipelinesBuilder
from .ai_transformers.ai_transformers import AITransformersBuilder
from .rules.rules import RulesBuilder
from .rules.rules_searching import RulesSearchBuilder

from .collection.iot_collection import IotCollectionBuilder
from .collection.iot_bulk_collection import IotBulkCollectionBuilder
from .provision.bulk.provision_bulk import ProvisionBulkBuilder
from .provision_processor.provision_processor import ProvisionProcessorBuilder


class OpenGateClient:
    """ Class representing the OpenGateClient """

    def __init__(self, url: str | None = None, user: str | None = None, password: str | None = None,
                 api_key: str | None = None) -> None:
        self.url: str = url
        self.user: str = user
        self.password: str | None = password
        self.api_key: str | None = api_key
        self.headers: dict[str, str] = {}
        self.client: OpenGateClient = self
        self.entity_type: str | None = None
        disable_warnings(InsecureRequestWarning)

        if not url:
            raise ValueError('You have not provided a URL')

        if user and password:
            data_user = {
                'email': self.user,
                'password': self.password
            }
            try:
                login_url = self.url + '/north/v80/provision/users/login'
                request = requests.post(login_url, json=data_user, timeout=5000, verify=False)
                request.raise_for_status()
                response_json = request.json()
                if 'user' in response_json:
                    self.headers.update({
                        'Authorization': f'Bearer {response_json["user"]["jwt"]}',
                    })
                else:
                    raise ValueError('Empty response received')

            except requests.exceptions.HTTPError as err:
                raise requests.exceptions.HTTPError(f'Request failed: {err}')
            except requests.exceptions.RequestException as error:
                raise requests.exceptions.RequestException(f'Connection failed: {error}')
        elif api_key:
            self.headers.update({
                'X-ApiKey': self.api_key
            })
        else:
            raise ValueError('You have not provided an API key or user and password')

    def new_entities_search_builder(self) -> EntitiesSearchBuilder:
        """ Represents the search builder of entities """
        return EntitiesSearchBuilder(self)

    def new_operations_search_builder(self) -> OperationsSearchBuilder:
        """ Represents the search builder of operations """
        return OperationsSearchBuilder(self)

    def new_datapoints_search_builder(self) -> DataPointsSearchBuilder:
        """ Represents the search builder of datapoints """
        return DataPointsSearchBuilder(self)

    def new_data_sets_search_builder(self) -> DatasetsSearchBuilder:
        """ Represents the search builder of datasets """
        return DatasetsSearchBuilder(self)

    def new_timeseries_search_builder(self) -> TimeseriesSearchBuilder:
        """ Represents the builder of timeseries """
        return TimeseriesSearchBuilder(self)

    def provision_processor(self) -> ProvisionProcessorBuilder:
        """ Represents the builder of provision processors """
        return ProvisionProcessorBuilder(self)

    def new_ai_models_builder(self) -> AIModelsBuilder:
        """ Represents the builder of artificial intelligence models """
        return AIModelsBuilder(self)

    def new_ai_pipelines_builder(self) -> AIPipelinesBuilder:
        """ Represents the builder of artificial intelligence models """
        return AIPipelinesBuilder(self)

    def new_ai_transformers_builder(self) -> AITransformersBuilder:
        """ Represents the builder of artificial intelligence models """
        return AITransformersBuilder(self)

    def new_rules_builder(self) -> RulesBuilder:
        """ Represents the builder rules """
        return RulesBuilder(self)

    def new_rules_search_builder(self) -> RulesSearchBuilder:
        """ Represents the builder rules """
        return RulesSearchBuilder(self)

    def new_iot_collection_builder(self) -> IotCollectionBuilder:
        """ Represents the builder iot collection builder """
        return IotCollectionBuilder(self)

    def new_iot_bulk_collection_builder(self) -> IotBulkCollectionBuilder:
        """ Represents the builder iot bulk collection builder """
        return IotBulkCollectionBuilder(self)

    def new_provision_bulk_builder(self) -> ProvisionBulkBuilder:
        return ProvisionBulkBuilder(self)