"""
Just another Travis CI (Python) API client.

Provide the access to the cron resource type.

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
from ..exceptions import (
    IncompatibleArgument,
    InvalidIntArgument,
    MissingArgument,
    TravisCIError,
)


class Cron(Communication):
    """
    Provide the cron information.

    Official Travis CI API documentation
        - https://developer.travis-ci.org/resource/cron#Cron
        - https://developer.travis-ci.org/resource/cron#delete
        - https://developer.travis-ci.org/resource/cron#for_branch
        - https://developer.travis-ci.org/resource/cron#create

    :param root:
        An initiated instance of :class:`~PyTravisCI.TravisCI`.
    :type root: :class:`~PyTravisCI.TravisCI`
    :param cron_id:
        A cron ID to get information for.

        Can be
            :code:`{cron.id}`
                Value uniquely identifying the cron.

    :type cron_id: str,int
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

    :ivar int id: Value uniquely identifying the cron.
    :ivar dict repository: Github repository to which this cron belongs.
    :ivar dict branch: Git branch of repository to which this cron belongs.
    :ivar str interval:
        Interval at which the cron will run (can be "daily", "weekly" or "monthly").
    :ivar bool dont_run_if_recent_build_exists:
        Whether a cron build should run if there
        has been a build on this branch in the last 24 hours.
    :ivar last_run: When the cron ran last.
    :vartype last_run: :class:`~datetime.datetime`
    :ivar next_run: When the cron is scheduled to run next.
    :vartype next_run: :class:`~datetime.datetime`
    :ivar created_at: When the cron was created.
    :vartype created_at: :class:`~datetime.datetime`
    :ivar bool active: 	The cron's active.


    :raise IncompatibleArgument:
        When :code:`cron_id` is given along with :code:`repo_id_or_slug`.
    :raise IncompatibleArgument:
        When :code:`cron_id` is given along with :code:`branch_name`.
    :raise MissingArgument:
        When :code:`repo_id_or_slug` is given but not :code:`branch_name`.
    :raise MissingArgument:
        When :code:`branch_name` is given but not :code:`repo_id_or_slug`.
    :raise MissingArgument:
        When :code:`cron_id`, :code:`repo_id_or_slug` nor :code:`branch_name`
        are given.
    :raise InvalidIntArgument:
        When :code:`cron_id` is not an :code:`int` or :code:`str.isdigit`.
    :raise TravisCIError:
        When something went wrong while communicating,
        getting or extracting data from or with the API.

    .. _standard URL encoding: http://www.w3schools.com/tags/ref_urlencode.asp
    .. _states: https://developer.travis-ci.org/resource/cron#cron
    """

    __path_name_base__ = "cron"

    _accepted_interval = ["daily", "weekly", "montly"]
    """
    The list of interval which are accepted when creating a cronjob.
    """

    _parameters = {"cron.interval": None, "cron.dont_run_if_recent_build_exists": None}
    """
    Provide the parameters we can parse to the query string.

    .. warning::
        This is only available when we create a cronjob.

    Indexes
        :code:`cron.interval`
            Interval at which the cron will run.

            .. seealso::
                All accepted interval
                    :attr:`~PyTravisCI.resource_types.cron.Cron._accepted_interval`
        :code:`dont_run_if_recent_build_exists`
            Whether a cron build should run if there has been
            a build on this branch in the last 24 hours.

    .. warning::
        If an index is set to :code:`None`, it will be omitted.

    .. warning::
        Only the indexes listed into this variable will be parsed.
    """

    # pylint: disable=too-many-arguments
    def __init__(self, root, cron_id=None, repo_id_or_slug=None, branch_name=None):
        super(Cron, self).__init__(root)

        if cron_id and repo_id_or_slug:
            raise IncompatibleArgument(["cron_id", "repo_id_or_slug"])
        if cron_id and branch_name:
            raise IncompatibleArgument(["cron_id", "branch_name"])
        if repo_id_or_slug and not branch_name:
            raise MissingArgument("branch_name")
        if branch_name and not repo_id_or_slug:
            raise MissingArgument("repo_id_or_slug")

        if not cron_id and not repo_id_or_slug and not branch_name:
            raise MissingArgument(["cron_id", "repo_id_or_slug", "branch_name"])

        if cron_id and not self.is_digit(cron_id):
            raise InvalidIntArgument("cron_id")

        repo_id_or_slug = self.format_slug(repo_id_or_slug)

        if cron_id:
            self._endpoint_url = self.bind_path_name_to_access_point(
                self.access_point, f"{self.__path_name_base__}/{cron_id}"
            )
        else:
            self._endpoint_url = (
                self.__standard_endpoint_url
            ) = self.bind_path_name_to_access_point(
                self.access_point, f"repo/{repo_id_or_slug}/branch/{branch_name}/cron"
            )

        try:
            self.response_to_attribute(
                self, self.standardize.it(self.get_request(follow_next_page=True))
            )
        except TravisCIError as exception:
            if (
                "not_found" in exception.error_type()
                and repo_id_or_slug
                and branch_name
            ):
                pass
            else:
                raise exception

    def delete(self):
        """
        Deletes the current cron.

        :return:
            A boolean when a request was made and :code:`None` if
            no :code:`interval` (aka :code:`self.interval`) was found.

        :rtype: bool,None

        :raise TravisCIError:
            When something went wrong while communicating,
            getting or extracting data from or with the API.
        """

        if self.id and self.interval:
            self._endpoint_url = self.bind_path_name_to_access_point(
                self.access_point, f"{self.__path_name_base__}/{self.id}"
            )

            if self.delete_request():
                return True
            return False
        return None

    def create(self, data):
        """
        Create a new cron.

        :param dict data:
            A dict with the desired parameters.

            .. seealso::
                Available parameters
                    :attr:`~PyTravisCi.resource_types.cron.Cron._parameters`

        :rtype: bool
        :raise TravisCIError:
            When something went wrong while communicating,
            getting or extracting data from or with the API.
        """

        self.filter_parameters(data)
        self._parameters = self.remove_not_needed_parameters(self._parameters)

        self._endpoint_url = self.__standard_endpoint_url
        response = self.post_request(data=self._parameters)

        if "id" in response and "interval" in response:
            self.response_to_attribute(self, self.standardize.it(response))
            return True
        return False
