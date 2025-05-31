#!/usr/bin/env python3
import unittest
from unittest.mock import Mock, patch, PropertyMock
from parameterized import parameterized

from client import GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):
    """Test GithubOrgClient class"""

    @parameterized.expand([
        ('google', ),
        ('abc', ),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test org method returns the correct values and calls the get_json once."""
        expected = {"login": org_name, "id": 12345}
        mock_get_json.return_value = expected

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
    
    def test_public_repos_url(self):
        """Test public repos url returns correct url from mocked org"""
        with patch.object(GithubOrgClient, 'org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "https://api.github.com/orgs/test_org/repos"}
            client = GithubOrgClient('test-org')
            self.assertEqual(client._public_repos_url, "https://api.github.com/orgs/test-org/repos")


if __name__ == '__main__':
    unittest.main()