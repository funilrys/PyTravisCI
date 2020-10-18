"""
Just another Python API for Travis CI (API).

A module which provides the tests of our requester module.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Project link:
    https://github.com/funilrys/PyTravisCI

Project documentation:
    https://pytravisci.readthedocs.io/en/latest/

License
::


    MIT License

    Copyright (c) 2019, 2020 Nissar Chababy

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

import json
import secrets
from unittest import TestCase
from unittest import main as launch_tests
from unittest.mock import patch

import requests

from PyTravisCI.__about__ import __version__
from PyTravisCI.exceptions import TravisCIError
from PyTravisCI.requester import Requester


class RequesterTest(TestCase):
    """
    Provides the tests of the requester class.
    """

    # pylint: disable=too-many-public-methods

    def test_default_header(self) -> None:
        """
        Tests if the expected header is set.
        """

        expected_api_version = "3"
        expected_user_agent = f"PyTravisCI/{__version__}"
        expected = {
            "Travis-API-Version": expected_api_version,
            "User-Agent": expected_user_agent,
        }

        requester = Requester()

        actual = requester.session.headers

        self.assertDictContainsSubset(expected, actual)

    def test_authorization_header(self) -> None:
        """
        Tests if the authorization header is correctly set.
        """

        given_token = secrets.token_urlsafe(16)
        expected = {"Authorization": f"token {given_token}"}

        requester = Requester()
        requester.set_authorization(given_token)

        actual = requester.session.headers

        self.assertDictContainsSubset(expected, actual)

    def test_authorization_header_non_string(self) -> None:
        """
        Tests that the method which let us communicate the token
        raises an exception if a non-string value is given.
        """

        given = True
        requester = Requester()

        self.assertRaises(TypeError, lambda: requester.set_authorization(given))

    def test_set_base_url(self) -> None:
        """
        Tests of the method which let us communicate the base url.
        """

        given_base_url = "https://example.org/api"
        expected = "https://example.org/api"

        requester = Requester()
        requester.set_base_url(given_base_url)

        actual = requester.base_url

        self.assertEqual(expected, actual)

    def test_set_base_url_ends_with_with_slash(self) -> None:
        """
        Tests of the method which let us communicate the base url for the case
        that a slash is given at the end of the URL.
        """

        given_base_url = "https://example.org/api/"
        expected = "https://example.org/api"

        requester = Requester()
        requester.set_base_url(given_base_url)

        actual = requester.base_url

        self.assertEqual(expected, actual)

    def test_set_base_url_non_string(self) -> None:
        """
        Tests of the method which let us communicate the base url for the case
        that a non-string is given.
        """

        given = True

        requester = Requester()

        self.assertRaises(TypeError, lambda: requester.set_base_url(given))

    def test_bind_endpoint_to_base_url(self) -> None:
        """
        Tests of the method which let us bind an endpoint with the previously
        given base url.
        """

        given_base_url = "https://example.org/api"
        given_endpoint = "hello/world"
        expected = "https://example.org/api/hello/world"

        requester = Requester()
        requester.set_base_url(given_base_url)

        actual = requester.bind_endpoint_to_base_url(given_endpoint)

        self.assertEqual(expected, actual)

    def test_bind_endpoint_to_base_url_endpoint_starts_with_slash(self) -> None:
        """
        Tests of the method which let us bind an endpoint with the previously
        given base url for the case that the given endpoint starts with a slash.
        """

        given_base_url = "https://example.org/api"
        given_endpoint = "/hello/world"

        expected = "https://example.org/api/hello/world"

        requester = Requester()
        requester.set_base_url(given_base_url)

        actual = requester.bind_endpoint_to_base_url(given_endpoint)

        self.assertEqual(expected, actual)

    def test_bind_endpoint_to_base_url_endpoint_not_string(self) -> None:
        """
        Tests of the method which let us bind an endpoint with the previouly
        given base url for the case that the given endpoint is a non-string.
        """

        given_base_url = "https://example.org/api"
        given_endpoint = True

        requester = Requester()
        requester.set_base_url(given_base_url)

        self.assertRaises(
            TypeError, lambda: requester.bind_endpoint_to_base_url(given_endpoint)
        )

    def test_is_error(self) -> None:
        """
        Tests of the method which checks if the API response is an error.
        """

        expected = True
        given = {
            "@type": "error",
            "error_type": "not_found",
            "error_message": "repository not found (or insufficient access)",
            "resource_type": "repository",
        }

        actual = Requester.is_error(given)

        self.assertEqual(expected, actual)

    def test_is_error_not_error(self) -> None:
        """
        Tests of the method whixh checks if the API response is an error for the
        case that a normal resource type is given.
        """

        expected = False
        given = {
            "@type": "user",
            "@href": "/user/4549848944894848948949",
            "@representation": "standard",
            "@permissions": {"read": True, "sync": True},
            "id": 4549848944894848948949,
            "login": "foobar",
            "name": "Foo Bar",
            "github_id": 1148942198798789784897949849484523106,
            "vcs_id": "1148942198798789784897949849484523106",
            "vcs_type": "GithubUser",
            "avatar_url": None,
            "education": False,
            "allow_migration": False,
            "email": "foo@example.org",
            "is_syncing": False,
            "synced_at": "2020-10-14T14:53:08Z",
            "recently_signed_up": False,
            "secure_user_hash": None,
        }

        actual = Requester.is_error(given)

        self.assertEqual(expected, actual)

    def test_get_error_message(self) -> None:
        """
        Tests of the method which let us get the actual error message.
        """

        given = {
            "@type": "error",
            "error_type": "not_found",
            "error_message": "repository not found (or insufficient access)",
            "resource_type": "repository",
        }
        expected = "repository not found (or insufficient access)"

        actual = Requester.get_error_message(given)

        self.assertEqual(expected, actual)

    def test_get_error_message_not_error(self) -> None:
        """
        Tests of the method which let us get the actual error message for the
        case that no error is actually given.
        """

        given = {
            "@type": "user",
            "@href": "/user/4549848944894848948949",
            "@representation": "standard",
            "@permissions": {"read": True, "sync": True},
            "id": 4549848944894848948949,
            "login": "foobar",
            "name": "Foo Bar",
            "github_id": 1148942198798789784897949849484523106,
            "vcs_id": "1148942198798789784897949849484523106",
            "vcs_type": "GithubUser",
            "avatar_url": None,
            "education": False,
            "allow_migration": False,
            "email": "foo@example.org",
            "is_syncing": False,
            "synced_at": "2020-10-14T14:53:08Z",
            "recently_signed_up": False,
            "secure_user_hash": None,
        }
        expected = None

        actual = Requester.get_error_message(given)

        self.assertEqual(expected, actual)

    def test_get_error_message_already_checked(self) -> None:
        """
        Tests of the method which let us get the actual error message for the
        case that we already know that it is an error.
        """

        given = {
            "@type": "error",
            "error_type": "not_found",
            "error_message": "repository not found (or insufficient access)",
            "resource_type": "repository",
        }
        expected = "repository not found (or insufficient access)"

        actual = Requester.get_error_message(given, already_checked=True)

        self.assertEqual(expected, actual)

    def test_get_error_message_fake_already_checked(self) -> None:
        """
        Tests of the method which let us get the actual error message for the
        case that we "already know" that it is an error but it was just fake.
        """

        given = {
            "@type": "user",
            "@href": "/user/4549848944894848948949",
            "@representation": "standard",
            "@permissions": {"read": True, "sync": True},
            "id": 4549848944894848948949,
            "login": "foobar",
            "name": "Foo Bar",
            "github_id": 1148942198798789784897949849484523106,
            "vcs_id": "1148942198798789784897949849484523106",
            "vcs_type": "GithubUser",
            "avatar_url": None,
            "education": False,
            "allow_migration": False,
            "email": "foo@example.org",
            "is_syncing": False,
            "synced_at": "2020-10-14T14:53:08Z",
            "recently_signed_up": False,
            "secure_user_hash": None,
        }

        self.assertRaises(
            KeyError, lambda: Requester.get_error_message(given, already_checked=True)
        )

    def test_get_error_type(self) -> None:
        """
        Tests of the method which let us get the actual error type.
        """

        given = {
            "@type": "error",
            "error_type": "not_found",
            "error_message": "repository not found (or insufficient access)",
            "resource_type": "repository",
        }
        expected = "not_found"

        actual = Requester.get_error_type(given)

        self.assertEqual(expected, actual)

    def test_get_error_type_not_error(self) -> None:
        """
        Tests of the method which let us get the actual error type for the
        case that no error is actually given.
        """

        given = {
            "@type": "user",
            "@href": "/user/4549848944894848948949",
            "@representation": "standard",
            "@permissions": {"read": True, "sync": True},
            "id": 4549848944894848948949,
            "login": "foobar",
            "name": "Foo Bar",
            "github_id": 1148942198798789784897949849484523106,
            "vcs_id": "1148942198798789784897949849484523106",
            "vcs_type": "GithubUser",
            "avatar_url": None,
            "education": False,
            "allow_migration": False,
            "email": "foo@example.org",
            "is_syncing": False,
            "synced_at": "2020-10-14T14:53:08Z",
            "recently_signed_up": False,
            "secure_user_hash": None,
        }
        expected = None

        actual = Requester.get_error_type(given)

        self.assertEqual(expected, actual)

    def test_get_error_type_already_checked(self) -> None:
        """
        Tests of the method which let us get the actual error type for the
        case that we already know that it is an error.
        """

        given = {
            "@type": "error",
            "error_type": "not_found",
            "error_message": "repository not found (or insufficient access)",
            "resource_type": "repository",
        }
        expected = "not_found"

        actual = Requester.get_error_type(given, already_checked=True)

        self.assertEqual(expected, actual)

    def test_get_error_type_fake_already_checked(self) -> None:
        """
        Tests of the method which let us get the actual error type for the
        case that we "already know" that it is an error but it was just fake.
        """

        given = {
            "@type": "user",
            "@href": "/user/4549848944894848948949",
            "@representation": "standard",
            "@permissions": {"read": True, "sync": True},
            "id": 4549848944894848948949,
            "login": "foobar",
            "name": "Foo Bar",
            "github_id": 1148942198798789784897949849484523106,
            "vcs_id": "1148942198798789784897949849484523106",
            "vcs_type": "GithubUser",
            "avatar_url": None,
            "education": False,
            "allow_migration": False,
            "email": "foo@example.org",
            "is_syncing": False,
            "synced_at": "2020-10-14T14:53:08Z",
            "recently_signed_up": False,
            "secure_user_hash": None,
        }

        self.assertRaises(
            KeyError, lambda: Requester.get_error_type(given, already_checked=True)
        )

    def test_raise_if_error(self) -> None:
        """
        Tests of the method which actually raises the exception when the
        API response is an error.
        """

        given = {
            "@type": "error",
            "error_type": "not_found",
            "error_message": "repository not found (or insufficient access)",
            "resource_type": "repository",
        }

        fake_response = requests.Response()
        fake_response.url = "https://example.org"

        self.assertRaises(
            TravisCIError, lambda: Requester.raise_if_error(fake_response, given)
        )

    def test_raise_if_error_not_error(self) -> None:
        """
        Tests of the method which actually raises the exception when the
        API response is an error, but for the case that no error
        is given (in the api_response)
        """

        given = {
            "@type": "user",
            "@href": "/user/4549848944894848948949",
            "@representation": "standard",
            "@permissions": {"read": True, "sync": True},
            "id": 4549848944894848948949,
            "login": "foobar",
            "name": "Foo Bar",
            "github_id": 1148942198798789784897949849484523106,
            "vcs_id": "1148942198798789784897949849484523106",
            "vcs_type": "GithubUser",
            "avatar_url": None,
            "education": False,
            "allow_migration": False,
            "email": "foo@example.org",
            "is_syncing": False,
            "synced_at": "2020-10-14T14:53:08Z",
            "recently_signed_up": False,
            "secure_user_hash": None,
        }
        expected = None

        fake_response = requests.Response()
        fake_response.url = "https://example.org"

        actual = Requester.raise_if_error(fake_response, given)

        self.assertEqual(expected, actual)

    @patch.object(requests.Session, "get")
    def test_request_factory(self, mock_session_get):
        """
        Tests of the request factory.
        """
        given_base_url = "https://example.org/api/"
        given_endpoint = "hello/world"

        response = {
            "@type": "user",
            "@href": "/user/4549848944894848948949",
            "@representation": "standard",
            "@permissions": {"read": True, "sync": True},
            "id": 4549848944894848948949,
            "login": "foobar",
            "name": "Foo Bar",
            "github_id": 1148942198798789784897949849484523106,
            "vcs_id": "1148942198798789784897949849484523106",
            "vcs_type": "GithubUser",
            "avatar_url": None,
            "education": False,
            "allow_migration": False,
            "email": "foo@example.org",
            "is_syncing": False,
            "synced_at": "2020-10-14T14:53:08Z",
            "recently_signed_up": False,
            "secure_user_hash": None,
        }

        requester = Requester()
        requester.set_base_url(given_base_url)

        mock_session_get.return_value.headers = dict()
        mock_session_get.return_value.status_code = 200
        mock_session_get.return_value.url = "https://example.org/api/hello/world"
        mock_session_get.return_value.json.return_value = response

        expected = response

        actual = requester.get(given_endpoint)

        self.assertEqual(expected, actual)

    @patch.object(requests.Session, "get")
    def test_request_factory_no_json_response(self, mock_session_get):
        """
        Tests of the request factory for the case that no JSON is given as response.
        """
        given_base_url = "https://example.org/api/"
        given_endpoint = "hello/world"

        response = {
            "@type": "user",
            "@href": "/user/4549848944894848948949",
            "@representation": "standard",
            "@permissions": {"read": True, "sync": True},
            "id": 4549848944894848948949,
            "login": "foobar",
            "name": "Foo Bar",
            "github_id": 1148942198798789784897949849484523106,
            "vcs_id": "1148942198798789784897949849484523106",
            "vcs_type": "GithubUser",
            "avatar_url": None,
            "education": False,
            "allow_migration": False,
            "email": "foo@example.org",
            "is_syncing": False,
            "synced_at": "2020-10-14T14:53:08Z",
            "recently_signed_up": False,
            "secure_user_hash": None,
        }

        requester = Requester()
        requester.set_base_url(given_base_url)

        mock_session_get.return_value.headers = dict()
        mock_session_get.return_value.status_code = 200
        mock_session_get.return_value.url = "https://example.org/api/hello/world"
        mock_session_get.return_value.text = json.dumps(response)
        mock_session_get.return_value.json.side_effect = json.decoder.JSONDecodeError(
            "hello", "world", 33
        )

        self.assertRaises(TravisCIError, lambda: requester.get(given_endpoint))

    @patch.object(requests.Session, "get")
    def test_request_factory_empty_esponse(self, mock_session_get):
        """
        Tests of the request factory for the case that an empty response is
        given (back).
        """
        given_base_url = "https://example.org/api/"
        given_endpoint = "hello/world"

        requester = Requester()
        requester.set_base_url(given_base_url)

        mock_session_get.return_value.status_code = 200
        mock_session_get.return_value.headers = dict()
        mock_session_get.return_value.url = "https://example.org/api/hello/world"
        mock_session_get.return_value.text = ""
        mock_session_get.return_value.json.side_effect = json.decoder.JSONDecodeError(
            "hello", "world", 33
        )

        self.assertRaises(TravisCIError, lambda: requester.get(given_endpoint))


if __name__ == "__main__":
    launch_tests()
