#!/usr/bin/env python3
"""Generate unit test for the `access_nested_map` function in utils.py"""

import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from unittest.mock import patch, Mock


class TestAccessNestedMap(unittest.TestCase):
    """
    Test case class for the `access_nested_map` utility function
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Test that `access_nested_map` returns the correct value for a given nested map and path.

        Args:
            nested_map (dict): The nested dictionary to access.
            path (tuple): A sequence of keys to traverse.
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
    """Tests if the given URL returns a JSON file."""

    @patch('utils.requests.get')
    def test_get_json(self, mock_get):
        """
    Test that get_json calls requests.get with the correct URL and
    returns the expected JSON payload.
    """
        
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


class TestMemoize(unittest.TestCase):
    """Test cases for the memoize decorator"""

    def test_memoize(self):
        """Test that the memoize decorator caches method results."""

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        test_instance = TestClass()

        with patch.object(TestClass, 'a_method') as mock_method:
            mock_method.return_value = 42

            result1 = test_instance.a_property
            result2 = test_instance.a_property

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            mock_method.assert_called_once()


if __name__ == '__main__':
    unittest.main()
