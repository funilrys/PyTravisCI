"""
Just another Python API for Travis CI (API).

A module which provides the "Log" resource type.

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

from PyTravisCI.communicator import _all as communicator

from . import _all as resource_types  # pylint: disable=unused-import
from .base import ResourceTypesBase


class Log(ResourceTypesBase):
    """
    Provides the description of a job log.

    Official Travis CI API documentation
        - https://developer.travis-ci.org/resource/log

    :ivar int id:
        The log's id.
    :ivar str content:
        The content of the log.
    :ivar list log_parts:
        The log parts that form the log.
    """

    id: Optional[int] = None
    content: Optional[str] = None
    log_parts: Optional[list] = None

    def delete(self) -> Union[bool, "resource_types.Log"]:
        """
        Deletes the current log

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/key_pair
        """

        comm = getattr(communicator, self.__class__.__name__)(
            self._PyTravisCI["com"]["requester"]
        )

        return comm.delete(**self._PyTravisCI["shared"])
