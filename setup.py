"""
Just another Travis CI (Python) API client.

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

from re import compile as comp
from unittest import TestLoader

from setuptools import setup

PACKAGE_NAME = "PyTravisCI"


def test_suite():
    """
    Discover the tests.
    """

    test_loader = TestLoader()
    discovered_tests = test_loader.discover("tests", pattern="test_*.py")

    return discovered_tests


def get_requirements():
    """
    Extract all requirements from requirements.txt.
    """

    with open("requirements.txt") as file:
        requirements = file.read().splitlines()

    return requirements


def get_version():
    """
    Extract the version from {PACKAGE_NAME}/__init__.py
    """

    to_match = comp(r'VERSION\s=\s"(.*)"\n')

    with open(f"{PACKAGE_NAME}/__init__.py", encoding="utf-8") as file_stream:
        extracted = to_match.findall(file_stream.read())[0]

    return ".".join([x for x in extracted.split(".") if x.isdigit()])


def get_long_description():
    """
    Extract the long description from README.rst.
    """

    return open("README.rst", encoding="utf-8").read()


if __name__ == "__main__":
    setup(
        name=PACKAGE_NAME,
        version=get_version(),
        python_requires=">=3.6, <4",
        install_requires=get_requirements(),
        description="Just another Travis CI (Python) API client.",
        long_description=get_long_description(),
        author="funilrys",
        author_email="contact@funilrys.com",
        license="MIT",
        url="https://github.com/funilrys/PyTravisCI",
        platforms=["any"],
        packages=[PACKAGE_NAME, f"{PACKAGE_NAME}.resource_types"],
        keywords=["Travis CI", "Travis", "CI", "API"],
        classifiers=[
            "Environment :: Console",
            "Topic :: Internet",
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
        ],
        test_suite="setup.test_suite",
    )
