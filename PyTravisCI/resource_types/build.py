"""
Just another Python API for Travis CI (API).

A module which provides the "Build" resource type.

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
from typing import List, Optional, Union

import PyTravisCI.communicator._all as communicator
import PyTravisCI.defaults as defaults
import PyTravisCI.exceptions as exceptions

from . import _all as resource_types
from .base import ResourceTypesBase


class Build(ResourceTypesBase):
    """
    Provides the description of a build

    Official Travis CI API documentation
        - https://developer.travis-ci.org/resource/build

    :ivar int id:
        Value uniquely identifying the build.
    :ivar str number:
        Incremental number for a repository's builds.
    :ivar str state:
        Current state of the build.
    :ivar int duration:
        Wall clock time in seconds.
    :ivar str event_type:
        Event that triggered the build.
    :ivar str previous_state:
        State of the previous build (useful to see if state changed).
    :ivar str pull_request_title:
        Title of the build's pull request.
    :ivar int pull_request_number:
        Number of the build's pull request.
    :ivar started_at:
        When the build started.
    :vartype started_at: :py:class:`~datetime.datetime`
    :ivar finished_at:
        When the build finished.
    :vartype finished_at: :py:class:`~datetime.datetime`
    :ivar bool private:
        Whether or not the build is private.
    :ivar repository:
        GitHub user or organization the build belongs to.
    :vartype repository: :class:`~PyTravisCI.resource_types.repository.Repository`
    :ivar branch:
        The branch the build is associated with.
    :vartype branch: :class:`~PyTravisCI.resource_types.branch.Branch`
    :ivar str tag:
        The build's tag.
    :ivar commit:
        The commit the build is associated with.
    :vartype commit: :class:`~PyTravisCI.resource_types.commit.Commit`
    :ivar jobs:
        List of jobs that are part of the build's matrix.
    :vartype jobs: List[:class:`~PyTravisCI.resource_types.job.Job`]
    :ivar stages:
        The stages of the build.
    :vartype stages: List[:class:`~PyTravisCI.resource_types.stage.Stage`]
    :ivar created_by:
        The User or Organization that created the build.
    :vartype created_by:
        Union[
            :class:`~PyTravisCI.resource_types.user.User`,
            :class:`~PyTravisCI.resource_types.organization.Organization`
        ]
    :ivar updated_at:
        The last time the build was updated.
    :vartype updated_at: :py:class:`~datetime.datetime`
    """

    id: Optional[int] = None
    number: Optional[str] = None
    state: Optional[str] = None
    duration: Optional[int] = None
    event_type: Optional[str] = None
    previous_state: Optional[str] = None
    pull_request_title: Optional[str] = None
    pull_request_number: Optional[int] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    private: Optional[bool] = None
    repository: Optional["resource_types.Repository"] = None
    branch: Optional["resource_types.Branch"] = None
    tag: Optional[str] = None
    commit: Optional["resource_types.Commit"] = None
    jobs: Optional[List["resource_types.Job"]] = None
    stages: Optional[List["resource_types.Stage"]] = None
    created_by: Optional[
        Union["resource_types.User", "resource_types.Organization"]
    ] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __init__(self, **kwargs) -> None:
        if "jobs" in kwargs:
            kwargs["jobs"] = [resource_types.Job(**x) for x in kwargs["jobs"]]

        if "repository" in kwargs:
            kwargs["repository"] = resource_types.Repository(**kwargs["repository"])

        if "branch" in kwargs:
            kwargs["branch"] = resource_types.Branch(**kwargs["branch"])

        if "stages" in kwargs:
            kwargs["stages"] = [resource_types.Stage(**x) for x in kwargs["stages"]]

        if "commit" in kwargs:
            kwargs["commit"] = resource_types.Commit(**kwargs["commit"])

        if "created_by" in kwargs and "_at_type" in kwargs["created_by"]:
            if kwargs["created_by"]["_at_type"] == "user":
                kwargs["created_by"] = resource_types.User(**kwargs["created_by"])
            elif kwargs["created_by"]["_at_type"] == "organization":
                kwargs["created_by"] = resource_types.Organization(
                    **kwargs["created_by"]
                )

        super().__init__(**kwargs)

    def sync(self) -> "resource_types.Build":
        """
        Fetches the latest information of the current job.
        """

        comm = getattr(communicator, self.__class__.__name__)(
            self._PyTravisCI["com"]["requester"]
        )

        self.__dict__ = comm.from_id(build_id=self.id).__dict__

        return self

    def is_canceled(self, *, sync: bool = False) -> bool:
        """
        Checks if the build canceled.

        :param sync:
            Authorizes the synchronization before checking.
        """

        if sync:
            self.sync()

        return self.state.lower() == defaults.states.CANCELED

    def is_errored(self, *, sync: bool = False) -> bool:
        """
        Checks if the build errored.

        :param sync:
            Authorizes the synchronization before checking.
        """

        if sync:
            self.sync()

        return self.state.lower() == defaults.states.ERRORED

    def is_failed(self, *, sync: bool = False) -> bool:
        """
        Checks if the build failed.

        :param sync:
            Authorizes the synchronization before checking.
        """

        if sync:
            self.sync()

        return self.state.lower() == defaults.states.FAILED

    def is_created(self, *, sync: bool = False) -> bool:
        """
        Checks if the build is created.

        :param sync:
            Authorizes the synchronization before checking.
        """

        if sync:
            self.sync()

        return self.state.lower() == defaults.states.CREATED

    def is_started(self, *, sync: bool = False) -> bool:
        """
        Checks if the build is started.

        :param sync:
            Authorizes the synchronization before checking.
        """

        if sync:
            self.sync()

        return self.state.lower() == defaults.states.STARTED

    def is_passed(self, *, sync: bool = False) -> bool:
        """
        Checks if the build is passed.

        :param sync:
            Authorizes the synchronization before checking.
        """

        if sync:
            self.sync()

        return self.state.lower() == defaults.states.PASSED

    def is_active(self, *, sync: bool = False) -> bool:
        """
        Checks if the build is active.

        :param sync:
            Authorizes the synchronization before checking.
        """

        if sync:
            self.sync()

        return self.state.lower() in defaults.states.ACTIVE

    def get_jobs(self, *, params: Optional[dict] = None) -> "resource_types.Jobs":
        """
        Provides the list of jobs of the current build

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/jobs

        :param params:
            The query parameters to append to the URL.
        """

        comm = getattr(communicator, "Jobs")(self._PyTravisCI["com"]["requester"])

        return comm.from_build_id(build_id=self.id, parameters=params)

    def get_stages(self, *, params: Optional[dict] = None) -> "resource_types.Stages":
        """
        Provides the list of stages of the current build

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/stages

        :param params:
            The query parameters to append to the URL.
        """

        comm = getattr(communicator, "Stages")(self._PyTravisCI["com"]["requester"])

        return comm.from_build_id(build_id=self.id, parameters=params)

    def cancel(self) -> "resource_types.Build":
        """
        Cancels the current build.

        :raise BuildAlreadyStopped:
            When the current build was already canceled.
        """

        if not self.is_active():
            raise exceptions.BuildAlreadyStopped()

        comm = getattr(communicator, self.__class__.__name__)(
            self._PyTravisCI["com"]["requester"]
        )

        return comm.cancel(build_id=self.id)

    def restart(self) -> "resource_types.Build":
        """
        Restarts the current build.

        :raise BuildAlreadyStarted:
            When the current build was already started.
        """

        if self.is_active():
            raise exceptions.BuildAlreadyStarted()

        comm = getattr(communicator, self.__class__.__name__)(
            self._PyTravisCI["com"]["requester"]
        )

        return comm.restart(build_id=self.id)
