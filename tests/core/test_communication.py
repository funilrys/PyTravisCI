"""
Just another Travis CI (Python) API client.

Test of the communication class.

Author
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Project link
    https://github.com/funilrys/PyTravisCI

License
    ::


        MIT License

        Copyright (c) 2019 Nissar Chababy

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

from collections import OrderedDict
from unittest import TestCase
from unittest import main as launch_test

from PyTravisCI import AccessPoints, TravisCI
from PyTravisCI.communication import Communication
from PyTravisCI.standardize import Standardize


class TestCommunication(TestCase):
    """
    Test of :class:`PyTravisCI.communication.Communication`.
    """

    def setUp(self):
        """
        Setup everything needed for the test.
        """

        self.root = TravisCI(None)

    def test_instance_attr(self):
        """
        Test the case that attribute can be accessible in both methods.

        As a dict :code:`x['y']` or with a direct access :code:`x.y`.
        """

        comm = Communication(self.root)

        comm["hello"] = "world"
        comm.world = "hello"

        self.assertEqual("world", comm.hello)
        self.assertEqual("world", comm["hello"])
        self.assertEqual("hello", comm.world)
        self.assertEqual("hello", comm["world"])

        # pylint: disable=protected-access
        self.assertEqual({}, comm.__parameters)
        self.assertIsInstance(comm.standardize, Standardize)
        self.assertEqual(None, comm.hello_world_hehe)

    def test_bind_path_name_to_access_point(self):
        """
        Test of :meth:`PyTravisCI.communication.Communication.bind_path_name_to_access_point`.
        """

        comm = Communication(self.root)

        expected = f"{AccessPoints.OPEN}/hello"
        actual = comm.bind_path_name_to_access_point(comm.access_point, "hello")

        self.assertEqual(expected, actual)

        expected = f"{AccessPoints.OPEN}/None/hello"
        path_name = None
        actual = comm.bind_path_name_to_access_point(
            comm.access_point, f"{path_name}/hello"
        )

        self.assertEqual(expected, actual)

        expected = f"{AccessPoints.OPEN}/1/hello"
        path_name = 1
        actual = comm.bind_path_name_to_access_point(
            comm.access_point, f"{path_name}/hello"
        )

        self.assertEqual(expected, actual)

        expected = f"{AccessPoints.OPEN}/1/hello"
        path_name = 1
        actual = comm.bind_path_name_to_access_point(
            f"{comm.access_point}/", f"{path_name}/hello"
        )

        self.assertEqual(expected, actual)

        expected = f"{AccessPoints.OPEN}/1534/hello"
        path_name = 1534
        actual = comm.bind_path_name_to_access_point(
            f"{comm.access_point}/", f"/{path_name}/hello"
        )

        self.assertEqual(expected, actual)

        expected = f"{AccessPoints.OPEN}/153/hello"
        path_name = 153
        actual = comm.bind_path_name_to_access_point(
            f"{comm.access_point}", f"/{path_name}/hello"
        )

        self.assertEqual(expected, actual)

        expected = f"{AccessPoints.OPEN}/5"
        path_name = 153
        actual = comm.bind_path_name_to_access_point(f"{comm.access_point}", 5)

        self.assertEqual(expected, actual)

        expected = path_name = "https://github.com/funilrys"
        actual = comm.bind_path_name_to_access_point(comm.access_point, path_name)

        self.assertEqual(expected, actual)

    def test_filter_response(self):
        """
        Test of :meth:`PyTravisCI.communication.Communication.filter_response`.
        """

        response = {
            "@type": "branches",
            "@href": "/repo/891/branches?exists_on_github=true&limit=5",
            "@representation": "standard",
            "@pagination": {
                "limit": 5,
                "offset": 0,
                "count": 24,
                "is_first": True,
                "is_last": False,
                "next": {
                    "@href": "/repo/891/branches?exists_on_github=true&limit=5&offset=5",
                    "offset": 5,
                    "limit": 5,
                },
                "prev": None,
                "first": {
                    "@href": "/repo/891/branches?exists_on_github=true&limit=5",
                    "offset": 0,
                    "limit": 5,
                },
                "last": {
                    "@href": "/repo/891/branches?exists_on_github=true&limit=5&offset=20",
                    "offset": 20,
                    "limit": 5,
                },
            },
            "id": 12345,
            "name": "XYZ",
            "data": {"@href": "XYWJFIWO", "id": 32032, "info": "hello"},
            "dataset": [
                {"@hred": "JOJEFWOFJ", "hello": "info"},
                "hello",
                [1, 23, 4],
                2,
            ],
        }

        expected = {
            "id": 12345,
            "name": "XYZ",
            "data": {"id": 32032, "info": "hello"},
            "dataset": [{"hello": "info"}, "hello", [1, 23, 4], 2],
        }

        comm = Communication(self.root)
        actual = comm.filter_response(response)

        self.assertEqual(expected, actual)

    def test_format_slug(self):
        """
        Test of :meth:`PyTravisCI.communication.Communication.format_slug`.
        """

        comm = Communication(self.root)

        expected = 1
        actual = comm.format_slug(1)

        self.assertEqual(expected, actual)

        expected = "example.org%2Ftest"
        actual = comm.format_slug("example.org/test")

        self.assertEqual(expected, actual)

        expected = "example.org%2Ftest"
        actual = comm.format_slug("example.org%2Ftest")

        self.assertEqual(expected, actual)

    def test_get_error_message(self):
        """
        Test of :meth:`PyTravisCI.communication.Communication.get_error_message`.
        """

        response_without_error = {
            "@type": "home",
            "@href": "/",
            "errors": {
                "login_required": {
                    "status": 403,
                    "default_message": "login required",
                    "additional_attributes": [],
                },
                "method_not_allowed": {
                    "status": 405,
                    "default_message": "method not allowed",
                    "additional_attributes": [],
                },
                "not_found": {
                    "status": 404,
                    "default_message": "resource not found (or insufficient access)",
                    "additional_attributes": ["resource_type"],
                },
            },
        }

        comm = Communication(self.root)

        expected = None
        actual = comm.get_error_message(response_without_error)

        self.assertEqual(expected, actual)

        response_with_error = {
            "@type": "error",
            "error_type": "not_found",
            "error_message": "repository not found (or insufficient access)",
            "resource_type": "repository",
        }

        expected = "repository not found (or insufficient access)"
        actual = comm.get_error_message(response_with_error)

        self.assertEqual(expected, actual)

    def test_get_error_type(self):
        """
        Test of :meth:`PyTravisCI.communication.Communication.get_error_type`.
        """

        response_without_error = {
            "@type": "home",
            "@href": "/",
            "errors": {
                "login_required": {
                    "status": 403,
                    "default_message": "login required",
                    "additional_attributes": [],
                },
                "method_not_allowed": {
                    "status": 405,
                    "default_message": "method not allowed",
                    "additional_attributes": [],
                },
                "not_found": {
                    "status": 404,
                    "default_message": "resource not found (or insufficient access)",
                    "additional_attributes": ["resource_type"],
                },
            },
        }

        comm = Communication(self.root)

        expected = None
        actual = comm.get_error_type(response_without_error)

        self.assertEqual(expected, actual)

        response_with_error = {
            "@type": "error",
            "error_type": "not_found",
            "error_message": "repository not found (or insufficient access)",
            "resource_type": "repository",
        }

        expected = "not_found"
        actual = comm.get_error_type(response_with_error)

        self.assertEqual(expected, actual)

    def test_is_digit(self):
        """
        Test of :meth:`PyTravisCI.communication.Communication.is_digit`.
        """

        comm = Communication(self.root)

        expected = False
        actual = comm.is_digit("hello")

        self.assertEqual(expected, actual)

        expected = True
        actual = comm.is_digit("1")

        self.assertEqual(expected, actual)

        actual = comm.is_digit(1)

        self.assertEqual(expected, actual)

    def test_is_error(self):
        """
        Test of :meth:`PyTravisCI.communication.Communication.is_error`.
        """

        response_without_error = {
            "@type": "home",
            "@href": "/",
            "errors": {
                "login_required": {
                    "status": 403,
                    "default_message": "login required",
                    "additional_attributes": [],
                },
                "method_not_allowed": {
                    "status": 405,
                    "default_message": "method not allowed",
                    "additional_attributes": [],
                },
                "not_found": {
                    "status": 404,
                    "default_message": "resource not found (or insufficient access)",
                    "additional_attributes": ["resource_type"],
                },
            },
        }

        comm = Communication(self.root)

        expected = False
        actual = comm.is_error(response_without_error)

        self.assertEqual(expected, actual)

        response_with_error = {
            "@type": "error",
            "error_type": "not_found",
            "error_message": "repository not found (or insufficient access)",
            "resource_type": "repository",
        }

        expected = True
        actual = comm.is_error(response_with_error)

        self.assertEqual(expected, actual)

    def test_remove_not_needed_parameters(self):
        """
        Test of :meth:`PyTravisCI.communication.Communication.remove_not_needed_parameters`.
        """

        parameters = {"hello": "world", "world": "hello", "test": None, "hehe": "yuhu"}

        comm = Communication(self.root)

        expected = {"hello": "world", "world": "hello", "hehe": "yuhu"}

        actual = comm.remove_not_needed_parameters(parameters)

        self.assertEqual(expected, actual)

    def test_response_to_attribute(self):
        """
        Test of :meth:`PyTravisCI.communication.Communication.response_to_attribute`.
        """

        formatted_response = {"user_setting": {"name": "build_pushes", "value": True}}

        comm = Communication(self.root)

        comm.response_to_attribute(comm, formatted_response)

        expected = {"name": "build_pushes", "value": True}

        self.assertEqual(expected, comm.user_setting)
        self.assertEqual(expected, comm["user_setting"])

    def test_convert_parameters_to_get_param(self):
        """
        Test of :meth:`PyTravisCI.communication.Communication.convert_parameters_to_get_param`.
        """

        # pylint: disable=protected-access

        comm = Communication(self.root)
        comm._parameters = OrderedDict()
        comm._parameters["hello"] = "world"
        comm._parameters["world"] = "hello"
        comm._parameters["repo"] = "example.org/test"
        comm._parameters["this_is_a_test"] = False
        comm._parameters["formatted_repo"] = "example.org%2Ftest"

        comm._excluded_parameters = ["world"]

        expected = (
            "?hello=world&repo=example.org%2Ftest"
            "&this_is_a_test=false&formatted_repo=example.org%2Ftest"
        )
        actual = comm.convert_parameters_to_get_param()

        self.assertEqual(expected, actual)

        comm._parameters = {}

        expected = ""
        actual = comm.convert_parameters_to_get_param()

        self.assertEqual(expected, actual)

    def test_filter_parameters(self):
        """
        Test of :meth:`PyTravisCI.communication.Communication.filter_parameters`.
        """

        # pylint: disable=protected-access

        comm = Communication(self.root)
        comm._parameters = {
            "hello": "world",
            "world": "hello",
            "repo": "example.org/test",
            "formatted_respo": "example.org%2Ftest",
        }

        expected = {
            "hello": "world",
            "world": "hello",
            "repo": "example.org/test",
            "formatted_respo": "example.org%2Ftest",
        }

        comm.filter_parameters({"test": "world"})

        self.assertEqual(expected, comm._parameters)

        expected = {
            "hello": "world",
            "world": "world",
            "repo": "example.org/test",
            "formatted_respo": "example.org%2Ftest",
        }
        comm.filter_parameters({"world": "world"})

        self.assertEqual(expected, comm._parameters)

        self.assertRaises(ValueError, comm.filter_parameters, 1)

    def test_get_url_of_next_page(self):
        """
        Test of :meth:`PyTravisCI.communication.Communication.get_url_of_next_page`.
        """

        response_without_pagination = {
            "@type": "home",
            "@href": "/",
            "errors": {
                "login_required": {
                    "status": 403,
                    "default_message": "login required",
                    "additional_attributes": [],
                },
                "method_not_allowed": {
                    "status": 405,
                    "default_message": "method not allowed",
                    "additional_attributes": [],
                },
                "not_found": {
                    "status": 404,
                    "default_message": "resource not found (or insufficient access)",
                    "additional_attributes": ["resource_type"],
                },
            },
        }

        comm = Communication(self.root)
        expected = None

        actual = comm.get_url_of_next_page(response_without_pagination)

        self.assertEqual(expected, actual)

        response_with_pagination = {
            "@type": "branches",
            "@href": "/repo/891/branches?exists_on_github=true&limit=5",
            "@representation": "standard",
            "@pagination": {
                "limit": 5,
                "offset": 0,
                "count": 24,
                "is_first": True,
                "is_last": False,
                "next": {
                    "@href": "/repo/891/branches?exists_on_github=true&limit=5&offset=5",
                    "offset": 5,
                    "limit": 5,
                },
                "prev": None,
                "first": {
                    "@href": "/repo/891/branches?exists_on_github=true&limit=5",
                    "offset": 0,
                    "limit": 5,
                },
                "last": {
                    "@href": "/repo/891/branches?exists_on_github=true&limit=5&offset=20",
                    "offset": 20,
                    "limit": 5,
                },
            },
        }

        expected = f"{AccessPoints.OPEN}/repo/891/branches?exists_on_github=true&limit=5&offset=5"
        actual = comm.get_url_of_next_page(response_with_pagination)

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_test()
