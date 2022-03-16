"""
Just another Python API for Travis CI (API).

A module which provides the tests of our data encryption module.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Project link:
    https://github.com/funilrys/PyTravisCI

Project documentation:
    https://pytravisci.readthedocs.io/en/latest/

License
::


    MIT License

    Copyright (c) 2019, 2020, 2021, 2022 Nissar Chababy

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
from unittest import TestCase
from unittest import main as launch_tests

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from PyTravisCI.encryption.data import DataEncryption


class TestDataEncryption(TestCase):
    """
    Provides the tests of the data encryption class.
    """

    private_key_password: bytes = b"Hello, World!"
    private_key: Optional[rsa.RSAPrivateKeyWithSerialization] = None
    public_key: Optional[rsa.RSAPublicKey] = None
    pem_private_key: Optional[Union[str, bytes]] = None
    pem_public_key: Optional[Union[str, bytes]] = None

    @staticmethod
    def get_new_key() -> rsa.RSAPrivateKeyWithSerialization:
        """
        Provides a new key to work with.
        """

        return rsa.generate_private_key(
            backend=default_backend(), public_exponent=65537, key_size=2048
        )

    def setUp(self):
        """
        Setups everything needed by the tests.
        """

        self.private_key = self.get_new_key()
        self.public_key = self.private_key.public_key()

        self.pem_private_key = self.private_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        )
        self.encrypted_pem_private_key = self.private_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.BestAvailableEncryption(self.private_key_password),
        )

        self.pem_public_key = self.public_key.public_bytes(
            serialization.Encoding.PEM, serialization.PublicFormat.PKCS1
        )

    def tearDown(self) -> None:
        """
        Destroy everything set by the setup method.
        """

        del self.private_key
        del self.pem_private_key
        del self.pem_public_key
        del self.encrypted_pem_private_key

    def test_set_public_key(self) -> None:
        """
        Tests of the method which let us set the public key to work with.
        """

        expected = self.pem_public_key.decode()

        encryptor = DataEncryption(public_key=self.pem_public_key)

        # pylint: disable=protected-access
        actual = encryptor._loaded_public_key.public_bytes(
            serialization.Encoding.PEM, serialization.PublicFormat.PKCS1
        ).decode()

        self.assertEqual(expected, actual)

    def test_set_public_key_setter(self) -> None:
        """
        Tests of the method which let us set the public key to work with.
        """

        expected = self.pem_public_key.decode()

        encryptor = DataEncryption()
        encryptor.set_public_key(self.pem_public_key)

        # pylint: disable=protected-access
        actual = encryptor._loaded_public_key.public_bytes(
            serialization.Encoding.PEM, serialization.PublicFormat.PKCS1
        ).decode()

        self.assertEqual(expected, actual)

    def test_set_public_key_setter_pem_str(self) -> None:
        """
        Tests of the method which let us set the public key to work with for the
        case that the given public key is a string.
        """

        expected = self.pem_public_key.decode()

        encryptor = DataEncryption()
        encryptor.set_public_key(self.pem_public_key.decode())

        # pylint: disable=protected-access
        actual = encryptor._loaded_public_key.public_bytes(
            serialization.Encoding.PEM, serialization.PublicFormat.PKCS1
        ).decode()

        self.assertEqual(expected, actual)

    def test_set_private_key(self) -> None:
        """
        Tests of the method which let us set the private key to work with.
        """

        expected = self.pem_private_key.decode()

        encryptor = DataEncryption(private_key=self.pem_private_key)

        # pylint: disable=protected-access
        actual = encryptor._loaded_private_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        ).decode()

        self.assertEqual(expected, actual)

    def test_set_private_key_setter(self) -> None:
        """
        Tests of the method which let us set the private key to work with.
        """

        expected = self.pem_private_key.decode()

        encryptor = DataEncryption()
        encryptor.set_private_key(self.pem_private_key)

        # pylint: disable=protected-access
        actual = encryptor._loaded_private_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        ).decode()

        self.assertEqual(expected, actual)

    def test_set_private_key_setter_pem_str(self) -> None:
        """
        Tests of the method which let us set the private key to work with for
        the case that the given private key is a string.
        """

        expected = self.pem_private_key.decode()

        encryptor = DataEncryption()
        encryptor.set_private_key(self.pem_private_key.decode())

        # pylint: disable=protected-access
        actual = encryptor._loaded_private_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        ).decode()

        self.assertEqual(expected, actual)

    def test_set_private_key_setter_encrypted_pem(self) -> None:
        """
        Tests of the method which let us set the private key to work with for
        the case that the given private key is encrypted with a password.
        """

        expected = self.pem_private_key.decode()

        encryptor = DataEncryption()
        encryptor.set_private_key(
            self.encrypted_pem_private_key, password=self.private_key_password
        )

        # pylint: disable=protected-access
        actual = encryptor._loaded_private_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        ).decode()

        self.assertEqual(expected, actual)

    def test_set_private_key_setter_encrypted_pem_str_password(self) -> None:
        """
        Tests of the method which let us set the private key to work with for
        the case that the given private key is encrypted with a string password.
        """

        expected = self.pem_private_key.decode()

        encryptor = DataEncryption()
        encryptor.set_private_key(
            self.encrypted_pem_private_key, password=self.private_key_password.decode()
        )

        # pylint: disable=protected-access
        actual = encryptor._loaded_private_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        ).decode()

        self.assertEqual(expected, actual)

    def test_get_public_key(self) -> None:
        """
        Tests of the method which let us get the public key we previously gave.
        """

        expected = self.pem_public_key

        encryptor = DataEncryption()
        encryptor.set_public_key(self.pem_public_key.decode())

        actual = encryptor.get_public_key()

        self.assertEqual(expected, actual)

    def test_get_private_key(self):
        """
        Tests of the method which let us get the private key we previously gave.
        """

        expected = self.pem_private_key

        encryptor = DataEncryption()
        encryptor.set_private_key(self.pem_private_key.decode())

        actual = encryptor.get_private_key()

        self.assertEqual(expected, actual)

    def test_encryption_with_pkcs1v15(self) -> None:
        """
        Tests the encryption/decryption with the PKCS1v15 padding.
        """

        given = "Hello, World!"
        expected = b"Hello, World!"

        encryptor = DataEncryption()
        encryptor.set_private_key(self.pem_private_key)
        encryptor.set_public_key(self.pem_public_key)

        actual = encryptor.encrypt_data(given, padd="PKCS1v15")

        self.assertNotEqual(given, actual)

        actual = encryptor.decrypt_data(actual, padd="PKCS1v15")

        self.assertEqual(expected, actual)

    def test_encryption_with_oeap(self) -> None:
        """
        Tests the encryption/decryption.
        """

        given = "Hello, World!"
        expected = b"Hello, World!"

        encryptor = DataEncryption()
        encryptor.set_private_key(self.pem_private_key)
        encryptor.set_public_key(self.pem_public_key)

        actual = encryptor.encrypt_data(given, padd="OEAP")

        self.assertNotEqual(given, actual)

        actual = encryptor.decrypt_data(actual, padd="OEAP")

        self.assertEqual(expected, actual)

    def test_encryption_public_key_not_given(self) -> None:
        """
        Tests the encryption for the case that no key is given.
        """

        given = "Hello, World!"

        encryptor = DataEncryption()

        self.assertRaises(ValueError, lambda: encryptor.encrypt_data(given))

    def test_encryption_unkown_padding_name(self) -> None:
        """
        Tests the encryption for the case that the given padding name is not
        known or supported.
        """

        given = "Hello, World!"
        given_padding = "Hello"

        encryptor = DataEncryption()
        encryptor.set_public_key(self.pem_public_key.decode())

        self.assertRaises(
            ValueError, lambda: encryptor.encrypt_data(given, padd=given_padding)
        )

    def test_decryption_private_key_not_given(self) -> None:
        """
        Tests the encryption for the case that no key is given.
        """

        given = "Hello, World!"

        encryptor = DataEncryption()

        self.assertRaises(ValueError, lambda: encryptor.decrypt_data(given))

    def test_encryption_with_data_to_decrypt_as_str(self) -> None:
        """
        Tests the encryption/decryption for the case that we give the string
        representation of the encoded data.
        """

        given = "Hello, World!"

        encryptor = DataEncryption()
        encryptor.set_private_key(self.pem_private_key)
        encryptor.set_public_key(self.pem_public_key)

        actual = encryptor.encrypt_data(given)

        self.assertNotEqual(given, actual)

        self.assertRaises(ValueError, lambda: encryptor.decrypt_data(actual.hex()))


if __name__ == "__main__":
    launch_tests()
