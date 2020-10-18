"""
Just another Python API for Travis CI (API).

A module which provides the "Caches" resource type.

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

from typing import List, Optional, Union

import PyTravisCI.communicator._all as communicator

from . import _all as resource_types
from .base import ResourceTypesBase


class Caches(ResourceTypesBase):
    """
    Provide the list of caches of a chosen repository.

    Official Travis CI API documentation
        - https://developer.travis-ci.org/resource/caches

    :ivar caches: List of caches.
    :vartype caches:
        List[:class:`~PyTravisCI.resource_types.cache.Cache`]

    :ivar repo:
        An internal representation of the repository linked to the current
        caches.
    :vartype repo:
        :class:`~PyTravisCI.resource_types.repository.Repository`
    :ivar str name:
        The name of the repository linked to the current caches.
    """

    __iter_through__: str = "caches"
    caches: Optional[List["resource_types.Cache"]] = None
    repo: Optional["resource_types.Repository"] = None
    name: Optional[str] = None

    def __init__(self, **kwargs) -> None:
        if "caches" in kwargs:
            kwargs["caches"] = [resource_types.Cache(**x) for x in kwargs["caches"]]

        super().__init__(**kwargs)

    def delete(self) -> Union[bool, "resource_types.Caches"]:
        """
        Deletes the current cache
        """

        comm = getattr(communicator, self.__class__.__name__)(
            self._PyTravisCI["com"]["requester"]
        )

        return comm.delete(
            repository_id_or_slug=self.repo.id, parameters={"match": self.name}
        )
