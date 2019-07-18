"""
Just another Travis CI (Python) API client.

Provide the access to the jobs resource type.

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


class Jobs(Communication):
    """
    Provide the list of jobs of a given :code:`build_id`.

    Official Travis CI API documentation
        - https://developer.travis-ci.org/resource/jobs#jobs
        - https://developer.travis-ci.org/resource/jobs#find

    :param root:
        An initiated instance of :class:`~PyTravisCI.TravisCI`.
    :type root: :class:`~PyTravisCI.TravisCI`
    :param build_id:
        The ID of the build to get information for.

        Can be
            :code:`{build.id}`
                Value uniquely identifying the build.

        .. note::
            If this variable is not given or :code:`None` is given, we return
            the list of jobs of the current user.

    :type build_id: str,int
    :param int limit:
        Set the last :code:`n` jobs to return.

        .. warning::
            If a negative number or :code:`0` is given, we return everything.

    :ivar jobs: List of jobs.
    :vartype jobs:
        Generator[:class:`~PyTravisCI.resource_types.job.Job`, :code:`None`, :code:`None`]

    :raise InvalidIntArgument:
        When :code:`build_id` is not an :code:`int` or :code:`str.isdigit`.
    :raise TravisCIError:
        When something went wrong while communicating,
        getting or extracting data from or with the API.
    """

    __path_name_base__ = "jobs"

    _excluded_parameters = ["include", "offset", "sort_by"]
    """
    The list of parameters to exclude.
    """

    _parameters = {
        "active": None,
        "created_by": None,
        "job.active": None,
        "job.created_by": None,
        "job.state": None,
        "state": None,
    }
    """
    Provide the parameters we can parse to the query string.

    Indexes
        :code:`active`
            Alias for :code:`job.active`.
        :code:`created_by`
            Alias for :code:`job.created_by`.
        :code:`job.active`
            Documentation missing.
        :code:`job.created_by`
            Documentation missing.
        :code:`job.state`
            Filters jobs by current state of the job.
        :code:`state`
            Alias for :code:`job.state`.

    .. warning::
        This is only available when we create a new environment variable.

    .. warning::
        If an index is set to :code:`None`, it will be omitted.

    .. warning::
        Only the indexes listed into this variable will be parsed.
    """

    # pylint: disable=too-many-arguments
    def __init__(self, root, build_id=None, limit=5, parameters=None):
        super(Jobs, self).__init__(root)

        if build_id:
            if not self.is_digit(build_id):
                raise InvalidIntArgument("build_id")

            self._endpoint_url = self.bind_path_name_to_access_point(
                self.access_point, f"build/{build_id}/jobs"
            )

            follow_next_page = True
        else:
            self._parameters["limit"] = limit
            self.filter_parameters(parameters)

            self._endpoint_url = self.bind_path_name_to_access_point(
                self.access_point,
                self.__path_name_base__ + f"{self.convert_parameters_to_url()}",
            )

            follow_next_page = limit <= 0

        response = self.standardize.it(
            self.get_request(follow_next_page=follow_next_page)
        )

        self.response_to_attribute(
            self, {x: y for x, y in response.items() if x != "jobs"}
        )

        self.jobs = (self._root.job(x["id"]) for x in response["jobs"])
