PyTravisCI - Just another Travis CI (Python) API client.
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
and was meant to be used as an imported module than something else.

It has nothing to do with `the ruby version of the Travis client`_ and
will never have similarities
(except maybe if one develops a CLI out of this) with it.


.. _V3 of the Travis API: https://developer.travis-ci.org/
.. _the ruby version of the Travis client: https://github.com/travis-ci/travis.rb

.. toctree::
   :maxdepth: 2
   :caption: Getting started

   history
   installation
   update
   usage

.. toctree::
   :maxdepth: 2
   :caption: Code Documentation

   code/api
   code/communication
   code/configuration
   code/encryption
   code/exceptions
   code/standardize

.. toctree::
   :maxdepth: 2
   :caption: Resource Types Documentation

   code/resource_types/todo
   code/resource_types/not_implemented
   code/resource_types/development
   code/resource_types/active
   code/resource_types/branch
   code/resource_types/branches
   code/resource_types/broadcasts
   code/resource_types/build
   code/resource_types/builds
   code/resource_types/caches
   code/resource_types/cron
   code/resource_types/crons
   code/resource_types/env_var
   code/resource_types/env_vars
   code/resource_types/job
   code/resource_types/jobs
   code/resource_types/key_pair_generated
   code/resource_types/log
   code/resource_types/organization
   code/resource_types/organizations
   code/resource_types/owner
   code/resource_types/repositories
   code/resource_types/repository
   code/resource_types/setting
   code/resource_types/settings
   code/resource_types/user


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
