PyTravisCI - Just another Travis CI (API) Python interface.
========================================================

.. image:: https://travis-ci.com/funilrys/PyTravisCI.svg?branch=master
    :target: https://travis-ci.com/funilrys/PyTravisCI
.. image:: https://coveralls.io/repos/github/funilrys/PyTravisCI/badge.svg?branch=master
    :target: https://coveralls.io/github/funilrys/PyTravisCI?branch=master
.. image:: https://api.codacy.com/project/badge/Grade/a7952fe4bcd44c05aac6f1a1494fab0b
    :target: https://www.codacy.com/app/funilrys/PyTravisCI?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=funilrys/PyTravisCI&amp;utm_campaign=Badge_Grade
.. image:: https://img.shields.io/badge/code%20style-black-000000.png
    :target: https://github.com/ambv/black


PyTravisCI is just another Travis CI API client for Python.
It has been meant to fit my needs but I hope that it will be useful to others.

It can only communicate and interpret outputs of the `V3 of the Travis API`_
and was meant to be used as an imported module rather through a CLI.

It has nothing to do with `the ruby version of the Travis client`_ and
may never have similarities
(except maybe if one develops a CLI out of this) with it.


.. _V3 of the Travis API: https://developer.travis-ci.org/
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
