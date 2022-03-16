"""
Just another Python API for Travis CI (API).

A module which provides the tests of our communicator base class.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Project link:
    https://github.com/funilrys/PyTravisCI

Project documentation:
    https://pytravisci.readthedocs.io/en/latest/

License
::


    MIT License

    Copyright (c) 2019, 2020, 2021, 2022 Nissar Chababy

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


from unittest import TestCase
from unittest import main as launch_tests

from PyTravisCI.communicator.base import CommunicatorBase
from PyTravisCI.resource_types.base import ResourceTypesBase


class TestCommunicatorBase(TestCase):
    """
    Provides the tests of the communicator base class.
    """

    def test_propagate_vars(self) -> None:
        """
        Tests of the method which let us propagate some variables
        across a given object.
        """

        given_response = {
            "_at_type": "user",
            "_at_href": "/user/4549848944894848948949",
            "_at_representation": "standard",
            "_at_permissions": {"read": True, "sync": True},
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
            "usernames": ["foo", "bar"],
        }
        given_response["sub_users"] = ResourceTypesBase(**given_response)
        given_response["sub_users"]["_PyTravisCI_secret"] = given_response[
            "_PyTravisCI_secret"
        ] = "huhu"

        given_resource = ResourceTypesBase(**given_response)

        to_propagate = {
            "_PyTravisCI": {"hello": "world"},
            "_PyTravisCI_internal": "hello",
            "_PyTravisCI_secret": "ThIsAsEcReTdOoR",
        }

        actual = CommunicatorBase.propagate_internal_vars(to_propagate, given_resource)

        self.assertDictContainsSubset(
            to_propagate["_PyTravisCI"], actual["_PyTravisCI"]
        )
        self.assertDictContainsSubset(
            to_propagate["_PyTravisCI"], actual["sub_users"]["_PyTravisCI"]
        )

        self.assertEqual(
            to_propagate["_PyTravisCI_internal"], actual["_PyTravisCI_internal"]
        )
        self.assertEqual(
            to_propagate["_PyTravisCI_internal"],
            actual["sub_users"]["_PyTravisCI_internal"],
        )

        self.assertEqual(
            to_propagate["_PyTravisCI_secret"], actual["_PyTravisCI_secret"]
        )
        self.assertEqual(
            to_propagate["_PyTravisCI_secret"],
            actual["sub_users"]["_PyTravisCI_secret"],
        )

    def test_is_digit(self) -> None:
        """
        Tests of the method which check if the given data is a digit.
        """

        given = 3
        expected = True

        actual = CommunicatorBase.is_digit(given)

        self.assertEqual(expected, actual)

        given = "3"

        actual = CommunicatorBase.is_digit(given)

        self.assertEqual(expected, actual)

    def test_is_not_digit(self) -> None:
        """
        Tests of the method which check if the given data is a digit for the
        case the it's actually no digit.
        """

        given = False
        expected = False

        actual = CommunicatorBase.is_digit(given)

        self.assertEqual(expected, actual)

        given = {"hello": "world"}

        actual = CommunicatorBase.is_digit(given)

        self.assertEqual(expected, actual)

        given = " 3"

        actual = CommunicatorBase.is_digit(given)

        self.assertEqual(expected, actual)

    def test_encode_slug(self) -> None:
        """
        Tests of the method which let us encode a given repository slug.
        """

        expected = "hello%2Fworld"
        given = "hello/world"

        actual = CommunicatorBase.encode_slug(given)

        self.assertEqual(expected, actual)

    def test_encode_not_slug(self) -> None:
        """
        Tests of the method which let us encode a given repository slug for
        the case that a slug is not given.
        """

        expected = "Hello, World!"

        given = "Hello, World!"

        actual = CommunicatorBase.encode_slug(given)

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
