class SearchBuilderBase:
    def __init__(self):
        self.utc: bool = False
        self.flatten: bool = False
        self.utc: bool = False
        self.summary: bool = False
        self.default_sorted: bool = False
        self.case_sensitive: bool = False

    def with_flattened(self) -> 'SearchBuilderBase':
        """
        Flatten the data

        Returns:
            SearchBuilderBase: Returns itself to allow for method chaining.
        """
        self.flatten = True
        return self

    def with_utc(self) -> 'SearchBuilderBase':
        """
        Set UTC flag

        Returns:
            SearchBuilderBase: Returns itself to allow for method chaining.
        """
        self.utc = True
        return self

    def with_summary(self) -> 'SearchBuilderBase':
        """
        Set summary flag

        Returns:
            SearchBuilderBase: Returns itself to allow for method chaining.
        """
        self.summary = True
        return self

    def with_default_sorted(self) -> 'SearchBuilderBase':
        """
        Set default sorted flag

        Returns:
            SearchBuilderBase: Returns itself to allow for method chaining.
        """
        self.default_sorted = True
        return self

    def with_case_sensitive(self) -> 'SearchBuilderBase':
        """
        Set case-sensitive flag

        Returns:
            SearchBuilder: Returns itself to allow for method chaining.
        """
        self.case_sensitive = True
        return self
