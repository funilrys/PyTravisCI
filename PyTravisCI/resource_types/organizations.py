"""
Just another Travis CI (Python) API client.

Provide the access to the organizations resource type.

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


# pylint:disable=line-too-long
class Organizations(Communication):
    """
    Provide the list of organizations of the current user.

    Official Travis CI API documentation
        - https://developer.travis-ci.org/resource/organizations#organizations
        - https://developer.travis-ci.org/resource/organizations#for_current_user

    :param root:
        An initiated instance of :class:`~PyTravisCI.TravisCI`.
    :type root: :class:`~PyTravisCI.TravisCI`

    :ivar organizations: List of organizations.
    :vartype organizations:
        Generator[:class:`~PyTravisCI.resource_types.organization.Organization`, :code:`None`, :code:`None`]

    :raise TravisCIError:
        When something went wrong while communicating,
        getting or extracting data from or with the API.
    """

    # pylint:enable=line-too-long

    __path_name_base__ = "orgs"

    def __init__(self, root):
        super(Organizations, self).__init__(root)

        self._endpoint_url = self.bind_path_name_to_access_point(
            self.access_point, self.__path_name_base__
        )

        response = self.standardize.it(self.get_request(follow_next_page=True))

        self.response_to_attribute(
            self, {x: y for x, y in response.items() if x != "organizations"}
        )

        self.organizations = (
            self._root.organization(x["id"]) for x in response["organizations"]
        )
