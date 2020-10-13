"""
Just another Travis CI (API) Python interface.

A module which provides the interface for the encryption of data for or within
the Travis CI infrastructure.

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

from typing import Optional, Union

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.backends.openssl import rsa
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding as asymmetric_padding


class DataEncryption:
    """
    Provides the interface for the encryption of information for or within the
    Travis CI infrastructure.

    :param public_key:
        The public key to use for encryption.
    """

    __SUPPORTED_PADDING = ["pkcs1v15", "oeap"]

    public_key: Optional[bytes] = None
    private_key: Optional[bytes] = None

    # pylint: disable=protected-access
    __loaded_public_key: Optional[rsa._RSAPublicKey] = None
    __loaded_private_key: Optional[rsa._RSAPrivateKey] = None

    def __init__(self, public_key: Optional[Union[str, bytes]] = None):
        if public_key:
            self.set_public_key(public_key)

    # pylint: disable=no-self-argument
    def encrypt_ensure_key_exists(func):
        """
        Ensures that the key needed for encryption exists.
        """

        def wrapper(self, *args, **kwargs):
            if not self.public_key:
                raise ValueError("<self.public_key> is not given.")

            # pylint: disable=not-callable
            return func(self, *args, **kwargs)

        return wrapper

    # pylint: disable=no-self-argument
    def decrypt_ensure_key_exists(func):
        """
        Ensures that the key needed for encryption exists.
        """

        def wrapper(self, *args, **kwargs):
            if not self.private_key:
                raise ValueError("<self.private_key> is not given.")

            # pylint: disable=not-callable
            return func(self, *args, **kwargs)

        return wrapper

    def set_public_key(self, value: Union[str, bytes]) -> None:
        """
        Sets the public key to use.

        :param value:
            The public key to set.
        """

        if not isinstance(value, bytes):
            self.public_key = value.encode()
        else:
            self.public_key = value

        self.__loaded_public_key = serialization.load_pem_public_key(
            data=self.public_key, backend=default_backend()
        )

    def set_private_key(
        self, value: Union[str, bytes], password: Optional[Union[str, bytes]] = None
    ) -> None:
        """
        Sets the private key to use.

        :param value:
            The private key to set.
        :param password:
            The password associated wiht the private key (if needed).
        """

        if not isinstance(value, bytes):
            self.private_key = value.encode()
        else:
            self.private_key = value

        if password and not isinstance(password, bytes):
            password = password.encode()

        self.__loaded_private_key = serialization.load_pem_private_key(
            self.private_key, password=password, backend=default_backend()
        )

    def get_public_key(self) -> Optional[bytes]:
        """
        Provides the currently loaded public key.
        """

        return self.public_key

    def get_private_key(self) -> Optional[bytes]:
        """
        Provided the currently loaded private key.
        """

        return self.private_key

    def __get_padding_from_name(self, name: str):
        """
        Provides the padding from its name.

        :param name:
            The name of the padding to user.
        """

        if name.lower() not in self.__SUPPORTED_PADDING:
            raise ValueError(f"<name> ({name!r}) not supported.")

        if name.lower() == "pkcs1v15":
            return asymmetric_padding.PKCS1v15()

        return asymmetric_padding.OAEP(
            mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        )

    @encrypt_ensure_key_exists
    def encrypt_data(self, data: Union[str, bytes], *, padd: str = "PKCS1v15") -> bytes:
        """
        Process the encryption of the given data with the given padding.

        :param data:
            The data to encrypt.
        :param padd:
            The padding to use.

            Accepted values:
                - :code:`PKCS1v15`
                - :code:`OAEP`
        """

        if not isinstance(data, bytes):
            data = data.encode()

        padd = self.__get_padding_from_name(padd)

        return self.__loaded_public_key.encrypt(data, padd)

    @decrypt_ensure_key_exists
    def decrypt_data(self, data: Union[str, bytes], *, padd: str = "PKCS1v15") -> bytes:
        """
        Process the decryption of the given data with the given padding.

        :param data:
            The data to encrypt.
        :param padd:
            The padding to use.

            Accepted values:
                - :code:`PKCS1v15`
                - :code:`OAEP`
        """

        if not isinstance(data, bytes):
            data = data.encode()

        padd = self.__get_padding_from_name(padd)

        return self.__loaded_private_key.decrypt(data, padd)
