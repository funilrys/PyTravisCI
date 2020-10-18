"""
Just another Python API for Travis CI (API).

A module which provides the "Cron" resource type.

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
from typing import Optional, Union

import PyTravisCI.communicator._all as communicator

from . import _all as resource_types
from .base import ResourceTypesBase


class Cron(ResourceTypesBase):
    """
    Provides the description of a cron.

    Official Travis CI API documentation
        - https://developer.travis-ci.org/resource/cron

    :ivar int id:
        Value uniquely identifying the build.
    :ivar repository:
        Github repository to which this cron belongs.
    :vartype repository: :class:`~PyTravisCI.resource_types.repository.Repository`
    :ivar branch:
        Git branch of repository to which this cron belongs.
    :vartype branch: :class:`~PyTravisCI.resource_types.branch.Branch`
    :ivar str interval:
        Interval at which the cron will run (can be "daily", "weekly" or "monthly").
    :ivar bool dont_run_if_recent_build_exists:
        Whether a cron build should run if there has
        been a build on this branch in the last 24 hours.
    :ivar last_run:
        When the cron ran last.
    :vartype last_run: :py:class:`~datetime.datetime`
    :ivar next_run:
        When the cron is scheduled to run next.
    :vartype next_run: :py:class:`~datetime.datetime`
    :ivar created_at:
        When the cron was created.
    :vartype created_at: :py:class:`~datetime.datetime`
    :ivar bool active:
        The cron's active.
    """

    id: Optional[int] = None
    repository: Optional["resource_types.Repository"] = None
    branch: Optional["resource_types.Branch"] = None
    interval: Optional[str] = None
    dont_run_if_recent_build_exists: Optional[bool] = None
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    created_at: Optional[datetime] = None
    active: Optional[bool] = None

    def __init__(self, **kwargs) -> None:
        if "repository" in kwargs:
            kwargs["repository"] = resource_types.Repository(**kwargs["repository"])

        if "branch" in kwargs:
            kwargs["branch"] = resource_types.Branch(**kwargs["branch"])

        super().__init__(**kwargs)

    def delete(self) -> Union[bool, "resource_types.Cron"]:
        """
        Deletes the current cron.
        """

        comm = getattr(communicator, self.__class__.__name__)(
            self._PyTravisCI["com"]["requester"]
        )

        return comm.delete(cron_id=self.id)
