#!/usr/bin/env python3

"""Unit tests for client.py using mock and parameterized."""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test GithubOrgClient class"""

    @parameterized.expand([
        ('google',),
        ('abc',),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Test org returns correct values and get_json is called once
        with the expected URL.
        """
        expected = {"login": org_name, "id": 12345}
        mock_get_json.return_value = expected

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """
        Test _public_repos_url returns correct URL based on mocked org
        payload.
        """
        with patch.object(
            GithubOrgClient, 'org', new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/test-org/repos"
            }
            client = GithubOrgClient('test-org')
            self.assertEqual(
                client._public_repos_url,
                "https://api.github.com/orgs/test-org/repos"
            )

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Test public_repos returns expected list of repo names and that
        both get_json and _public_repos_url are called once.
        """
        mock_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = mock_payload

        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = (
                "https://api.github.com/orgs/test-org/repos"
            )

            client = GithubOrgClient("test-org")
            repos = client.public_repos()

            self.assertEqual(repos, ["repo1", "repo2", "repo3"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/test-org/repos"
            )


if __name__ == '__main__':
    unittest.main()
