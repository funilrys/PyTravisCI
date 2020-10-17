Examples
--------

You are invited to look at the resource types objects in order to get the method
and attributes you look for.

In this section we present some example which may be asked a lot in issues.
If we are missing some or if you have some questions, let me know per issue!

.. warning::
    This section may be unuseful if you don't know how to interact with
    resource type objects.

Information of the current user
"""""""""""""""""""""""""""""""

::

    from PyTravisCI import TravisCI

    # We initiate our "communication" object.
    travis = TravisCI(acces_token="XYZ")

    # We get the current user information.
    me = travis.get_user()

    print(me.json())

Repositories of the current user
""""""""""""""""""""""""""""""""

::

    from PyTravisCI import TravisCI

    # We initiate our "communication" object.
    travis = TravisCI(acces_token="XYZ")

    # We get the initial list of Repositories
    repositories = travis.repositoris()

    while True:
        # We loop until there is no more page to navigate.

        for repository in repositories:
            print(repository.json())

        if repositories.has_next_page():
            repositories = repositories.next_page()
            continue
        break

Organizations of the current user
"""""""""""""""""""""""""""""""""

::

    from PyTravisCI import TravisCI

    # We initiate our "communication" object.
    travis = TravisCI(acces_token="XYZ")

    # We get the jobs.
    organizations = travis.get_organizations()

    while True:
        # We loop until there is no more page to navigate.

        for organization in organizations:
            print(organization.json())

        if organizations.has_next_page():
            organizations = organizations.next_page()
            continue
        break

Active builds of the current user
"""""""""""""""""""""""""""""""""

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

    while True:
        # We loop until there is no more page to navigate.

        for active_build in active_builds:
            print(active_build.json())

        if active_build.has_next_page():
            active_builds = active_builds.next_page()
            continue
        break


Builds of the current user
""""""""""""""""""""""""""

::

    from PyTravisCI import TravisCI

    # We initiate our "communication" object.
    travis = TravisCI(acces_token="XYZ")

    # We get the builds.
    builds = travis.get_builds()

    while True:
        # We loop until there is no more page to navigate.

        for build in builds:
            print(build.json())

        if builds.has_next_page():
            builds = builds.next_page()
            continue
        break


Jobs of the current user
""""""""""""""""""""""""

::

    from PyTravisCI import TravisCI

    # We initiate our "communication" object.
    travis = TravisCI(acces_token="XYZ")

    # We get the jobs.
    jobs = travis.get_jobs()

    while True:
        # We loop until there is no more page to navigate.

        for job in jobs:
            print(job.json())

        if jobs.has_next_page():
            jobs = jobs.next_page()
            continue
        break

Restart the last build of a repository
""""""""""""""""""""""""""""""""""""""

::

    from PyTravisCI import TravisCI

    # We initiate our "communication" object.
    travis = TravisCI(acces_token="XYZ")

    # We get the repository that interests us.
    repository = travis.get_repository("funilrys/PyTravisCI")
    # We get the build that interrest us (the latest one is always the first one).
    build = repository.get_builds()[0]

    try:
        build.restart()
    except PyTravisCI.exceptions.BuildAlreadyStarted:
        # We really want to start so, we cancel it first.
        build.cancel()
        time.sleep(0.5)
        build.restart()

    while build.is_active(sync=True):
        print("Build is running...")

        time.sleep(5)

    print("Build finished!")

Lint a configuration file
"""""""""""""""""""""""""

::

    from PyTravisCI import TravisCI

    # We initiate our "communication" object.
    travis = TravisCI(acces_token="XYZ")

    with open(".travis.yml", "r") as file_stream:
        for index, warning in enumerate(travis.lint(file_stream)):
            if index > 0:
                print("*" * 100)

            print(
                f"{index + 1}. WARNING ({warning.warning_type}):\n"
                f"MESSAGE:\n\n{warning.message}\n\n"
            )

Create a new (build) request
""""""""""""""""""""""""""""

::

    from PyTravisCI import TravisCI

    # We initiate our "communication" object.
    travis = TravisCI(acces_token="XYZ")

    # Let's get the repository to work with.
    repository = travis.get_repository("funilrys/PyTravisCI")

    # Let's create a new request.
    print(
        repository.create_request(
            "Hello, this request was created with PyTravisCI", "master"
        ).json()
    )

Encrypt global environment variables for our configuration files
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Travis allow us to directly give is a new environment variable.
But we may want our environment variable to be encrypted into
our configuration file.

Here is an example which show you how to get the encrypted string to put into
your configuration file.

::

    from PyTravisCI import TravisCI

    # We initiate our "communication" object.
    travis = TravisCI(acces_token="XYZ")

    # Let's get the repository we want to work with.
    repository = travis.get_repository("funilrys/PyTravisCI")

    # This is what we are going to encrypt.
    # one decrypted by TravisCI it will produces:
    #
    #   $ export HELLO=[secure]
    #   $ export WORLD=[secure]
    #
    env_vars = {"HELLO": "world", "WORLD": "hello"}

    # We now encrypt the shell environment variable:
    #   HELLO=world
    encrypte_vars = repository.encrypt_env_var(env_vars)

    print(
        "Please append the following into the global environment variables "
        "section of your configuration file:"
    )

    for encrypted_var in encrypte_vars:
        print(f"- secure: \"{encrypted_var['secure']}\"\n\n")

Encrypt file
""""""""""""

You may want to encrypt a file for a repository.
This is what we will do in this example.

In this example, we have an off git file which is called :code:`id_rsa`.
We want to use it in our build process, so we will encrypt it into
:code:`id_rsa.enc` which will be then pushed to the repository.

PyTravisCI can generate the :code:`id_rsa.enc` file for you but you will have
to manually write the command to decrypt it. But don't be stressed out,
PyTravisCI will give you the command to run.

Here is an example which show you how to get help with the encryption of secret
files.

::

    from PyTravisCI import TravisCI

    # We initiate our "communication" object.
    travis = TravisCI(acces_token="XYZ")

    # Let's get the repository we want to work with.
    repository = travis.get_repository("funilrys/PyTravisCI")

    with open("id_rsa", "rb") as secret_file, open(
        "id_rsa.enc", "wb"
    ) as encrypted_secret_file:

        information = repository.encrypt_file(secret_file, encrypted_secret_file)

        print(
            "Please append the following into the script section of "
            "your configuration file:\n\n"
            f"{information['command']}"
        )

Encrypt secrets
"""""""""""""""

You may need to encrypt your/a password that you need to write into
your configuration file for the deployment.
This is what we will do in this example.

::

    from PyTravisCI import TravisCI

    # We initiate our "communication" object.
    travis = TravisCI(acces_token="XYZ")

    # Let's get the repository we want to work with.
    repository = travis.get_repository("funilrys/PyTravisCI")

    # Let's get our password :-)
    password = "HeLlOW0rLd!"

    # Let's encrypt our passowrd
    encrypted_password = repository.encrypt_secrets([password])[0]

    print(f'Here is your encrypted password:\n\n"{encrypted_password}"')
