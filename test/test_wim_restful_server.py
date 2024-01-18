import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import unittest
from unittest.mock import patch, MagicMock
from WIMRestfulServer.wim_restful_server import WeightInMotionServer
from flask import json

class TestWeightInMotionServer(unittest.TestCase):

    def setUp(self):
        self.server = WeightInMotionServer()
        self.server.app.testing = True
        self.client = self.server.app.test_client()

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data='5')
    def test_load_current_id(self, mock_file, mock_exists):
        """
        Test the loading of the current measurement ID from a file.
        """
        mock_exists.return_value = True
        current_id = self.server.load_current_id()
        self.assertEqual(current_id, 5)

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_save_current_id(self, mock_file):
        """
        Test the saving of the current measurement ID to a file.
        """
        self.server.current_id = 10
        self.server.save_current_id()
        mock_file().write.assert_called_with('10')

    def test_health_endpoint(self):
        """
        Test the '/health' endpoint of the server.
        """
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "OK"})

    @patch('WIMRestfulServer.wim_restful_server.WeightInMotionServer.update_data')
    def test_data_endpoint(self, mock_update_data):
        """
        Test the '/data' endpoint of the server.
        """
        mock_update_data.return_value = None  # Mock the behavior of update_data if needed
        self.server.time_iso_format = "2024-01-17T12:00:00"  # Set a mock timestamp
        response = self.client.get('/data')
        self.assertEqual(response.status_code, 200)
        # Add additional assertions to validate the structure of the returned data

    # Additional tests can be added for other methods and functionalities

if __name__ == '__main__':
    unittest.main()
