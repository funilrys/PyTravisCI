"""
Just another Travis CI (Python) API client.

Provide the access to the user resource type.

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


class User(Communication):
    """
    Provide the information of a given :code:`user_id`.

    Official Travis CI API documentation
        - https://developer.travis-ci.org/resource/setting#setting
        - https://developer.travis-ci.org/resource/setting#find
        - https://developer.travis-ci.org/resource/setting#update

    :param root:
        An initiated instance of :class:`~PyTravisCI.TravisCI`.
    :type root: :class:`~PyTravisCI.TravisCI`
    :param user_id:
        A user ID.

        Can be
            :code:`{user.id}`
                Value uniquely identifying the user.
    :type user_id: str,int

    :ivar int id: Value uniquely identifying the user.
    :ivar str login: Login set on Github.
    :ivar str name: Name set on GitHub.
    :ivar int github_id: Id set on GitHub.
    :ivar str avatar_url: Avatar URL set on GitHub.
    :ivar bool education: Whether or not the user has an education account.
    :ivar bool allow_migration: The user's allow_migration.
    :ivar bool is_syncing: Whether or not the user is currently being synced with Github.
    :ivar synced_at: The last time the user was synced with GitHub.
    :vartype synced_at: :class:`~datetime.datetime`


    :raise InvalidIntArgument:
        When :code:`user_id` is not an :code:`int` or :code:`str.isdigit`.
    :raise TravisCIError:
        When something went wrong while communicating,
        getting or extracting data from or with the API.
    """

    __path_name_base__ = "user"

    def __init__(self, root, user_id=None):
        super(User, self).__init__(root)

        if user_id and not self.is_digit(user_id):
            raise InvalidIntArgument("user_id")

        self.__standard_endpoint_url = self.bind_path_name_to_access_point(
            self.access_point, f"{self.__path_name_base__}"
        )

        if user_id:
            self._endpoint_url = self.bind_path_name_to_access_point(
                self.__standard_endpoint_url, user_id
            )
        else:
            self._endpoint_url = self.__standard_endpoint_url

        self.response_to_attribute(
            self, self.standardize.it(self.get_request(follow_next_page=False))
        )

    def sync(self):
        """
        Triggers a sync on a user's account with their GitHub account.

         :return:
            A boolean if the request was made and :code:`None` if :code:`is_syncing`
            is set to :code:`True`.

        :rtype: bool,None

        :raise MissingArgument:
            When :code:`self.id` is not found.
        :raise TravisCIError:
            When something went wrong while communicating,
            getting or extracting data from or with the API.
        """

        if not self.is_syncing:
            if not self.id:
                raise MissingArgument("self.id")

            self._endpoint_url = self.bind_path_name_to_access_point(
                self.__standard_endpoint_url, f"{self.id}/sync"
            )

            response = self.post_request()

            if "id" in response and "login" in response and "github_id" in response:
                self.response_to_attribute(self, self.standardize.it(response))

                return True
            return False
        return None
