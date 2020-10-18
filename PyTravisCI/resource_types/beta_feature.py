"""
Just another Python API for Travis CI (API).

A module which provides the "Beta Feature" resource type.

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


class BetaFeature(ResourceTypesBase):
    """
    Provides the description of a beta feature.

    Official Travis CI API documentation:
        - https://developer.travis-ci.org/resource/beta_feature

    :ivar int id:
        Value uniquely identifying the beta feature.
    :ivar str name:
        The name of the feature.
    :ivar str description:
        Longer description of the feature.
    :ivar bool enabled:
        Indicates if the user has this feature turned on.
    :ivar str feedback_url:
        Url for users to leave Travis CI feedback on this feature.
    """

    id: Optional[int] = None
    name: Optional[str] = None
    decription: Optional[str] = None
    enabled: Optional[bool] = None
    feedback_url: Optional[str] = None

    def enable(self) -> bool:
        """
        Enables the current beta feature.
        """

        if not self.enabled:
            comm = getattr(communicator, self.__class__.__name__)(
                self._PyTravisCI["com"]["requester"]
            )

            self.__dict__ = comm.update(
                beta_feature_id=self.id,
                data={"beta_feature.enabled": False},
                **self._PyTravisCI["shared"],
            ).__dict__

        return self.enabled

    def disable(self) -> bool:
        """
        Disables the current beta feature.
        """

        if self.enabled:
            comm = getattr(communicator, self.__class__.__name__)(
                self._PyTravisCI["com"]["requester"]
            )

            self.__dict__ = comm.update(
                beta_feature_id=self.id,
                data={"beta_feature.enabled": False},
                **self._PyTravisCI["shared"],
            ).__dict__

        return not self.enabled

    def delete(self) -> Union[bool, "resource_types.BetaFeature"]:
        """
        Deletes the current beta feature.

        :param params:
            The query parameters to append to the URL.
        """

        comm = getattr(communicator, self.__class__.__name__)(
            self._PyTravisCI["com"]["requester"]
        )

        self.__dict__ = comm.delete(
            beta_feature_id=self.id, **self._PyTravisCI["shared"]
        ).__dict__

        return self
