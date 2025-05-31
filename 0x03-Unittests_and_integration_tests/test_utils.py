#!/usr/bin/env python3
"""Generate unit test for  the `access_nested_map` function in the utils.py"""

import unittest
from parameterized import parameterized
from utils import access_nested_map
from unittest.mock import patch, Mock
from utils import get_json
import requests
from typing import Dict

def get_json(url: str) -> Dict:
    """
        Get JSON from remote URL.
    """
    response = requests.get(url)
    return response.json()


class TestAccessNestedMap(unittest.TestCase):
    """
    Test case class for the `access_nested_map` utility function
    """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b":2}),
        ({"a": {"b":2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Test that `access_nested_map` returns the correct value for a given nested map and path.

        Args:
            nested_map (dict): The nested dictionary to access.
            path (tuple): A sequence of keys to translate
            expected (any): The expected result from the function.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)
    
    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Ensures a KeyError is raised when invalid keys are provided."""
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)

class TestGetJson(unittest.TestCase):
    """Tests if the giver URL returns a JSON file."""
    @patch('requests.get')
    def test_get_json(self, mock_get):
        test_cases = [
            ('https://example.com', {"payload": True}),
            ('http://holberton.io', {"payload": True}),
        ]

        for url, expected_payload in test_cases:
            mock_response = Mock()
            mock_response.json.return_value = expected_payload
            mock_get.return_value = mock_response

            result = get_json(url)

            mock_get.assert_called_once_with(url)
            self.assertEqual(result, expected_payload)
            mock_get.reset_mock()

if __name__ == '__main__':
    unittest.main()
if __name__ == "__main__":
    unittest.main()