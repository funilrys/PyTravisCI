"""
Just another Python API for Travis CI (API).

A module which provides the "Setting" resource type.

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

import PyTravisCI.communicator._all as communicator

from . import _all as resource_types  # pylint: disable=unused-import
from .base import ResourceTypesBase


class Setting(ResourceTypesBase):
    """
    Provides an individual repository setting.

    Official Travis CI API documentation
        - https://developer.travis-ci.org/resource/setting

    :ivar str name:
        The settings's name.
    :ivar str value:
        The settings's value.
    """

    name: Optional[str] = None
    value: Optional[str] = None

    def set_value(self, value: Union[bool, int]) -> "resource_types.Setting":
        """
        Set the new value of the current setting.

        :param value:
            The new value.
        """

        if not isinstance(value, (str, int)):
            raise TypeError(
                f"<value> {value} should be {str} or {int}, {type(value)} given."
            )

        data = {"setting.value": value}

        comm = getattr(communicator, self.__class__.__name__)(
            self._PyTravisCI["com"]["requester"]
        )

        if "setting_name" not in self._PyTravisCI["shared"]:
            response = comm.update(
                setting_name=self.name, data=data, **self._PyTravisCI["shared"]
            )
        else:
            response = comm.update(data=data, **self._PyTravisCI["shared"])

        self.__dict__ = response.__dict__

        return self
