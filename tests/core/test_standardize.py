"""
Just another Travis CI (Python) API client.

Test of the standardize class.

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

from datetime import datetime
from random import choice
from unittest import TestCase
from unittest import main as launch_test

from PyTravisCI.standardize import Standardize


class TestStandardize(TestCase):
    """
    Test of :class:`PyTravisCI.standardize.Standardize`.
    """

    def setUp(self):
        """
        Provide everything needed for the test.
        """

        formats = ["%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S.%fZ"]

        self.api_response = {}

        for index in Standardize.date_time_indexes:
            self.api_response[index] = datetime.now().strftime(choice(formats))

    def test_date_and_time(self):
        """
        Test of :meth:`PyTravisCI.standardize.Standardize.date_and_time`.
        """

        actual = Standardize(None).it(api_response=self.api_response)

        for index, data in actual.items():
            self.assertIsInstance(
                data, datetime, msg=f"{index} is not an instance of `datetime`."
            )


if __name__ == "__main__":
    launch_test()
