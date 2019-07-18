"""
Just another Travis CI (Python) API client.

Provide the access to the branch resource type.

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
from ..exceptions import MissingArgument


class Branch(Communication):
    """
    Provide the information of a given :code:`branch_name` if exists at the given
    :code:`repo_id_or_slug`.

    Official Travis CI API documentation
        - https://developer.travis-ci.org/resource/branch#Branch
        - https://developer.travis-ci.org/resource/branch#find

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

    :type repo_id_or_slug: str,int

    :param str branch_name:
        The name of the git branch to get information from.

        Can be
            :code:`{branch.name}`
                Name of the git branch.

    :ivar str name: Name of the git branch.
    :ivar dict repository:
        GitHub user or organization the branch belongs to.
    :ivar bool default_branch:
        Whether or not this is the resposiotry's default branch.
    :ivar bool exists_on_github:
        Whether or not the branch still exists on GitHub.
    :ivar last_build:
        Last build on the branch.
    :vartype last_build: :class:`~PyTravisCI.resource_types.build.Build`

    :raise MissingArgument:
        When :code:`repo_is_or_slug` is not given or is empty.
    :raise MissingArgument:
        When :code:`branch_name` is not given or is empty.
    :raise TravisCIError:
        When something went wrong while communicating,
        getting or extracting data from or with the API.

    .. _standard URL encoding: http://www.w3schools.com/tags/ref_urlencode.asp
    .. _states: https://developer.travis-ci.org/resource/branch#branch
    """

    __path_name_base__ = "repo"

    def __init__(self, root, repo_id_or_slug, branch_name):
        super(Branch, self).__init__(root)

        if not repo_id_or_slug:
            raise MissingArgument("repo_id_or_slug")

        if not branch_name:
            raise MissingArgument("branch_name")

        repo_id_or_slug = self.format_slug(repo_id_or_slug)

        self._endpoint_url = self.bind_path_name_to_access_point(
            self.access_point,
            f"{self.__path_name_base__}" f"/{repo_id_or_slug}/branch/{branch_name}",
        )

        response = self.standardize.it(self.get_request(follow_next_page=True))

        if "last_build" in response and response["last_build"]:
            response["last_build"] = self._root.build(
                build_id=response["last_build"]["id"]
            )

        self.response_to_attribute(self, response)
