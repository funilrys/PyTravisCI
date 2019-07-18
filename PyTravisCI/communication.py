"""
Just another Travis CI (Python) API client.

Provide some connection related methods.

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

import urllib.parse as urllib_parse
from http.client import responses as http_status_code_responses
from json import decoder

from requests import Session

from PyTravisCI.exceptions import TravisCIError
from PyTravisCI.helpers.dict import Dict
from PyTravisCI.standardize import Standardize


class Communication:
    """
    Provide some interesting methods which we use to:

        - Prepare the communication with the API.
        - Communicate with the API.
        - Interpret API responses.
    """

    def __init__(self, root):
        self._root = root
        self.__session = self._root.session

        self.access_point = self._root.access_point
        self.standardize = Standardize(self._root)

    def __getitem__(self, index):
        return getattr(self, index, None)

    def __setitem__(self, index, value):
        setattr(self, index, value)

    def __getattr__(self, index):
        if index.startswith("_"):
            return {}

        return None

    @classmethod
    def bind_path_name_to_access_point(cls, access_point, path_name):
        """
        Bind the pathname with the access point.

        Example
            Given :code:`https://example.org` as :code:`access_point`
            and :code:`/orgs/list` as :code:`path_name`, we return
            :code:`https://example.org/orgs/list`.

        :param str access_point: The access point to bind :code:`path_name` with.
        :param str path_name: The path name to bind to :code:`access_point`.

        :rtype: str
        """

        if not isinstance(path_name, str):
            path_name = str(path_name)

        if not path_name.startswith("http"):
            if access_point.endswith("/"):
                if path_name.startswith("/"):
                    path_name = path_name[1:]
            else:
                if not path_name.startswith("/"):
                    path_name = f"/{path_name}"

            return access_point + path_name
        return path_name

    @classmethod
    def filter_response(cls, api_response):
        """
        Filter the API response for future usage.

        The objective befind this method is to remove all tags (:code:`@xyz`)
        from the API response.

        :param dict api_response: The API response.

        :rtype: dict
        """

        if isinstance(api_response, dict):
            result = {}

            for key, value in api_response.items():
                if key.startswith("@"):
                    continue

                if isinstance(value, dict):
                    result[key] = cls.filter_response(value)
                elif isinstance(value, list):
                    result[key] = [cls.filter_response(x) for x in value]
                else:
                    result[key] = value

            return result

        if isinstance(api_response, list):
            return [cls.filter_response(x) for x in api_response]

        return api_response

    @classmethod
    def format_slug(cls, slug):
        """
        Convert a slug into a URL encoded string.

        Example
            Given :code:`example.org/test` will give us
            :code:`example.org%2Ftest`

        :param slug: The slug to format.
        :type slug: str,int

        .. warning::
            As we do not want some headache as everytime
            the slug is accepted an :code:`id` can be given,
            we choose to handle both case.

            Indeed, if an ID is given, we simply return it without
            formatting.

        :rtype: str,int
        """

        if slug and not cls.is_digit(slug) and "%" not in slug:
            slug = urllib_parse.quote(slug, safe="")

        return slug

    @classmethod
    def get_error_message(cls, api_response):
        """
        Get the error message if the API response is or contain an error.

        :param dict api_response: The API response.

        :rtype: None,str
        """
        if cls.is_error(api_response):
            return api_response["error_message"]
        return None

    @classmethod
    def get_error_type(cls, api_response):
        """
        Get the error type if the API response is or contain an error.

        :param dict api_response: The API response.

        :rtype: None,str
        """

        if cls.is_error(api_response):
            return api_response["error_type"]
        return None

    @classmethod
    def is_digit(cls, user_input):
        """
        Checks if the given input is an integer or a digit string.

        :rtype: bool
        """

        return isinstance(user_input, int) or (
            isinstance(user_input, str) and user_input.isdigit()
        )

    @classmethod
    def is_error(cls, api_response):
        """
        Check if the API response is or contain an error.

        :param dict api_response: The API response.

        :rtype: bool
        """

        if api_response and isinstance(api_response, dict):
            if "@type" in api_response and api_response["@type"] == "error":
                return True

        return False

    @classmethod
    def remove_not_needed_parameters(cls, parameters):
        """
        Remove the paramaters that are not needed.

        .. note::
            A paramater is considerer as not needed if its value is equal
            to :code:`None`.
        """

        return {x: y for x, y in parameters.items() if y is not None}

    @classmethod
    def response_to_attribute(cls, instance, api_response):
        """
        Convert the API response into attribute of the given instance.

        Example
            If the API response gives us

            ::

                {
                    "hello": "world",
                    "world": "hello"
                }

            this method set the attribute so that they become accessible with
            :code:`instance.hello` :code:`instance.world`.

            .. note::
                The :code:`hello` index (for exampel) is always accessible
                through the following methods

                - :code:`instance.hello`
                - :code:`instance["hello"]`

        :param obj instance: The instance we have to initiate the attribute into.
        :param dict api_response: The API response.
        """

        if isinstance(api_response, dict):
            for key, value in api_response.items():
                setattr(instance, key, value)

        return instance

    def convert_parameters_to_get_param(self):
        """
        Convert the given :code:`dict` paramaters into an URL encoded
        parameters.

        :rtype: str
        """

        parameters = self._parameters
        excluded = self._excluded_parameters

        result = ""
        if parameters:

            for index, value in parameters.items():
                if index in excluded:
                    continue

                if value is not None:
                    index = urllib_parse.quote(index, safe="")

                    if isinstance(value, str) and "%" not in value:
                        value = urllib_parse.quote(value, safe="")
                    elif isinstance(value, bool):
                        value = str(value).lower()
                    else:
                        value = value

                    result += f"{index}={value}&"

            if result:
                return f"?{result[:-1]}"
        return result

    def delete_request(self):  # pragma: no cover
        """
        Make a DELETE request to the :code:`self._endpoint_url` (expected),
        filter its response, and return it.

        :raise TravisCIError:
            - When something went wrong with our request.
            - When permissions are missing.
        """

        if self._endpoint_url and isinstance(self.__session, Session):
            result = {}

            req = self.__session.delete(self._endpoint_url)

            try:
                response = req.json()
                is_error = self.is_error(response)

                if not is_error and req.status_code == 200:
                    result = self.filter_response(response)
                elif is_error:
                    raise TravisCIError(
                        req.url,
                        self.get_error_message(response),
                        self.get_error_type(response),
                    )
                else:
                    raise TravisCIError(
                        req.url,
                        http_status_code_responses[req.status_code],
                        req.status_code,
                    )

                return result
            except decoder.JSONDecodeError:
                if req.status_code == 204:
                    return True
                return False
        return None

    def filter_parameters(self, given):
        """
        Filter the given parameters.

        Indeed, as we want to only get the supported one,
        this method return the given parameters without
        the indexes which are not supported.

        :param list supported: The list of supported indexes.
        :param dict given: The given parameters.

        :rtype: dict
        """

        result = {}

        if given:
            if isinstance(given, dict):
                result = {
                    x: y for x, y in given.items() if x in self._parameters.keys()
                }
            else:
                raise ValueError(f"<parameters> has the wrong type ({type(given)})")

        self._parameters.update(result)

    def get_request(self, follow_next_page=True):  # pragma: no cover
        """
        Make a GET request to the :code:`self._endpoint_url` (expected),
        filter its response, and return it.

        :param bool follow_next_page:
            As Travis CI use a pager for some page, setting this argument
            to :code:`True` will means that we follow and fetch the
            response of all pages. Otherwise, only the first page
            is fetched.

        :raise TravisCIError:
            - When something went wrong with our request.
            - When permissions are missing.
        """

        # pylint: disable=access-member-before-definition
        if self._endpoint_url and isinstance(self.__session, Session):
            result = {}

            while True:
                # pylint: disable=access-member-before-definition
                req = self.__session.get(self._endpoint_url)
                response = req.json()
                is_error = self.is_error(response)

                if not is_error and req.status_code == 200:
                    result = Dict(result).merge(
                        self.filter_response(response), strict=False
                    )

                    if follow_next_page:
                        url_of_next_page = self.get_url_of_next_page(response)

                        if url_of_next_page:
                            # pylint: disable=attribute-defined-outside-init
                            self._endpoint_url = url_of_next_page
                        else:
                            break
                    else:
                        break
                elif is_error:
                    raise TravisCIError(
                        req.url,
                        self.get_error_message(response),
                        self.get_error_type(response),
                    )
                else:
                    raise TravisCIError(
                        req.url,
                        http_status_code_responses[req.status_code],
                        req.status_code,
                    )

            return result
        return None

    def get_url_of_next_page(self, api_response):
        """
        Given an API response we extract and construct the url to the next page
        if given.

        :param dict api_response: The API response.

        :rtype: None,str
        """

        if api_response:
            if "@pagination" in api_response:
                if "next" in api_response["@pagination"] and isinstance(
                    api_response["@pagination"]["next"], dict
                ):
                    return self.bind_path_name_to_access_point(
                        self.access_point, api_response["@pagination"]["next"]["@href"]
                    )
        return None

    def patch_request(self, data=None):  # pragma: no cover
        """
        Make a PATCH request to the :code:`self._endpoint_url` (expected),
        filter its response, and return it.

        :param dict data: The data to transmit along with the POST request.

        :raise TravisCIError:
            - When something went wrong with our request.
            - When permissions are missing.
        """

        if self._endpoint_url and isinstance(self.__session, Session):
            result = {}

            if not data:
                data = {}

            req = self.__session.patch(self._endpoint_url, data=data)
            response = req.json()
            is_error = self.is_error(response)

            if not is_error and req.status_code == 200:
                result = self.filter_response(response)
            elif is_error:
                raise TravisCIError(
                    req.url,
                    self.get_error_message(response),
                    self.get_error_type(response),
                )
            else:
                raise TravisCIError(
                    req.url,
                    http_status_code_responses[req.status_code],
                    req.status_code,
                )

            return result
        return None

    def post_request(self, data=None):  # pragma: no cover
        """
        Make a POST request to the :code:`self._endpoint_url` (expected),
        filter its response, and return it.

        :param dict data: The data to transmit along with the POST request.

        :raise TravisCIError:
            - When something went wrong with our request.
            - When permissions are missing.
        """

        if self._endpoint_url and isinstance(self.__session, Session):
            result = {}

            if not data:
                data = {}

            req = self.__session.post(self._endpoint_url, data=data)
            response = req.json()
            is_error = self.is_error(response)

            if not is_error and req.status_code == 200:
                result = self.filter_response(response)
            elif is_error:
                raise TravisCIError(
                    req.url,
                    self.get_error_message(response),
                    self.get_error_type(response),
                )
            else:
                raise TravisCIError(
                    req.url,
                    http_status_code_responses[req.status_code],
                    req.status_code,
                )

            return result
        return None
