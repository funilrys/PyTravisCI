"""
Just another Python API for Travis CI (API).

A module which provides the "Crons" resource type.

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


class Crons(ResourceTypesBase):
    """
    Provides the list of crons.

    Official Travis CI API documentation
        - https://developer.travis-ci.org/resource/crons

    :ivar crons: List of crons.
    :vartype crons: List[:class:`~PyTravisCI.resource_types.cron.Cron`]
    """

    __iter_through__ = "crons"
    crons: Optional[List["resource_types.Cron"]] = None

    def __init__(self, **kwargs) -> None:
        if "crons" in kwargs:
            kwargs["crons"] = [resource_types.Cron(**x) for x in kwargs["crons"]]

        super().__init__(**kwargs)
