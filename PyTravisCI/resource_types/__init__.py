"""
Just another Travis CI (Python) API client.

Provide the different resource types along with their logics.

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


from .active import Active
from .branch import Branch
from .branches import Branches
from .broadcasts import Broadcasts
from .build import Build
from .builds import Builds
from .caches import Caches
from .cron import Cron
from .crons import Crons
from .env_var import EnvVar
from .env_vars import EnvVars
from .job import Job
from .jobs import Jobs
from .key_pair_generated import KeyPairGenerated
from .log import Log
from .organization import Organization
from .organizations import Organizations
from .owner import Owner
from .repositories import Repositories
from .repository import Repository
from .setting import Setting
from .settings import Settings
from .user import User
