#!/usr/bin/env python3
"""Generate unit test for  the `access_nested_map` function in the utils.py"""

import unittest
from parameterized import parameterized
from utils import access_nested_map

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

if __name__ == "__main__":
    unittest.main()