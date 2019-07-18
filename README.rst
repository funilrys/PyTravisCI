PyTravisCI - Another Travis CI (Python) API client
==================================================

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


Documentation as the place to be!
---------------------------------

Want to know more about PyTravisCI? We invite you to read `the documentation`_.

Want a local copy? We get you covered!

Simply run the following and enjoy our documentation!

::

    $ cd docs/
    $ make html
    $chromium _build/html/index.html # Chromium or whatever browser you use.

.. _the documentation: https://pytravisci.readthedocs.io/en/latest/

Why is there a lack of tests?
-----------------------------

If you read what I wrote previously, I said:

    It has been meant to fit my needs but I hope that it will be useful to others.

which means that I use this project manually at least once a week and automated
almost every day.

It was not my priority to write the tests for each resource types. But if you have
time, your PR is welcome!

License
-------

::

    MIT License

    Copyright (c) 2019 Nissar Chababy

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

