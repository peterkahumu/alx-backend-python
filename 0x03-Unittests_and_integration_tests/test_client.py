#!/usr/bin/env python3

"""Unit tests for client.py using mock and parameterized."""
import unittest
from unittest.mock import patch, PropertyMock, MagicMock
from parameterized import parameterized, parameterized_class

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


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
       
    @parameterized.expand([
        (
            {"license": {"key": "my_license"}}, "my_license", True
        ),
        (
            {"license": {"key": "other_license"}}, "my_license", False
        ),
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test has_license returns True when license matches,
        otherwise False.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch('requests.get')
        mock_get = cls.get_patcher.start()

        def mock_get_json(url, *args, **kwargs):
            if url == "https://api.github.com/orgs/test-org":
                mock_resp = MagicMock()
                mock_resp.json.return_value = cls.org_payload
                return mock_resp
            elif url == cls.org_payload["repos_url"]:
                mock_resp = MagicMock()
                mock_resp.json.return_value = cls.repos_payload
                return mock_resp
            else:
                raise ValueError(f"Unexpected URL: {url}")

        mock_get.side_effect = mock_get_json

    @classmethod
    def tearDownClass(cls):
        """Stop patcher after tests"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repos from fixtures"""
        client = GithubOrgClient("test-org")
        result = client.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Test public_repos filters repos by license='apache-2.0'
        using fixture data.
        """
        client = GithubOrgClient("test-org")
        result = client.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)


if __name__ == '__main__':
    unittest.main()
