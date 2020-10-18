"""
Just another Python API for Travis CI (API).

A module which provides the "Job" resource type.

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


class Job(ResourceTypesBase):
    """
    Provides the description of a single build.

    Official Travis CI API documentation
        - https://developer.travis-ci.org/resource/job

    :ivar int id:
        Value uniquely identifying the job.
    :ivar bool allow_failure:
        The job's allow_failure.
    :ivar str number:
        Incremental number for a repository's builds.
    :ivar str state:
        Current state of the job.
    :ivar started_at:
        When the job started.
    :vartype started_at: :py:class:`~datetime.datetime`
    :ivar finished_at:
        When the job finished.
    :vartype finished_at: :py:class:`~datetime.datetime`
    :ivar build:
        The build the job is associated with.
    :vartype build: :class:`~PyTravisCI.resource_types.build.Build`
    :ivar str queue:
        Worker queue this job is/was scheduled on.
    :ivar repository:
        GitHub user or organization the job belongs to.
    :vartype repository: :class:`~PyTravisCI.resource_types.repository.Repository`
    :ivar commit:
        The commit the job is associated with.
    :vartype commit: :class:`~PyTravisCI.resource_types.commit.Commit`
    :ivar owner:
        GitHub user or organization the job belongs to.
    :vartype owner:
        Union[
            :class:`~PyTravisCI.resource_types.user.User`,
            :class:`~PyTravisCI.resource_types.organization.Organization`
        ]
    :ivar stage:
        The stages of the job.
    :vartype stage: List[:class`~PyTravisCI.resource_types.stage.Stage`]
    :ivar created_at:
        When the job was created.
    :vartype created_at: :py:class:`~datetime.datetime`
    :ivar updated_at:
        When the job was updated.
    :vartype updated_at: :py:class:`~datetime.datetime`
    """

    id: Optional[int] = None
    allow_failure: Optional[bool] = None
    number: Optional[str] = None
    state: Optional[str] = None
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    build: Optional["resource_types.Build"] = None
    queue: Optional[str] = None
    repository: Optional["resource_types.Repository"] = None
    commit: Optional["resource_types.Commit"] = None
    owner: Optional[Union["resource_types.User", "resource_types.Organization"]] = None
    stage: Optional[List["resource_types.Stage"]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    private: Optional[bool] = None

    def __init__(self, **kwargs) -> None:
        if "build" in kwargs:
            kwargs["build"] = resource_types.Build(**kwargs["build"])

        if "repository" in kwargs:
            kwargs["repository"] = resource_types.Repository(**kwargs["repository"])

        if "commit" in kwargs:
            kwargs["commit"] = resource_types.Commit(**kwargs["commit"])

        if "stage" in kwargs and kwargs["stage"]:
            kwargs["stage"] = resource_types.Stage(**kwargs["stage"])

        if "owner" in kwargs and "_at_type" in kwargs["owner"]:
            if kwargs["owner"]["_at_type"] == "user":
                kwargs["owner"] = resource_types.User(**kwargs["owner"])
            elif kwargs["owner"]["_at_type"] == "organization":
                kwargs["owner"] = resource_types.Organization(**kwargs["owner"])

        super().__init__(**kwargs)

    def sync(self) -> "resource_types.Job":
        """
        Fetches the latest information of the current job.
        """

        comm = getattr(communicator, self.__class__.__name__)(
            self._PyTravisCI["com"]["requester"]
        )

        self.__dict__ = comm.from_id(job_id=self.id).__dict__

        return self

    def is_canceled(self, *, sync: bool = False) -> bool:
        """
        Checks if the job canceled.

        :param sync:
            Authorizes the synchronization before checking.
        """

        if sync:
            self.sync()

        return self.state.lower() == defaults.states.CANCELED

    def is_errored(self, *, sync: bool = False) -> bool:
        """
        Checks if the job errored.

        :param sync:
            Authorizes the synchronization before checking.
        """

        if sync:
            self.sync()

        return self.state.lower() == defaults.states.ERRORED

    def is_failed(self, *, sync: bool = False) -> bool:
        """
        Checks if the job failed.

        :param sync:
            Authorizes the synchronization before checking.
        """

        if sync:
            self.sync()

        return self.state.lower() == defaults.states.FAILED

    def is_created(self, *, sync: bool = False) -> bool:
        """
        Checks if the job is created.

        :param sync:
            Authorizes the synchronization before checking.
        """

        if sync:
            self.sync()

        return self.state.lower() == defaults.states.CREATED

    def is_started(self, *, sync: bool = False) -> bool:
        """
        Checks if the job is started.

        :param sync:
            Authorizes the synchronization before checking.
        """

        if sync:
            self.sync()

        return self.state.lower() == defaults.states.STARTED

    def is_passed(self, *, sync: bool = False) -> bool:
        """
        Checks if the job is passed.

        :param sync:
            Authorizes the synchronization before checking.
        """

        if sync:
            self.sync()

        return self.state.lower() == defaults.states.PASSED

    def is_active(self, *, sync: bool = False) -> bool:
        """
        Checks if the jpb is active.

        :param sync:
            Authorizes the synchronization before checking.
        """

        if sync:
            self.sync()

        return self.state.lower() in defaults.states.ACTIVE

    def get_log(self, *, params: Optional[dict] = None) -> "resource_types.Log":
        """
        Provides the logs of the current job.

        :param params:
            The query parameters to append to the URL.
        """

        comm = getattr(communicator, "Log")(self._PyTravisCI["com"]["requester"])

        return comm.from_id(job_id=self.id, parameters=params)

    def cancel(self) -> "resource_types.Job":
        """
        Cancels the current job.
        """

        if not self.is_active():
            raise exceptions.JobAlreadyStopped()

        comm = getattr(communicator, self.__class__.__name__)(
            self._PyTravisCI["com"]["requester"]
        )

        return comm.cancel(job_id=self.id)

    def restart(self) -> "resource_types.Job":
        """
        Restarts the current job.

        :raise JobAlreadyStarted:
            When the current job was already started.
        """

        if self.is_active():
            raise exceptions.JobAlreadyStarted()

        comm = getattr(communicator, self.__class__.__name__)(
            self._PyTravisCI["com"]["requester"]
        )

        return comm.restart(job_id=self.id)

    def debug(self) -> "resource_types.Job":
        """
        Restart the current job in debug mode.

        .. warning::
            This method may not work if you are
            not allowed to restart in debug mode.
        """

        comm = getattr(communicator, self.__class__.__name__)(
            self._PyTravisCI["com"]["requester"]
        )

        return comm.debug(job_id=self.id)
