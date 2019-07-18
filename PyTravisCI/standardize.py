"""
Just another Travis CI (Python) API client.

Provide a way to standardize some information and indexes.

Author
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Project link
    https://github.com/funilrys/PyTravisCI

License
    ::


        MIT License

        Copyright (c) 2019 Nissar Chababy

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

from datetime import datetime


class Standardize:
    """
    Standardize the format of type of indexes from the API response.

    :param root:
        An initiated instance of :class:`~PyTravisCI.TravisCI`.

        .. note::
            This is not used for not but might me in the future.
    :type root: :class:`~PyTravisCI.TravisCI`

    .. warning::
        You should never call or use this class "manually" (unless you know what you do).
    """

    __date_format__ = "%Y-%m-%dT%H:%M:%SZ"
    __alternative_date_format = "%Y-%m-%dT%H:%M:%S.%fZ"

    date_time_indexes = [
        "committed_at",
        "created_at",
        "finished_at",
        "last_run",
        "next_run",
        "started_at",
        "updated_at",
        "synced_at",
    ]
    """
    Provide the index which will be converted by
    :meth:`PyTravisCI.standardize.Standardize.date_and_time`.
    """

    def __init__(self, root):
        self.root = root
        self.api_response = {}

    def date_and_time(self):
        """
        Unify the dates format. Indeed, as we want to be able to manipulate
        the dates, I think that it's great to convert them to
        a usable :class:`~datetime.datetime` format.
        """

        for index in self.date_time_indexes:
            if index in self.api_response and self.api_response[index]:
                try:
                    self.api_response[index] = datetime.strptime(
                        self.api_response[index], self.__date_format__
                    )
                except ValueError:
                    self.api_response[index] = datetime.strptime(
                        self.api_response[index], self.__alternative_date_format
                    )

    # pylint: disable=invalid-name
    def it(self, api_response):
        """
        Process the standardization of the given
        :code:`api_response`.

        :param dict api_response: An API response.
        """

        self.api_response = api_response

        self.date_and_time()

        return self.api_response
