import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import unittest
from utils.api_client import APIClient
import requests_mock

class TestAPIClient(unittest.TestCase):
    """
    Test Suite for the APIClient class.

    This suite tests the functionality of the APIClient class,
    ensuring that it correctly handles both successful and unsuccessful
    responses from the API.
    """

    def setUp(self):
        """
        Set up the test environment.

        Initializes the APIClient with a predefined base URL.
        """
        self.base_url = "http://localhost:5000"
        self.api_client = APIClient(self.base_url)

    @requests_mock.Mocker()
    def test_fetch_data_success(self, mock):
        """
        Test if fetch_data method successfully retrieves data.

        This test ensures that the fetch_data method correctly processes
        and returns data when the API endpoint responds with a status code of 200.
        It mocks a successful API response and asserts that the method
        returns the expected data.
        """
        # Mock the API response
        mock.get(f"{self.base_url}/endpoint", json={"status": "success"}, status_code=200)

        # Test successful data fetch
        response = self.api_client.fetch_data("endpoint")
        self.assertIsNotNone(response)
        self.assertEqual(response['status'], 'success')

    @requests_mock.Mocker()
    def test_fetch_data_error(self, mock):
        """
        Test error handling in fetch_data method.

        This test verifies that the fetch_data method correctly handles errors
        when the API endpoint responds with an error status code (e.g., 404).
        It mocks an API response indicating an error and asserts that the method
        properly returns an error status.
        """
        # Mock the API response for an error
        mock.get(f"{self.base_url}/invalid_endpoint", json={"status": "error"}, status_code=404)

        # Test response handling when an error occurs
        response = self.api_client.fetch_data("invalid_endpoint")
        self.assertIsNotNone(response)
        self.assertEqual(response['status'], 'error')

if __name__ == '__main__':
    unittest.main()
