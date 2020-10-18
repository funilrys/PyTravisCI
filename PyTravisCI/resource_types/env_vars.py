"""
Just another Python API for Travis CI (API).

A module which provides the "Env Vars" resource type.

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

from . import _all as resource_types
from .base import ResourceTypesBase


class EnvVars(ResourceTypesBase):
    """
    Provides the list of environment variables.

    Official Travis CI API documentation
        - https://developer.travis-ci.org/resource/env_vars

    :ivar env_vars:
        List of env_vars.
    :vartype env_vars: List[:class:`PyTravisCI.resource_types.env_var.EnvVar`]
    """

    __iter_through__: str = "env_vars"
    env_vars: Optional[List["resource_types.EnvVar"]] = None

    def __init__(self, **kwargs) -> None:
        if "env_vars" in kwargs:
            kwargs["env_vars"] = [
                resource_types.EnvVar(**x) for x in kwargs["env_vars"]
            ]

        super().__init__(**kwargs)
