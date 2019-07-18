"""
Just another Travis CI (Python) API client.

Provide the access to the setting resource type.

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


class Setting(Communication):
    """
    Provide the value of a given :code:`repo_id_or_slug` and :code:`setting_name`.

    Official Travis CI API documentation
        - https://developer.travis-ci.org/resource/setting#setting
        - https://developer.travis-ci.org/resource/setting#find
        - https://developer.travis-ci.org/resource/setting#update

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
    :param str setting_name:
        A setting name.

        Can be
            - :code:`builds_only_with_travis_yml`
            - :code:`build_pushes`
            - :code:`build_pull_requests`
            - :code:`maximum_number_of_builds`
            - :code:`auto_cancel_pushes`
            - :code:`auto_cancel_pull_requests`

    :ivar str name: The setting's name.
    :ivar value: The setting's value.
    :vartype value: bool,int

    :raise MissingArgument:
        When :code:`repo_id_or_slug` nor :code:`setting_name` are given.
    :raise ValueError:
        When :code:`setting_name` is not into the list of accepted setting name.
    :raise TravisCIError:
        When something went wrong while communicating,
        getting or extracting data from or with the API.

    .. _standard URL encoding: http://www.w3schools.com/tags/ref_urlencode.asp
    .. _states: https://developer.travis-ci.org/resource/setting#Setting
    """

    __path_name_base__ = "repo"

    accepted_setting_name = [
        "builds_only_with_travis_yml",
        "build_pushes",
        "build_pull_requests",
        "maximum_number_of_builds",
        "auto_cancel_pushes",
        "auto_cancel_pull_requests",
    ]
    """
    The list of accepted :code:`setting_name`.
    """

    def __init__(self, root, repo_id_or_slug, setting_name):
        super(Setting, self).__init__(root)

        if not repo_id_or_slug and not setting_name:
            raise MissingArgument(["repo_id_or_slug", "setting_name"])

        if repo_id_or_slug and not setting_name:
            raise MissingArgument("setting_name")

        if setting_name and not repo_id_or_slug:
            raise MissingArgument("repo_id_or_slug")

        if setting_name.lower() not in self.accepted_setting_name:
            raise ValueError("Unknown setting name.")

        repo_id_or_slug = self.format_slug(repo_id_or_slug)
        setting_name = setting_name.lower()

        self._endpoint_url = (
            self.__standard_endpoint_url
        ) = self.bind_path_name_to_access_point(
            self.access_point,
            f"{self.__path_name_base__}/{repo_id_or_slug}/setting/{setting_name}",
        )

        self.response_to_attribute(
            self, self.standardize.it(self.get_request(follow_next_page=False))
        )

    def update(self, new_value):
        """
        Update the current setting value.

        :param new_value: The new value to set.
        :type new_value: int,bool

        :raise ValueError:
            When a :code:`bool` nor an :code:`int` is given.
        :raise TravisCIError:
            When something went wrong while communicating,
            getting or extracting data from or with the API.
        """

        if not isinstance(new_value, int) and not isinstance(new_value, bool):
            raise ValueError(f"{type(bool)} or {type(int)} expected.")

        self._endpoint_url = self.__standard_endpoint_url
        response = self.patch_request(data={"setting.value": new_value})

        if "name" in response and "value" in response:
            self.response_to_attribute(self, self.standardize.it(response))
            return True
        return False
