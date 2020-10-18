"""
Just another Python API for Travis CI (API).

A module which provides the requester object. It's the object which communicates
with the API endpoints.

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

import functools
import json
import logging
from typing import Optional

import requests

import PyTravisCI.defaults as defaults
import PyTravisCI.exceptions as exceptions


class Requester:
    """
    Handles all our communication / requests to the Travis CI API.

    This only provides lower level implementation. Meaning that you give it
    raw data and it provides you raw data in exchange.
    While working with this class, you don't have access to enhanced feature
    provided by something like Resource Types objects.

    .. warning::
        You are not expected or invited to use this class directly if you
        don't know what it may imply!
    """

    def __init__(self) -> None:
        self.base_url = ""
        self.session = requests.Session()

        self.session.headers = defaults.requester.HEADERS

    def request_factory(verb: str):  # pylint: disable=no-self-argument
        """
        A decorator which acts as an universal request factory.
        """

        def request_method(func):
            @functools.wraps(func)
            def wrapper(self, endpoint, **kwargs):
                req = getattr(self.session, verb.lower())(  # pylint: disable=no-member
                    self.bind_endpoint_to_base_url(endpoint), **kwargs
                )

                try:
                    response = req.json()

                    self.raise_if_error(req, response)
                except json.decoder.JSONDecodeError:
                    if req.text:
                        # pylint: disable=raise-missing-from
                        raise exceptions.TravisCIError(
                            req.url,
                            req.text,
                            req.text.splitlines()[0],
                            response={
                                "text": req.text,
                                "headers": req.headers,
                                "status_code": req.status_code,
                            },
                        )

                    # pylint: disable=raise-missing-from
                    raise exceptions.TravisCIError(
                        req.url,
                        req.text,
                        req.text,
                        response={
                            "text": req.text,
                            "headers": req.headers,
                            "status_code": req.status_code,
                        },
                    )

                return response

            return wrapper

        return request_method

    @staticmethod
    def is_error(api_response: dict) -> bool:
        """
        Checks if the API response is or contain an error as
        defined by the Travis CI API documentation.
        """

        return (
            api_response
            and "@type" in api_response
            and api_response["@type"] == "error"
        )

    @classmethod
    def get_error_message(
        cls, api_response: dict, *, already_checked: bool = False
    ) -> Optional[str]:
        """
        Provides the error message.
        """

        is_error = True if already_checked else cls.is_error(api_response)

        return api_response["error_message"] if is_error else None

    @classmethod
    def get_error_type(
        cls, api_response: dict, *, already_checked: bool = False
    ) -> Optional[str]:
        """
        Provides the error type.
        """

        is_error = True if already_checked else cls.is_error(api_response)

        return api_response["error_type"] if is_error else None

    @classmethod
    def raise_if_error(cls, req: requests.Request, api_response: dict) -> None:
        """
        Raises a :py:class:`~PyTravisCI.exceptions.TravisCIError`
        if the given API response contain an error.
        """

        is_error = cls.is_error(api_response)

        if is_error:
            raise exceptions.TravisCIError(
                req.url,
                cls.get_error_message(api_response, already_checked=True),
                cls.get_error_type(api_response, already_checked=True),
                response=api_response,
            )

    def set_authorization(self, value: str) -> None:
        """
        Sets the authorization header.

        :raise TypeError:
            If :code:`value` is not a string.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}. {type(value)} given.")

        self.session.headers["Authorization"] = f"token {value}"

    def set_base_url(self, value: str) -> None:
        """
        Sets the base URL we have to communicate with.

        :raise TypeError:
            If :code:`value` is not a string.
        """

        if not isinstance(value, str):
            raise TypeError(f"<value> should be {str}. {type(value)} given.")

        if value.endswith("/"):
            self.base_url = value[:-1]
        else:
            self.base_url = value

        logging.debug("Base URL set to: %s", self.base_url)

    def bind_endpoint_to_base_url(self, endpoint: str) -> str:
        """
        Binds the endpoint with the base url.
        """

        if not isinstance(endpoint, str):
            raise TypeError(f"<endpoint> should be {str}, {type(endpoint)} given.")

        if not endpoint.startswith("/"):
            endpoint = f"/{endpoint}"

        return self.base_url + endpoint

    @request_factory("get")
    def get(self, endpoint: str, **kwargs) -> dict:
        """
        Sends a GET requests and returns the response.
        """

    @request_factory("options")
    def options(self, endpoint: str, **kwargs) -> dict:
        """
        Sends a OPTIONS requests and returns the response.
        """

    @request_factory("head")
    def head(self, endpoint: str, **kwargs) -> dict:
        """
        Sends a HEAD requests and returns the response.
        """

    @request_factory("post")
    def post(self, endpoint: str, **kwargs) -> dict:
        """
        Sends a POST requests and returns the response.
        """

    @request_factory("put")
    def put(self, endpoint: str, **kwargs) -> dict:
        """
        Sends a PUT requests and returns the response.
        """

    @request_factory("patch")
    def patch(self, endpoint: str, **kwargs) -> dict:
        """
        Sends a PATCH requests and returns the response.
        """

    @request_factory("delete")
    def delete(self, endpoint: str, **kwargs) -> dict:
        """
        Sends a DELETE requests and returns the response.
        """
