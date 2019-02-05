##################
racket      |pic1|
##################

.. |pic1| image:: docs/images/table-tennis_60px.png
    :width: 40px


.. image:: https://travis-ci.org/carlomazzaferro/racket.svg?branch=master
    :target: https://travis-ci.org/carlomazzaferro/racket

.. image:: https://img.shields.io/pypi/v/racket.svg
    :target: https://pypi.python.org/pypi/racket

.. image:: https://readthedocs.org/projects/racket/badge/?version=latest
    :target: https://racket.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
                
.. image:: https://coveralls.io/repos/github/carlomazzaferro/racket/badge.svg?branch=master
    :target: https://coveralls.io/github/carlomazzaferro/racket?branch=master
    :alt: Coverage

.. image:: https://pepy.tech/badge/racket
     :target: https://pepy.tech/badge/racket
     :alt: Downloads



Serve models with confidence.


* Free software: GNU General Public License v3
* Documentation: https://racket.readthedocs.io/en/latest/


Overview
--------

Let's face it. Building models is already challenging enough. But putting them into production is
usually a big enough challenge to grant the employment of an entire separate team. The goal of
the project is removing (or at least softening) the dependency on machine learning engineers and devops,
enabling data scientist to go from concept to production in minutes.

.. note:: **STATUS**: alpha. Active development, but breaking changes may come.

Presented at PyData: video_, slides_

.. _video: https://www.youtube.com/watch?v=AVj3G2MbjOM
.. _slides: https://www.slideshare.net/PyData/restful-machine-learning-with-flask-and-tensorflow-serving-carlo-mazzaferro

Features
--------

* Easy integration with TensorFlow Serving and Keras
* RESTful interface with interactive Swagger documentation
* Model introspection: ability to view model performance and input requirements
* Ability to deploy automatically different models with a single command
* Rich CLI capabilities, going from project scaffolding to training, serving, and dashboarding
* Small codebase, statically typed with mypy, and extensive docstrings
* **Coming Soon** :sup:`TM`: Web-ui for managing, introspecting, and deploying models.



.. _DemoVideo:


Demo
----


.. image:: https://asciinema.org/a/pqGkxdzvGRzmKG8SZ7q35WvJW.svg
    :target: https://asciinema.org/a/pqGkxdzvGRzmKG8SZ7q35WvJW?autoplay=1


Roadmap
-------

* Web dashboard for model management and introspection
* Support for Pytorch using ONNX
* Path to production: docker-based deployments to major cloud providers
* Security capabilities with SSL encryption



Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

The icon was created by smashicons_.

.. _smashicons: https://www.flaticon.com/authors/smashicons
