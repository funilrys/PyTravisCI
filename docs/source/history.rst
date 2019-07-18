History
=======

While working on the monitoring and automation tool (private source code) for the `Ultimate-Hosts-Blacklist`_ and `Dead-Hosts`_ infrastructure which I manage,
I constantly need to interact with the Travis CI infrastructure - so implicitly its API.

And unfortunaly, I could make `The Travis Client`_ work on my (new) machine.

So, as the automation tool itself is written in Python and I could not find any tool which could fit my needs or simplify the way to communicate and/or interpret the response of
the Travis CI API V3, I wrote my own.

Therefore, please keep in mind that this project was mainly developed for my needs while developing the infrastructures of `Ultimate-Hosts-Blacklist`_ and/or `Dead-Hosts`_.


.. _Ultimate-Hosts-Blacklist: https://github.com/Ultimate-Hosts-Blacklist
.. _Dead-Hosts: https://github.com/dead-hosts
.. _The Travis Client: https://github.com/travis-ci/travis.rb