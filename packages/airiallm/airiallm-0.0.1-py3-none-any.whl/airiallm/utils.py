import os
import sys
import datetime
import json
import requests
import numpy as np
from typing import Dict, Any
from . import constants

class Utilities:

    @staticmethod
    def get_embeddings(api_key: str, dims: int, model: str, data: Any) -> Dict[str, Any]:
        """
        Get embeddings from the API using the provided parameters.

        Args:
            api_key (str): The API key for authentication.
            dims (int): The number of dimensions for the embeddings.
            model (str): The model to be used for generating embeddings.
            data (Any): The data to be embedded.

        Returns:
            Dict[str, Any]: A dictionary containing the response from the API or error details.
        """
        # Set up headers for the API request
        headers = {
            "API-Key": api_key,
            "Content-Type": "application/json"
        }
        
        # Create the payload with the necessary data
        payload = {
            "dims": dims,
            "model": model,
            "data": data
        }

        try:
            # Make a POST request to the API endpoint
            response = requests.post(
                f"{constants.AIRIA_COGNITION_BASE_URL}/api/embedd",
                headers=headers,
                data=json.dumps(payload)
            )
            # Raise an HTTPError if the HTTP request returned an unsuccessful status code
            response.raise_for_status()
            # Return the JSON response if the request is successful
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            # Handle HTTP errors
            print(f"HTTP error occurred: {http_err}")
            return {"status_code": response.status_code, "error": str(http_err)}
        except Exception as err:
            # Handle any other exceptions
            print(f"An error occurred: {err}")
            return {"error": str(err)}

    @staticmethod
    def ask(api_key: str, query: str="", model: str=""):
        
        headers = {
            "API-Key": api_key,
            "Content-Type": "application/json"
        }
        
        # Create the payload with the necessary data
        payload = {
            "query": query,
            "model": model
        }

        try:
            # Make a POST request to the API endpoint
            response = requests.post(
                f"{constants.AIRIA_COGNITION_BASE_URL}/api/llm_airiacognition",
                headers=headers,
                data=json.dumps(payload)
            )
            # Raise an HTTPError if the HTTP request returned an unsuccessful status code
            response.raise_for_status()
            # Return the JSON response if the request is successful
            return response
        except requests.exceptions.HTTPError as http_err:
            # Handle HTTP errors
            print(f"HTTP error occurred: {http_err}")
            return {"status_code": response.status_code, "error": str(http_err)}
        except Exception as err:
            # Handle any other exceptions
            print(f"An error occurred: {err}")
            return {"error": str(err)}
