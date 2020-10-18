"""
Just another Python API for Travis CI (API).

A module which provides the "Stage" resource type.

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
from typing import List, Optional

from . import _all as resource_types
from .base import ResourceTypesBase


class Stage(ResourceTypesBase):
    """
    Provides the description of a stage

    Official Travis CI API documentation
        - https://developer.travis-ci.org/resource/stage

    :ivar int id:
        Value uniquely identifying the stage.
    :ivar int number:
        Incremental number for a stage.
    :ivar str name:
        The name of the stage.
    :ivar str state:
        Current state of the stage.
    :ivar started_at:
        When the stage started.
    :vartype started_at: :py:class:`~datetime.datetime`
    :ivar finished_at:
        When the stage finished.
    :vartype finished_at: :py:class:`~datetime.datetime`
    :ivar jobs:
        The jobs of a stage.
    :vartype jobs: List[:class:`PyTravisCI.resource_types.job.Job`]
    """

    id: Optional[int] = None
    number: Optional[int] = None
    name: Optional[str] = None
    state: Optional[str] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    jobs: Optional[List["resource_types.Job"]] = None

    def __init__(self, **kwargs) -> None:
        if "jobs" in kwargs:
            kwargs["jobs"] = [resource_types.Job(**x) for x in kwargs["jobs"]]

        super().__init__(**kwargs)
