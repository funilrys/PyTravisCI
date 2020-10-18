"""
Just another Python API for Travis CI (API).

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

import secrets
from io import IOBase
from typing import IO, Optional, Union

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding as primitive_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class FileEncryption:
    """
    Provides the interface for the encryption of files for or within the
    Travis CI infrastructure.

    :param key:
        The key to use to encrypt the file.
    :param iv:
        The IV to use to encrypt the file.
    """

    # pylint: disable=invalid-name

    AES_BLOCK_SIZE: int = 128
    KEY_SIZE: int = 32
    IV_SIZE: int = 16

    key: Optional[bytes] = None
    iv: Optional[bytes] = None

    def __init__(
        self,
        *,
        key: Optional[Union[str, bytes]] = None,
        iv: Optional[Union[str, bytes]] = None,
    ):
        if key:
            self.set_key(key)

        if iv:
            self.set_iv(iv)

    # pylint: disable=no-self-argument
    def encrypt_ensure_keys_exists(func):
        """
        Ensures that the keys exists before any encryption.
        """

        def wrapper(self, *args, **kwargs):
            if not self.key:
                self.generate_key()

            if not self.iv:
                self.generate_iv()

            # pylint: disable=not-callable
            return func(self, *args, **kwargs)

        return wrapper

    # pylint: disable=no-self-argument
    def decrypt_ensure_keys_exists(func):
        """
        Ensures that the keys exists before any decryption.
        """

        def wrapper(self, *args, **kwargs):
            if not self.key:
                raise ValueError("<self.key> is not given.")

            if not self.iv:
                raise ValueError("<self.iv> is not given.")

            # pylint: disable=not-callable
            return func(self, *args, **kwargs)

        return wrapper

    def set_key(self, value: Union[str, bytes]) -> None:
        """
        Sets the Key to use.

        :raise ValueError:
            When the size of the given key is not correct.
        """

        if not isinstance(value, bytes):
            self.key = value.encode()
        else:
            self.key = value

        if len(self.key) != self.KEY_SIZE:
            raise ValueError(
                f"<value> should have a length of {self.KEY_SIZE}, {len(self.key)} given."
            )

    def set_iv(self, value: Union[str, bytes]) -> None:
        """
        Sets the IV to use.

        :raise ValueError:
            When the size of the given key is not correct.
        """

        if not isinstance(value, bytes):
            self.iv = value.encode()
        else:
            self.iv = value

        if len(self.iv) != self.IV_SIZE:
            raise ValueError(
                f"<value> should have a length of {self.IV_SIZE}, {len(self.iv)} given."
            )

    def get_key(self) -> Optional[bytes]:
        """
        Provides the hexadecimal representation of the currently set key.
        """

        if self.key:
            return self.key.hex()
        return self.key

    def get_iv(self) -> Optional[bytes]:
        """
        Provides the hexadecimal representation of the currently set iv.
        """

        if self.iv:
            return self.iv.hex()
        return self.iv

    def generate_key(self, *, save: bool = True) -> bytes:
        """
        Generates a new key.

        :param save:
            Dis-authorize the saving into the global key attribute.
        """

        new_key = secrets.token_bytes(self.KEY_SIZE)

        if save:
            self.set_key(new_key)

        return new_key

    def generate_iv(self, *, save: bool = True) -> bytes:
        """
        Generate a new IV key.

        :param save:
            Dis-authorize the saving into the global iv attribute.
        """

        new_iv = secrets.token_bytes(self.IV_SIZE)

        if save:
            self.set_iv(new_iv)
        return new_iv

    # pylint: disable=protected-access
    def __get_cipher(self) -> Cipher:
        """
        Provides the encryptor to use.
        """

        return Cipher(
            algorithms.AES(self.key), modes.CBC(self.iv), backend=default_backend()
        )

    @encrypt_ensure_keys_exists
    def encrypt_file_content(self, file_content: Union[str, bytes]) -> bytes:
        """
        Encrypts the given "file content" into something which can later be
        decrypted through:

        ::

            $ openssl aes-256-cbc -K $encrypted_0a6446eb3ae3_key -iv \\
            $encrypted_0a6446eb3ae3_iv -in super_secret.txt.enc -out \\
            super_secret.txt -d

        where the delivered result is the content of :code:`super_secret.txt.enc`
        """

        if not isinstance(file_content, bytes):
            file_content = file_content.encode()

        pad = primitive_padding.PKCS7(self.AES_BLOCK_SIZE).padder()
        padded_file_content = pad.update(file_content) + pad.finalize()

        encryptor = self.__get_cipher().encryptor()

        return encryptor.update(padded_file_content) + encryptor.finalize()

    @decrypt_ensure_keys_exists
    def decrypt_file_content(self, encrypted_file_content: bytes) -> bytes:
        """
        Decrypts the given encrypted "file content". Take it as the equivalent of:

        ::

            $ openssl aes-256-cbc -K $encrypted_0a6446eb3ae3_key -iv \\
            $encrypted_0a6446eb3ae3_iv -in super_secret.txt.enc -out \\
            super_secret.txt -d

        but in Python :-)

        :raise ValueError:
            When :code:`encrypted_file_content` is not a :py:class:`bytes`.
        """

        if not isinstance(encrypted_file_content, bytes):
            raise ValueError(
                f"<encrypted_file_content> must be {bytes}, {type(encrypted_file_content)} given."
            )

        decryptor = self.__get_cipher().decryptor()
        decrypted = decryptor.update(encrypted_file_content) + decryptor.finalize()

        unpad = primitive_padding.PKCS7(self.AES_BLOCK_SIZE).unpadder()

        return unpad.update(decrypted) + unpad.finalize()

    @encrypt_ensure_keys_exists
    def encrypt_file(
        self,
        input_file: Union[IO, IOBase],
        output_file: Union[IO, IOBase],
    ) -> None:
        """
        Encrypts the content of :code:`input_file` into :code:`output_file`.
        """

        output_file.write(self.encrypt_file_content(input_file.read()))

    @decrypt_ensure_keys_exists
    def decrypt_file(
        self,
        input_file: Union[IO, IOBase],
        output_file: Union[IO, IOBase],
    ) -> None:
        """
        Decrypts the content of :code:`input_file` into :code:`output_file`.
        """

        output_file.write(self.decrypt_file_content(input_file.read()))
