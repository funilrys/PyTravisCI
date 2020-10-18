"""
Just another Python API for Travis CI (API).

A module which provides the gateway to the Travis CI API. All interaction starts
with this module's class-es.

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

from io import TextIOWrapper
from typing import Optional, Union

import PyTravisCI.communicator._all as communicator
import PyTravisCI.defaults as defaults
import PyTravisCI.requester as requester
import PyTravisCI.resource_types._all as resource_types  # pylint: disable=unused-import


class TravisCI:
    """
    The gateway to the interaction with the Travis CI API.

    :param str access_token:
        The access token to use to authenticate ourselves.
    :param str access_point:
        The access point to communicate with.
    """

    # pylint: disable=too-many-public-methods

    def __init__(
        self,
        *,
        access_token: Optional[str] = None,
        access_point: Optional[str] = defaults.access_points.OPEN,
    ) -> None:
        self.__requester = requester.Requester()

        self.set_access_point(access_point)

        if access_token:
            self.set_access_token(access_token)

    def set_access_token(self, value: str) -> None:
        """
        Sets the access token.
        """

        self.__requester.set_authorization(value)

    def get_access_point(self) -> str:
        """
        Provides the currently set access point.
        """

        return self.__requester.base_url

    def set_access_point(self, value: str) -> None:
        """
        Sets the access point to communicate with.
        """

        self.__requester.set_base_url(value)

    def get_active_from_github_id(
        self, github_id: Union[str, int], *, params: Optional[dict] = None
    ) -> "resource_types.Active":
        """
        Provides the list of all active builds.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/active

        :param github_id:
            Documentation missing.
            The GitHub user or organization ID to get the active builds for.
        :param params:
            The query parameters to append to the URL.
        """

        return communicator.Active(self.__requester).from_github_id(
            github_id=int(github_id), parameters=params
        )

    def get_active_from_login(
        self, login: str, *, provider: str = "github", params: Optional[dict] = None
    ) -> "resource_types.Active":
        """
        Provides the list of all active builds for the given
        login in the given provider.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/active

        :param login:
            Documentation missing.
            The Login of to user to fetch the data for.
        :param provider:
            Documentation missing.
        :param params:
            The query parameters to append to the URL.
        """

        return communicator.Active(self.__requester).from_login(
            login=login, provider=provider, parameters=params
        )

    def get_broadcasts(
        self, *, params: Optional[dict] = None
    ) -> "resource_types.Broadcasts":
        """
        Provides the list of broadcasts of the current user.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/broadcasts

        :param params:
            The query parameters to append to the URL.
        """

        return communicator.Broadcasts(self.__requester).fetch(parameters=params)

    def get_build(
        self, build_id: Union[int, str], *, params: Optional[dict] = None
    ) -> "resource_types.Build":
        """
        Provides the build information from its ID.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/build

        :param build_id:
            Value uniquely identifying the build.
        :param params:
            The query parameters to append to the URL.
        """

        return communicator.Build(self.__requester).from_id(
            build_id=build_id, parameters=params
        )

    def get_builds(self, *, params: Optional[dict] = None) -> "resource_types.Builds":
        """
        Provides the list of builds of the current user.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/build

        :param params:
            The query parameters to append to the URL.
        """

        return communicator.Builds(self.__requester).fetch(parameters=params)

    def get_cron(
        self, cron_id: Union[str, int], *, params: Optional[dict] = None
    ) -> "resource_types.Cron":
        """
        Provides a cron from its given ID.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/cron

        :param cron_id:
            Value uniquely identifying the cron.
        :param params:
            The query parameters to append to the URL.
        """

        return communicator.Cron(self.__requester).from_id(
            cron_id=cron_id, parameters=params
        )

    def get_job(
        self, job_id: Union[str, int], *, params: Optional[dict] = None
    ) -> "resource_types.Job":
        """
        Provides a job from its given ID.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/job

        :param job_id:
            Value uniquely identifying the job.
        :param params:
            The query parameters to append to the URL.
        """

        return communicator.Job(self.__requester).from_id(
            job_id=job_id, parameters=params
        )

    def get_jobs(self, *, params: Optional[dict] = None) -> "resource_types.Jobs":
        """
        Provides the list of jobs of the current user.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/jobs

        :param params:
            The query parameters to append to the URL.
        """

        return communicator.Jobs(self.__requester).fetch(parameters=params)

    def lint(self, subject: Union[TextIOWrapper, bytes, str]) -> "resource_types.Lint":
        """
        Lints the given subject.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/lint

        :param subject:
            A string, file stream or bytes.

        :raise TypeError:
            When then given :code:`subject` is not correct.
        """

        if isinstance(subject, TextIOWrapper):
            data = subject.read()
        elif isinstance(subject, (str, bytes)):
            data = subject
        else:
            raise TypeError(
                f"<subject> must be {TextIOWrapper}, {str} or {bytes}, {type(subject)} given."
            )

        return communicator.Lint(self.__requester).fetch(data=data)

    def get_organization(
        self, organization_id: Union[str, int], *, params: Optional[dict] = None
    ) -> "resource_types.Organization":
        """
        Provides an organization from its given ID.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/organization

        :param organization_id:
            Value uniquely identifying the organization.
        :param params:
            The query parameters to append to the URL.
        """

        return communicator.Organization(self.__requester).from_id(
            organization_id=organization_id, parameters=params
        )

    def get_organizations(
        self, *, params: Optional[dict] = None
    ) -> "resource_types.Organizations":
        """
        Provides the list of organizations of the current user.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/organization

        :param params:
            The query parameters to append to the URL.
        """

        return communicator.Organizations(self.__requester).fetch(parameters=params)

    def get_repositories(
        self, *, params: Optional[dict] = None
    ) -> "resource_types.Repositories":
        """
        Provides the list of repositories of the current user.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/repositories

        :param params:
            The query parameters to append to the URL.
        """

        return communicator.Repositories(self.__requester).fetch(parameters=params)

    def get_repositories_from_github_id(
        self, github_id: Union[str, int], *, params: Optional[dict] = None
    ) -> "resource_types.Repositories":
        """
        Provides the list of repositories of the given GitHub ID.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/repositories

        :param github_id:
            Documentation missing.
            The GitHub user or organization ID to get the repositories for.
        :param params:
            The query parameters to append to the URL.
        """

        return communicator.Repositories(self.__requester).from_github_id(
            github_id=int(github_id), parameters=params
        )

    def get_repositories_from_login(
        self, login: str, *, provider: str = "github", params: Optional[dict] = None
    ) -> "resource_types.Repositories":
        """
        Provides the list of repositories for the given
        login in the given provider.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/repositories

        :param login:
            Documentation missing.
            The Login of to user to fetch the data for.
        :param provider:
            Documentation missing.
        :param params:
            The query parameters to append to the URL.
        """

        return communicator.Repositories(self.__requester).from_login(
            login=login, provider=provider, parameters=params
        )

    def get_repository_from_provider(
        self,
        provider: str,
        repository_id_or_slug: Union[str, int],
        *,
        params: Optional[dict] = None,
    ) -> "resource_types.Repository":
        """
        Provides the repository from its given provider, ID
        or slug.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/repository

        :param str provider:
            Documentation missing.
        :param repository_id_or_slug:
            Value uniquely identifying the repository.
        :param params:
            The query parameters to append to the URL.
        """

        return communicator.Repository(self.__requester).from_provider(
            provider=provider,
            repository_id_or_slug=repository_id_or_slug,
            parameters=params,
        )

    def get_repository(
        self, repository_id_or_slug: Union[str, int], *, params: Optional[dict] = None
    ) -> "resource_types.Repository":
        """
        Provides the repository from its given ID or slug.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/repository

        :param repository_id_or_slug:
            Value uniquely identifying the repository.
        :param params:
            The query parameters to append to the URL.
        """

        return communicator.Repository(self.__requester).from_id_or_slug(
            repository_id_or_slug=repository_id_or_slug, parameters=params
        )

    def get_user(self, *, params: Optional[dict] = None) -> "resource_types.User":
        """
        Provides the information of the current user.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/user

        :param params:
            The query parameters to append to the URL.
        """

        return communicator.User(self.__requester).fetch(parameters=params)

    def get_user_from_id(
        self, user_id: Union[str, int], *, params: Optional[dict] = None
    ) -> "resource_types.User":
        """
        Provides the information of a user from its ID.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/user

        :param user_id:
            Value uniquely identifying the user.

        :param params:
            The query parameters to append to the URL.
        """

        return communicator.User(self.__requester).from_user_id(
            user_id=user_id, parameters=params
        )
