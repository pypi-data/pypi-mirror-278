# sort_builder.py
class SortBuilder:
    def __init__(self):
        self._sort_template = {"sort": {"parameters": []}}

    def add(self, *sort_criteria):
        """
        Adds one or multiple fields to the sort clause.

        Args:
            *sort_criteria: A variable number of tuples, where each tuple contains the field name and the order.

        Returns:
            SortBuilder: Returns itself to allow for method chaining.

        Example:
            sort_builder.add(("datapoints._current.at", "DESCENDING"))
            sort_builder.add(("datapoints._current.at", "DESCENDING"), ("devices._current.at", "ASCENDING"))
        """
        for criteria in sort_criteria:
            if not isinstance(criteria, tuple) or len(criteria) != 2:
                raise ValueError("Each sort criteria must be a tuple with exactly two elements: (name, order)")
            name, order = criteria
            if order not in ["ASCENDING", "DESCENDING"]:
                raise ValueError("Order must be 'ASCENDING' or 'DESCENDING'")
            self._sort_template["sort"]["parameters"].append({"name": name, "type": order})
        return self

    def build(self):
        """
        Builds the final sort clause.

        Returns:
            dict: The final sort clause.

        Raises:
            ValueError: If no sort criteria have been added.

        Example:
            final_sort = sort_builder.build()
        """
        if not self._sort_template["sort"]["parameters"]:
            raise ValueError("No sort criteria have been added")
        return self._sort_template
