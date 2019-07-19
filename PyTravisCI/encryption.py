"""
Just another Travis CI (Python) API client.

Provide a way to encrpyt environment variable for Travis CI.

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

from base64 import b64encode

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.padding import (MGF1, OAEP,
                                                               PKCS1v15)
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.serialization import load_pem_public_key

from PyTravisCI.exceptions import IncompatibleArgument, MissingArgument


class Encryption:
    """
    Encrypts the given environment variable so that they can be
    used inside a Travis CI VM.

    :param to_encrypt:
        A dict, list or string representing the data to encrypt.

        Example
            ::

                {
                    "HELLO": "WORLD",
                    "WORLD": "HELLO"
                }

            will encrpyt :code:`HELLO=WORLD`, :code:'WORLD=HELLO'

            when

            ::

                ["Hello", "World"]

            will encrypt :code:`Hello` then :code:`World`.

            finally,

            ::

                "Hello_world"

            will encrypt :code:`Hello_world`

        .. warning::
            if a space is present into a key, it will be replaced with an
            underscore.

    :type to_encrypt: str, dict, list

    :parm public_key:
        The public key to use to encrypt the given env.
    :type public_key: str, bytes

    .. warning::
        This class has been built just in order to encrypt global environment variables
        which can later be stored into the :code:`env[global]`
        index of your :code:`.travis.yml` file.
    """

    def __init__(self, to_encrypt, public_key):
        self.to_encrypt = to_encrypt
        self.public_key = self.load_public_key(public_key)

    @classmethod
    def load_public_key(cls, public_key):
        """
        Load the given :code:`public_key`.
        """

        if not isinstance(public_key, bytes):  # pragma: no cover
            public_key = public_key.encode()

        return load_pem_public_key(public_key, default_backend())

    def __encrypt_it_with_pkcs1v15(self, to_encrypt):
        """
        Encrypt the given data using the PKCS1v15 padding.

        :param bytes to_encrypt: The data to encrypt.

        :rtype: str
        """

        return b64encode(self.public_key.encrypt(to_encrypt, PKCS1v15())).decode(
            "ASCII"
        )

    def __encrypt_it_with_oeap(self, to_encrypt):
        """
        Encrypt the given data using the OEAP padding.

        :param bytes to_encrypt: The data to encrypt.

        :rtype: str
        """

        return b64encode(
            self.public_key.encrypt(
                to_encrypt,
                OAEP(mgf=MGF1(algorithm=SHA256()), algorithm=SHA256(), label=None),
            )
        ).decode("ASCII")

    def __encrypt_env_vars(self, to_encrypt, pkcs1v15_mode=True):
        """
        Encrypt the given environment variables.
        """

        result = []

        for env_name, value in to_encrypt.items():
            env_name = env_name.replace(" ", "_")

            if " " in value:
                to_encrypt = f'{env_name}="{value}"'.encode()
            else:
                to_encrypt = f"{env_name}={value}".encode()

            if pkcs1v15_mode:
                encrypted = self.__encrypt_it_with_pkcs1v15(to_encrypt)
            else:
                encrypted = self.__encrypt_it_with_oeap(to_encrypt)

            result.append({"secure": encrypted})

        return result

    def __encrypt_secrets(self, to_encrypt, pkcs1v15_mode=True):
        """
        Encrypt the given secrets.
        """

        result = []

        for data in to_encrypt:
            if not isinstance(data, bytes):
                data = data.encode()

            if pkcs1v15_mode:
                result.append(self.__encrypt_it_with_pkcs1v15(data))
            else:
                result.append(self.__encrypt_it_with_oeap(data))

        return result

    def __encrypt_password(self, to_encrypt, pkcs1v15_mode=True):
        """
        Encrypt the given password.
        """

        if not isinstance(to_encrypt, bytes):
            to_encrypt = to_encrypt.encode()

        if pkcs1v15_mode:
            return self.__encrypt_it_with_pkcs1v15(to_encrypt)
        return self.__encrypt_it_with_oeap(to_encrypt)

    def encrypt(self, pkcs1v15_mode=True, oeap_mode=False):
        """
        Encrypt the given envs with the given public key.

        :param bool pkcs1v15_mode:
            Activate the PKCS1v15 padding which is the default one Travis CI uses.

            References
                - https://github.com/travis-ci/travis-ci/issues/5394
                - https://github.com/travis-ci/travis-ci/issues/5394#issue-124658348

        :param bool oeap_mode:
            Activate the OAEP paddingw which will probably be the one
            Travis CI may adopt in the future.

        :raise IncompatibleArgument:
            When :code:`pskcs1v15_mode` is given along with :code:`oeap_mode`.
        :raise MissingArgument:
            When :code:`pskcs1v15_mode` nor :code:`oeap_mode` is given.
        """

        if pkcs1v15_mode and oeap_mode:  # pragma: no cover
            raise IncompatibleArgument(["oeap_mode", "pskcs1v15_mode"])

        if not pkcs1v15_mode and not oeap_mode:  # pragma: no cover
            raise MissingArgument(["pskcs1v15_mode", "oeap_mode"])

        if isinstance(self.to_encrypt, dict):
            result = self.__encrypt_env_vars(
                self.to_encrypt, pkcs1v15_mode=pkcs1v15_mode
            )
        elif isinstance(self.to_encrypt, list):
            result = self.__encrypt_secrets(
                self.to_encrypt, pkcs1v15_mode=pkcs1v15_mode
            )
        else:
            result = self.__encrypt_password(
                self.to_encrypt, pkcs1v15_mode=pkcs1v15_mode
            )

        return result
