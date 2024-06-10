import os
import sys
import datetime
import json
from typing import Dict, Any, List

from .utils import Utilities
from . import constants

class AiriaLLM:
    def __init__(self, api_key: str = ""):
        """
        Initialize the AiriaLLM with the given API key.
        :param api_key: API key for authorization

        """
        self.api_key = api_key
        

    def embedd(self, dims: int = 3072, model: str = "", data: List[str] = None):
        """
        Embeds data using a specified model and dimensionality.

        Parameters:
        dims (int): The dimensionality for the embedding. Must be 3072.
        model (str): The model name for embedding.
        data (List[str]): The data to be embedded, expected to be a list of strings.

        Raises:
        ValueError: If dims is not 3072.
        ValueError: If model is not a valid non-empty string.
        ValueError: If data is not a list of strings.
        """

        # Validate dims parameter
        if dims != 3072:
            raise ValueError("The 'dims' parameter must be 3072.")

        # Validate model parameter
        if not isinstance(model, str) or not model:
            raise ValueError("The 'model' parameter must be a valid non-empty string.")

        # Validate data parameter
        if not isinstance(data, list) or not all(isinstance(item, str) for item in data):
            raise ValueError("The 'data' parameter must be a list of strings.")

        # If all validations pass, proceed with the embedding process
        # Embedding logic goes here

        return Utilities.get_embeddings(self.api_key, dims, model, data)

    def ask(self, query: str = "", model: str = ""):
        # Validation for query
        if not query:
            raise ValueError("The query parameter cannot be empty.")
        if not isinstance(query, str):
            raise TypeError("The query parameter must be a string.")
        
        # Validation for model
        if not model:
            raise ValueError("The model parameter cannot be empty.")
        if not isinstance(model, str):
            raise TypeError("The model parameter must be a string.")
        
        return Utilities.ask(self.api_key, query, model)
        