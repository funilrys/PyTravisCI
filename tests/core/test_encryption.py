"""
Just another Travis CI (Python) API client.

Test of the encryption class.

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

from base64 import b64decode
from unittest import TestCase
from unittest import main as launch_test

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.padding import MGF1, OAEP, PKCS1v15
from cryptography.hazmat.primitives.asymmetric.rsa import generate_private_key
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from PyTravisCI.encryption import Encryption


class TestEncryption(TestCase):
    """
    Test of :class:`PyTravisCI.encryption.Encryption`.
    """

    RSA_EXPONENT = 65537
    """
    The public exponent to use.
    """

    KEY_SIZE = 2048
    """
    The size of the keys to generate.
    """

    def setUp(self):
        """
        Provide everything needed for the test.
        """

        self.private_key = generate_private_key(
            self.RSA_EXPONENT, self.KEY_SIZE, backend=default_backend()
        )
        public_key = self.private_key.public_key()

        self.public_key = public_key.public_bytes(
            encoding=Encoding.PEM, format=PublicFormat.SubjectPublicKeyInfo
        )

        self.envs = {"hello": "word", "world": "hello world", "break it": "hehe"}
        self.secrets = ["hello", "world", "this", "is", "my", "secret"]
        self.password = ":".join(self.secrets)

    def test_encrypt_pkcs1v15_mode_env_var(self):
        """
        Test of :class:`PyTravisCI.encryption.Encryption.encrypt` with
        the :code:`pkcs1v15_mode` mode activated.
        """

        actual = Encryption(self.envs, self.public_key).encrypt(pkcs1v15_mode=True)

        for encrypted in actual:
            self.assertIn("secure", encrypted, "No `secure` index given.")

            to_decrypt = b64decode(encrypted["secure"].encode("ASCII"))
            decrypted = self.private_key.decrypt(to_decrypt, PKCS1v15()).decode()

            self.assertIn(
                "=", decrypted, "Environment variable not correctly encrypted."
            )

            env_name, value = decrypted.replace('"', "").replace("_", " ").split("=")

            self.assertEqual(
                self.envs[env_name],
                value,
                "Environment variable not correctly encrypted.",
            )

    def test_encrypt_oeap_mode_env_var(self):
        """
        Test of :class:`PyTravisCI.encryption.Encryption.encrypt` with
        the :code:`oeap_mode` mode activated.
        """

        actual = Encryption(self.envs, self.public_key).encrypt(
            oeap_mode=True, pkcs1v15_mode=False
        )

        for encrypted in actual:
            self.assertIn("secure", encrypted, "No `secure` index given.")

            to_decrypt = b64decode(encrypted["secure"].encode("ASCII"))
            decrypted = self.private_key.decrypt(
                to_decrypt,
                OAEP(mgf=MGF1(algorithm=SHA256()), algorithm=SHA256(), label=None),
            ).decode()

            self.assertIn(
                "=", decrypted, "Environment variable not correctly encrypted."
            )

            env_name, value = decrypted.replace('"', "").replace("_", " ").split("=")

            self.assertEqual(
                self.envs[env_name],
                value,
                "Environment variable not correctly encrypted.",
            )

    def test_encrypt_pkcs1v15_mode_list_of_secrets(self):
        """
        Test of :class:`PyTravisCI.encryption.Encryption.encrypt` with
        the :code:`pkcs1v15_mode` mode activated.
        """

        actual = Encryption(self.secrets, self.public_key).encrypt(pkcs1v15_mode=True)

        for index, encrypted in enumerate(actual):
            to_decrypt = b64decode(encrypted.encode("ASCII"))
            decrypted = self.private_key.decrypt(to_decrypt, PKCS1v15()).decode()

            self.assertEqual(
                self.secrets[index], decrypted, "Secret not correctly encrypted."
            )

    def test_encrypt_oeap_mode_list_of_secrets(self):
        """
        Test of :class:`PyTravisCI.encryption.Encryption.encrypt` with
        the :code:`oeap_mode` mode activated.
        """

        actual = Encryption(self.secrets, self.public_key).encrypt(
            pkcs1v15_mode=False, oeap_mode=True
        )

        for index, encrypted in enumerate(actual):
            to_decrypt = b64decode(encrypted.encode("ASCII"))
            decrypted = self.private_key.decrypt(
                to_decrypt,
                OAEP(mgf=MGF1(algorithm=SHA256()), algorithm=SHA256(), label=None),
            ).decode()

            self.assertEqual(
                self.secrets[index], decrypted, "Secret not correctly encrypted."
            )

    def test_encrypt_pkcs1v15_mode_password(self):
        """
        Test of :class:`PyTravisCI.encryption.Encryption.encrypt` with
        the :code:`pkcs1v15_mode` mode activated.
        """

        actual = Encryption(self.password, self.public_key).encrypt(pkcs1v15_mode=True)

        to_decrypt = b64decode(actual.encode("ASCII"))
        decrypted = self.private_key.decrypt(to_decrypt, PKCS1v15()).decode()

        self.assertEqual(self.password, decrypted, "Password not correctly encrypted.")

    def test_encrypt_oeap_mode_password(self):
        """
        Test of :class:`PyTravisCI.encryption.Encryption.encrypt` with
        the :code:`oeap_mode` mode activated.
        """

        actual = Encryption(self.password, self.public_key).encrypt(
            pkcs1v15_mode=False, oeap_mode=True
        )

        to_decrypt = b64decode(actual.encode("ASCII"))
        decrypted = self.private_key.decrypt(
            to_decrypt,
            OAEP(mgf=MGF1(algorithm=SHA256()), algorithm=SHA256(), label=None),
        ).decode()

        self.assertEqual(self.password, decrypted, "Password not correctly encrypted.")


if __name__ == "__main__":
    launch_test()
