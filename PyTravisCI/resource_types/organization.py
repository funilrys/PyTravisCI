"""
Just another Python API for Travis CI (API).

A module which provides the "Organization" resource type.

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

from PyTravisCI.communicator import _all as communicator

from . import _all as resource_types
from .base import ResourceTypesBase


class Organization(ResourceTypesBase):
    """
    Provide the description of an organization.

    Official Travis CI API documentation
        - https://developer.travis-ci.org/resource/organization

    :ivar int id:
        Value uniquely identifying the user.
    :ivar str login:
        Login set on Github.
    :ivar str name:
        Name set on GitHub.
    :ivar int github_id:
        Id set on GitHub.
    :ivar vcs_id:
        The user's vcs_id.
    :ivar vcs_type:
        The user's vcs_type.
    :ivar str avatar_url:
        Avatar URL set on GitHub.
    :ivar bool education:
        Whether or not the user has an education account.
    :ivar allow_migration:
        The user's allow_migration.
    :ivar repositories:
        Repositories belonging to this organization.
    :vartype repositories: List[:class:`PyTravisCI.resource_types.repository.Repository`]
    :ivar installation:
        Installation belonging to the organization.
    :vartype installation: :class:`PyTravisCI.resource_types.installation.Installation`
    """

    id: Optional[int] = None
    login: Optional[str] = None
    name: Optional[str] = None
    github_id: Optional[int] = None
    vcs_id = None
    vcs_type = None
    avatar_url: Optional[str] = None
    education: Optional[bool] = None
    allow_migration = None
    repositories: Optional[List["resource_types.Repository"]] = None
    installation: Optional["resource_types.Installation"] = None

    def __init__(self, **kwargs) -> None:
        if "repositories" in kwargs:
            kwargs["repositories"] = [
                resource_types.Repository(**x) for x in kwargs["repositories"]
            ]

        if "installation" in kwargs:
            kwargs["installation"] = resource_types.Installation(
                **kwargs["installation"]
            )

        super().__init__(**kwargs)

    def get_active(self, *, params: Optional[dict] = None) -> "resource_types.Active":
        """
        Provides the list of active builds of the
        current user.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/active

        :param params:
            The query parameters to append to the URL.
        """

        comm = getattr(communicator, "Active")(self._PyTravisCI["com"]["requester"])

        return comm.from_github_id(github_id=self.github_id, parameters=params)
