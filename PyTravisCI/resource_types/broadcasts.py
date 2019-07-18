"""
Just another Travis CI (Python) API client.

Provide the access to the broadcasts resource type.

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


class Broadcasts(Communication):
    """
    Provide the list of broadcasts of the current user.

    Official Travis CI API documentation
        - https://developer.travis-ci.org/resource/broadcasts#Broadcasts
        - https://developer.travis-ci.org/resource/broadcasts#for_current_user

    :param root:
        An initiated instance of :class:`~PyTravisCI.TravisCI`.
    :type root: :class:`~PyTravisCI.TravisCI`
    :param dict parameters:
        A :code:`dict` of parameters to parse to the request.

        .. seealso::
            - :attr:`~PyTravisCI.resource_types.broadcasts.Broadcasts._parameters`

    :ivar list broadcasts: List of broadcasts.

    :raise ValueError:
        When :code:`parameters` is not a :code:`dict`.
    :raise TravisCIError:
        When something went wrong while communicating,
        getting or extracting data from or with the API.
    """

    __path_name_base__ = "broadcasts"

    _excluded_parameters = ["include"]
    """
    The list of parameters to exclude.
    """

    _parameters = {"active": None, "broadcast.active": None}
    """
    Provide the parameters we can parse to the query string.

    Indexes
        :code:`active`
            Alias for :code:`broadcast.active`.
        :code:`broadcast.active`
            Filters broadcasts by whether or not the brodacast should still be displayed.

    .. warning::
        If an index is set to :code:`None`, it will be omitted.

    .. warning::
        Only the indexes listed into this variable will be parsed.
    """

    def __init__(self, root, parameters=None):
        super(Broadcasts, self).__init__(root)

        self.filter_parameters(parameters)

        self._endpoint_url = self.bind_path_name_to_access_point(
            self.access_point,
            self.__path_name_base__ + self.convert_parameters_to_get_param(),
        )

        self.response_to_attribute(
            self, self.standardize.it(self.get_request(follow_next_page=True))
        )
