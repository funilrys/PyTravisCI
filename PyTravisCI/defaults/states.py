"""
Just another Travis CI (API) Python interface.

A module which provides some defaults related to builds or jobs states.

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

STOPPED = ["canceled", "errored", "failed"]
"""
Provides the list of states which we use to consider a job/build as stopped.
"""

ACTIVE = ["created", "started"]
"""
Provides the list of states which we use to consider a job/build or job as processing.
"""

FINISHED = ["passed"]
"""
Provides the list of states which we use to consider a job/build as done.
"""

NOT_STARTED = FINISHED + ACTIVE
"""
Provides the list of states which we use to consider a job/build
as not started.
"""

NOT_CANCELLED = ACTIVE
"""
Provides the list of states which we use to consider a build as
not cancelled.
"""
