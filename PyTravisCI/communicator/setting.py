"""
Just another Python API for Travis CI (API).

A module which provides the communicator of the "Setting" resource type.

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

import copy

from .base import CommunicatorBase


class Setting(CommunicatorBase):
    """
    The communicator of the Setting resource type.
    """

    # pylint: disable=missing-function-docstring

    endpoints = {
        "from_provider": "/repo/%(provider)s/%(repository_id_or_slug)s/setting/%(setting_name)s",
        "from_id_or_slug": "/repo/%(repository_id_or_slug)s/setting/%(setting_name)s",
        "update": "/repo/%(repository_id_or_slug)s/setting/%(setting_name)s",
    }

    @CommunicatorBase.complete_response
    @CommunicatorBase.filter_before_action
    def from_provider(self, **kwargs) -> "resource_types.Setting":
        return self.resource_types.Setting(
            **self.get_standardized(
                self.get_response(self.get_and_construct_endpoint(kwargs))
            )
        )

    @CommunicatorBase.complete_response
    @CommunicatorBase.filter_before_action
    def from_id_or_slug(self, **kwargs) -> "resource_types.Setting":
        return self.resource_types.Setting(
            **self.get_standardized(
                self.get_response(self.get_and_construct_endpoint(kwargs))
            )
        )

    @CommunicatorBase.complete_response
    @CommunicatorBase.filter_before_action
    def update(self, **kwargs) -> "resource_types.Setting":
        data = None

        if "data" in kwargs:
            data = copy.deepcopy(kwargs["data"])

            del kwargs["data"]

        return self.resource_types.Setting(
            **self.get_standardized(
                self.patch_response(self.get_and_construct_endpoint(kwargs), data=data)
            )
        )
