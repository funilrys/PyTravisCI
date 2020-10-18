"""
Just another Python API for Travis CI (API).

A module which provides all our exceptions.

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

from typing import Union


class PyTravisCIException(Exception):
    """
    The base of all our exceptions.
    """


class TravisCIError(PyTravisCIException):
    """
    Raises an exception with the error we got from the API.
    """

    def __init__(
        self,
        url: str,
        error_message: str,
        error_type: str,
        response: Union[dict, str] = None,
    ) -> None:
        self.url = url
        self.err_message = error_message
        self.err_type = error_type
        self.response = response

        super().__init__(self.message())

    def message(self) -> str:
        """
        Provides the message to raise.
        """

        return f"[{self.err_type}::{self.url}] {self.err_message}"

    def get_error_message(self):
        """
        Provides the error message from upstream.
        """

        return self.err_message

    def get_error_type(self):
        """
        Provides the error type from upstream.
        """

        return self.err_type

    def get_url(self):
        """
        Provides the url from upstream.
        """

        return self.url

    def get_response(self):
        """
        Provides the complete response from Travis CI.
        """

        return self.response


class PageNotFound(PyTravisCIException):
    """
    Raises an exception which informs the end-user that
    we could not find a page.
    """


class NextPageNotFound(PageNotFound):
    """
    Informs that the next page could not be found.
    """


class PreviousPageNotFound(PageNotFound):
    """
    Informs that the previous page could not be found.
    """


class FirstPageNotFound(PageNotFound):
    """
    Informs that the first page could not be found.
    """


class LastPageNotFound(PageNotFound):
    """
    Informs that the last page could not be found.
    """


class NotIncomplete(PyTravisCIException):
    """
    Informs that the current object is not incomplete.
    """


class JobAlreadyStarted(PyTravisCIException):
    """
    Informs that the current job was already started.
    """


class JobAlreadyStopped(PyTravisCIException):
    """
    Informs that the current job was already stopped.
    """


class BuildAlreadyStarted(PyTravisCIException):
    """
    Informs that the current build was already started.
    """


class BuildAlreadyStopped(PyTravisCIException):
    """
    Informs that the current build was already stopped.
    """
