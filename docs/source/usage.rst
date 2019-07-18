Usage
=====

As an imported module
---------------------

You'll need your TravisCI API token which you can find in one of the following URL.

- https://travis-ci.org/account/preferences
- https://travis-ci.com/account/preferences


Please report to the API and resource types documentation for details about available
methods and attributes/variables.

::

    from PyTravisCI import TravisCI

    t = TravisCI(token="XYZ")

    # Let's get the information of the current user.
    user = t.user()
    print("Name:", user.name)  # Give us the name of the current user.
    print("Name:", user["name"])  # Give us the name of the current user.
    print("Login:", user.login)  # Give us the login of the current user.

    # Let's get the list of organizations I'm into
    orgs = t.organizations()

    # As you can see, it is a generator.
    print("Organizations:", orgs.organizations)

    i = 1
    # Let's consume the content the generator
    for org in orgs.organizations:
        print(f"Organization Name {i}:", org.name)

        i += 1

    # Let's get the list of repo I own/administrate.
    repos = t.repositories()

    # As you can see, it is also a generator.
    print(repos.repositories)

    i = 1
    # Let's consume the content the generator
    for repo in repos.repositories:
        print(f"Repo {i}:", repo.slug)

        i += 1
