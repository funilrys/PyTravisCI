"""
Just another Python API for Travis CI (API).

A module which provides the "Stages" resource type.

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

from typing import List, Optional

from . import _all as resource_types
from .base import ResourceTypesBase


class Stages(ResourceTypesBase):
    """
    Provides a list of stage.

    Official Travis CI API documentation
        - https://developer.travis-ci.org/resource/stages

    :ivar stages:
        A list of stage.
    :vartype stages: List[:class:`PyTravisCI.resource_types.stage.Stage`]
    """

    __iter_through__: str = "stages"
    stages: Optional[List["resource_types.Stage"]] = None

    def __init__(self, **kwargs) -> None:
        if "stages" in kwargs:
            kwargs["stages"] = [resource_types.Stage(**x) for x in kwargs["stages"]]

        super().__init__(**kwargs)
