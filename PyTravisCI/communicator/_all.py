"""
Just another Python API for Travis CI (API).

A module which provides every public available communicators.

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

# pylint: disable=unused-import

from .active import Active
from .beta_feature import BetaFeature
from .beta_features import BetaFeatures
from .branch import Branch
from .branches import Branches
from .broadcasts import Broadcasts
from .build import Build
from .builds import Builds
from .cache import Cache
from .caches import Caches
from .cron import Cron
from .crons import Crons
from .env_var import EnvVar
from .env_vars import EnvVars
from .job import Job
from .jobs import Jobs
from .key_pair import KeyPair
from .key_pair_generated import KeyPairGenerated
from .lint import Lint
from .log import Log
from .messages import Messages
from .organization import Organization
from .organizations import Organizations
from .repositories import Repositories
from .repository import Repository
from .request import Request
from .requests import Requests
from .setting import Setting
from .settings import Settings
from .stages import Stages
from .user import User
