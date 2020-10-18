"""
Just another Python API for Travis CI (API).

A module which provides the standardizer class. It's basically a way to unify
everything before parsing them to their end-location or objects.

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
from datetime import datetime
from functools import wraps
from typing import Any, Optional

import PyTravisCI.defaults as defaults


class Standardization:
    """
    The standardizer. It format the response from the Travis CI API into
    something useful (for later usage and distribution).
    """

    data: Optional[Any] = None

    def __init__(self, data: Optional[Any] = None) -> None:
        self.data = data

    def set_data(self, value: Any) -> None:
        """
        Overwrites the data to work with.
        """

        self.data = value

    def get_data(self) -> Any:
        """
        Provides the currently set data.
        """

        return self.data

    def run_standardization(func):  # pylint: disable=no-self-argument
        """
        A decorator which actually do the standardization.
        """

        @wraps(func)
        def wrapper(self):

            result = copy.deepcopy(self.data)

            for method_name in dir(self):
                if method_name.startswith("standardize_"):
                    result = getattr(self, method_name)(result)

            return result

        return wrapper

    @run_standardization
    def get_standardized(self) -> dict:
        """
        Provides the standardized version.
        """

    def standardize_datetime(self, data: dict) -> dict:
        """
        Provides a way to unify/convert the dates to something more
        Python friendly.
        """

        date_time_indexes = [
            "committed_at",
            "created_at",
            "finished_at",
            "last_modified",
            "last_run",
            "next_run",
            "started_at",
            "synced_at",
            "updated_at",
        ]

        if isinstance(data, dict):
            result = dict()

            for key, value in copy.deepcopy(data).items():
                if (
                    value
                    and key in date_time_indexes
                    and not isinstance(value, datetime)
                ):
                    try:
                        result[key] = datetime.strptime(
                            value, defaults.formats.STANDARD_DATE_FORMAT
                        )
                    except ValueError:
                        result[key] = datetime.strptime(
                            value, defaults.formats.ALTERNATIVE_DATE_FORMAT
                        )
                else:
                    if isinstance(value, dict):
                        result[key] = self.standardize_datetime(value)
                    elif isinstance(value, list):
                        result[key] = [self.standardize_datetime(x) for x in value]
                    else:
                        result[key] = value
        elif isinstance(data, list):
            result = [self.standardize_datetime(x) for x in data]
        else:
            result = data

        return result

    def standardize_at_tagged(self, data: dict) -> dict:
        """
        Standardize the :code:`@tags` to something universal
        and reusable.
        """

        if isinstance(data, dict):
            result = dict()

            for key, value in copy.deepcopy(data).items():
                result[key.replace("@", "_at_")] = self.standardize_at_tagged(value)
        elif isinstance(data, list):
            result = [self.standardize_at_tagged(x) for x in data]
        else:
            result = data

        return result
