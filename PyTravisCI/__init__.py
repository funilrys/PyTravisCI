"""
Just another Travis CI (Python) API client.

This is the main entry of the project.

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
# pylint: disable=invalid-name, too-many-lines


from requests import Session

import PyTravisCI.resource_types as ResourceTypes
from PyTravisCI.configuration import AccessPoints
from PyTravisCI.configuration import Communication as CommunicationConfig
from PyTravisCI.encryption import Encryption

VERSION = "1.1.2"

# pylint: disable=too-many-public-methods
class TravisCI:
    """
    Provide a quick access to everything needed.

    :param str token: The Travis CI API token.
    :param str access_point: The Travis CI API access point to communicate with.
    """

    def __init__(self, token, access_point=AccessPoints.OPEN):
        headers = {
            "Travis-API-Version": CommunicationConfig.API_VERSION,
            "User-Agent": f"funilrys/{CommunicationConfig.USER_AGENT}/{VERSION}",
        }

        if token:
            headers["Authorization"] = f"token {token}"

        self.access_point = access_point

        self.session = Session()
        self.session.headers.update(headers)

    @classmethod
    def encrypt(cls, environment_variables, public_key):
        """
        Encrypts the given environment variable so that they can be
        used inside a Travis CI VM.

        :param dict environment_variables:
            A dict representing the env to encrypt.

            Example
                ::

                    {
                        "HELLO": "WORLD",
                        "WORLD": "HELLO"
                    }

                will encrpyt :code:`HELLO=WORLD`, :code:'WORLD=HELLO'

            .. warning::
                if a space is present into a key, it will be replaced with an
                underscore.

        :parm str public_key:
            The public key to use to encrypt the  given env.

        .. warning::
            This class has been built just in order to encrypt global environment variables
            which can later be stored into the :code:`env[global]`
            index of your :code:`.travis.yml` file.
        """

        return Encryption(
            environment_variables=environment_variables, public_key=public_key
        ).encrypt()

    def active(self, owner=None, github_id=None):
        """
        Provide the list of all active builds.

        Official Travis CI API documentation
            - https://developer.travis-ci.org/resource/active#Active
            - https://developer.travis-ci.org/resource/active#for_owner

        Extended documentation
            - :class:`~PyTravisCI.resource_types.active.Active`

        .. warning::
            :code:`owner` can't be set at the same time as :code:`github_id`.

        :param str owner:
            The GitHub user or organization login to get the list of active builds for.

            Can be
                :code:`{owner.login}`
                    User or organization login set on GitHub.
                :code:`{user.login}`
                    Login set on Github.
                :code:`{organization.login}`
                    Login set on GitHub.

        :param github_id:
            The GitHub user or organization ID to get the active builds for.

            Can be
                :code:`{owner.github_id}`
                    User or organization id set on GitHub.

        :type github_id: str,int

        :raise MissingArgument:
            When :code:`owner` nor :code:`github_id` are given.
        :raise IncompatibleArgument:
            When :code:`owner` is given along with :code:`github_id`.
        :raise InvalidIntArgument:
            When :code:`github_id` is not an :code:`int` nor :code:`str.is_digit`.
        :raise TravisCIError:
            When something went wrong while communicating,
            getting or extracting data from or with the API.
        """

        return ResourceTypes.Active(self, owner=owner, github_id=github_id)

    def branch(self, repo_id_or_slug, branch_name):
        """
        Provide the information of a given :code:`branch_name` if exists at the given
        :code:`repo_id_or_slug`.

        Official Travis CI API documentation
            - https://developer.travis-ci.org/resource/branch#Branch
            - https://developer.travis-ci.org/resource/branch#find

        Extended documentation
            - :class:`~PyTravisCI.resource_types.branch.Branch`

        :param repo_id_or_slug:
            A repository ID or slug to get the information for.

            Can be
                :code:`{repository.id}`
                    Value uniquely identifying the repository.
                :code:`{repository.slug}`
                    Same as :code:`{repository.owner.name}/{repository.name}`

            .. warning::
                The Travis CI API states:

                    If querying using the repository slug, it must be formatted using
                    standard URL encoding, including any special characters.

                We do not except nor want that that from you.
                In fact, we do the encoding for you.

        :type repo_id_or_slug: str,int

        :param str branch_name:
            The name of the git branch to get information from.

            Can be
                :code:`{branch.name}`
                    Name of the git branch.

        :raise MissingArgument:
            When :code:`repo_is_or_slug` is not given or is empty.
        :raise MissingArgument:
            When :code:`branch_name` is not given or is empty.
        :raise TravisCIError:
            When something went wrong while communicating,
            getting or extracting data from or with the API.
        """

        return ResourceTypes.Branch(
            self, repo_id_or_slug=repo_id_or_slug, branch_name=branch_name
        )

    def branches(self, repo_id_or_slug, sort_by=None, parameters=None):
        """
        Provide the list of branches of the given :code:`repo_id_or_slug`.

        Official Travis CI API documentation
            - https://developer.travis-ci.org/resource/branches#Branches
            - https://developer.travis-ci.org/resource/branches#find

        Extended documentation
            - :class:`~PyTravisCI.resource_types.branche.Branches`

        :param repo_id_or_slug:
            A repository ID or slug to get the information for.

            Can be
                :code:`{repository.id}`
                    Value uniquely identifying the repository.
                :code:`{repository.slug}`
                    Same as :code:`{repository.owner.name}/{repository.name}`

            .. warning::
                The Travis CI API states:

                    If querying using the repository slug, it must be formatted using
                    standard URL encoding, including any special characters.

                We do not except nor want that that from you.
                In fact, we do the encoding for you.

        :type repo_id_or_slug: str,int

        :param sort_by:
            Set the sorting to use.

            .. note::
                One can append :code:`:desc` to any indexes in order to reverse the order.

        :param dict parameters:
            A :code:`dict` of parameters to parse to the request.

            .. seealso::
                - :attr:`PyTravisCI.resource_types.branches.Branches._parameters`

        :type sort_by: str,list

        :raise ValueError:
            When :code:`parameters` is not a :code:`dict`.
        :raise MissingArgument:
            When :code:`repo_id_or_slug` is not given or is empty.
        :raise TravisCIError:
            When something went wrong while communicating,
            getting or extracting data from or with the API.
        """

        return ResourceTypes.Branches(
            self,
            repo_id_or_slug=repo_id_or_slug,
            sort_by=sort_by,
            parameters=parameters,
        )

    def broadcasts(self, parameters=None):
        """
        Provide the list of broadcasts of the current user.

        Official Travis CI API documentation
            - https://developer.travis-ci.org/resource/broadcasts#Broadcasts
            - https://developer.travis-ci.org/resource/broadcasts#for_current_user

        Extended documentation
            - :class:`~PyTravisCI.resource_types.broadcasts.Broadcasts`

        :param dict parameters:
            A :code:`dict` of parameters to parse to the request.

            .. seealso::
                - :attr:`~PyTravisCI.resource_types.broadcasts.Broadcasts._parameters`

        :raise ValueError:
            When :code:`parameters` is not a :code:`dict`.
        :raise TravisCIError:
            When something went wrong while communicating,
            getting or extracting data from or with the API.
        """

        return ResourceTypes.Broadcasts(self, parameters=parameters)

    def build(self, build_id):
        """
        Provide the information of a given :code:`build_id`.

        Official Travis CI API documentation
            - https://developer.travis-ci.org/resource/build#Build
            - https://developer.travis-ci.org/resource/build#find
            - https://developer.travis-ci.org/resource/build#cancel
            - https://developer.travis-ci.org/resource/build#restart

        Extended documentation
            - :class:`~PyTravisCI.resource_types.build.Build`

        :param build_id:
            The ID of the build to get information for.

            Can be
                :code:`{build.id}`
                    Value uniquely identifying the build.
        :type build_id: str,int

        Methods
            * :meth:`~PyTravisCI.resource_types.build.Build.cancel`
            * :meth:`~PyTravisCI.resource_types.build.Build.restart`

        :raise MissingArgument:
            When :code:`build_id` is not givne or is empty.
        :raise InvalidIntArgument:
            When :code:`build_id` is not an :code:`int` or :code:str.isdigit()`.
        :raise TravisCIError:
            When something went wrong while communicating,
            getting or extracting data from or with the API.
        """

        return ResourceTypes.Build(self, build_id)

    def builds(self, repo_id_or_slug=None, limit=5):
        """
        Provide the information of a given :code:`repo_id_or_slug`.

        Official Travis CI API documentation
            - https://developer.travis-ci.org/resource/builds#Builds
            - https://developer.travis-ci.org/resource/builds#for_current_user
            - https://developer.travis-ci.org/resource/builds#find

        Extended documentation
            - :class:`~PyTravisCI.resource_types.builds.Builds`

        :param repo_id_or_slug:
            A repository ID or slug to get the information for.

            Can be
                :code:`{repository.id}`
                    Value uniquely identifying the repository.
                :code:`{repository.slug}`
                    Same as :code:`{repository.owner.name}/{repository.name}`

            .. warning::
                The Travis CI API states:

                    If querying using the repository slug, it must be formatted using
                    standard URL encoding, including any special characters.

                We do not except nor want that that from you.
                In fact, we do the encoding for you.

            .. note::
                If this variable is not given or :code:`None` is given, we return
                the list of builds of the current user.
        :type repo_id_or_slug: str,int
        :param int limit:
            Set the last :code:`n` build to return.

            .. warning::
                If a negative number or :code:`0` is given, we return everything.

        :raise InvalidIntArgument:
            When :code:`limit` is not an :code:`int` or :code:`str.isdigit`.
        :raise TravisCIError:
            When something went wrong while communicating,
            getting or extracting data from or with the API.
        """

        return ResourceTypes.Builds(self, repo_id_or_slug=repo_id_or_slug, limit=limit)

    def caches(self, repo_id_or_slug):
        """
        Provide the cache information of a given :code:`repo_id_or_slug`.

        Official Travis CI API documentation
            - https://developer.travis-ci.org/resource/caches#Caches
            - https://developer.travis-ci.org/resource/caches#find
            - https://developer.travis-ci.org/resource/caches#delete

        Extended documentation
            - :class:`~PyTravisCI.resource_types.caches.Caches`

        :param repo_id_or_slug:
            A repository ID or slug to get the information for.

            Can be
                :code:`{repository.id}`
                    Value uniquely identifying the repository.
                :code:`{repository.slug}`
                    Same as :code:`{repository.owner.name}/{repository.name}`

            .. warning::
                The Travis CI API states:

                    If querying using the repository slug, it must be formatted using
                    standard URL encoding, including any special characters.

                We do not except nor want that that from you.
                In fact, we do the encoding for you.

        :type repo_id_or_slug: str,int

        Methods
            * :meth:`~PyTravisCI.resource_types.caches.Caches.delete`

        :raise MissingArgument:
            When :code:`repo_is_or_slug` is not given or is empty.
        :raise TravisCIError:
            When something went wrong while communicating,
            getting or extracting data from or with the API.
        """

        return ResourceTypes.Caches(self, repo_id_or_slug=repo_id_or_slug)

    def cron(self, cron_id=None, repo_id_or_slug=None, branch_name=None):
        """
        Provide the cron information.

        Official Travis CI API documentation
            - https://developer.travis-ci.org/resource/cron#Cron
            - https://developer.travis-ci.org/resource/cron#delete
            - https://developer.travis-ci.org/resource/cron#for_branch
            - https://developer.travis-ci.org/resource/cron#create

        Extended documentation
            - :class:`~PyTravisCI.resource_types.cron.Cron`

        :param cron_id:
            A cron ID to get information for.

            Can be
                :code:`{cron.id}`
                    Value uniquely identifying the cron.

        :type cron_id: str,int
        :param repo_id_or_slug:
            A repository ID or slug to get the information for.

            Can be
                :code:`{repository.id}`
                    Value uniquely identifying the repository.
                :code:`{repository.slug}`
                    Same as :code:`{repository.owner.name}/{repository.name}`

            .. warning::
                The Travis CI API states:

                    If querying using the repository slug, it must be formatted using
                    standard URL encoding, including any special characters.

                We do not except nor want that that from you.
                In fact, we do the encoding for you.

        :type repo_id_or_slug: str,int
        :param str branch_name:
            The name of the git branch to get information from.

            Can be
                :code:`{branch.name}`
                    Name of the git branch.

        Methods
            * :meth:`~PyTravisCI.resource_types.cron.Cron.delete`
            * :meth:`~PyTravisCI.resource_types.cron.Cron.create`

        :raise IncompatibleArgument:
            When :code:`cron_id` is given along with :code:`repo_id_or_slug`.
        :raise IncompatibleArgument:
            When :code:`cron_id` is given along with :code:`branch_name`.
        :raise MissingArgument:
            When :code:`repo_id_or_slug` is given but not :code:`branch_name`.
        :raise MissingArgument:
            When :code:`branch_name` is given but not :code:`repo_id_or_slug`.
        :raise MissingArgument:
            When :code:`cron_id`, :code:`repo_id_or_slug` nor :code:`branch_name`
            are given.
        :raise InvalidIntArgument:
            When :code:`cron_id` is not an :code:`int` or :code:`str.isdigit`.
        :raise TravisCIError:
            When something went wrong while communicating,
            getting or extracting data from or with the API.
        """

        return ResourceTypes.Cron(
            self,
            cron_id=cron_id,
            repo_id_or_slug=repo_id_or_slug,
            branch_name=branch_name,
        )

    def crons(self, repo_id_or_slug):
        """
        Provide the list of crons of a given :code:`repo_id_or_slug`.

        Official Travis CI API documentation
            - https://developer.travis-ci.org/resource/crons#crons
            - https://developer.travis-ci.org/resource/crons#for_repository

        Extended documentation
            - :class:`~PyTravisCI.resource_types.crons.Crons`

        :param repo_id_or_slug:
            A repository ID or slug to get the information for.

            Can be
                :code:`{repository.id}`
                    Value uniquely identifying the repository.
                :code:`{repository.slug}`
                    Same as :code:`{repository.owner.name}/{repository.name}`

            .. warning::
                The Travis CI API states:

                    If querying using the repository slug, it must be formatted using
                    standard URL encoding, including any special characters.

                We do not except nor want that that from you.
                In fact, we do the encoding for you.

        :type repo_id_or_slug: str,int

        :raise MissingArgument:
            When :code:`repo_id_or_slug` is not given or is empty.
        :raise TravisCIError:
            When something went wrong while communicating,
            getting or extracting data from or with the API.
        """

        return ResourceTypes.Crons(self, repo_id_or_slug=repo_id_or_slug)

    def env_var(self, repo_id_or_slug, env_var_id):
        """
        Provide the information of a given :code:`repo_id_or_slug`
        and :code:`env_var_id`.

        Official Travis CI API documentation
            - https://developer.travis-ci.org/resource/env_var#env%20var
            - https://developer.travis-ci.org/resource/env_var#find
            - https://developer.travis-ci.org/resource/env_var#update
            - https://developer.travis-ci.org/resource/env_var#delete

        Extended documentation
            - :class:`~PyTravisCI.resource_types.env_var.EnvVar`

        :param repo_id_or_slug:
            A repository ID or slug to get the information for.

            Can be
                :code:`{repository.id}`
                    Value uniquely identifying the repository.
                :code:`{repository.slug}`
                    Same as :code:`{repository.owner.name}/{repository.name}`

            .. warning::
                The Travis CI API states:

                    If querying using the repository slug, it must be formatted using
                    standard URL encoding, including any special characters.

                We do not except nor want that that from you.
                In fact, we do the encoding for you.

        :type repo_id_or_slug: str,int
        :param str env_var_id:
            An environment variable ID.

            Can be
                :code:`{env_var.id}`
                    The environment variable id.

        Methods
            * :meth:`~PyTravisCI.resource_types.env_var.EnvVar.update`
            * :meth:`~PyTravisCI.resource_types.env_var.EnvVar.delete`

        :raise MissingArgument:
            When :code:`repo_id_or_slug` nor :code:`env_var_id` is given.
        :raise TravisCIError:
            When something went wrong while communicating,
            getting or extracting data from or with the API.
        """

        return ResourceTypes.EnvVar(
            self, repo_id_or_slug=repo_id_or_slug, env_var_id=env_var_id
        )

    def env_vars(self, repo_id_or_slug):
        """
        Provide the list of environment variables of a given :code:`repo_id_or_slug`.

        Official Travis CI API documentation
            - https://developer.travis-ci.org/resource/env_vars#Env%20vars
            - https://developer.travis-ci.org/resource/env_vars#for_repository
            - https://developer.travis-ci.org/resource/env_vars#create

        Extended documentation
            - :class:`~PyTravisCI.resource_types.env_vars.EnvVars`

        :param repo_id_or_slug:
            A repository ID or slug to get the information for.

            Can be
                :code:`{repository.id}`
                    Value uniquely identifying the repository.
                :code:`{repository.slug}`
                    Same as :code:`{repository.owner.name}/{repository.name}`

            .. warning::
                The Travis CI API states:

                    If querying using the repository slug, it must be formatted using
                    standard URL encoding, including any special characters.

                We do not except nor want that that from you.
                In fact, we do the encoding for you.

        :type repo_id_or_slug: str,int

        Methods
            * :meth:`~PyTravisCI.resource_types.env_vars.EnvVars.create`

        :raise MissingArgument:
            When :code:`repo_id_or_slug` is not given or empty.
        :raise TravisCIError:
            When something went wrong while communicating,
            getting or extracting data from or with the API.
        """

        return ResourceTypes.EnvVars(self, repo_id_or_slug=repo_id_or_slug)

    def job(self, job_id):
        """
        Provide the information of a given :code:`job_id`.

        Official Travis CI API documentation
            - https://developer.travis-ci.org/resource/job#Job
            - https://developer.travis-ci.org/resource/job#find
            - https://developer.travis-ci.org/resource/job#cancel
            - https://developer.travis-ci.org/resource/job#restart
            - https://developer.travis-ci.org/resource/job#debug

        Extended documentation
            - :class:`~PyTravisCI.resource_types.job.Job`

        :param job_id:
            A job ID to get the information for.

            Can be
                :code:`{job.id}`
                    Value uniquely identifying the job.

        :type job_id: str,int

        Methods
            * :meth:`~PyTravisCI.resource_types.job.Job.cancel`
            * :meth:`~PyTravisCI.resource_types.job.Job.restart`
            * :meth:`~PyTravisCI.resource_types.job.Job.debug`

        :raise MissingArgument:
            When :code:`job_id` is not given or empty.
        :raise TravisCIError:
            When something went wrong while communicating,
            getting or extracting data from or with the API.
        """

        return ResourceTypes.Job(self, job_id=job_id)

    def jobs(self, build_id=None, limit=5, parameters=None):
        """
        Provide the list of jobs of a given :code:`build_id`.

        Official Travis CI API documentation
            - https://developer.travis-ci.org/resource/jobs#jobs
            - https://developer.travis-ci.org/resource/jobs#find

        Extended documentation
            - :class:`~PyTravisCI.resource_types.jobs.Jobs`

        :param build_id:
            The ID of the build to get information for.

            Can be
                :code:`{build.id}`
                    Value uniquely identifying the build.

            .. note::
                If this variable is not given or :code:`None` is given, we return
                the list of jobs of the current user.

        :type build_id: str,int
        :param int limit:
            Set the last :code:`n` jobs to return.

            .. warning::
                If a negative number or :code:`0` is given, we return everything.

        :raise InvalidIntArgument:
            When :code:`build_id` is not an :code:`int` or :code:`str.isdigit`.
        :raise TravisCIError:
            When something went wrong while communicating,
            getting or extracting data from or with the API.
        """

        return ResourceTypes.Jobs(
            self, build_id=build_id, limit=limit, parameters=parameters
        )

    def key_pair_generated(self, repo_id_or_slug):
        """
        Provide the Key Pair information of a given :code:`repo_id_or_slug`.

        Official Travis CI API documentation
            - https://developer.travis-ci.org/resource/key_pair_generated#key%20pair%20(generated)
            - https://developer.travis-ci.org/resource/key_pair_generated#find
            - https://developer.travis-ci.org/resource/key_pair_generated#create

        Extended documentation
            - :class:`~PyTravisCI.resource_types.key_pair_generated.KeyPairGenerated`

        :param repo_id_or_slug:
            A repository ID or slug to get the information for.

            Can be
                :code:`{repository.id}`
                    Value uniquely identifying the repository.
                :code:`{repository.slug}`
                    Same as :code:`{repository.owner.name}/{repository.name}`

            .. warning::
                The Travis CI API states:

                    If querying using the repository slug, it must be formatted using
                    standard URL encoding, including any special characters.

                We do not except nor want that that from you.
                In fact, we do the encoding for you.

        :type repo_id_or_slug: str,int

        Methods
            * :meth:`~PyTravisCI.resource_types.key_pair_generated.KeyPairGenerated.create`

        :raise MissingArgument:
            When :code:`repo_id_or_slug` is not given or empty.
        :raise TravisCIError:
            When something went wrong while communicating,
            getting or extracting data from or with the API.
        """

        return ResourceTypes.KeyPairGenerated(self, repo_id_or_slug=repo_id_or_slug)

    def log(self, job_id):
        """
        Provide the log of a given :code:`job_id`.

        Official Travis CI API documentation
            - https://developer.travis-ci.org/resource/log#log
            - https://developer.travis-ci.org/resource/log#find
            - https://developer.travis-ci.org/resource/log#delete

        Extended documentation
            - :class:`~PyTravisCI.resource_types.log.Log`

        :param job_id:
            A job ID to get the information for.

            Can be
                :code:`{job.id}`
                    Value uniquely identifying the job.

        :type job_id: str,int

        Methods
            * :meth:`~PyTravisCI.resource_types.log.Log.delete`

        :raise MissingArgument:
            When :code:`job_id` is not given or is empty.
        :raise InvalidIntArgument:
            When :code:`job_id` is not an :code:`int` or :code:`str.isdigit`.
        :raise TravisCIError:
            When something went wrong while communicating,
            getting or extracting data from or with the API.
        """

        return ResourceTypes.Log(self, job_id=job_id)

    def organization(self, org_id):
        """
        Provide the information of a given :code:`org_id`.

        Official Travis CI API documentation
            - https://developer.travis-ci.org/resource/organization#organization
            - https://developer.travis-ci.org/resource/organization#find

        Extended documentation
            - :class:`~PyTravisCI.resource_types.organization.Organization`

        :param org_id:
            An organization ID to get the information for.

            Can be
                :code:`{organization.id}`
                    Value uniquely identifying the organization.

        :type org_id: str,int

        :raise MissingArgument:
            When :code:`org_id` is empty.
        :raise InvalidIntArgument:
            When :code:`org_id` is not an :code:`int` or a :code:`str.isdigit()`.
        :raise TravisCIError:
            When something went wrong while communicating,
            getting or extracting data from or with the API.
        """

        return ResourceTypes.Organization(self, org_id=org_id)

    def organizations(self):
        """
        Provide the list of organizations of the current user.

        Official Travis CI API documentation
            - https://developer.travis-ci.org/resource/organizations#organizations
            - https://developer.travis-ci.org/resource/organizations#for_current_user

        Extended documentation
            - :class:`~PyTravisCI.resource_types.organizations.Organizations`

        :raise TravisCIError:
            When something went wrong while communicating,
            getting or extracting data from or with the API.
        """

        return ResourceTypes.Organizations(self)

    def owner(self, login=None, github_id=None):
        """
        Provide the information of a given :code:`login` of :code:`github_id`.

        Official Travis CI API documentation
            - https://developer.travis-ci.org/resource/owner#owner
            - https://developer.travis-ci.org/resource/owner#find

        Extended documentation
            - :class:`~PyTravisCI.resource_types.owner.Owner`

        :param str login:
            A GitHub login

            Can be
                :code:`{owner.login}`
                    User or organization login set on GitHub.
                :code:`{user.login}`
                    Login set on Github.
                :code:`{organization.login}`
                    Login set on GitHub.

        :param github_id:
            A GitHub user or organization ID.

            Can be
                :code:`{owner.github_id}`
                    User or organization id set on GitHub.
        :type github_id: str,int

        :raise MissingArgument:
            When :code:`login` nor :code:`github_id` are given.
        :raise IncompatibleArgument:
            When :code:`login` is given along with :code:`github_id`.
        :raise InvalidIntArgument:
            When :code:`github_id` is not an :code:`int` or a :code:`str.is_digit()`.Is
        :raise TravisCIError:
            When something went wrong while communicating,
            getting or extracting data from or with the API.
        """

        return ResourceTypes.Owner(self, login=login, github_id=github_id)

    def repositories(self, login=None, github_id=None):
        """
        Provide the information of a given :code:`login` of :code:`github_id`.

        Official Travis CI API documentation
            - https://developer.travis-ci.org/resource/owner#owner
            - https://developer.travis-ci.org/resource/owner#find

        Extended documentation
            - :class:`~PyTravisCI.resource_types.repositories.Repositories`

        :param str login:
            A GitHub login

            Can be
                :code:`{owner.login}`
                    User or organization login set on GitHub.
                :code:`{user.login}`
                    Login set on Github.
                :code:`{organization.login}`
                    Login set on GitHub.

        :param github_id:
            A GitHub user or organization ID.

            Can be
                :code:`{owner.github_id}`
                    User or organization id set on GitHub.
        :type github_id: str,int

        :raise MissingArgument:
            When :code:`login` nor :code:`github_id` are given.
        :raise IncompatibleArgument:
            When :code:`login` is given along with :code:`github_id`.
        :raise InvalidIntArgument:
            When :code:`github_id` is not an :code:`int` or a :code:`str.is_digit()`.
        :raise TravisCIError:
            When something went wrong while communicating,
            getting or extracting data from or with the API.
        """

        return ResourceTypes.Repositories(self, login=login, github_id=github_id)

    def repository(self, repo_id_or_slug):
        """
        Provide the information of a given :code:`repo_id_or_slug`.

        Official Travis CI API documentation
            - https://developer.travis-ci.org/resource/owner#owner
            - https://developer.travis-ci.org/resource/owner#find

        Extended documentation
            - :class:`~PyTravisCI.resource_types.repository.Repository`

        :param repo_id_or_slug:
            A repository ID or slug to get the information for.

            Can be
                :code:`{repository.id}`
                    Value uniquely identifying the repository.
                :code:`{repository.slug}`
                    Same as :code:`{repository.owner.name}/{repository.name}`

            .. warning::
                The Travis CI API states:

                    If querying using the repository slug, it must be formatted using
                    standard URL encoding, including any special characters.

                We do not except nor want that that from you.
                In fact, we do the encoding for you.

        :type repo_id_or_slug: str,int

        :param github_id:
            A GitHub user or organization ID.

            Can be
                :code:`{owner.github_id}`
                    User or organization id set on GitHub.
        :type github_id: str,int

        Methods
            * :meth:`~PyTravisCI.resource_types.repository.Repository.activate`
            * :meth:`~PyTravisCI.resource_types.repository.Repository.deactivate`
            * :meth:`~PyTravisCI.resource_types.repository.Repository.migrate`
            * :meth:`~PyTravisCI.resource_types.repository.Repository.star`
            * :meth:`~PyTravisCI.resource_types.repository.Repository.unstar`


        :raise MissingArgument:
            When :code:`login` nor :code:`github_id` are given.
        :raise IncompatibleArgument:
            When :code:`login` is given along with :code:`github_id`.
        :raise InvalidIntArgument:
            When :code:`github_id` is not an :code:`int` or a :code:`str.is_digit()`.Is
        :raise TravisCIError:
            When something went wrong while communicating,
            getting or extracting data from or with the API.
        """

        return ResourceTypes.Repository(self, repo_id_or_slug=repo_id_or_slug)

    def setting(self, repo_id_or_slug, setting_name):
        """
        Provide the value of a given :code:`repo_id_or_slug` and :code:`setting_name`.

        Official Travis CI API documentation
            - https://developer.travis-ci.org/resource/setting#setting
            - https://developer.travis-ci.org/resource/setting#find
            - https://developer.travis-ci.org/resource/setting#update

        Extended documentation
            - :class:`~PyTravisCI.resource_types.setting.Settings`

        :param repo_id_or_slug:
            A repository ID or slug to get the information for.

            Can be
                :code:`{repository.id}`
                    Value uniquely identifying the repository.
                :code:`{repository.slug}`
                    Same as :code:`{repository.owner.name}/{repository.name}`

            .. warning::
                The Travis CI API states:

                    If querying using the repository slug, it must be formatted using
                    standard URL encoding, including any special characters.

                We do not except nor want that that from you.
                In fact, we do the encoding for you.

        :type repo_id_or_slug: str,int
        :param str setting_name:
            A setting name.

            Can be
                - :code:`builds_only_with_travis_yml`
                - :code:`build_pushes`
                - :code:`build_pull_requests`
                - :code:`maximum_number_of_builds`
                - :code:`auto_cancel_pushes`
                - :code:`auto_cancel_pull_requests`

        Methods
            * :meth:`~PyTravisCI.resource_types.setting.Setting.update`

        :raise MissingArgument:
            When :code:`repo_id_or_slug` nor :code:`setting_name` are given.
        :raise ValueError:
            When :code:`setting_name` is not into the list of accepted setting name.
        :raise TravisCIError:
            When something went wrong while communicating,
            getting or extracting data from or with the API.
        """

        return ResourceTypes.Setting(
            self, repo_id_or_slug=repo_id_or_slug, setting_name=setting_name
        )

    def settings(self, repo_id_or_slug):
        """
        Provide the information of a given :code:`repo_id_or_slug`.

        Official Travis CI API documentation
            - https://developer.travis-ci.org/resource/settings#Settings
            - https://developer.travis-ci.org/resource/settings#for_repository

        Extended documentation
            - :class:`~PyTravisCI.resource_types.settings.Settings`

        :param repo_id_or_slug:
            A repository ID or slug to get the information for.

            Can be
                :code:`{repository.id}`
                    Value uniquely identifying the repository.
                :code:`{repository.slug}`
                    Same as :code:`{repository.owner.name}/{repository.name}`

            .. warning::
                The Travis CI API states:

                    If querying using the repository slug, it must be formatted using
                    standard URL encoding, including any special characters.

                We do not except nor want that that from you.
                In fact, we do the encoding for you.

        :type repo_id_or_slug: str,int

        :raise MissingArgument:
            When :code:`repo_id_or_slug` is not given or empty.
        :raise TravisCIError:
            When something went wrong while communicating,
            getting or extracting data from or with the API.
        """

        return ResourceTypes.Settings(self, repo_id_or_slug=repo_id_or_slug)

    def user(self, user_id=None):
        """
        Provide the information of a given :code:`user_id`.

        Official Travis CI API documentation
            - https://developer.travis-ci.org/resource/setting#setting
            - https://developer.travis-ci.org/resource/setting#find
            - https://developer.travis-ci.org/resource/setting#update

        Extended documentation
            - :class:`~PyTravisCI.resource_types.user.User`

        :param user_id:
            A user ID.

            Can be
                :code:`{user.id}`
                    Value uniquely identifying the user.
        :type user_id: str,int

        :raise InvalidIntArgument:
            When :code:`user_id` is not an :code:`int` or :code:`str.isdigit`.
        :raise TravisCIError:
            When something went wrong while communicating,
            getting or extracting data from or with the API.
        """

        return ResourceTypes.User(self, user_id=user_id)
