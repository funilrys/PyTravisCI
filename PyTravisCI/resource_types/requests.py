"""
Just another Python API for Travis CI (API).

A module which provides the "Requests" resource type.

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

from typing import List, Optional

from . import _all as resource_types
from .base import ResourceTypesBase


class Requests(ResourceTypesBase):
    """
    Provides the list of requests.

    Official Travis CI API documentation
        - https://developer.travis-ci.org/resource/builds

    :ivar requests: List of requests.
    :vartype builds:
        List[:class:`~PyTravisCI.resource_types.request.Requests`]
    """

    __iter_through__: str = "requests"
    requests: Optional[List["resource_types.Request"]] = None

    def __init__(self, **kwargs) -> None:
        if "requests" in kwargs:
            kwargs["requests"] = [
                resource_types.Request(**x) for x in kwargs["requests"]
            ]

        super().__init__(**kwargs)
