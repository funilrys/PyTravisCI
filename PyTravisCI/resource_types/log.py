"""
Just another Travis CI (Python) API client.

Provide the access to the log resource type.

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
from ..exceptions import InvalidIntArgument, MissingArgument


class Log(Communication):
    """
    Provide the log of a given :code:`job_id`.

    Official Travis CI API documentation
        - https://developer.travis-ci.org/resource/log#log
        - https://developer.travis-ci.org/resource/log#find
        - https://developer.travis-ci.org/resource/log#delete

    :param root:
        An initiated instance of :class:`~PyTravisCI.TravisCI`.
    :type root: :class:`~PyTravisCI.TravisCI`
    :param job_id:
        A job ID to get the information for.

        Can be
            :code:`{job.id}`
                Value uniquely identifying the job.

    :type job_id: str,int

    :ivar int id: The log's id.
    :ivar str content: The content of the log.
    :ivar dict log_parts: The log parts that form the log.

    :raise MissingArgument:
        When :code:`job_id` is not given or is empty.
    :raise InvalidIntArgument:
        When :code:`job_id` is not an :code:`int` or :code:`str.isdigit`.
    :raise TravisCIError:
        When something went wrong while communicating,
        getting or extracting data from or with the API.
    """

    __path_name_base__ = "job"

    def __init__(self, root, job_id):
        super(Log, self).__init__(root)

        if not job_id:
            raise MissingArgument("job_id")

        if not self.is_digit(job_id):
            raise InvalidIntArgument(job_id)

        self._endpoint_url = (
            self.__standard_endpoint_url
        ) = self.bind_path_name_to_access_point(
            self.access_point, f"{self.__path_name_base__}/{job_id}/log"
        )

        self.__fetch_log()

    def __fetch_log(self):
        """
        Fetch the log of the given :code:`job_id`.
        """

        self.response_to_attribute(
            self, self.standardize.it(self.get_request(follow_next_page=True))
        )

    def delete(self):
        """
        Deletes the log of the given :code:`job_id`.

        :return:
            A boolean when a request was made and :code:`None` if
            no :code:`id`, :code:`content` or :code:`log_parts` were found.

        :rtype: bool,None

        :raise TravisCIError:
            When something went wrong while communicating,
            getting or extracting data from or with the API.

            .. warning::
                You may get :code:`log_already_removed`
                into :meth:`..exceptions.TravisCIError.error_type` if you
                try to delete something already delete.
        """

        if self.id and self.content or self.log_parts:
            self._endpoint_url = self.__standard_endpoint_url

            response = self.delete_request()

            if "id" in response and "content" in response:
                self.__fetch_log()
                return True
            return False
        return None
