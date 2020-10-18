"""
Just another Python API for Travis CI (API).

A module which provides the "Installation" resource type.

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

from typing import Optional, Union

from . import _all as resource_types
from .base import ResourceTypesBase


class Installation(ResourceTypesBase):
    """
    Provides the description of a GitHub App installation

    Official Travis CI API documentation
        - https://developer.travis-ci.org/resource/installation

    :ivar int id:
        Value uniquely identifying the user.
    :ivar int github_id:
        The installation's id on GitHub.
    :ivar owner:
        GitHub user or organization the installation belongs to.
    :vartype owner:
        Union[
            :class:`~PyTravisCI.resource_types.user.User`,
            :class:`~PyTravisCI.resource_types.organization.Organization`
        ]
    """

    id: Optional[int] = None
    github_id: Optional[int] = None
    owner: Optional[Union["resource_types.User", "resource_types.Organization"]] = None

    def __init__(self, **kwargs) -> None:
        if "owner" in kwargs and "_at_type" in kwargs["owner"]:
            if kwargs["owner"]["_at_type"] == "user":
                kwargs["owner"] = resource_types.User(**kwargs["owner"])
            elif kwargs["owner"]["_at_type"] == "organization":
                kwargs["owner"] = resource_types.Organization(**kwargs["owner"])

        super().__init__(**kwargs)
