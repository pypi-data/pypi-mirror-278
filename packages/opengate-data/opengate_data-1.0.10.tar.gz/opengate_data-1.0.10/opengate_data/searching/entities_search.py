"""  EntitiesSearchBuilder """

from ..searching.search import SearchBuilder
from ..utils import validate_type, set_method_call


class EntitiesSearchBuilder(SearchBuilder):
    """ Builder search entities"""

    def __init__(self, opengate_client):
        super().__init__()
        self.client = opengate_client
        self.headers = self.client.headers
        self.builder: bool = False
        self.url: str | None = None
        self.method: str | None = None

    @set_method_call
    def build(self):
        """
        Finalizes the construction of the entities search configuration.

        This method prepares the builder to execute the collection by ensuring all necessary configurations are set and validates the overall integrity of the build. It should be called before executing the collection to ensure that the configuration is complete and valid.

        The build process involves checking that mandatory fields such as the device identifier are set. It also ensures that method calls that are incompatible with each other (like `build` and `build_execute`) are not both used.

        Example:
            builder.build()

        Returns:
            EntitiesSearchBuilder: Returns itself to allow for method chaining, enabling further actions like `execute`.

        Raises:
            ValueError: If required configurations are missing or if incompatible methods are used together.

        Note:
            This method should be used as a final step before `execute` to prepare the entities search configuration. It does not modify the state but ensures that the builder's state is ready for execution.
        """
        self.builder = True
        self._validate_builds()

        if self.method_calls.count('build_execute') > 0:
            raise Exception("You cannot use build() together with build_execute()")

        return self

    @set_method_call
    def execute(self):
        """
        Executes the operations search based on the built configuration.

        Returns:
            dict, csv or  dataframe: The response data in the specified format.

        Raises:
            Exception: If the build() method was not called before execute().
        """
        return self._send_request('entities', self.headers)

    def _validate_builds(self):
        if self.format_data is not None and all(
                keyword not in self.format_data for keyword in ["csv", "pandas", "dict"]):
            raise ValueError(
                'Invalid value for the "with_format" method. Available parameters are only "dict", "csv", and "pandas".')
