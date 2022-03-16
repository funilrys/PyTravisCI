"""
Just another Python API for Travis CI (API).

A module which provides the tests of our resource types base class.

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

import copy
import json
from datetime import datetime
from unittest import TestCase
from unittest import main as launch_tests

from PyTravisCI.resource_types.base import ResourceTypesBase


class TestResourceTypesBase(TestCase):
    """
    Provides the tests of the resource types base class.
    """

    # pylint: disable=too-many-public-methods

    given_data: dict = {
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
        "synced_at": datetime(2020, 10, 14, 15, 53, 8),
        "recently_signed_up": False,
        "secure_user_hash": None,
        "usernames": ["foo", "bar"],
    }

    given_data_minimal: dict = {
        "_at_type": "user",
        "_at_href": "/user/4549848944894848948949",
        "_at_representation": "minimal",
        "id": 4549848944894848948949,
        "name": "Foo Bar",
        "login": "foobar",
    }

    pagination_data: dict = {
        "_at_type": "branches",
        "_at_href": "/repo/891/branches?exists_on_github=true&limit=5",
        "_at_representation": "standard",
        "_at_pagination": {
            "limit": 5,
            "offset": 0,
            "count": 24,
            "is_first": True,
            "is_last": False,
            "next": {
                "_at_href": "/repo/25387022/branches?exists_on_github=true&limit=5&offset=5",
                "offset": 5,
                "limit": 5,
            },
            "prev": {
                "_at_href": "/repo/25387022/branches?exists_on_github=true&limit=0&offset=5",
                "offset": 0,
                "limit": 5,
            },
            "first": {
                "_at_href": "/repo/25387022/branches?exists_on_github=true&limit=5",
                "offset": 0,
                "limit": 5,
            },
            "last": {
                "_at_href": "/repo/25387022/branches?exists_on_github=true&limit=5&offset=20",
                "offset": 20,
                "limit": 5,
            },
        },
    }

    def test_init(self) -> None:
        """
        Tests of the method which let us initiate a resource type.
        """

        resource = ResourceTypesBase(**self.given_data)

        for index, value in self.given_data.items():
            self.assertEqual(value, resource.__dict__[index])

    def test_getitem(self) -> None:
        """
        Tests of the getitem method.
        """

        resource = ResourceTypesBase(**self.given_data)

        for index, value in self.given_data.items():
            self.assertEqual(value, resource[index])

    def test_getitem_not_set(self) -> None:
        """
        Tests of the getitem method for the case that we want to access an
        unexistant attribute.
        """

        resource = ResourceTypesBase(**self.given_data)

        self.assertRaises(AttributeError, lambda: resource["hello_world"])

    def test_getitem_through_iter(self) -> None:
        """
        Tests of the getitem method for the case that we declar an
        index/attribute to iter through.
        """

        given_data = {
            "__iter_through__": "users",
            "users": [self.given_data for _ in range(3)],
        }

        resource = ResourceTypesBase(**given_data)

        self.assertEqual(given_data["users"][2], resource[2])

    def test_repr(self) -> None:
        """
        Tests of the repr method.
        """

        given_data = {"hello": "world", "world": "hello"}

        resource = ResourceTypesBase(**given_data)

        expected = f"<ResourceTypesBase {given_data} />"
        actual = repr(resource)

        self.assertEqual(expected, actual)

    def test_setattr(self) -> None:
        """
        Tests of the setattr method.
        """

        expected = "Hello, World!"
        resource = ResourceTypesBase(**self.given_data)

        # pylint: disable=protected-access
        resource._PyTravisCI = "Hello, World!"
        actual = resource._PyTravisCI

        self.assertEqual(expected, actual)

    def test_setattr_overwrite(self) -> None:
        """
        Tests of the setattr method for the case that we want to overwrite all
        attributes.
        """

        to_overwrite = {
            "_at_type": "user",
            "_at_href": "/user/5555555555555555555555555555555",
            "_at_representation": "standard",
            "_at_permissions": {"read": True, "sync": True},
            "id": 5555555555555555555555555555555,
            "login": "foobar",
            "name": "Foo Bar",
            "github_id": 5555555555555555555555555555555,
            "vcs_id": "5555555555555555555555555555555",
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
        resource = ResourceTypesBase(**self.given_data)

        resource.__dict__ = to_overwrite

        for index, value in to_overwrite.items():
            self.assertEqual(value, resource[index])

    def test_setattr_unauthorized(self) -> None:
        """
        Tests of the setattr method for the case that we want to manually
        overwrite an attribute.
        """

        resource = ResourceTypesBase(**self.given_data)

        self.assertRaises(AttributeError, lambda: resource.__setattr__("name", "hello"))

    def test_setitem(self) -> None:
        """
        Tests of the setitem method.
        """

        expected = "Hello, World!"
        resource = ResourceTypesBase(**self.given_data)

        # pylint: disable=protected-access
        resource["_PyTravisCI"] = "Hello, World!"
        actual = resource["_PyTravisCI"]

        self.assertEqual(expected, actual)

    def test_setitem_overwrite(self) -> None:
        """
        Tests of the item method for the case that we want to overwrite all
        attributes.
        """

        to_overwrite = {
            "_at_type": "user",
            "_at_href": "/user/5555555555555555555555555555555",
            "_at_representation": "standard",
            "_at_permissions": {"read": True, "sync": True},
            "id": 5555555555555555555555555555555,
            "login": "foobar",
            "name": "Foo Bar",
            "github_id": 5555555555555555555555555555555,
            "vcs_id": "5555555555555555555555555555555",
            "vcs_type": "GithubUser",
            "avatar_url": None,
            "education": False,
            "allow_migration": False,
            "email": "foo@example.org",
            "is_syncing": False,
            "synced_at": "2020-10-14T14:53:08Z",
            "recently_signed_up": False,
            "secure_user_hash": None,
            "usernames": ["hehehe", "huhuhu"],
        }
        resource = ResourceTypesBase(**self.given_data)

        resource["__dict__"] = to_overwrite

        for index, value in to_overwrite.items():
            self.assertEqual(value, resource[index])

    def test_setitem_unauthorized(self) -> None:
        """
        Tests of the setitem method for the case that we want to manually
        overwrite an attribute.
        """

        resource = ResourceTypesBase(**self.given_data)

        self.assertRaises(AttributeError, lambda: resource.__setitem__("name", "hello"))

    def test_iteration(self) -> None:
        """
        Tests of the iteration capabilities.
        """

        given_data = {
            "__iter_through__": "users",
            "users": [self.given_data for _ in range(3)],
        }

        resource = ResourceTypesBase(**given_data)

        for index, data in enumerate(resource):
            self.assertEqual(given_data["users"][index], data)

    def test_iteration_nothing_to_iter(self) -> None:
        """
        Tests of the iteration capabilities for the case that there is nothing
        to iterate through.
        """

        resource = ResourceTypesBase(**self.given_data)

        self.assertRaises(NotImplementedError, lambda: enumerate(resource))

    def test_equality(self) -> None:
        """
        Tests of the equality comparison.
        """

        first_resource = ResourceTypesBase(**self.given_data)
        second_resource = ResourceTypesBase(**self.given_data)

        expected = True
        actual = first_resource == second_resource

        self.assertEqual(expected, actual)

    def test_not_equality(self) -> None:
        """
        Tests of the (not) equallity comparison.
        """

        given_data = {
            "__iter_through__": "users",
            "users": [self.given_data for _ in range(3)],
        }

        first_resource = ResourceTypesBase(**self.given_data)
        second_resource = ResourceTypesBase(**given_data)

        expected = False
        actual = first_resource == second_resource

        self.assertEqual(expected, actual)

    def test_inequality(self) -> None:
        """
        Tests of the inquallity comparison.
        """

        given_data = {
            "__iter_through__": "users",
            "users": [self.given_data for _ in range(3)],
        }

        first_resource = ResourceTypesBase(**self.given_data)
        second_resource = ResourceTypesBase(**given_data)

        expected = True
        actual = first_resource != second_resource

        self.assertEqual(expected, actual)

    def test_not_inequality(self) -> None:
        """
        Tests of the (not) inquallity comparison.
        """

        first_resource = ResourceTypesBase(**self.given_data)
        second_resource = ResourceTypesBase(**self.given_data)

        expected = False
        actual = first_resource != second_resource

        self.assertEqual(expected, actual)

    def test_json(self) -> None:
        """
        Tests of the method which let us convert to JSON.
        """

        expected = {
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
            "synced_at": "2020-10-14T15:53:08Z",
            "recently_signed_up": False,
            "secure_user_hash": None,
            "usernames": ["foo", "bar"],
        }

        resource = ResourceTypesBase(**self.given_data)
        converted = resource.json()

        self.assertIsInstance(converted, str)

        self.assertEqual(expected, json.loads(converted))

    def test_to_json(self) -> None:
        """
        Tests of the method which let us convert to JSON.
        """

        expected_base = {
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
            "synced_at": "2020-10-14T15:53:08Z",
            "recently_signed_up": False,
            "secure_user_hash": None,
            "usernames": ["foo", "bar"],
        }

        expected = copy.deepcopy(expected_base)
        expected["related_user"] = expected_base

        given_data = copy.deepcopy(self.given_data)
        given_data["related_user"] = ResourceTypesBase(**given_data)

        resource = ResourceTypesBase(**given_data)
        converted = resource.to_json()

        self.assertIsInstance(converted, str)

        self.assertEqual(expected, json.loads(converted))

    def test_to_json_tags_not_wanted(self) -> None:
        """
        Tests of the method which let us convert to JSON for the case that
        we don't want any tags.
        """

        expected = {
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
            "synced_at": "2020-10-14T15:53:08Z",
            "recently_signed_up": False,
            "secure_user_hash": None,
            "usernames": ["foo", "bar"],
        }

        resource = ResourceTypesBase(**self.given_data)
        converted = resource.to_json(remove_tags=True)

        self.assertIsInstance(converted, str)

        self.assertEqual(expected, json.loads(converted))

    def test_dict(self) -> None:
        """
        Tests of the method which let us convert to :py:class:`dict`.
        """

        expected = {
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
            "synced_at": "2020-10-14T15:53:08Z",
            "recently_signed_up": False,
            "secure_user_hash": None,
            "usernames": ["foo", "bar"],
        }

        resource = ResourceTypesBase(**self.given_data)
        actual = resource.dict()

        self.assertIsInstance(actual, dict)

        self.assertEqual(expected, actual)

    def test_to_dict(self) -> None:
        """
        Tests of the method which let us convert to :py:class:`dict`.
        """

        expected = {
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
            "synced_at": "2020-10-14T15:53:08Z",
            "recently_signed_up": False,
            "secure_user_hash": None,
            "usernames": ["foo", "bar"],
        }

        resource = ResourceTypesBase(**self.given_data)
        actual = resource.to_dict()

        self.assertIsInstance(actual, dict)

        self.assertEqual(expected, actual)

    def test_to_dict_deep_relationships(self) -> None:
        """
        Tests of the method which let us convert to :py:class:`dict` for the
        case that we have some nested resources.
        """

        expected_base = {
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
            "synced_at": "2020-10-14T15:53:08Z",
            "recently_signed_up": False,
            "secure_user_hash": None,
            "usernames": ["foo", "bar"],
        }

        expected = copy.deepcopy(expected_base)
        expected["related_user"] = copy.deepcopy(expected_base)

        given_data = copy.deepcopy(self.given_data)
        given_data["related_user"] = ResourceTypesBase(**given_data)

        resource = ResourceTypesBase(**given_data)
        actual = resource.to_dict()

        self.assertIsInstance(actual, dict)

        self.assertEqual(expected, actual)

    def test_to_dict_tags_not_wanted(self) -> None:
        """
        Tests of the method which let us convert to :py:class:`dict` for the
        case that we don't want any tags.
        """

        expected = {
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
            "synced_at": "2020-10-14T15:53:08Z",
            "recently_signed_up": False,
            "secure_user_hash": None,
            "usernames": ["foo", "bar"],
        }

        given_data = copy.deepcopy(self.given_data)
        given_data["_PyTravisCI"] = {"hello": "world"}

        resource = ResourceTypesBase(**given_data)
        actual = resource.to_dict(remove_tags=True)

        self.assertIsInstance(actual, dict)

        self.assertEqual(expected, actual)

    def test_has_next_page(self):
        """
        Tests of the method which let us check if the current resource has
        a next page.
        """

        resource = ResourceTypesBase(**self.pagination_data)

        expected = True
        actual = resource.has_next_page()

        self.assertEqual(expected, actual)

    def test_has_next_page_not(self):
        """
        Tests of the methods which let us check if the current resource has
        a next page for the case that there is no pager.
        """

        resource = ResourceTypesBase(**self.given_data)

        expected = False
        actual = resource.has_next_page()

        self.assertEqual(expected, actual)

    def test_has_previous_page(self):
        """
        Tests of the method which let us check if the current resource has
        a previous page.
        """

        resource = ResourceTypesBase(**self.pagination_data)

        expected = True
        actual = resource.has_previous_page()

        self.assertEqual(expected, actual)

    def test_has_previous_page_not(self):
        """
        Tests of the methods which let us check if the current resource has
        a previous page for the case that there is no pager.
        """

        resource = ResourceTypesBase(**self.given_data)

        expected = False
        actual = resource.has_previous_page()

        self.assertEqual(expected, actual)

    def test_has_first_page(self):
        """
        Tests of the method which let us check if the current resource has
        a first page.
        """

        resource = ResourceTypesBase(**self.pagination_data)

        expected = True
        actual = resource.has_first_page()

        self.assertEqual(expected, actual)

    def test_has_first_page_not(self):
        """
        Tests of the methods which let us check if the current resource has
        a previous page for the case that there is no pager.
        """

        resource = ResourceTypesBase(**self.given_data)

        expected = False
        actual = resource.has_first_page()

        self.assertEqual(expected, actual)

    def test_has_last_page(self):
        """
        Tests of the method which let us check if the current resource has
        a last page.
        """

        resource = ResourceTypesBase(**self.pagination_data)

        expected = True
        actual = resource.has_last_page()

        self.assertEqual(expected, actual)

    def test_has_last_page_not(self):
        """
        Tests of the methods which let us check if the current resource has
        a last page for the case that there is no pager.
        """

        resource = ResourceTypesBase(**self.given_data)

        expected = False
        actual = resource.has_last_page()

        self.assertEqual(expected, actual)

    def test_is_incomplete(self):
        """
        Tests of the method which let us check if the current resource is
        incomplete.
        """

        resource = ResourceTypesBase(**self.given_data_minimal)

        expected = True
        actual = resource.is_incomplete()

        self.assertEqual(expected, actual)

    def test_is_not_incomplete(self):
        """
        Tests of the method which let us check if the current resource is
        incomplete for the case that it is not actually incomplete.
        """

        resource = ResourceTypesBase(**self.given_data)

        expected = False
        actual = resource.is_incomplete()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
