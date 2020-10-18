PyTravisCI - Just another Python API for Travis CI (API)
========================================================

.. image:: https://travis-ci.com/funilrys/PyTravisCI.svg?branch=master
    :target: https://travis-ci.com/funilrys/PyTravisCI
.. image:: https://coveralls.io/repos/github/funilrys/PyTravisCI/badge.svg?branch=master
    :target: https://coveralls.io/github/funilrys/PyTravisCI?branch=master
.. image:: https://api.codacy.com/project/badge/Grade/a7952fe4bcd44c05aac6f1a1494fab0b
    :target: https://www.codacy.com/app/funilrys/PyTravisCI?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=funilrys/PyTravisCI&amp;utm_campaign=Badge_Grade

---------------

.. image:: https://img.shields.io/badge/code%20style-black-000000.png
    :target: https://github.com/ambv/black
.. image:: https://img.shields.io/github/license/funilrys/PyTravisCI.png
    :target: https://github.com/funilrys/PyTravisCI/blob/master/LICENSE
.. image:: https://img.shields.io/pypi/v/PyTravisCI.png
    :target: https://pypi.org/project/PyTravisCI
.. image:: https://img.shields.io/github/issues/funilrys/PyTravisCI.png
    :target: https://github.com/funilrys/PyTravisCI/issues

---------------

.. image:: https://pepy.tech/badge/PyTravisCI/week
    :target: https://pepy.tech/project/pyfunceble
.. image:: https://pepy.tech/badge/PyTravisCI/month
    :target: https://pepy.tech/project/PyTravisCI
.. image:: https://pepy.tech/badge/PyTravisCI
    :target: https://pepy.tech/project/PyTravisCI

---------------

Just another Python API for Travis CI (API).
It has been meant to fit my needs but in hope that it will be useful to others.

In other words, PyTravisCI gives us a Python interface to interact with the
the `Travis API v3`_ or the Travis CI Infrastructure.

It can interact with repositories, jobs, build and almost everything the Travis
CI API v3 has to offer.

It can also helps you with the encryption of information and files.
Give the interface a variable name and its value and it will gives you what
you are supposed to write into your :code:`.travis.yml` configuration file.
Same with the encryption of files and the linting of your configuration files.

Please keep in mind that:

- this project was meant to be used as "an imported module" than something else.
- this project has nothing to do with `the ruby version of the Travis client`_
  and will never have similarities with it

  (except if someone develop a client on top this).

Hava a question ? Fill a new issue!

Have an issue ? Report it!

Have an improvement idea ? Submit a PR!

Every improvement and constructive discussions are welcome!

.. _Travis API v3: https://developer.travis-ci.org/
.. _the ruby version of the Travis client: https://github.com/travis-ci/travis.rb

Documentation as the place to be!
---------------------------------

Want to know more about PyTravisCI? We invite you to read `the documentation`_.

Want a local copy? We get you covered!

Simply run the following and enjoy our documentation!

::

    $ cd docs/
    $ make html
    $ chromium build/html/index.html # Chromium or whatever browser you use.

.. _the documentation: https://pytravisci.readthedocs.io/en/latest/

Why is there a lack of tests?
-----------------------------

Well, I don't know what you may call "lack" but I wrote (105!) tests for what I
think is important.

It was not my priority to write the tests for each resource types or
communicators. But if you have time, your PR is welcome!

License
-------

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

