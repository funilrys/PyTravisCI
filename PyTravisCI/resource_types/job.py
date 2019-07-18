"""
Just another Travis CI (Python) API client.

Provide the access to the job resource type.

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
from ..exceptions import MissingArgument, TravisCIError


class Job(Communication):
    """
    Provide the information of a given :code:`job_id`.

    Official Travis CI API documentation
        - https://developer.travis-ci.org/resource/job#Job
        - https://developer.travis-ci.org/resource/job#find
        - https://developer.travis-ci.org/resource/job#cancel
        - https://developer.travis-ci.org/resource/job#restart
        - https://developer.travis-ci.org/resource/job#debug

    :param root:
        An initiated instance of :class:`~PyTravisCI.TravisCI`.
    :type root: :class:`~PyTravisCI.TravisCI`
    :param job_id:
        A job ID to get the information for.

        Can be
            :code:`{job.id}`
                Value uniquely identifying the job.

    :type job_id: str,int

    :ivar int id: Value uniquely identifying the job.
    :ivar bool allow_failure: The job's allow_failure.
    :ivar str number: Incremental number for a repository's builds.
    :ivar str state: Current state of the job.
    :ivar started_at: When the job started.
    :vartype started_at: :class:`~datetime.datetime`
    :ivar finished_at: When the job finished.
    :vartype finished_at: :class:`~datetime.datetime`
    :ivar dict build: The build the job is associated with.
    :ivar str queue: Worker queue this job is/was scheduled on.
    :ivar dict repository: GitHub user or organization the job belongs to.
    :ivar dict commit: The commit the job is associated with.
    :ivar dict owner: GitHub user or organization the job belongs to.
    :ivar dict stage: The stages of the job.
    :ivar created_at: When the job was created.
    :vartype created_at: :class:`~datetime.datetime`
    :ivar updated_at: When the job was updated.
    :vartype updated_at: :class:`~datetime.datetime`
    :ivar bool private: Whether or not the job is private.

    :raise MissingArgument:
        When :code:`job_id` is not given or empty.
    :raise TravisCIError:
        When something went wrong while communicating,
        getting or extracting data from or with the API.
    """

    __path_name_base__ = "job"

    def __init__(self, root, job_id):
        super(Job, self).__init__(root)

        if not job_id:
            raise MissingArgument("job_id")

        self._endpoint_url = (
            self.__standard_endpoint_url
        ) = self.bind_path_name_to_access_point(
            self.access_point, f"{self.__path_name_base__}/{job_id}"
        )

        self.response_to_attribute(
            self, self.standardize.it(self.get_request(follow_next_page=True))
        )

    def cancel(self):
        """
        Cancels the current job.

        :return:
            A boolean if the request was made and :code:`None` if the
            state of the build is already :code:`canceled`, :code:`failed`
            or :code:`errored`.
        """

        if self.state not in StatesConfig.STOPPED:
            self._endpoint_url = self.bind_path_name_to_access_point(
                self.__standard_endpoint_url, "cancel"
            )

            try:
                _ = self.post_request()
            except TravisCIError as exception:
                if (
                    "Accepted" in exception.error_message()
                    or "job_not_cancelable" in exception.error_type()
                ):
                    return True
                raise exception
        return None

    def restart(self):
        """
        Restarts the current job.

        :return:
            A boolean if the request was made and :code:`None` if the state
            of the job is :code:`created` or :code:`started`.

        :rtype: bool,None
        :raise TravisCIError:
            When somthing went wrong while communicating,
            getting or extracting data from or with the API.
        """

        if self.state not in StatesConfig.PROCESSING:
            self._endpoint_url = self.bind_path_name_to_access_point(
                self.__standard_endpoint_url, "restart"
            )

            try:
                _ = self.post_request()
            except TravisCIError as exception:
                if "Accepted" in exception.error_message():
                    return True
                raise exception
        return None

    def debug(self):
        """
        :raise NotImplementedError: When called.
        """

        raise NotImplementedError(
            "This method is not implemented yet because I could not find a way to test its logic."
        )
