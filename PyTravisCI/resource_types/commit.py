"""
Just another Python API for Travis CI (API).

A module which provides the "Commit" resource type.

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

from datetime import datetime
from typing import Optional

from .base import ResourceTypesBase


class Commit(ResourceTypesBase):
    """
    Provides the description of a commit

    Official Travis CI API documentation
        - https://developer.travis-ci.org/resource/commit

    :ivar int id:
        Value uniquely identifying the commit.
    :ivar str sha:
        Checksum the commit has in git and is identified by.
    :ivar str ref:
        Named reference the commit has in git.
    :ivar str message:
        Commit mesage.
    :ivar str compare_url:
        URL to the commit's diff on GitHub.
    :ivar committed_at:
        Commit date from git.
    :vartype committed_at: :py:class`~datetime.datetime`
    """

    id: Optional[int] = None
    sha: Optional[str] = None
    ref: Optional[str] = None
    message: Optional[str] = None
    compare_url: Optional[str] = None
    committed_at: Optional[datetime] = None
