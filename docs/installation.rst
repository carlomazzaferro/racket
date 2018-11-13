.. highlight:: shell

============
Installation
============

Requirements
------------

``racket`` is tested on python 3.6. It won't work in 3.7, as there is no TensorFlow release for
this python version, and it probably won't work either on 3.5 since I use f-strings extensively.

Contributions are more than welcome to make the project compatible with other python versions!

``docker`` and ``docker-compose`` are also required. Reasonably up-to-date versions should suffice.


Stable release
--------------

To install racket, run this command in your terminal:

.. code-block:: console

    $ pip install racket

This is the preferred method to install racket, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
------------

The sources for racket can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/carlomazzaferro/racket

Or download the `tarball`_:

.. code-block:: console

    $ curl  -OL https://github.com/carlomazzaferro/racket/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://github.com/carlomazzaferro/racket
.. _tarball: https://github.com/carlomazzaferro/racket/tarball/master
