#####
Usage
#####

While the Demo_ provides a quick overview of the functionality of ``racket``,
this document will explain in detail the steps of the demo, and provide resources to learn more
about the inner workings of the project.


.. _Demo: https://asciinema.org/a/dinc7mQrUfO2JqFhV3iyYllIc

**********************
Starting a New Project
**********************


From the command-line::

    racket init --name project-name --path path/to/directory

Will create a directory named ``project-name`` in the the specified path with all the required files to
start serving models. Of particular note, the directory will have the following files::

    docker-compose.yaml
    Dockerfile
    racket.yaml
    classification.py
    .gitignore

To start TensorFlow Serving (TFS), run::

    docker-compose up --build

Add the ``-d`` flag if you'd like to run it on the background.


************************
Serving Your First Model
************************

To create a new model, you can edit the ``classification.py`` file. It define very basic Keras models,
but they have a few quirks. Namely, the class definition inherits from the class\ :class:`racket.KerasLearner`, which provides
built in functionality to store models in a suitable format for TFS, as well as functionality to store metadata and
historical scores of the model. The method\ :meth:`racket.KerasLearner.store` is responsible for this functionality.


The ``KerasLearner`` Base Class
===============================

In order to user the class as your base class, when you create a class that inherits from it you must
define a few things. Namely, it must have the following attributes and methods implemented:

Required attributes:

* ``VERSION``: a string of the form ``'major.minor.patch'``
* ``MODEL_TYPE``: a string specifying what kind of model it is (e.g. a regression or classification) a string specifying the model's name
* ``MODEL_NAME``: a string specifying the model's name

Required methods:

* ``fit(x, y, x_val, y_val, *args, **kwargs)``: a method that specifies how to fit the model
* ``build_model()``: a method that specifies how to compile the model

That's all. Having done that, you can call ``fit()`` as you normally would, after which
you can call ``store()``, which will take care of all the wiring needed to version, serve, serialize,
and expose the model.


Refer to\ :class:`racket.KerasLearner` for more information about the inner workings of the methods
implemented, and how the inner workings are leveraged to interact with TFS


Examples
========

We also provide a set of example projects with widely used models that
are ready to be used. See the examples_ folder for more information
on how to get some existing models up and running quickly.


.. _examples:  https://github.com/carlomazzaferro/racket/tree/master/examples
