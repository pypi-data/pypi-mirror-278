class SelectElement:
    @staticmethod
    def element(name, fields):
        """
        Creates a select element.

        Args:
            name (str): The name of the data stream.
            fields (list): A list of fields to retrieve, each field being a dictionary with 'field' and optional 'alias'.

        Returns:
            dict: The select element.

        Example:
            builder.element('provision.device.identifier', [{'field': 'value', 'alias': 'id'}])
        """
        return {"name": name, "fields": fields}
