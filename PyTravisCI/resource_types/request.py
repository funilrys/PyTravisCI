"""
Just another Python API for Travis CI (API).

A module which provides the "Request" resource type.

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

from . import _all as resource_types
from .base import ResourceTypesBase


class Request(ResourceTypesBase):
    """
    Provides the description of a request.

    Official Travis CI API documentation
        - https://developer.travis-ci.org/resource/request

    :ivar int id:
        Value uniquely identifying the build.
    :ivar str state:
        Current state of the build.
    :ivar str result:
        The result of the request (eg. rejected or approved).
    :ivar str message:
        Travis-ci status message attached to the request.
    :ivar str previous_state:
        State of the previous build (useful to see if state changed).
    :ivar pull_request_mergeable:
        The request's pull_request_mergeable.
    :ivar repository:
        GitHub user or organization the build belongs to.
    :vartype repository: :class:`~PyTravisCI.resource_types.repository.Repository`
    :ivar str branch_name:
        Name of the branch requested to be built.
    :ivar commit:
        The commit the request is associated with.
    :vartype commit: :class:`~PyTravisCI.resource_types.commit.Commit`
    :ivar builds:
                The request's builds.
    :vartype builds: List[:class:`~PyTravisCI.resource_types.build.Build`]
    :ivar owner:
        GitHub user or organization the request belongs to.
    :vartype owner:
        Union[
            :class:`~PyTravisCI.resource_types.user.User`,
            :class:`~PyTravisCI.resource_types.organization.Organization`
        ]
    :ivar created_at:
        When the build started.
    :vartype created_at: :py:class:`~datetime.datetime`
    :ivar str event_type:
        Origin of request (push, pull request, api).
    :ivar str base_commit:
        The base commit the request is associated with.
    :ivar str head_commit:
        The head commit the request is associated with.
    :ivar messages:
        The request's messages.
    :ivar config:
        Build configuration (as parsed from .travis.yml).
    :ivar raw_configs:
        The request's raw_configs.
    """

    id: Optional[int] = None
    state: Optional[str] = None
    result: Optional[str] = None
    message: Optional[str] = None
    pull_request_mergeable = None
    repository: Optional["resource_types.Repository"] = None
    brnach_name: Optional[str] = None
    commit: Optional["resource_types.Commit"] = None
    builds: Optional[List["resource_types.Build"]] = None
    owner: Optional[Union["resource_types.User", "resource_types.Organization"]] = None
    created_at: Optional[datetime] = None
    event_type: Optional[str] = None
    base_commit: Optional[str] = None
    head_commit: Optional[str] = None
    messages = None
    config = None
    raw_configs = None

    def __init__(self, **kwargs) -> None:
        if "repository" in kwargs:
            kwargs["repository"] = resource_types.Repository(**kwargs["repository"])

        if "commit" in kwargs:
            kwargs["commit"] = resource_types.Commit(**kwargs["commit"])

        if "builds" in kwargs:
            kwargs["builds"] = [resource_types.Build(**x) for x in kwargs["builds"]]

        if "owner" in kwargs and "_at_type" in kwargs["owner"]:
            if kwargs["owner"]["_at_type"] == "user":
                kwargs["owner"] = resource_types.User(**kwargs["owner"])
            elif kwargs["owner"]["_at_type"] == "organization":
                kwargs["owner"] = resource_types.Organization(**kwargs["owner"])

        super().__init__(**kwargs)
