import os
import sys
import datetime
import json
from typing import Dict, Any

from .utils import Utilities

class Airiaclient:
    def __init__(self, host: str = "", port: str = "", db_name: str = "", api_key: str = ""):
        """
        Initialize the Airiaclient with the given host, port, database name, and API key.
        
        :param host: Host address for the database connection
        :param port: Port number for the database connection
        :param db_name: Name of the database to connect to
        :param api_key: API key for authorization
        """
        self.host = host
        self.port = port
        self.db_name = db_name
        self.api_key = api_key
        self.connection = Utilities.connection(host, port, db_name)

    def search(self, data: Dict[str, Any] = None):
        """
        Perform a search operation using the provided data.

        :param data: A dictionary containing search parameters
        :return: Search results from the database
        :raises ValueError: If data is not provided or if required fields are missing
        """
        if data is None:
            raise ValueError("Please provide a valid JSON object containing a valid collection name and query.")
        
        if not isinstance(data, dict):
            raise ValueError("The data parameter must be a JSON object represented as a dictionary.")

        required_fields = {"collection", "query", "query_fields", "result_columns", "limit"}
        
        # Check if all required fields are present
        if not required_fields.issubset(data.keys()):
            missing_fields = required_fields - data.keys()
            raise ValueError(f"The data parameter is missing the following required fields: {missing_fields}")
        
        # Process the JSON data here, potentially using the api_key
        try:
            return Utilities.ann_search(self.connection, data, self.api_key)  # If the search function requires the API key
        except Exception as e:
            print(f"An error occurred during the search operation: {e}")
            raise