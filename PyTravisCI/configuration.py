"""
Just another Travis CI (Python) API client.

Provide some configurable variable which we use/parse into our infrastructure.

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

# pylint: disable=too-few-public-methods
class AccessPoints:
    """
    Provide some access point which can be used.
    """

    OPEN = "https://api.travis-ci.org"
    """
    The access point for Open Source projects.

    .. warning::
        It should never ends with :code:`/`
    """

    PRIVATE = "https://api.travis-ci.com"
    """
    The access point for private projects.

    .. warning::
        It should never ends with :code:`/`
    """

    ENTERPRISE = "https://{0}/api"
    """
    The access point for enterprise environments.

    .. note::
        If used :code:`{0}` can be replaced with the enterprise hostname.

    .. warning::
        It should never ends with :code:`/`
    """


# pylint: disable=too-few-public-methods
class Communication:
    """
    Provide some configurable variables which are parsed
    while communicating with the access point.
    """

    API_VERSION = "3"
    """
    The API version to use.

    .. warning::
        This must always be a :code:`str`.
    """

    USER_AGENT = "travisci-python-client-in-development"
    """
    The user agent to communicate to the API.

    .. note::
        We always append :code:`/The_Current_Version_Of_this_project` to
        the user agent.
    """


class States:
    """
    Provide some states oriented configuration.
    """

    STOPPED = ["canceled", "errored", "failed"]
    """
    Provide the list of states which we use to consider a build or job as stop.
    """

    PROCESSING = ["created", "started"]
    """
    Provice the list of states which we use to consider a build or job as processing.
    """
