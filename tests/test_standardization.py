"""
Just another Travis CI (API) Python interface.

A module which provides the tests of our standardization module.

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

from datetime import datetime
from typing import List
from unittest import TestCase
from unittest import main as launch_tests

from PyTravisCI.standardization import Standardization


class TestStandardization(TestCase):
    """
    Tests of the standardization class.
    """

    datetime_indexes: List[str] = [
        "committed_at",
        "created_at",
        "finished_at",
        "last_modified",
        "last_run",
        "next_run",
        "started_at",
        "synced_at",
        "updated_at",
    ]

    STANDARD_DATE_FORMAT: str = "%Y-%m-%dT%H:%M:%SZ"
    ALTERNATIVE_DATE_FORMAT: str = "%Y-%m-%dT%H:%M:%S.%fZ"

    def test_get_and_set_data(self) -> None:
        """
        Tests the methods which are supposed to update the data to work with.
        """

        expected = {"hello": "world"}
        standardization = Standardization()
        standardization.set_data({"hello": "world"})

        actual = standardization.get_data()

        self.assertEqual(expected, actual)

        expected = {"world": "hello"}

        standardization.set_data({"world": "hello"})
        actual = standardization.get_data()

        self.assertEqual(expected, actual)

    def test_datetime_with_standard_format(self) -> None:
        """
        Tests the standardization for the case that the standard format
        is given along with our list of known datetim indexes.
        """

        our_datetime = datetime(2020, 10, 15, 20, 30)
        api_response = {
            x: our_datetime.strftime(self.STANDARD_DATE_FORMAT)
            for x in self.datetime_indexes
        }

        expected = {x: our_datetime for x in self.datetime_indexes}

        standardization = Standardization()
        standardization.set_data(api_response)

        actual = standardization.get_standardized()

        self.assertEqual(expected, actual)

    def test_datetime_with_standard_format_in_list_of_dict(self) -> None:
        """
        Tests the standardization for the cast the a list of dict is given.
        """

        our_datetime = datetime(2020, 10, 15, 20, 30)
        api_response_standard_date = {
            x: our_datetime.strftime(self.STANDARD_DATE_FORMAT)
            for x in self.datetime_indexes
        }
        api_response_alternative_date = {
            x: our_datetime.strftime(self.ALTERNATIVE_DATE_FORMAT)
            for x in self.datetime_indexes
        }

        api_response_standard_date["hello"] = api_response_alternative_date[
            "hello"
        ] = list(range(15))
        api_response_standard_date["world"] = api_response_alternative_date["world"] = {
            "hello": "world"
        }

        custom_format = [api_response_standard_date, api_response_alternative_date]

        expected_inner = {x: our_datetime for x in self.datetime_indexes}
        expected_inner["hello"] = list(range(15))
        expected_inner["world"] = {"hello": "world"}

        expected = [expected_inner, expected_inner]

        standardization = Standardization()
        standardization.set_data(custom_format)

        actual = standardization.get_standardized()

        self.assertEqual(actual, expected)

    def test_datetime_with_alternative_format(self) -> None:
        """
        Tests the standardization for the case that the alternative format
        is given along with our list of known datetim indexes.
        """

        our_datetime = datetime(2020, 10, 15, 20, 30)
        api_response = {
            x: our_datetime.strftime(self.ALTERNATIVE_DATE_FORMAT)
            for x in self.datetime_indexes
        }

        expected = {x: our_datetime for x in self.datetime_indexes}

        standardization = Standardization()
        standardization.set_data(api_response)

        actual = standardization.get_standardized()

        self.assertEqual(expected, actual)

    def test_tagged_conversion(self) -> None:
        """
        Tests the standardization for the case that @tags are given.
        """

        api_response = {
            "@type": "hello",
            "resource_type": "world",
        }

        expected = {"_at_type": "hello", "resource_type": "world"}

        standardization = Standardization()
        standardization.set_data(api_response)

        actual = standardization.get_standardized()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_tests()
