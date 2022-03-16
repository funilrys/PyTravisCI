"""
Just another Python API for Travis CI (API).

A module which provides the tests of our file encryption module.

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

import os
import secrets
from tempfile import NamedTemporaryFile
from unittest import TestCase
from unittest import main as launch_tests

from PyTravisCI.encryption.file import FileEncryption


class TestFileEncryption(TestCase):
    """
    Provides the tests of the file encryption class.
    """

    # pylint: disable=too-many-public-methods

    def setUp(self) -> None:
        """
        Setups everything needed by the tests.
        """

        self.encryption_key = secrets.token_bytes(32)
        self.encryption_key_str = secrets.token_hex(16)

        self.iv_key = secrets.token_bytes(16)
        self.iv_key_str = secrets.token_hex(8)

    def tearDown(self) -> None:
        """
        Destroys everything set by the setup method.
        """

        del self.encryption_key
        del self.encryption_key_str

    def test_set_key(self):
        """
        Tests of the method which let us set the key to work with.
        """

        expected = self.encryption_key

        encryptor = FileEncryption(key=self.encryption_key)

        actual = encryptor.key

        self.assertEqual(expected, actual)

    def test_set_str_key(self):
        """
        Tests of the method which let us set the key to work with.
        """

        expected = self.encryption_key_str.encode()

        encryptor = FileEncryption()
        encryptor.set_key(self.encryption_key_str)

        actual = encryptor.key

        self.assertEqual(expected, actual)

    def test_set_key_wrong_size(self):
        """
        Tests of the method which let us set the key to work with for the case
        that the size is not correct.
        """

        encryptor = FileEncryption()

        self.assertRaises(ValueError, lambda: encryptor.set_key(self.iv_key))

    def test_set_iv(self):
        """
        Tests of the method which let us set the iv to work with.
        """

        expected = self.iv_key

        encryptor = FileEncryption(iv=self.iv_key)

        actual = encryptor.iv

        self.assertEqual(expected, actual)

    def test_set_str_iv(self):
        """
        Tests of the method which let us set the iv to work with.
        """

        expected = self.iv_key_str.encode()

        encryptor = FileEncryption()
        encryptor.set_iv(self.iv_key_str)

        actual = encryptor.iv

        self.assertEqual(expected, actual)

    def test_set_iv_wrong_size(self):
        """
        Tests of the method which let us set the iv to work with for the case
        that the size is not correct.
        """

        encryptor = FileEncryption()

        self.assertRaises(ValueError, lambda: encryptor.set_iv(self.encryption_key))

    def test_get_key(self):
        """
        Tests of the method which let us get the hexadecimal representation of
        our key.
        """

        expected = self.encryption_key.hex()

        encryptor = FileEncryption()
        encryptor.set_key(self.encryption_key)

        actual = encryptor.get_key()

        self.assertEqual(expected, actual)

    def test_get_key_not_set(self):
        """
        Tests of the method which let us get the hexadecimal representation
        of our key for the case that it is not given.
        """

        expected = None

        encryptor = FileEncryption()

        actual = encryptor.get_key()

        self.assertEqual(expected, actual)

    def test_get_iv(self):
        """
        Tests of the method which let us get the hexadecimal representation of
        our iv.
        """

        expected = self.iv_key.hex()

        encryptor = FileEncryption()
        encryptor.set_iv(self.iv_key)

        actual = encryptor.get_iv()

        self.assertEqual(expected, actual)

    def test_get_iv_not_set(self):
        """
        Tests of the method which let us get the hexadecimal representation
        of our iv for the case that it is not given.
        """

        expected = None

        encryptor = FileEncryption()

        actual = encryptor.get_iv()

        self.assertEqual(expected, actual)

    def test_generate_key(self):
        """
        Tests of the method which let us generate a new key.
        """

        expected_length = 32

        encryptor = FileEncryption()

        actual = encryptor.generate_key(save=True)

        self.assertIsInstance(actual, bytes)
        self.assertEqual(expected_length, len(actual))

        self.assertEqual(actual, encryptor.key)

    def test_generate_key_not_saving(self):
        """
        Tests of the method which let us generate a new key for the case that
        we don't want to propagate the new key into the object.
        """

        expected_length = 32

        encryptor = FileEncryption()

        actual = encryptor.generate_key(save=False)

        self.assertIsInstance(actual, bytes)
        self.assertEqual(expected_length, len(actual))

        self.assertNotEqual(actual, encryptor.key)

    def test_generate_iv(self):
        """
        Tests of the method which let us generate a new iv.
        """

        expected_length = 16

        encryptor = FileEncryption()

        actual = encryptor.generate_iv(save=True)

        self.assertIsInstance(actual, bytes)
        self.assertEqual(expected_length, len(actual))

        self.assertEqual(actual, encryptor.iv)

    def test_generate_iv_not_saving(self):
        """
        Tests of the method which let us generate a new iv for the case that
        we don't want to propagate the new iv into the object.
        """

        expected_length = 16

        encryptor = FileEncryption()

        actual = encryptor.generate_iv(save=False)

        self.assertIsInstance(actual, bytes)
        self.assertEqual(expected_length, len(actual))

        self.assertNotEqual(actual, encryptor.iv)

    def test_file_content_encryption(self):
        """
        Tests of the method which let us encrypt a given file content
        (or string/bytes).
        """

        given = "Hello, World!"
        expected = b"Hello, World!"

        encryptor = FileEncryption()
        encryptor.set_key(self.encryption_key)
        encryptor.set_iv(self.iv_key)

        actual = encryptor.encrypt_file_content(given)

        self.assertNotEqual(given, actual)

        actual = encryptor.decrypt_file_content(actual)

        self.assertEqual(expected, actual)

    def test_file_encryption_no_key_given(self):
        """
        Tests of the method which let us encrypt a given file content for the
        case that no key is given.
        """

        expected_key_length = 32
        expected_iv_length = 16

        given = "Hello, World!"
        expected = b"Hello, World!"

        encryptor = FileEncryption()

        actual = encryptor.encrypt_file_content(given)

        self.assertNotEqual(given, actual)
        self.assertIsNotNone(encryptor.key)
        self.assertIsNotNone(encryptor.iv)

        self.assertEqual(expected_key_length, len(encryptor.key))
        self.assertEqual(expected_iv_length, len(encryptor.iv))

        actual = encryptor.decrypt_file_content(actual)

        self.assertEqual(expected, actual)

    def test_bytes_file_content_encryption(self):
        """
        Tests of the method which let us encrypt a given file content
        (or string/bytes).
        """

        given = b"Hello, World!"
        expected = b"Hello, World!"

        encryptor = FileEncryption()
        encryptor.set_key(self.encryption_key)
        encryptor.set_iv(self.iv_key)

        actual = encryptor.encrypt_file_content(given)

        self.assertNotEqual(given, actual)

        actual = encryptor.decrypt_file_content(actual)

        self.assertEqual(expected, actual)

    def test_file_content_decryption_not_bytes(self):
        """
        Tests of the method which let us decrypt a previously encrypted
        file content for the case that the given content is not a bytes.
        """

        given = "Hello, World!"

        encryptor = FileEncryption()
        encryptor.set_key(self.encryption_key)
        encryptor.set_iv(self.iv_key)

        actual = encryptor.encrypt_file_content(given)

        self.assertNotEqual(given, actual)

        self.assertRaises(
            ValueError, lambda: encryptor.decrypt_file_content(actual.hex())
        )

    def test_file_content_decryption_no_key_given(self):
        """
        Tests of the method which let us decrypt a previously encrypted
        file content for the case that no key is given.
        """

        given = "Hello, World!"

        encryptor = FileEncryption()

        self.assertRaises(ValueError, lambda: encryptor.decrypt_file_content(given))

    def test_file_content_decryption_no_iv_given(self):
        """
        Tests of the method which let us decrypt a previously encrypted file
        content for the case that no iv is given.
        """

        given = "Hello, World!"

        encryptor = FileEncryption()
        encryptor.set_key(self.encryption_key)

        self.assertRaises(ValueError, lambda: encryptor.decrypt_file_content(given))

    def test_file_encryption(self):
        """
        Tests of the method which let us encrypt a file object.
        """

        given = b"Hello, World!"
        expected = b"Hello, World!"

        input_file = NamedTemporaryFile()
        output_file = NamedTemporaryFile()
        decrypted_file = NamedTemporaryFile()

        input_file.write(given)

        encryptor = FileEncryption()
        encryptor.set_key(self.encryption_key)
        encryptor.set_iv(self.iv_key)

        input_file.seek(0)
        encryptor.encrypt_file(input_file, output_file)

        self.assertTrue(os.path.exists(input_file.name))
        self.assertTrue(os.path.exists(output_file.name))

        output_file.seek(0)

        encryptor.decrypt_file(output_file, decrypted_file)

        decrypted_file.seek(0)

        self.assertEqual(expected, decrypted_file.read())


if __name__ == "__main__":
    launch_tests()
