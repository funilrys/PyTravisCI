Working with resource type objects
----------------------------------

Although resource types have some nice method to help you, PyTravisCI provides
you some other useful "helpers".

:py:class:`repr` representation
"""""""""""""""""""""""""""""""

If you :py:class:`print` a resource type, you will get the following format.

::

    <ResourceTypeClassName {... attributes ...} />

:py:class:`dict` representation
"""""""""""""""""""""""""""""""

You can at anytime get the :py:class:`dict` representation of a resource type
object.

::

    from PyTravisCI import TravisCI

    # We initiate our "communication" object.
    travis = TravisCI(acces_token="XYZ")

    # We get the list of repositories we have access to.
    # Note: we limit to 3 because we have much more!
    my_repositories = travis.get_repositories(params={"limit": 3})

    # We can now get the dict representation of our object.
    # The .dict() method is actually an alias to .to_dict()!
    print(my_repositories.dict())


JSON representation
"""""""""""""""""""

You can at anytime get the JSON representation of a representation of a
resource type object.

::

    from PyTravisCI import TravisCI

    # We initiate our "communication" object.
    travis = TravisCI(acces_token="XYZ")

    # We get the list of repositories we have access to.
    # Note: we limit to 3 because we have much more!
    my_repositories = travis.get_repositories(params={"limit": 3})

    # We can now get the dict representation of our object.
    # The .json() method is actually an alias to .to_json()!
    print(my_repositories.json())

Loop over collection of resources
"""""""""""""""""""""""""""""""""

Most of time, we may work with single entries or resources. But while working
with a collection of resource, you may want to loop over them.

Guess what ? You can do it here too!

.. warning::
    If the current resource type is not a collection a
    :py:class:`NotImplementedError` will be raised.

::

    from PyTravisCI import TravisCI

    # We initiate our "communication" object.
    travis = TravisCI(acces_token="XYZ")

    # We get the list of repositories we have access to.
    # Note: we limit to 3 because we have much more!
    my_repositories = travis.get_repositories(params={"limit": 3})

    for repository in my_repositories:
        print(repository.json())

Comparison of resource types
""""""""""""""""""""""""""""

You can easily compare 2 resource types object by checking if :code:`x == y`.
Where :code:`x` and :code:`y` are 2 resource type objects.

::

    from PyTravisCI import TravisCI

    # We initiate our "communication" object.
    travis = TravisCI(acces_token="XYZ")

    # We get a single repository
    my_repo = travis.get_repository("funilrys/PyTravisCI")

    # In this example because it is a collection we can directly access
    # a member of the collection through its position.
    # Or (most of time) you will have an attribute which held them.
    #
    # As presented here, we are accessing the same object in 2 different way.
    wanted_job = my_repo.get_builds().builds[0].jobs[0]
    wanted_job2 = my_repo.get_builds()[0].jobs[0]

    assert wanted_job == wanted_job2

Handling incomplete or minimal representation of a resource type
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Most of the time, Travis CI give us incomplete attributes which represents
a resource type but in its minimal representation. With PyTravisCI you can
directly get the complete representation directly.

Let's take our previous example.

::

    from PyTravisCI import TravisCI

    # We initiate our "communication" object.
    travis = TravisCI(acces_token="XYZ")

    # We get a single repository
    my_repo = travis.get_repository("funilrys/PyTravisCI")

    # In this example because it is a collection we can directly access
    # a member of the collection through its position.
    # Or (most of time) you will have an attribute which held them.
    #
    # As presented here, we are accessing the same object in 2 different way.

    # Both variables are minimal representation of the same job.
    wanted_job = my_repo.get_builds().builds[0].jobs[0]
    wanted_job2 = my_repo.get_builds()[0].jobs[0]

    assert wanted_job == wanted_job2

    if wanted_job2.is_incomplete():
        print(wanted_job.json())  # incomplete representation
        print("*" * 100)
        print(wanted_job2.get_complete().json())  # complete/standard representation


Next page of a resource type
""""""""""""""""""""""""""""

Most of the times, you will have to play with the pagging system of the Travis CI
API. We made it a bit simplier :-).

::

    from PyTravisCI import TravisCI

    # We initiate our "communication" object.
    travis = TravisCI(acces_token="XYZ")

    # We get the list of repositories we have access to.
    # Note: we limit to 3 because we have much more!
    my_repositories = travis.get_repositories(params={"limit": 3})

    while my_repositories.has_next_page():
        # We loop until we are sure there is no page (anymore).

        for repository in my_repositories:
            print(repository.json())

        my_repositories = my_repositories.next_page()

Last page of a resource type
""""""""""""""""""""""""""""

You can get the last page of a resource type too.

::

    from PyTravisCI import TravisCI

    # We initiate our "communication" object.
    travis = TravisCI(acces_token="XYZ")

    # We get the list of repositories we have access to.
    # Note: we limit to 3 because we have much more!
    my_repositories = travis.get_repositories(params={"limit": 3}).last_page()

    for repository in my_repositories:
        print(repository.json())

First page of a resource type
"""""""""""""""""""""""""""""

Sometime you are in a middle of a loop but for whatever reason, you want to go
back to the first page. It's possible too!

::

    from PyTravisCI import TravisCI

    # We initiate our "communication" object.
    travis = TravisCI(acces_token="XYZ")

    # We get the list of repositories we have access to.
    # Note: we limit to 3 because we have much more!
    my_repositories = travis.get_repositories(params={"limit": 3}).last_page()

    while my_repositories.has_next_page():
        # We loop until we are sure there is no page (anymore).

        funilrys_repo_found = False

        for repository in my_repositories:
            print(repository.json())
            if "funilrys" in repository.slug:
                funilrys_repo_found = True

        if not funilrys_repo_found:
            my_repositories = my_repositories.next_page()

    # Now we work from the first page :-)
    my_repositories = my_repositories.first_page()

Previous page of a resource type
""""""""""""""""""""""""""""""""

Sometime you want to loop backwards :-).

::

    from PyTravisCI import TravisCI

    # We initiate our "communication" object.
    travis = TravisCI(acces_token="XYZ")

    # We get the list of repositories we have access to.
    # Note: we limit to 3 because we have much more!
    my_repositories = travis.get_repositories(params={"limit": 3}).last_page()

    while my_repositories.has_previous_page():
        # We loop until we are sure there is no page (anymore).

        for repository in my_repositories:
            print(repository.json())

        my_repositories = my_repositories.previous_page()
