"""
Just another Travis CI (Python) API client.

Provide the access to the build resource type.

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
from ..configuration import States as StatesConfig
from ..exceptions import InvalidIntArgument, MissingArgument, TravisCIError


class Build(Communication):
    """
    Provide the information of a given :code:`build_id`.

    Official Travis CI API documentation
        - https://developer.travis-ci.org/resource/build#Build
        - https://developer.travis-ci.org/resource/build#find
        - https://developer.travis-ci.org/resource/build#cancel
        - https://developer.travis-ci.org/resource/build#restart

    :param root:
        An initiated instance of :class:`~PyTravisCI.TravisCI`.
    :type root: :class:`~PyTravisCI.TravisCI`
    :param build_id:
        The ID of the build to get information for.

        Can be
            :code:`{build.id}`
                Value uniquely identifying the build.
    :type build_id: str,int

    :ivar int id: Value uniquely identifying the build.
    :ivar str number: Incremental number for a repository's builds.
    :ivar str state: Current state of the build.
    :ivar int duration: Wall clock time in seconds.
    :ivar str event_type: Event that triggered the build.
    :ivar str previous_state: State of the previous build (useful to see if state changed).
    :ivar str pull_request_title: Title of the build's pull request.
    :ivar int pull_request_number: Number of the build's pull request.
    :ivar started_at: When the build started.
    :vartype started_at: :class:`~datetime.datetime`
    :ivar finished_at: When the build finished.
    :vartype finished_at: :class:`~datetime.datetime`
    :ivar bool private: Whether or not the build is private.
    :ivar dict repository: GitHub user or organization the build belongs to.
    :ivar dict branch: The branch the build is associated with.
    :ivar str tag: The build's tag.
    :ivar dict commit: The commit the build is associated with.
    :ivar list jobs: List of jobs that are part of the build's matrix.
    :ivar list stages: The stages of the build.
    :ivar dict created_by: The User or Organization that created the build.
    :ivar updated_at: The last time the build was updated.
    :vartype updated_at: :class:`~datetime.datetime`

    :raise MissingArgument:
        When :code:`build_id` is not givne or is empty.
    :raise InvalidIntArgument:
        When :code:`build_id` is not an :code:`int` or :code:str.isdigit()`.
    :raise TravisCIError:
        When something went wrong while communicating,
        getting or extracting data from or with the API.
    """

    __path_name_base__ = "build"

    def __init__(self, root, build_id):
        super(Build, self).__init__(root)

        if not build_id:
            raise MissingArgument("build_id")

        if not self.is_digit(build_id):
            raise InvalidIntArgument("build_id")

        self.___standard_enpoint_url = self.bind_path_name_to_access_point(
            self.access_point, f"{self.__path_name_base__}/{build_id}"
        )

        self._endpoint_url = self.___standard_enpoint_url

        self.response_to_attribute(
            self, self.standardize.it(self.get_request(follow_next_page=False))
        )

    def cancel(self):
        """
        Cancels a currently running build. It will set the :code:`build`
        and associated :code:`jobs` to :code:`"state": "canceled"`.

        :return:
            A boolean if the request was made and :code:`None` if the
            state of the build is already :code:`canceled`.

        :rtype: bool,None
        :raise TravisCIError:
            When something went wrong while communicating,
            getting or extracting data from or with the API.
        """

        if self.state not in StatesConfig.STOPPED:
            self._endpoint_url = self.bind_path_name_to_access_point(
                self.___standard_enpoint_url, "cancel"
            )

            try:
                response = self.post_request()

                if "build" in response and "id" in response["build"]:
                    self.response_to_attribute(
                        self, self.standardize.it(response["build"])
                    )
                    return True
                return False
            except TravisCIError as exception:
                if (
                    "Accepted" in exception.error_message()
                    or "build_not_cancelable" in exception.error_type()
                ):
                    return True
                raise exception
        return None

    def restart(self):
        """
        Restarts a build that has completed or been canceled.

        :return:
            A boolean if the request was made and :code:`None` if
            the state of the build is :code:`created` or :code:`started`.

        :rtype: bool,None
        :raise TravisCIError:
            When something went wrong while communicating,
            getting or extracting data from or with the API.
        """

        if self.state not in StatesConfig.PROCESSING:
            self._endpoint_url = self.bind_path_name_to_access_point(
                self.___standard_enpoint_url, "restart"
            )

            try:
                response = self.post_request()

                if "build" in response and "id" in response["build"]:
                    self.response_to_attribute(
                        self, self.standardize.it(response["build"])
                    )
                    return True
                return False
            except TravisCIError as exception:
                if "Accepted" in exception.error_message():
                    return True
                raise exception
        return None
