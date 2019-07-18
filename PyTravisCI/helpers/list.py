"""
Just another Travis CI (Python) API client.

Provide some list related helpers.

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


# pylint: disable=too-few-public-methods
class List:
    """
    Provide some list related helpers.
    """

    def __init__(self, st_list):
        if isinstance(st_list, list):
            self.st_list = st_list
        else:
            raise TypeError(
                f"<st_list> ({type(st_list)}) must be of type `{type(list)}`"
            )

    def merge(self, nd_list, strict=True):
        """
        Merge :code:`nd_list` into :code:`st_list`.

        :param dict nd_nd_listdict: The :code:`list()` to merge.
        :param bool strict: Tell us if we do a strict merging.
        """

        from PyTravisCI.helpers.dict import Dict

        result = []

        if strict:
            for index, element in enumerate(nd_list):
                try:
                    if isinstance(element, dict) and isinstance(
                        self.st_list[index], dict
                    ):
                        result.append(Dict(self.st_list[index]).merge(element))
                    elif isinstance(element, list) and isinstance(
                        self.st_list[index], list
                    ):
                        result.append(List(self.st_list[index]).merge(element))
                    else:
                        result.append(element)
                except IndexError:  # pragma: no cover
                    result.append(element)

            result.extend(self.st_list[len(nd_list) :])
        else:
            result = self.st_list

            for element in nd_list:
                if element not in result:
                    result.append(element)

        return result
