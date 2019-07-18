"""
Just another Travis CI (Python) API client.

Provide the access to the branches resource type.

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


class Branches(Communication):
    """
    Provide the list of branches of the given :code:`repo_id_or_slug`.

    Official Travis CI API documentation
        - https://developer.travis-ci.org/resource/branches#Branches
        - https://developer.travis-ci.org/resource/branches#find

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

    :param sort_by:
        Set the sorting to use.

        .. note::
             One can append :code:`:desc` to any indexes in order to reverse the order.

    :param dict parameters:
        A :code:`dict` of parameters to parse to the request.

        .. seealso::
            - :attr:`PyTravisCI.resource_types.branches.Branches._parameters`

    :type sort_by: str,list

    :ivar branches: List of branches.
    :vartype branches:
        Generator[:class:`~PyTravisCI.resource_types.branch.Branch`, :code:`None`, :code:`None`]

    :raise ValueError:
        When :code:`parameters` is not a :code:`dict`.
    :raise MissingArgument:
        When :code:`repo_id_or_slug` is not given or is empty.
    :raise TravisCIError:
        When something went wrong while communicating,
        getting or extracting data from or with the API.

    .. _standard URL encoding: http://www.w3schools.com/tags/ref_urlencode.asp
    .. _states: https://developer.travis-ci.org/resource/branches#branches
    """

    __path_name_base__ = "repo"

    _excluded_parameters = ["include", "offset", "limit"]
    """
    The list of parameters to exclude.
    """

    _parameters = {
        "branch.exists_on_github": None,
        "branch.name": None,
        "exists_on_github": None,
        "name": None,
    }
    """
    Provide the parameters we can parse to the query string.

    Indexes
        :code:`branch.exists_on_github`
            Filters branches by whether or not the branch still exists on GitHub.
        :code:`branch.name`
            Filters branches by name of the git branch.
        :code:`exists_on_github`
            Alias for :code:`branch.exists_on_github`.
        :code:`name`
            Alias for :code:`branch.name`.

    .. warning::
        If an index is set to :code:`None`, it will be omitted.

    .. warning::
        Only the indexes listed into this variable will be parsed.
    """

    sort_by = ["default_branch", "exists_on_github", "last_build:desc"]
    """
    Provide the default sorting to use.

    .. note::
        One can append :code:`:desc` to any indexes in order to reverse the order.
    """

    # pylint: disable=too-many-arguments
    def __init__(self, root, repo_id_or_slug, sort_by=None, parameters=None):
        super(Branches, self).__init__(root)

        if not repo_id_or_slug:
            raise MissingArgument("repo_id_or_slug")

        if not sort_by:
            sort_by = self.sort_by
        else:
            if isinstance(sort_by, str):
                sort_by = [sort_by]
            else:
                sort_by = sort_by

        self._parameters["sort_by"] = ",".join(sort_by)
        repo_id_or_slug = self.format_slug(repo_id_or_slug)

        self.filter_parameters(parameters)

        self._endpoint_url = self.bind_path_name_to_access_point(
            self.access_point,
            f"{self.__path_name_base__}/{repo_id_or_slug}"
            f"/branches{self.convert_parameters_to_get_param()}",
        )

        response = self.standardize.it(self.get_request(follow_next_page=True))

        self.response_to_attribute(
            self, {x: y for x, y in response.items() if x != "branches"}
        )

        self.branches = (
            self._root.branch(x["repository"]["id"], x["name"])
            for x in response["branches"]
        )
