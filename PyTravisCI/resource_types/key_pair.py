"""
Just another Python API for Travis CI (API).

A module which provides the "Key Pair" resource type.

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


class KeyPair(ResourceTypesBase):
    """
    Provides the description of a key pair.

    Official Travis CI API documentation
        - https://developer.travis-ci.org/resource/key_pair

    :ivar str description:
        A text description.
    :ivar str public_key:
        The public key.
    :ivar str fingerprint:
        The fingerprint.
    """

    description: Optional[str] = None
    public_key: Optional[str] = None
    fingerprint: Optional[str] = None

    def set_value(self, value: str) -> "resource_types.KeyPair":
        """
        Sets the new value (private key) of the current key pair.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/key_pair

        :param value:
            The new value (private key).

        :raise TypeError:
            Whether :code:`value` is not :py:class`str` nor :py:class`bytes`.
        """

        if not isinstance(value, (str, bytes)):
            raise TypeError(
                f"<value> {value} should be {str} or {bytes}. {type(value)} given."
            )

        data = {"key_pair.value": value}

        comm = getattr(communicator, self.__class__.__name__)(
            self._PyTravisCI["com"]["requester"]
        )

        self.__dict__ = comm.update(data=data, **self._PyTravisCI["shared"]).__dict__

        return self

    def set_description(self, description: str) -> "resource_types.KeyPair":
        """
        Sets the new description of the current key pair.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/key_pair

        :param value:
            The new value (private key).

        :raise TypeError:
            Whether :code:`value` is not :py:class`str`.
        """

        if not isinstance(description, str):
            raise TypeError(
                f"<value> {description} should be {str}. {type(description)} given."
            )

        data = {"key_pair.description": description}

        comm = getattr(communicator, self.__class__.__name__)(
            self._PyTravisCI["com"]["requester"]
        )

        self.__dict__ = comm.update(data=data, **self._PyTravisCI["shared"]).__dict__

        return self

    def delete(self) -> Union[bool, "resource_types.KeyPair"]:
        """
        Deletes the current key pair.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/key_pair
        """

        comm = getattr(communicator, self.__class__.__name__)(
            self._PyTravisCI["com"]["requester"]
        )

        return comm.delete(**self._PyTravisCI["shared"])
