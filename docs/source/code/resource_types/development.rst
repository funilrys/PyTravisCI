Development
==============

New RT
------

Here is a short list of things to think of while developing a new resource type.

1. Resource types are children of :class:`~PyTravisCI.communication.Communication`.

    This give us all the tools for the communication with the Travis CI API.

2. Resource types should be callable from :class:`~PyTravisCI.TravisCI`.

    That means that an endpoint and its "short" documentation should be created out there.

3. URL to communicate with should be constructted with :meth:`~PyTravisCI.communication.Communication.bind_path_name_to_access_point`
   and assigned to a variable called :code:`self._endpoint_url`.

    By design every communication methods will look for that :code:`self._endpoint_url`.

    I choosed to work like that in order to simplify the way the communciation is handled and made.

4. While developing states or action methods, :code:`self.___standard_enpoint_url` should be used to
   save the constructed :code:`self._endpoint_url`.

    As we mostly follow the next page of a request, this allow us to still have a record of the
    initialy called :code:`self._endpoint_url`.

5. The resource types class should have a :code:`__path_name_base__` attribute with the main endpoint.

    What is meant is if we have the following endpoint to call :code:`hello/world/its_funilrys`,
    :code:`__path_name_base__` will have the value :code:`hello`.

6. Always use the exceptions listed into :code:`~PyTravisCI.exception`.

7. Always use the :code:`self.standardize` attribute after you get a response from the API and before you work with the response.

    As we may want to work with the standardize version of some index, this is highly needed.

8. Avoid import for cross resource type call, use :code:`self._root` instead.

    As all resource types are available into :class:`~PyTravisCI.TravisCI`, we use it (as :code:`self._root`)
    to make cross resource type call.
