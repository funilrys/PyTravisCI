"""
Just another Travis CI (Python) API client.

Provide the access to the active resource type.

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
        SOFTWARE.s
"""

from ..communication import Communication
from ..exceptions import IncompatibleArgument, InvalidIntArgument, MissingArgument


class Active(Communication):
    """
    Provide the list of all active builds.

    Official Travis CI API documentation
        - https://developer.travis-ci.org/resource/active#Active
        - https://developer.travis-ci.org/resource/active#for_owner

    .. warning::
        :code:`owner` can't be set at the same time as :code:`github_id`.

    :param root:
        An initiated instance of :class:`~PyTravisCI.TravisCI`.
    :type root: :class:`~PyTravisCI.TravisCI`
    :param str owner:
        The GitHub user or organization login to get the list of active builds for.

        Can be
            :code:`{owner.login}`
                User or organization login set on GitHub.
            :code:`{user.login}`
                Login set on Github.
            :code:`{organization.login}`
                Login set on GitHub.

    :param github_id:
        The GitHub user or organization ID to get the active builds for.

        Can be
            :code:`{owner.github_id}`
                User or organization id set on GitHub.

    :type github_id: str,int

    :ivar builds: The active builds.
    :vartype builds:
        Generator[:class:`~PyTravisCI.resource_types.build.Build`, :code:`None`, :code:`None`]

    :raise MissingArgument:
        When :code:`owner` nor :code:`github_id` are given.
    :raise IncompatibleArgument:
        When :code:`owner` is given along with :code:`github_id`.
    :raise InvalidIntArgument:
        When :code:`github_id` is not an :code:`int` nor :code:`str.is_digit`.
    :raise TravisCIError:
        When something went wrong while communicating,
        getting or extracting data from or with the API.
    """

    __path_name_base__ = "owner"

    def __init__(self, root, owner=None, github_id=None):
        super(Active, self).__init__(root)

        if not owner and not github_id:
            MissingArgument(["owner", "github_id"])

        if owner and github_id:
            raise IncompatibleArgument(["owner", "github_id"])

        if github_id and not self.is_digit(github_id):
            raise InvalidIntArgument("github_id")

        if owner:
            self._endpoint_url = self.bind_path_name_to_access_point(
                self.access_point, f"{self.__path_name_base__}/{owner}/active"
            )
        else:
            self._endpoint_url = self.bind_path_name_to_access_point(
                self.access_point,
                f"{self.__path_name_base__}/github_id/{github_id}/active",
            )

        response = self.standardize.it(self.get_request(follow_next_page=True))

        self.response_to_attribute(
            self, {x: y for x, y in response.items() if x != "builds"}
        )

        self.builds = (self._root.build(x["id"]) for x in response["builds"])
