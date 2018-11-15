#########
Concepts
#########

The project is built with the premise of getting to a working prototype quickly without
sacrificing flexibility.

This is achieved by leveraging the full capabilities of TFS while enabling the user to interact
with a simple, expressive API.


Model Versioning
================

TFS has as one of its features model discovery. Namely, if a new model gets persisted in the directory where models
have been specified to live (done usually in a Docker file (see `here  <https://github.com/carlomazzaferro/racket/blob/master/example/Dockerfile#L45>`_
for more details), and the subdirectory of the model path has a number strictly greater than the existing folders,
it will automatically load it.

Although useful, this formulation is clearly quite inflexible. If you want to modify the discovery scheme, you'd have to
fiddle with TFS's `C++ API <https://www.tensorflow.org/serving/api_docs/cc/>`_. If instead you'd like to roll back models,
you may have to create a new directory or modify the existing ones.

Racket instead abstracts away TFS the versioning schematics and allows the user to simply define the model version
when instantiating a new model, while allowing the user to any specific version with a single cli command.

Model versions in racket follow semantic versioning and are supplied to it as strings.

Learners
========

Apart from the CLI and the RESTful access layer, most of the public API revolves around the Learner set of classes.
These essentially define the patterns of interaction between the code that generates the models and the filesystem/database.

The idea is letting the user define the core of their needs (i.e., the learner's architecture) while getting for free
the storage, versioning, and serving capabilities.

A Word on Persistence
=====================

The project relies heavily on `SQLAlchemy <http://flask-sqlalchemy.pocoo.org/2.3/>`_ to manage model metadata. I've found
it to greatly reduce complexity when managing a relatively high number of models, as it makes it extremely easy to query
for, and reason about the existing models. As a default, the project will use SQLite as its default data store, but that
can be changed very easily by changing the configuration and specifying a database backend in the ``racket.yaml`` file, which
gets generated automatically once the ``racket init`` command gets called.






