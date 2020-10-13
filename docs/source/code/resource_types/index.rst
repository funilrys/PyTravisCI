Resource Types
==============

Resource types are objects provides by the Travis CI API documentation.
For us, as developers they are our direct way to interact with their API.

Please keep in mind, that I built this tool to stay as close as possible
from the official documentation located at https://developer.travis-ci.org.
Most of the resource types are documented correctly but Travis CI will continue
its development cycle, there please take a look at their documentation from
time to time.

One of the rare things which was leaved undocumented are the :code:`params`.
Therefore, using this tool without the documentation while using the
:code:`params` argument may be a lost of time.

.. warning::
    I tried to make the attributes match the documentation. But with the time
    some may be missing. You are invited to report them per issue or
    pull request.

.. include:: not_implemented.rst
.. include:: base.rst
.. include:: active.rst
.. include:: beta_feature.rst
.. include:: beta_features.rst
.. include:: branch.rst
.. include:: branches.rst
.. include:: broadcast.rst
.. include:: broadcasts.rst
.. include:: build.rst
.. include:: builds.rst
.. include:: cache.rst
.. include:: caches.rst
.. include:: cron.rst
.. include:: crons.rst
.. include:: env_var.rst
.. include:: env_vars.rst
.. include:: installation.rst
.. include:: job.rst
.. include:: jobs.rst
.. include:: key_pair_generated.rst
.. include:: key_pair.rst
.. include:: lint.rst
.. include:: log.rst
.. include:: message.rst
.. include:: messages.rst
.. include:: organization.rst
.. include:: organizations.rst
.. include:: repositories.rst
.. include:: repository.rst
.. include:: setting.rst
.. include:: settings.rst
.. include:: stage.rst
.. include:: stages.rst
.. include:: user.rst