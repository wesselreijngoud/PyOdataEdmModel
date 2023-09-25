# This file adheres to the "black" code formatting style.
# More information about black: https://github.com/psf/black
import json


class OdataConverter:
    def __init__(
        self,
        file_path: str,
        database_client: str
    ):
        """
        Initialize an OdataConverter instance.

        Parameters:
            database_client (str): The name of the database client (e.g., "SQLServer").
            file_path (str): The path to the JSON file containing data type templates.
        """
        self.file_path = file_path
        # lower and delete spaces from input string
        self.database_client = ''.join(database_client.split()).lower()
        self.load_json_data()

    def load_json_data(self):
        """
        Load JSON data from the specified file and validate the presence of the
        specified database client's data types.

        Raises:
            ValueError: If the database client is not present in the JSON data.
        """
        with open(self.file_path, "r") as file:
            json_data = json.load(file)
            if self.database_client not in json_data:
                raise ValueError(
                    """Database client not yet present in data type template,
                    please add it manually."""
                )
            else:
                self.json_data = json_data[self.database_client]

    def convert_to_odata(self, data_type: str) -> str:
        """
        Convert a database-specific data type to its OData equivalent.

        Parameters:
            data_type (str): The database-specific data type to convert.

        Returns:
            str: The OData equivalent data type, or "Edm.String" if not found.
        """
        return self.json_data.get(data_type.lower(), "Edm.String")
