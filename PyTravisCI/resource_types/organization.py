"""
Just another Travis CI (Python) API client.

Provide the access to the organization resource type.

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
from ..communication import Communication
from ..exceptions import InvalidIntArgument, MissingArgument


class Organization(Communication):
    """
    Provide the information of a given :code:`org_id`.

    Official Travis CI API documentation
        - https://developer.travis-ci.org/resource/organization#organization
        - https://developer.travis-ci.org/resource/organization#find

    :param root:
        An initiated instance of :class:`~PyTravisCI.TravisCI`.
    :type root: :class:`~PyTravisCI.TravisCI`
    :param org_id:
        An organization ID to get the information for.

        Can be
            :code:`{organization.id}`
                Value uniquely identifying the organization.

    :type org_id: str,int

    :ivar int id: Value uniquely identifying the organization.
    :ivar str login: Login set on GitHub.
    :ivar str name: Name set on GitHub.
    :ivar int github_id: Id set on GitHub.
    :ivar str avatar_url: Avatar_url set on GitHub.
    :ivar bool education: Whether or not the organization has an education account.
    :ivar bool allow_migration: The organization's allow_migration.

    :raise MissingArgument:
        When :code:`org_id` is empty.
    :raise InvalidIntArgument:
        When :code:`org_id` is not an :code:`int` or a :code:`str.isdigit()`.
    :raise TravisCIError:
        When something went wrong while communicating,
        getting or extracting data from or with the API.
    """

    __path_name_base__ = "org"

    def __init__(self, root, org_id):
        super(Organization, self).__init__(root)

        if not org_id:
            raise MissingArgument("org_id")

        if not self.is_digit(org_id):
            raise InvalidIntArgument("org_id")

        self._endpoint_url = self.bind_path_name_to_access_point(
            self.access_point, f"{self.__path_name_base__}/{org_id}"
        )

        self.response_to_attribute(
            self, self.standardize.it(self.get_request(follow_next_page=True))
        )
