PyTravisCI - Just another Travis CI (API) Python interface
==========================================================

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

Just another Travis CI (API) Python interface.
It has been meant to fit my needs but in hope that it will be useful to others.

In other words, PyTravisCI gives us a Python interface to interact with the
the `Travis API v3`_ or the Travis CI Infrastructure.

It can interact with repositories, jobs, build and almost everything the Travis
CI API v3 has to offer.

It can also helps you with the encryption of information and files.
Give the interface a variable name and its value and it will gives you what
you are supposed to write into your :code:`.travis.yml` configuration file.
Same with the encryption of files.

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

.. toctree::
   :maxdepth: 2
   :caption: Getting started

   history
   installation
   update

.. toctree::
   :maxdepth: 2
   :caption: Usage

   usage/index

.. toctree::
   :maxdepth: 2
   :caption: Code Documentation

   code/api
   code/resource_types/index
   code/encryption/index

   code/exceptions
   code/standardization
   code/requester

   code/communicator/index


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
