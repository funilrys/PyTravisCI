"""
Just another Travis CI (Python) API client.

Provide some dict related helpers.

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
from PyTravisCI.helpers.list import List


# pylint: disable=too-few-public-methods
class Dict:
    """
    Provide some dict related helpers.
    """

    def __init__(self, st_dict):
        if isinstance(st_dict, dict):
            self.st_dict = st_dict
        else:
            raise TypeError(
                f"<st_dict> ({type(st_dict)}) must be of type `{type(dict)}`"
            )

    def merge(self, nd_dict, strict=True):
        """
        Merge :code:`nd_dict` into :code:`st_dict`.

        :param dict nd_dict: The :code:`dict()` to merge.
        :param bool strict: Tell us if we do a strict merging.
        """

        result = {}

        for index, data in nd_dict.items():
            if index in self.st_dict:
                if isinstance(data, dict) and isinstance(self.st_dict[index], dict):
                    result[index] = Dict(self.st_dict[index]).merge(data, strict=strict)
                elif isinstance(data, list) and isinstance(self.st_dict[index], list):
                    result[index] = List(self.st_dict[index]).merge(data, strict=strict)
                else:
                    result[index] = data
            else:
                result[index] = data

        for index, data in self.st_dict.items():
            if index not in result:
                result[index] = data

        return result
