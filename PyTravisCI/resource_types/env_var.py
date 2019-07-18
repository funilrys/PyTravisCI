"""
Just another Travis CI (Python) API client.

Provide the access to the env var resource type.

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


class EnvVar(Communication):
    """
    Provide the information of a given :code:`repo_id_or_slug`
    and :code:`env_var_id`.

    Official Travis CI API documentation
        - https://developer.travis-ci.org/resource/env_var#env%20var
        - https://developer.travis-ci.org/resource/env_var#find
        - https://developer.travis-ci.org/resource/env_var#update
        - https://developer.travis-ci.org/resource/env_var#delete

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
    :param str env_var_id:
        An environment variable ID.

        Can be
            :code:`{env_var.id}`
                The environment variable id.

    :ivar str id: The environment variable id.
    :ivar str name: The environment variable name, e.g. FOO.
    :ivar str value: The environment variable's value, e.g. bar.
    :ivar str public: Whether this environment variable should be publicly visible or not.
    :ivar str branch: The env_var's branch.

    :raise MissingArgument:
        When :code:`repo_id_or_slug` nor :code:`env_var_id` is given.
    :raise TravisCIError:
        When something went wrong while communicating,
        getting or extracting data from or with the API.

    .. _standard URL encoding: http://www.w3schools.com/tags/ref_urlencode.asp
    .. _states: https://developer.travis-ci.org/resource/env_var#env%20var
    """

    __path_name_base__ = "repo"

    _parameters = {
        "env_var.name": None,
        "env_var.value": None,
        "env_var.public": None,
        "env_var.branch": None,
    }
    """
    Provide the parameters we can parse to the query string.

    Indexes
        :code:`env_var.name`
            The environment variable name, e.g. FOO.
        :code:`env_var.value`
            The environment variable's value, e.g. bar.
        :code:`env_var.public`
            Whether this environment variable should be publicly visible or not.
        :code:`env_var.branch`
            The env_var's branch.

            .. note::
                If omitted it will be available in all branches.

    .. warning::
        This is only available when we create a new environment variable.

    .. warning::
        If an index is set to :code:`None`, it will be omitted.

    .. warning::
        Only the indexes listed into this variable will be parsed.
    """

    def __init__(self, root, repo_id_or_slug, env_var_id):
        super(EnvVar, self).__init__(root)

        if not repo_id_or_slug and not env_var_id:
            raise MissingArgument(["repo_id_or_slug", "env_var_id"])

        self.__repo_id_or_slug = repo_id_or_slug

        self._endpoint_url = (
            self.__standard_endpoint_url
        ) = self.bind_path_name_to_access_point(
            self.access_point,
            f"{self.__path_name_base__}"
            f"/{self.format_slug(self.__repo_id_or_slug)}/env_var/{env_var_id}",
        )

        self.response_to_attribute(
            self, self.standardize.it(self.get_request(follow_next_page=True))
        )

    def update(self, data):
        """
        Updates the current environment variable.

        :param dict data:
            A dict with the desired parameters.

            .. seealso::
                Available parameters
                    :attr:`~PyTravisCI.resource_types.env_var.EnvVar._parameters`

        :rtype: bool

        :raise TravisCIError:
            When something went wrong while communicating,
            getting or extracting data from or with the API.
        """

        self.filter_parameters(data)
        self._parameters = self.remove_not_needed_parameters(self._parameters)

        self._endpoint_url = self.__standard_endpoint_url

        response = self.patch_request(data=self._parameters)

        if "id" in response and "name" in response:
            self.response_to_attribute(self, self.standardize.it(response))
            return True
        return False

    def delete(self):
        """
        Deletes the current environment variable.

        :rtype: bool

        :raise TravisCIError:
            When something went wrong while communicating,
            getting or extracting data from or with the API.
        """

        self._endpoint_url = self.__standard_endpoint_url

        if self.delete_request():
            return True
        return False
