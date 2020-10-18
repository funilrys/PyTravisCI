"""
Just another Python API for Travis CI (API).

A module which provides the "Beta Features" resource type.

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

from typing import Optional

from . import _all as resource_types
from .base import ResourceTypesBase


class BetaFeatures(ResourceTypesBase):
    """
    Provides a list of all beta features

    Official Travis CI API documentation:
        - https://developer.travis-ci.org/resource/beta_features

    :ivar beta_features: The active builds.
    :vartype beta_features: List[:class:`~PyTravisCI.resource_types.beta_feature.BetaFeature`]
    """

    __iter_through__: str = "beta_features"
    beta_features: Optional["resource_types.BetaFeature"] = None

    def __init__(self, **kwargs) -> None:
        if "beta_features" in kwargs:
            kwargs["beta_features"] = [
                resource_types.BetaFeature(**x) for x in kwargs["beta_features"]
            ]

        super().__init__(**kwargs)
