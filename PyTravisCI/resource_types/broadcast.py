"""
Just another Python API for Travis CI (API).

A module which provides the "Broadcast" resource type.

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

from . import _all as resource_types
from .base import ResourceTypesBase


class Broadcast(ResourceTypesBase):
    """
    Provides the description of a broadcast.

    Official Travis CI API documentation
        - https://developer.travis-ci.org/resource/broadcast

    :ivar int id:
        Value uniquely identifying the broadcast.
    :ivar str message:
        Message to display to the user.
    :ivar created_at:
        When the broadcast was created.
    :vartype created_at: :py:class`~datetime.datetime`
    :ivar str category:
        Broadcast category (used for icon and color).
    :ivar bool active:
        Whether or not the brodacast should still be displayed.
    :ivar recipient:
        Either a user, organization or repository, or null for global.
    :vartype recipient:
        Union[
            :class:`~PyTravisCI.resource_types.user.User`,
            :class:`~PyTravisCI.resource_types.organization.Organization`,
            :class:`~PyTravisCI.resource_types.repository.Repository`
        ]
    """

    id: Optional[int] = None
    message: Optional[str] = None
    created_at: Optional[datetime] = None
    category: Optional[str] = None
    active: Optional[bool] = None
    recipient: Optional[
        Union[
            "resource_types.User",
            "resource_types.Organization",
            "resource_types.Repository",
        ]
    ] = None

    def __init__(self, **kwargs) -> None:
        if "recipient" in kwargs and "_at_type" in kwargs["recipient"]:
            if kwargs["recipient"]["_at_type"] == "user":
                kwargs["recipient"] = resource_types.User(**kwargs["recipient"])
            elif kwargs["recipient"]["_at_type"] == "organization":
                kwargs["recipient"] = resource_types.Organization(**kwargs["recipient"])
            elif kwargs["recipient"]["_at_type"] == "repository":
                kwargs["recipient"] = resource_types.Repository(**kwargs["recipient"])

        super().__init__(**kwargs)
