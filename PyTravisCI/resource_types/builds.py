"""
Just another Travis CI (Python) API client.

Provide the access to the builds resource type.

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
from ..exceptions import InvalidIntArgument


class Builds(Communication):
    """
    Provide the information of a given :code:`repo_id_or_slug`.

    Official Travis CI API documentation
        - https://developer.travis-ci.org/resource/builds#Builds
        - https://developer.travis-ci.org/resource/builds#for_current_user
        - https://developer.travis-ci.org/resource/builds#find

    :param root:
        An initiated instance of :class:`~PyTravisCI.TravisCI`.
    :type root: :class:`~PyTravisCI.TravisCI`
    :param repo_id_or_slug:
        A repository ID or slug to get the information for.

        Can be
            :code:`{repository.id}`
                Value uniquely identifying the repository.
            :code:`{repository.slug}`
                Same as :code:`{repository.owner.name}/{repository.name}`

        .. warning::
            The Travis CI API `states`_:

                If querying using the repository slug, it must be formatted using
                `standard URL encoding`_, including any special characters.

            We do not except nor want that that from you.
            In fact, we do the encoding for you.

        .. note::
            If this variable is not given or :code:`None` is given, we return
            the list of builds of the current user.
    :type repo_id_or_slug: str,int
    :param int limit:
        Set the last :code:`n` build to return.

        .. warning::
            If a negative number or :code:`0` is given, we return everything.

    :ivar builds: The active builds.
    :vartype builds:
        Generator[:class:`~PyTravisCI.resource_types.build.Build`, :code:`None`, :code:`None`]

    :raise InvalidIntArgument:
        When :code:`limit` is not an :code:`int` or :code:`str.isdigit`.
    :raise TravisCIError:
        When something went wrong while communicating,
        getting or extracting data from or with the API.

    .. _standard URL encoding: http://www.w3schools.com/tags/ref_urlencode.asp
    .. _states: https://developer.travis-ci.org/resource/builds#builds
    """

    __path_name_base__ = "builds"

    def __init__(self, root, repo_id_or_slug=None, limit=5):
        super(Builds, self).__init__(root)

        if not self.is_digit(limit):
            raise InvalidIntArgument("limit")

        limit = int(limit)

        if repo_id_or_slug:
            repo_id_or_slug = self.format_slug(repo_id_or_slug)

            self._endpoint_url = self.bind_path_name_to_access_point(
                self.access_point, f"repo/{repo_id_or_slug}/builds?limit={int(limit)}"
            )
        else:
            self._endpoint_url = self.bind_path_name_to_access_point(
                self.access_point, f"{self.__path_name_base__}?limit={int(limit)}"
            )

        follow_next_page = limit <= 0
        response = self.standardize.it(
            self.get_request(follow_next_page=follow_next_page)
        )

        self.response_to_attribute(
            self, {x: y for x, y in response.items() if x != "builds"}
        )

        self.builds = (self._root.build(x["id"]) for x in response["builds"])
