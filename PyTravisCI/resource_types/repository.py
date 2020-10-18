"""
Just another Python API for Travis CI (API).

A module which provides the "Repository" resource type.

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

import base64
import os
import re
from io import IOBase
from typing import List, Optional, Union

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

import PyTravisCI.communicator._all as communicator
from PyTravisCI.encryption.data import DataEncryption
from PyTravisCI.encryption.file import FileEncryption

from . import _all as resource_types
from .base import ResourceTypesBase


class Repository(ResourceTypesBase):
    """
    Provides the description of a repository.

    Official Travis CI API documentation
        - https://developer.travis-ci.org/resource/repository

    :ivar int id:
        Value uniquely identifying the repository.
    :ivar str name:
        The repository's name on GitHub.
    :ivar str slug:
        Same as {repository.owner.name}/{repository.name}.
    :ivar str description:
        The repository's description from GitHub.
    :ivar int github_id:
        The repository's id on GitHub.
    :ivar vcs_id:
        The repository's vcs_id.
    :ivar vcs_type:
        The repository's vcs_type.
    :ivar str github_language:
        The main programming language used according to GitHub.
    :ivar bool active:
        Whether or not this repository is currently enabled on Travis CI.
    :ivar bool private:
        Whether or not this repository is private.
    :ivar owner:
        GitHub user or organization the repository belongs to.
    :vartype owner:
        Union[
            :class:`~PyTravisCI.resource_types.user.User`,
            :class:`~PyTravisCI.resource_types.organization.Organization`
        ]
    :ivar owner_name:
        The repository's owner_name.
    :ivar vcs_name:
        The repository's vcs_name.
    :ivar default_branch:
        The default branch on GitHub.
    :vartype default_branch: :class:`~PyTravisCI.resource_types.branch.Branch`
    :ivar bool starred:
        Whether or not this repository is starred.
    :ivar bool managed_by_installation:
        Whether or not this repository is managed by a GitHub App installation.
    :ivar bool active_on_org:
        Whether or not this repository runs builds on travis-ci.org (may also be null).
    :ivar migration_status:
        The repository's migration_status.
    :ivar history_migration_status:
        The repository's history_migration_status.
    :ivar shared:
        The repository's shared.
    :ivar config_validation:
        The repository's config_validation.
    :ivar allow_migration:
        The repository's allow_migration.
    """

    # pylint: disable=too-many-public-methods

    id: Optional[int] = None
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    github_id: Optional[int] = None
    vcs_id = None
    vcs_type = None
    github_language: Optional[str] = None
    active: Optional[bool] = None
    private: Optional[bool] = None
    owner: Optional[Union["resource_types.User", "resource_types.Organization"]] = None
    owner_name = None
    vcs_name = None
    default_branch: Optional["resource_types.Branch"] = None
    starred: Optional[bool] = None
    managed_by_installation: Optional[bool] = None
    active_on_org: Optional[bool] = None
    migration_status = None
    history_migration_status = None
    shared = None
    config_validation = None
    allow_migration = None

    def __init__(self, **kwargs) -> None:
        if "default_branch" in kwargs:
            kwargs["default_branch"] = resource_types.Branch(**kwargs["default_branch"])

        if "owner" in kwargs and "_at_type" in kwargs["owner"]:
            if kwargs["owner"]["_at_type"] == "user":
                kwargs["owner"] = resource_types.User(**kwargs["owner"])
            elif kwargs["owner"]["_at_type"] == "organization":
                kwargs["owner"] = resource_types.Organization(**kwargs["owner"])

        super().__init__(**kwargs)

    def activate(self, *, params: Optional[dict] = None) -> "resource_types.Repository":
        """
        Activates the current repository, allowing its test to be
        run on Travis Ci.

        :param params:
            The query parameters to append to the URL.
        """

        comm = getattr(communicator, self.__class__.__name__)(
            self._PyTravisCI["com"]["requester"]
        )

        self.__dict__ = comm.activate(
            repository_id_or_slug=self.id, parameters=params
        ).__dict__

        return self

    def deactivate(
        self, *, params: Optional[dict] = None
    ) -> "resource_types.Repository":
        """
        Activates the current repository, preventing any tests from
        runningIs on Travis CI.

        :param params:
            The query parameters to append to the URL.
        """

        comm = getattr(communicator, self.__class__.__name__)(
            self._PyTravisCI["com"]["requester"]
        )

        self.__dict__ = comm.deactivate(
            repository_id_or_slug=self.id, parameters=params
        ).__dict__

        return self

    def star(self, *, params: Optional[dict] = None) -> "resource_types.Repository":
        """
        Stars the current repository.

        :param params:
            The query parameters to append to the URL.
        """

        comm = getattr(communicator, self.__class__.__name__)(
            self._PyTravisCI["com"]["requester"]
        )

        self.__dict__ = comm.star(
            repository_id_or_slug=self.id, parameters=params
        ).__dict__

        return self

    def unstar(self, *, params: Optional[dict] = None) -> "resource_types.Repository":
        """
        Unstars the current repository.

        :param params:
            The query parameters to append to the URL.
        """

        comm = getattr(communicator, self.__class__.__name__)(
            self._PyTravisCI["com"]["requester"]
        )

        self.__dict__ = comm.unstar(
            repository_id_or_slug=self.id, parameters=params
        ).__dict__

        return self

    def get_branch(
        self, branch_name: str, *, params: Optional[dict] = None
    ) -> "resource_types.Branch":
        """
        Provides the information of a given branch.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/branch

        :param branch_name:
            Name of the git branch.
        :param params:
            The query parameters to append to the URL.
        """

        comm = getattr(communicator, "Branch")(self._PyTravisCI["com"]["requester"])

        return comm.from_id_or_slug(
            repository_id_or_slug=self.id, branch_name=branch_name, parameters=params
        )

    def get_branches(
        self, *, params: Optional[dict] = None
    ) -> "resource_types.Branches":
        """
        Provides the list of branches of the current repository.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/branches

        :param params:
            The query parameters to append to the URL.
        """

        comm = getattr(communicator, "Branches")(self._PyTravisCI["com"]["requester"])

        return comm.from_id_or_slug(repository_id_or_slug=self.id, parameters=params)

    def get_builds(self, *, params: Optional[dict] = None) -> "resource_types.Builds":
        """
        Provides the list of builds of the current repository.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/builds

        :param params:
            The query parameters to append to the URL.
        """

        comm = getattr(communicator, "Builds")(self._PyTravisCI["com"]["requester"])

        return comm.from_id_or_slug(repository_id_or_slug=self.id, parameters=params)

    def get_caches(self, *, params: Optional[dict] = None) -> "resource_types.Caches":
        """
        Provides the list of caches of the current repository.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/caches

        :param params:
            The query parameters to append to the URL.
        """

        comm = getattr(communicator, "Caches")(self._PyTravisCI["com"]["requester"])

        return comm.from_id_or_slug(repository_id_or_slug=self.id, parameters=params)

    def get_crons(self, *, params: Optional[dict] = None) -> "resource_types.Crons":
        """
        Provides the list of crons of the current repository.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/crons

        :param params:
            The query parameters to append to the URL.
        """

        comm = getattr(communicator, "Crons")(self._PyTravisCI["com"]["requester"])

        return comm.from_id_or_slug(repository_id_or_slug=self.id, parameters=params)

    def get_env_var(
        self, env_var_id: str, *, params: Optional[dict] = None
    ) -> "resource_types.EnvVar":
        """
        Provides an environment variable from its ID.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/env_var

        :param env_var_id:
            The ID of the environment variable to get.

        :param params:
            The query parameters to append to the URL.
        """

        comm = getattr(communicator, "EnvVar")(self._PyTravisCI["com"]["requester"])

        return comm.from_id_or_slug(
            env_var_id=env_var_id, repository_id_or_slug=self.id, parameters=params
        )

    def get_env_vars(
        self, *, params: Optional[dict] = None
    ) -> "resource_types.EnvVars":
        """
        Provides the list of environment variables of the current repository.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/env_vars

        :param params:
            The query parameters to append to the URL.
        """

        comm = getattr(communicator, "EnvVars")(self._PyTravisCI["com"]["requester"])

        return comm.from_id_or_slug(repository_id_or_slug=self.id, parameters=params)

    def create_env_var(
        self,
        name: str,
        value: str,
        *,
        is_public: bool = False,
        branch: Optional[str] = None,
        params: Optional[dict] = None,
    ) -> "resource_types.EnvVar":
        """
        Creates a new environment variable into the current repository.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/env_vars

        :param name:
            The environment variable name, e.g. FOO.
        :param value:
            The environment variable's value, e.g. bar.
        :param is_public:
            Whether this environment variable should be publicly visible or not.
        :param branch:
            The env_var's branch.

        :raise TypeError:
            When the types of :code:`name` and :code:`value` are not :py:class`str`.
        """

        if not isinstance(name, str):
            raise TypeError(f"<name> {name} should be {str}. {type(name)} given.")

        if not isinstance(value, str):
            raise TypeError(f"<value> {value} should be {str}. {type(value)} given.")

        data = {
            "env_var.name": name,
            "env_var.value": value,
            "env_var.public": is_public,
        }

        if branch is not None:
            data["env_var.branch"] = branch

        comm = getattr(communicator, "EnvVars")(self._PyTravisCI["com"]["requester"])

        return comm.create(repository_id_or_slug=self.id, data=data, parameters=params)

    def get_key_pair(
        self, *, params: Optional[dict] = None
    ) -> "resource_types.KeyPair":
        """
        Provides the RSA key pair of the current repository.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/key_pair

        :param params:
            The query parameters to append to the URL.
        """

        comm = getattr(communicator, "KeyPair")(self._PyTravisCI["com"]["requester"])

        return comm.from_id_or_slug(repository_id_or_slug=self.id, parameters=params)

    def create_key_pair(
        self,
        description: str,
        value: Union[str, bytes],
        *,
        params: Optional[dict] = None,
    ) -> "resource_types.KeyPair":
        """
        Creates a new RSA key pair.

        :param description:
            A text description.
        :param value:
            The private key.

        :raise TypeError:
            When the types of :code:`name` and :code:`value`
            are not :py:class`str` nor :py:class`bytes`.
        """

        if not isinstance(description, str):
            raise TypeError(
                f"<description> {description} should be {str}. {type(description)} given."
            )

        if not isinstance(value, (str, bytes)):
            raise TypeError(
                f"<value> {value} should be {str} or {bytes}. {type(value)} given."
            )

        data = {
            "key_pair.description": description,
            "key_pair.value": value,
        }

        comm = getattr(communicator, "KeyPair")(self._PyTravisCI["com"]["requester"])

        return comm.create(repository_id_or_slug=self.id, data=data, parameters=params)

    def get_key_pair_generated(
        self, *, params: Optional[dict] = None
    ) -> "resource_types.KeyPairGenerated":
        """
        Provides the generated RSA key pair of the current repository.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/key_pair_generated

        :param params:
            The query parameters to append to the URL.
        """

        comm = getattr(communicator, "KeyPairGenerated")(
            self._PyTravisCI["com"]["requester"]
        )

        return comm.from_id_or_slug(repository_id_or_slug=self.id, parameters=params)

    def generate_key_pair(
        self,
        *,
        params: Optional[dict] = None,
    ) -> "resource_types.KeyPairGenerated":
        """
        Generates a new RSA key pair.
        """

        comm = getattr(communicator, "KeyPairGenerated")(
            self._PyTravisCI["com"]["requester"]
        )

        return comm.create(repository_id_or_slug=self.id, parameters=params)

    def get_setting(
        self, setting_name: str, *, params: Optional[dict] = None
    ) -> "resource_types.Setting":
        """
        Provides a single setting from its given name.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/setting

        :param params:
            The query parameters to append to the URL.
        """

        comm = getattr(communicator, "Setting")(self._PyTravisCI["com"]["requester"])

        return comm.from_id_or_slug(
            setting_name=setting_name, repository_id_or_slug=self.id, parameters=params
        )

    def get_settings(
        self, *, params: Optional[dict] = None
    ) -> "resource_types.Settings":
        """
        Provides the list of settings of the current repository.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/settings

        :param params:
            The query parameters to append to the URL.
        """

        comm = getattr(communicator, "Settings")(self._PyTravisCI["com"]["requester"])

        return comm.from_id_or_slug(repository_id_or_slug=self.id, parameters=params)

    def get_request(
        self, request_id: Union[str, int], *, params: Optional[dict] = None
    ) -> "resource_types.Request":
        """
        Provides a single request from its given ID.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/requests

        :param request_id:
            The ID of the request to get.

        :param params:
            The query parameters to append to the URL.
        """

        comm = getattr(communicator, "Request")(self._PyTravisCI["com"]["requester"])

        return comm.from_id_or_slug(
            request_id=request_id, repository_id_or_slug=self.id, parameters=params
        )

    def get_requests(
        self, *, params: Optional[dict] = None
    ) -> "resource_types.Requests":
        """
        Provides the list of requests of the current repository.

        Official Travis CI API documentation:
            - https://developer.travis-ci.org/resource/requests

        :param params:
            The query parameters to append to the URL.
        """

        comm = getattr(communicator, "Requests")(self._PyTravisCI["com"]["requester"])

        return comm.from_id_or_slug(repository_id_or_slug=self.id, parameters=params)

    def create_request(
        self,
        message: str,
        branch: str,
        *,
        config: Optional[dict] = None,
        params: Optional[dict] = None,
    ) -> "resource_types.Request":
        """
        Creates a Request

        :param message:
            Travis-ci status message attached to the request.
        :param branch:
            Branch requested to be built.
        :param config:
            Build configuration (as parsed from .travis.yml).

        :raise TypeError:
            When the types of :code:`name` and :code:`value`
            are not :py:class`str` nor :py:class`bytes`.
        """

        if not isinstance(message, str):
            raise TypeError(
                f"<message> {message} should be {str}. {type(message)} given."
            )

        if not isinstance(branch, str):
            raise TypeError(f"<branch> {branch} should be {str}. {type(branch)} given.")

        if config and not isinstance(config, dict):
            raise TypeError(
                f"<branch> {config} should be {dict}. {type(branch)} given."
            )

        data = {
            "request.message": message,
            "request.branch": branch,
        }

        if config:
            data["request.config"] = config

        comm = getattr(communicator, "Requests")(self._PyTravisCI["com"]["requester"])

        return comm.create(repository_id_or_slug=self.id, data=data, parameters=params)

    def encrypt_env_var(
        self, env_vars: dict, padding: Optional[str] = "PKCS1v15"
    ) -> dict:
        """
        Process the encryption of the given environment variables.

        .. info::
            This method provides you what you have to write into your Travis file.


        :param env_vars:
            The key-value representing the environment variables to encrypt.

            .. warning::
                Spaces in keys will be automatically converted to underscore!

        :param padding:
            The padding to use.

            Supported by PyTravisCI:

                - :code:`PKCS1v15`
                - :code:`OAEP`

            Supported by Travis CI:

                - :code:`PKCS1v15`

            .. warning::
                DO NOT CHANGE THIS UNLESS INVITED TO.

                As of today, Travis CI use the :code:`PKCS1v15` padding.
                But it may be possible that one day they will change it to OAEP.

                Please report to the following references/discussion:

                    - https://github.com/travis-ci/travis-ci/issues/5394
                    - https://github.com/travis-ci/travis-ci/issues/5394#issue-124658348

        :return:
            A list representing each encrypted values.

            As example, if the following is given:

            ::

                {
                    "HELLO": "WORLD",
                    "WORLD": "HELLO"
                }

            The response will be:

            ::

                [
                    {"secure": "encrypted version of HELLO=WORLD" },
                    {"secure": "encrypted version of WORLD=HELLo" }
                ]
        """

        result = []

        if self.private:
            key_pair = self.get_key_pair()
        else:
            key_pair = self.get_key_pair_generated()

        encryption_obj = DataEncryption(public_key=key_pair.public_key)

        for env_name, value in env_vars.items():
            env_name = re.sub(r"[^\w+]", "_", env_name)

            to_encrypt = f'{env_name}="{value}"'.encode()

            result.append(
                {
                    "secure": base64.b64encode(
                        encryption_obj.encrypt_data(to_encrypt, padd=padding)
                    ).decode("ascii")
                }
            )

        return result

    def encrypt_secrets(
        self, secrets: List[Union[str, bytes]], padding: Optional[str] = "PKCS1v15"
    ) -> str:
        """
        Encrypts the given secret.

        :param secret:
            A list of secrets to encrypt.

        :param padding:
            The padding to use.

            Supported by PyTravisCI:

                - :code:`PKCS1v15`
                - :code:`OAEP`

            Supported by Travis CI:

                - :code:`PKCS1v15`

            .. warning::
                DO NOT CHANGE THIS UNLESS INVITED TO.

                As of today, Travis CI use the :code:`PKCS1v15` padding.
                But it may be possible that one day they will change it to OAEP.

                Please report to the following references/discussion:

                    - https://github.com/travis-ci/travis-ci/issues/5394
                    - https://github.com/travis-ci/travis-ci/issues/5394#issue-124658348

        :return:
            A list of encrypted secrets.
        """

        result = []

        if self.private:
            key_pair = self.get_key_pair()
        else:
            key_pair = self.get_key_pair_generated()

        encryption_obj = DataEncryption(public_key=key_pair.public_key)

        for secret in secrets:
            if not isinstance(secret, bytes):
                secret = secret.encode()

            result.append(
                base64.b64encode(
                    encryption_obj.encrypt_data(secret, padd=padding)
                ).decode("ascii")
            )

        return result

    def encrypt_file(
        self,
        input_file: Union[IOBase, str],
        output_file: Union[IOBase, str],
        *,
        branch: Optional[str] = None,
    ) -> dict:
        """
        Encrypts the content of the given :code:`input_file` into :code:`output_file`.

        Side Effects:
            - Generates a new IV key.
            - Generates a new encryption key.
            - Save the IV key into a (new) repository environment variable.
            - Save the encryption key into a (new) repository environment variable.

        :param input_file:
            The (plain) file to read.

            If a :py:class:`str` is given, this method will open and close the
            file for you.

            If a :py:class:`io.TextIOWrapper` is given, this method expects it to
            be in `rb` mode.

        :param output_file:
            The file to write.

            If a :py:class:`str` is given, this method will open and close the
            file for you.

            If a :py:class:`io.TextIOWrapper` is given, this method expects it to
            be in `wb` mode.

        :param branch:
            The branch to save the IV and key for.

        :return:
            A :py:class:`dict` which represents the data which are supposed to
            help the end-user decrypt the encrypted data.

            Given an input file :code:`hello` and an output file :code:`hello.enc`,
            this method will provides the following:

            ::

                {
                    "command": "openssl aes-256-cbc -K "
                    "$ENCRYPTED_BB6A5397D5B2_KEY -iv $ENCRYPTED_BB6A5397D5B2_IV "
                    "-in hello.enc -out hello -d",
                    "iv": {
                        "ENCRYPTED_BB6A5397D5B2_IV": "hexadecimal representation of the IV."
                    },
                    "key": {
                        "ENCRYPTED_BB6A5397D5B2_KEY": "hexadecimal representation of the key."
                    },
                }


        """

        input_file_self_opened = output_file_self_opened = False

        if not isinstance(input_file, IOBase):
            input_file = open(input_file, "rb")
            input_file_self_opened = True

        if not isinstance(output_file, IOBase):
            output_file = open(output_file, "wb")
            output_file_self_opened = True

        input_filename = os.path.split(input_file.name)[-1]
        output_filename = os.path.split(output_file.name)[-1]

        encryption_obj = FileEncryption()
        encryption_obj.encrypt_file(input_file, output_file)

        digest_backend = default_backend()
        input_digest = hashes.Hash(hashes.SHA1(), backend=digest_backend)
        input_digest.update(input_filename.encode())
        input_var_digest = input_digest.finalize().hex()[:12].upper()

        key_var_name = f"ENCRYPTED_{input_var_digest}_KEY"
        iv_var_name = f"ENCRYPTED_{input_var_digest}_IV"

        self.create_env_var(key_var_name, encryption_obj.get_key(), branch=branch)
        self.create_env_var(iv_var_name, encryption_obj.get_iv(), branch=branch)

        if input_file_self_opened:
            input_file.close()

        if output_file_self_opened:
            output_file.close()

        return {
            "command": f"openssl aes-256-cbc -K ${key_var_name} -iv "
            f"${iv_var_name} -in {output_filename} -out "
            f"{input_filename} -d",
            "iv": {iv_var_name: encryption_obj.get_iv()},
            "key": {key_var_name: encryption_obj.get_key()},
        }
