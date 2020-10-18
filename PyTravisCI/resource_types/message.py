"""
Just another Python API for Travis CI (API).

A module which provides the "Message" resource type.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Project link:
    https://github.com/funilrys/PyTravisCI

Project documentation:
    https://pytravisci.readthedocs.io/en/latest/

License
::


    MIT License

    Copyright (c) 2019, 2020 Nissar Chababy

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

from typing import Optional

from .base import ResourceTypesBase


class Message(ResourceTypesBase):
    """
    Provides the description of an individual message.

    Official Travis CI API documentation
        - https://developer.travis-ci.org/resource/message

    :ivar int id:
        The log's id.
    :ivar str level:
        The message's level.
    :ivar str key:
        The message's key.
    :ivar str code:
        The message's code.
    :ivar dict args:
        The message's args.
    :ivar src:
        The message's src.
    :ivar line:
        The message's line.
    """

    id: Optional[int] = None
    level: Optional[str] = None
    key: Optional[str] = None
    code: Optional[str] = None
    args: Optional[dict] = None
    src = None
    line = None
