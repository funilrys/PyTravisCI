"""
Just another Travis CI (Python) API client.

Provide the exceptions we (might) raise.

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


class TravisCIError(Exception):
    """
    Raise an exception with the error we got from the API.

    :param str url: The endpoint URL we communicated with.
    :param str error_message: The error message.
    :param str error_type: The error type.
    """

    def __init__(self, url, error_message, error_type):
        self.url = url
        self.err_message = error_message
        self.err_type = error_type

        super(TravisCIError, self).__init__(self.message())

    def message(self):
        """
        Provide the message to return while raising the exception.
        """

        return f"[{self.url},{self.err_type}]: {self.err_message}"

    def error_message(self):
        """
        Provide the error message (ONLY).
        """

        return self.err_message

    def error_type(self):
        """
        Provide the error type (ONLY).
        """

        return self.err_type

    def error_url(self):
        """
        Provide the URL we requested when we got teh error.
        """

        return self.url


class MissingArgument(Exception):
    """
    Raise an exception for the case that one or multiple arguments are not given.

    :param missing_argument: The name of the missing argument(s).
    :type missing_argument: list,str
    """

    def __init__(self, missing_argument):
        if not isinstance(missing_argument, list):
            self.missing = [missing_argument]
        else:
            self.missing = missing_argument

        self.missing = [f"<{x}>" for x in self.missing]

        super(MissingArgument, self).__init__(self.message())

    def message(self):
        """
        Construct the message to return.
        """

        if len(self.missing) > 1:
            beginning = "{0} nor {1}".format(
                ", ".join(self.missing[:-1]), self.missing[-1]
            )
        else:
            beginning = f"{self.missing[0]} is not"

        return f"{beginning} given."


class InvalidIntArgument(Exception):
    """
    Raise an exception for the case that an ID which should be an integer
    (or a digit string) is excepted and not given.

    :param invalid_argument: The name of the invalid argument(s).
    :type invalid_argument: list,str
    """

    def __init__(self, invalid_argument):
        if not isinstance(invalid_argument, list):
            self.invalid = [invalid_argument]
        else:
            self.invalid = invalid_argument

        self.invalid = [f"<{x}>" for x in self.invalid]

        super(InvalidIntArgument, self).__init__(self.message())

    def message(self):
        """
        Construct the message to return.
        """

        if len(self.invalid) > 1:
            beginning = "{0} and {1} are not".format(
                ", ".join(self.invalid[:-1]), self.invalid[-1]
            )
        else:
            beginning = f"{self.invalid[0]} is not"

        return f"{beginning} valid. {type(int)} or `str.isdigit()` expected."


class IncompatibleArgument(Exception):
    """
    Raise an exception when one or more arguments are not compatible together.

    :param incompatible_argument: The name of the argument(s) which are incompatible together.
    :type incompatible_argument: list

    :raise ValueError:
        When :code:`incompatible_argument` is not a list.
    :raise ValueError:
        When :code:`incompatible_argument` don't have at least 2 indexes.
    """

    def __init__(self, incompatible_argument):
        if not isinstance(incompatible_argument, list):
            raise ValueError("We except a list.")

        if not len(incompatible_argument) > 1:
            raise ValueError("We except at least 2 arguments.")

        self.incompatible = [f"<{x}>" for x in incompatible_argument]

        super(IncompatibleArgument, self).__init__(self.message())

    def message(self):
        """
        Construct the message to run.
        """

        return "{0} and {1} are not compatible together.".format(
            ", ".join(self.incompatible[:-1]), self.incompatible[-1]
        )
