"""
Just another Python API for Travis CI (API).

A module which provides the "Branch" resource type.

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

import PyTravisCI.communicator._all as communicator
import PyTravisCI.exceptions as exceptions

from . import _all as resource_types
from .base import ResourceTypesBase


class Branch(ResourceTypesBase):
    """
    Provides the description of a branch.

    Official Travis CI API documentation:
        - https://developer.travis-ci.org/resource/branch

    :ivar str name: Name of the git branch.
    :ivar repository:
        GitHub user or organization the branch belongs to.
    :vartype repository: :class:`~PyTravisCI.resource_types.repository.Repository`
    :ivar bool default_branch:
        Whether or not this is the respository's default branch.
    :ivar bool exists_on_github:
        Whether or not the branch still exists on GitHub.
    :ivar last_build:
        Last build on the branch.
    :vartype last_build: :class:`~PyTravisCI.resource_types.build.Build`
    :ivar recent_builds:
        Last 10 builds on the branch (when :code:`include=branch.recent_builds` is used).
    :vartype recent_builds: List[:class:`~PyTravisCI.resource_types.build.Build`]
    """

    name: Optional[str] = None
    repository: Optional["resource_types.Repository"] = None
    default_branch: Optional[bool] = None
    exists_on_github: Optional[bool] = None
    last_build: Optional["resource_types.Build"] = None
    recent_builds: Optional[List["resource_types.Build"]] = None

    def __init__(self, **kwargs) -> None:
        if "repository" in kwargs:
            kwargs["repository"] = resource_types.Repository(**kwargs["repository"])

        if "last_build" in kwargs and isinstance(kwargs["last_build"], dict):
            kwargs["last_build"] = resource_types.Build(**kwargs["last_build"])

        if "recent_builds" in kwargs:
            kwargs["recent_builds"] = [
                resource_types.Build(**x) for x in kwargs["recent_builds"]
            ]

        super().__init__(**kwargs)

    def get_cron(
        self, *, params: Optional[dict] = None
    ) -> Optional["resource_types.Cron"]:
        """
        Provides the cron of the current branch.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/cron

        :param params:
            The query parameters to append to the URL.
        """

        comm = getattr(communicator, "Cron")(self._PyTravisCI["com"]["requester"])

        try:
            return comm.from_id_or_slug_and_branch(
                repository_id_or_slug=self.repository.id,
                branch_name=self.name,
                parameters=params,
            )
        except exceptions.TravisCIError as exception:
            if exception.get_error_type() != "not_found":
                raise exception

        return None

    def create_cron(
        self,
        interval: str,
        *,
        dont_run_if_recent_build_exists: bool = False,
        params: Optional[dict] = None,
    ) -> "resource_types.Cron":
        """
        Creates a new cron associated to the current branch.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/cron

        :param interval:
            Interval at which the cron will run
            (can be :code:`daily`, :code:`weekly` or :code:`monthly`).
        :param dont_run_if_recent_build_exists:
            Whether a cron build should run if there has been a
            build on this branch in the last 24 hours.
        :param params:
            The query parameters to append to the URL.
        """

        known_interval = ["daily", "weekly", "monthly"]
        interval = interval.strip()

        if interval not in known_interval:
            raise ValueError(
                f"<interval> must be in {known_interval}, {interval} given."
            )

        data = {
            "cron.interval": interval,
            "cron.dont_run_if_recent_build_exists": dont_run_if_recent_build_exists,
        }

        comm = getattr(communicator, "Cron")(self._PyTravisCI["com"]["requester"])

        return comm.create(
            repository_id_or_slug=self.repository.id,
            branch_name=self.name,
            data=data,
            parameters=params,
        )
