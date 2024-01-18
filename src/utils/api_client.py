# api_client.py

import requests

class APIClient:
    """
    A simple API client for making HTTP GET requests to a RESTful API.

    This class allows you to create an instance of an API client that can be used to fetch data
    from a specified API endpoint using HTTP GET requests.

    Args:
    base_url (str): The base URL of the RESTful API.

    Attributes:
    base_url (str): The base URL of the RESTful API.

    Methods:
    fetch_data(endpoint):
    Fetch data from a specified API endpoint.
    """
    def __init__(self, base_url):
        """
        Initialize the APIClient with a base URL.

        Args:
        base_url (str): The base URL of the RESTful API.
        """        
        self.base_url = base_url

    def fetch_data(self, endpoint):
        """
        Fetch data from a specified API endpoint.

        This method constructs the full URL based on the base URL and the provided endpoint and
        sends an HTTP GET request to retrieve data from the API.

        Args:
        endpoint (str): The API endpoint to fetch data from.

        Returns:
        dict: A dictionary containing the JSON response from the API if the request is successful.
        If the request fails, it returns a dictionary with an "error" status and additional
        information.      

        Raises:
        requests.exceptions.RequestException: If the HTTP GET request encounters an error.

        Note:
        Proper error handling should be implemented to handle potential exceptions raised during
        the HTTP request.
        """
        
        url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                return {"status": "error", "code": response.status_code}
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return {"status": "error", "message": str(e)}
