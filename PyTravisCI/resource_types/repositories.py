"""
Just another Python API for Travis CI (API).

A module which provides the "Repositories" resource type.

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


class Repositories(ResourceTypesBase):
    """
    Provides a list of repository.

    Official Travis CI API documentation
        - https://developer.travis-ci.org/resource/repositories

    :ivar repositories:
        A list of repository.
    :vartype repositories: List[PyTravisCI.resource_types.repository.Repository]
    """

    __iter_through__: str = "repositories"

    organizations: Optional[List["resource_types.Repository"]] = None

    def __init__(self, **kwargs) -> None:
        if "repositories" in kwargs:
            kwargs["repositories"] = [
                resource_types.Repository(**x) for x in kwargs["repositories"]
            ]

        super().__init__(**kwargs)
