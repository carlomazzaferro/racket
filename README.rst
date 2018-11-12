======
racket
======

.. image:: https://travis-ci.com/carlomazzaferro/racket.svg?token=6AsKrC8jkbpeAsBBbVut&branch=master


.. image:: https://img.shields.io/pypi/v/racket.svg
        :target: https://pypi.python.org/pypi/racket

.. image:: https://readthedocs.com/projects/r-racket/badge/?version=latest
    :target: https://r-racket.readthedocs-hosted.com/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://pyup.io/repos/github/carlomazzaferro/racket/shield.svg
     :target: https://pyup.io/repos/github/carlomazzaferro/racket/
     :alt: Updates


Serve models with confidence.


* Free software: GNU General Public License v3
* Documentation: https://racket.readthedocs.io.


Overview
--------

Let's face it. Building models is already challenging enough. But putting them into production is
usually a big enough challenge to grant the employment of an entire separate team. The goal of
the project is removing (or at least softening) the dependency on machine learning engineers and devops,
enabling data scientist to go from concept to production in minutes.

.. note:: **STATUS**: early alpha. Active development, but breaking changes may come.

Features
--------

* Easy integration with TensorFlow Serving and Keras
* RESTful interface with interactive Swagger documentation
* Model introspection: ability to view model performance and input requirements
* Ability to deploy automatically different models with a single command
* Rich CLI capabilities, going from project scaffolding to training, serving, and dashboarding
* Small codebase, statically typed, and extensive docstrings
* **Coming Soon** :sup:`TM`: Web-ui for managing, introspecting, and deploying models.



.. _DemoVideo:

Demo
----

.. raw:: html

    <a href="https://asciinema.org/a/dinc7mQrUfO2JqFhV3iyYllIc?autoplay=1" target="_blank"><img src="https://asciinema.org/a/dinc7mQrUfO2JqFhV3iyYllIc.svg" width="835"/></a>

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
