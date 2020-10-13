Initialization
--------------

There is 4 way to get started, but 1 gateway.

1. Without any token.
2. With a token from https://travis-ci.org (for public GitHub repositories)
3. With a token from https://travis-ci.com (private GitHub repositories)
4. With a token from an enterprise domain (e.g https://example.org/)

The gateway of all the mechanism is the :class:`~PyTravisCI.travis_ci.TravisCI`
object. From there, you can start to navigate through the Travis CI API.

Without any token
"""""""""""""""""

::

    from PyTravisCI import TravisCI

    travis = TravisCI()

With a token from travis-ci.org
"""""""""""""""""""""""""""""""

::

    from PyTravisCI import TravisCI

    travis = TravisCI(access_token="XYZ")

With a token from travis-ci.com
"""""""""""""""""""""""""""""""

::

    from PyTravisCI import defaults, TravisCI

    travis = TravisCI(
        access_token="XYZ", access_point=defaults.access_points.PRIVATE
    )

With a token from an enterprise domain
""""""""""""""""""""""""""""""""""""""

::

    from PyTravisCI import defaults, TravisCI

    travis = TravisCI(
        access_token="XYZ", access_point=defaults.access_points.ENTERPRISE.format("example.org")
    )
