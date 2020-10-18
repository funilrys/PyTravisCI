"""
Just another Python API for Travis CI (API).

A module which provides the "Env Var" resource type.

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


class EnvVar(ResourceTypesBase):
    """
    Provides the description of an environment variable.

    Official Travis CI API documentation
        - https://developer.travis-ci.org/resource/env_var

    :ivar str id:
        The environment variable id.
    :ivar str name;
        The environment variable name, e.g. FOO.
    :ivar str value:
        The environment variable's value, e.g. bar.
    :ivar bool public:
        Whether this environment variable should be publicly visible or not.
    :ivar branch:
        The env_var's branch.
    """

    id: Optional[str] = None
    name: Optional[str] = None
    value: Optional[str] = None
    public: Optional[bool] = None
    branch = None

    def make_public(self) -> "resource_types.EnvVar":
        """
        Makes this environment variable public.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/env_var
        """

        if not self.public:
            data = {"env_var.public": True}

            comm = getattr(communicator, "EnvVar")(self._PyTravisCI["com"]["requester"])

            if "env_var_id" not in self._PyTravisCI["shared"]:
                response = comm.update(
                    env_var_id=self.id,
                    data=data,
                    **self._PyTravisCI["shared"],
                )
            else:
                response = comm.update(
                    data=data,
                    **self._PyTravisCI["shared"],
                )

            self.__dict__ = response.__dict__

        return self

    def make_private(self) -> "resource_types.EnvVar":
        """
        Makes this environment variable public.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/env_var
        """

        if self.public:
            data = {"env_var.public": False}

            comm = getattr(communicator, "EnvVar")(self._PyTravisCI["com"]["requester"])

            if "env_var_id" not in self._PyTravisCI["shared"]:
                response = comm.update(
                    env_var_id=self.id,
                    data=data,
                    **self._PyTravisCI["shared"],
                )
            else:
                response = comm.update(
                    data=data,
                    **self._PyTravisCI["shared"],
                )

            self.__dict__ = response.__dict__

        return self

    def set_branch(self, branch_name: str) -> "resource_types.EnvVar":
        """
        Sets the name of the branch which is covered by the current
        environment variable.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/env_var

        :param branch_name:
            The name of the branch to apply.
        """

        if self.branch != branch_name:
            data = {"env_var.branch": branch_name}

            comm = getattr(communicator, "EnvVar")(self._PyTravisCI["com"]["requester"])

            if "env_var_id" not in self._PyTravisCI["shared"]:
                response = comm.update(
                    env_var_id=self.id,
                    data=data,
                    **self._PyTravisCI["shared"],
                )
            else:
                response = comm.update(
                    data=data,
                    **self._PyTravisCI["shared"],
                )

            self.__dict__ = response.__dict__

        return self

    def set_value(self, value: str) -> "resource_types.EnvVar":
        """
        Sets the new value of the current environment variable.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/env_var

        :param value:
            The new value.

        :raise TypeError:
            Whether :code:`value` is not :py:class:`str`.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> {value} should be {str}. {type(value)} given.")

        data = {"env_var.value": value}

        comm = getattr(communicator, self.__class__.__name__)(
            self._PyTravisCI["com"]["requester"]
        )

        if "env_var_id" not in self._PyTravisCI["shared"]:
            response = comm.update(
                env_var_id=self.id,
                data=data,
                **self._PyTravisCI["shared"],
            )
        else:
            response = comm.update(
                data=data,
                **self._PyTravisCI["shared"],
            )

        self.__dict__ = response.__dict__

        return self

    def set_name(self, name: str) -> "resource_types.EnvVar":
        """
        Sets the new name of the current environment variable.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/env_var

        :param name:
            The new name

        :raise TypeError:
            Whether :code:`name` is not :py:class:`str`.
        """

        if not isinstance(name, str):
            raise TypeError(f"<value> {name} should be {str}. {type(name)} given.")

        if self.name != name:
            data = {"env_var.name": name}

            comm = getattr(communicator, self.__class__.__name__)(
                self._PyTravisCI["com"]["requester"]
            )

            if "env_var_id" not in self._PyTravisCI["shared"]:
                response = comm.update(
                    env_var_id=self.id,
                    data=data,
                    **self._PyTravisCI["shared"],
                )
            else:
                response = comm.update(
                    data=data,
                    **self._PyTravisCI["shared"],
                )

            self.__dict__ = response.__dict__

        return self

    def delete(self) -> Union[bool, "resource_types.EnvVar"]:
        """
        Deletes the current environment variable.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/env_var
        """

        comm = getattr(communicator, self.__class__.__name__)(
            self._PyTravisCI["com"]["requester"]
        )

        return comm.delete(env_var_id=self.id, **self._PyTravisCI["shared"])
