"""
Just another Python API for Travis CI (API).

A module which provides the communicator of the "Cron" resource type.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Project link:
    https://github.com/funilrys/PyTravisCI

Project documentation:
    https://pytravisci.readthedocs.io/en/latest/

License
::


    MIT License

    Copyright (c) 2019, 2020, 2021, 2022 Nissar Chababy

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
from typing import Union

from .base import CommunicatorBase


class Cron(CommunicatorBase):
    """
    The communicator of the Cron resource type.
    """

    # pylint: disable=missing-function-docstring

    endpoints = {
        "from_id": "/cron/%(cron_id)s",
        "from_provider_and_branch": "/repo/%(provider)s/%(repository_id_or_slug)s/branch/%(branch_name)s/cron",  # pylint: disable=line-too-long
        "from_id_or_slug_and_branch": "/repo/%(repository_id_or_slug)s/branch/%(branch_name)s/cron",
        "create": "/repo/%(repository_id_or_slug)s/branch/%(branch_name)s/cron",
        "delete": "/cron/%(cron_id)s",
    }

    @CommunicatorBase.complete_response
    def from_id(self, **kwargs) -> "resource_types.Cron":
        return self.resource_types.Cron(
            **self.get_standardized(
                self.get_response(self.get_and_construct_endpoint(kwargs))
            )
        )

    @CommunicatorBase.complete_response
    @CommunicatorBase.filter_before_action
    def from_provider_and_branch(self, **kwargs) -> "resource_types.Cron":
        return self.resource_types.Cron(
            **self.get_standardized(
                self.get_response(self.get_and_construct_endpoint(kwargs))
            )
        )

    @CommunicatorBase.complete_response
    @CommunicatorBase.filter_before_action
    def from_id_or_slug_and_branch(self, **kwargs) -> "resource_types.Cron":
        return self.resource_types.Cron(
            **self.get_standardized(
                self.get_response(self.get_and_construct_endpoint(kwargs))
            )
        )

    @CommunicatorBase.complete_response
    @CommunicatorBase.filter_before_action
    def create(self, **kwargs) -> "resource_types.Cron":
        data = None

        if "data" in kwargs:
            data = copy.deepcopy(kwargs["data"])

            del kwargs["data"]

        return self.resource_types.Cron(
            **self.get_standardized(
                self.post_response(self.get_and_construct_endpoint(kwargs), data=data)
            )
        )

    @CommunicatorBase.complete_response
    def delete(self, **kwargs) -> Union[bool, "resource_types.Cron"]:
        response = self.get_standardized(
            self.delete_response(self.get_and_construct_endpoint(kwargs))
        )
        try:
            data = self.resource_types.Cron(**response)
        except TypeError:
            data = response

        return data
