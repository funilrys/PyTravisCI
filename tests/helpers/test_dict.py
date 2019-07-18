"""
Just another Travis CI (Python) API client.

Test of the Dict helpers.

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

from unittest import TestCase
from unittest import main as launch_test

from PyTravisCI.helpers.dict import Dict


class TestList(TestCase):
    """
    Test of the dict helper.
    """

    def setUp(self):
        """
        Setup everything needed.
        """

        self.st_dict = {
            "hello": ["This is Funilrys!", "Uhh!"],
            "world": "Fun Ilrys",
            "hello_world": {"author": "funilrys", "name": "Fun"},
        }

    def test_simple_merge(self):
        """
        Test the merging method in a simple case.
        """

        nd_dict = {
            "hello": ["hello", "Uhh"],
            "hello_world": {"author": "nobody", "surname": "body"},
        }

        expected = {
            "hello": ["hello", "Uhh"],
            "world": "Fun Ilrys",
            "hello_world": {"author": "nobody", "name": "Fun", "surname": "body"},
        }
        actual = Dict(self.st_dict).merge(nd_dict, strict=True)

        self.assertEqual(expected, actual)

    def test_non_strict_merge(self):
        """
        Test the merging method without the strict mode.
        """

        nd_dict = {
            "hello": ["hello", "Uhh"],
            "hello_world": {"author": "nobody", "surname": "body"},
        }

        expected = {
            "hello": ["This is Funilrys!", "Uhh!", "hello", "Uhh"],
            "world": "Fun Ilrys",
            "hello_world": {"author": "nobody", "name": "Fun", "surname": "body"},
        }
        actual = Dict(self.st_dict).merge(nd_dict, strict=False)

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    launch_test()
