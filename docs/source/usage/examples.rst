Examples
--------

You are invited to look at the resource types objects in order to get the method
and attributes you look for.

In this section we present some example which may be asked a lot in issues.
If we are missing some or if you have some questions, let me know per issue!

.. warning::
    This section may be unuseful if you don't know how to interact with
    resource type objects.

List of active builds of the current user
"""""""""""""""""""""""""""""""""""""""""

.. note::
    Active builds are build which are builds which have the state
    :code:`pending` or :code:`started`.

::

    from PyTravisCI import TravisCI

    # We initiate our "communication" object.
    travis = TravisCI(acces_token="XYZ")

    # We get the current user information.
    me = travis.get_user()

    # We can now get the list of active builds.
    active_builds = me.get_active()

    # We can loop over each provided builds too.
    for build in active_builds:
        print(build)
