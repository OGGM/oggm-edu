.. _technical_details:

Technical details
=================

We provide more information about the platform's internals for instructors and
contributors. Make sure you read :ref:`notebooks_howto` before going on!

The computing environments
--------------------------

The computing environments available via Binder are
`Docker containers <https://www.docker.com/resources/what-container>`_,
or "software capsules" that can be created, pushed and pulled online. We create
these containers using a few simple configuration files specifying the
software packages and python libraries we would like to used in OGGM-Edu.
These configurations files are found in this repository:
`<https://github.com/OGGM/oggm-edu-r2d>`_

Binder uses `repo2docker <https://repo2docker.readthedocs.io>`_ to build these
environments and stores them in a hidden database. Once built, they won't
be built again unless a new change is made to the ``oggm-edu-r2d``
repository.

We use the same principle to build images that can be used by your own
JupyterHub deployment, if you have one.
These images are available `here <https://hub.docker.com/r/oggm/oggm-edu-r2d>`_.
We use these in :ref:`oggm_hub`.

The notebooks
-------------

The notebooks are developped collaboratively. We welcome your input and
contributions! You will find the directory with all notebooks (educational and
tutorials) on GitHub: `<https://github.com/OGGM/oggm-edu-notebooks>`_


This website
------------

The content of this website is written within the `Sphinx <http://sphinx-doc.org/>`_
framework and is hosted on `ReadTheDocs <https://readthedocs.org>`_.

.. _oggm_hub:

OGGM's own jupyterhub (experimental)
------------------------------------

We are currently working on getting our own service to serve jupyter notebooks
to our users: this is called a `JupyterHub <https://jupyter.org/hub>`_ and
we run it in an experimental phase. The advantages over Binder are:

- more resources, faster launches
- user management
- persistent sessions (work can be saved between sessions and log-ins)

If you have a specific need for an OGGM hub service (e.g. for a class or a
workshop), :ref:`title_contact` and we'll see what we can do.
