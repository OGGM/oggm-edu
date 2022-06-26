.. _user_content:

Run your own notebooks
======================

You might be interested in running your own notebooks
in an OGGM-Edu environment, for example during the development phase or
for a class you are giving.

Fortunately, this is very easy to do! All you need to do is to provide the
notebooks you would like to run in an online git repository
(e.g. GitHub, Gitlab, Bitbucket). For example, we have created an
`oggm-edu-contrib <https://github.com/OGGM/oggm-edu-contrib>`_ with one single
notebook to get you started. We use the same principle for the official
`OGGM-Edu notebooks <https://github.com/OGGM/oggm-edu-notebooks>`_ repository.
See also :ref:`existing-classes` for examples from other instructors.

Ideally, we would like all OGGM-Edu related content to be bundled here on this
open platform: if you are creating educational resources based on OGGM-Edu,
please :ref:`get in touch <title_contact>` so that we can advertise them!

On MyBinder
-----------

Using your own notebooks in an OGGM-Edu Binder environment is super easy!
Once your notebooks are online, you simply have to provide the correct
link to your students. The syntax is following::

    https://mybinder.org/v2/gh/OGGM/binder/stable?urlpath=git-pull?repo=<PATH/TO/YOUR/REPO>

For example, a link to our contrib repository looks like:

`<https://mybinder.org/v2/gh/OGGM/binder/stable?urlpath=git-pull?repo=https://github.com/OGGM/oggm-edu-contrib>`_

What is happening here? The first part of the link (up to the question mark)
is telling MyBinder to use the OGGM environment we are maintaining
`here <https://github.com/OGGM/binder>`_ (we use the stable branch).
The second part of the link
is using `nbgitpuller <https://jupyterhub.github.io/nbgitpuller/>`_ to fetch
the provided online repository and its content. That's all!

This was the most basic example. If you want to use other features, like using
the Jupyter Lab interface (instead of the simple notebooks interface), and if
you want to start at an arbitrary location in the repository (for example
within a folder), the syntax is a bit more clumsy. The best way (by far!)
is to rely on nbgitpuller's `link generator`_
to do the job for you.

For example, we start the OGGM-Edu tutorials with this link:

`<https://mybinder.org/v2/gh/OGGM/binder/stable?urlpath=git-pull%3Frepo%3Dhttps%253A%252F%252Fgithub.com%252FOGGM%252Foggm-edu-notebooks%26urlpath%3Dlab%252Ftree%252Foggm-edu-notebooks%252Fwelcome.ipynb%26branch%3Dmaster>`_

It's getting quite long, I know! What's best therefore is to hide the links
`behind a badge <https://mybinder.readthedocs.io/en/latest/howto/badges.html>`_.

.. _link generator: https://jupyterhub.github.io/nbgitpuller/link.html

On classroom.oggm.org
---------------------

Since August 2021, we provide a dedicated OGGM JupyterLab server running on
a dedicated machine in Bremen. `classroom.oggm.org <https://classroom.oggm.org>`_
(that's its name!) is like `OGGM-Hub <https://docs.oggm.org/en/stable/cloud.html#oggm-hub>`_,
but tailored for instructors and their classes.

The advantages of OGGM-classroom over Binder are:

- more resources for your students, faster launches
- user management: you can set passwords and user names at wish
- persistent sessions: work can be saved between sessions and log-ins (this is by far the main advantage)

We are currently in the testing phase, and it is unclear how many students we
can allow to run their notebooks at the same time. We managed to run classes with more than
20 students logged in at the same time. If you are willing to try
it out, please :ref:`get in touch <title_contact>` and we will do our best
to let you use it with your class!

Similarly to MyBinder, you can create a link for your students to download
the content of your notebooks repository very easily. We recommend to use
nbgitpuller's `link generator`_ for this purpose.

For example, we can start the OGGM-Edu tutorials on classroom.oggm.org with this link:

`<https://classroom.oggm.org/hub/user-redirect/git-pull?repo=https%3A%2F%2Fgithub.com%2FOGGM%2Foggm-edu-notebooks&urlpath=lab%2Ftree%2Foggm-edu-notebooks%2Fwelcome.ipynb&branch=master>`_

Again, hiding the links
`behind a badge <https://mybinder.readthedocs.io/en/latest/howto/badges.html>`_ makes it prettier:

|badge_classroom_tutos|

Enjoy!

.. _technical_details:

Technical details
-----------------

The computing environments available via MyBinder are
`Docker containers <https://www.docker.com/resources/what-container>`_,
or "software capsules" that can be created, pushed and pulled online. We create
these containers using a few simple configuration files specifying the
software packages and python libraries we would like to used in OGGM-Edu.
These configurations files are found in these repositories:
`<https://github.com/OGGM/r2d>`_ (for JupyterHub),
`<https://github.com/OGGM/binder>`_ (for MyBinder).

Working images are available `on ghcr.io <https://github.com/OGGM/OGGM-Docker/pkgs/container/r2d>`_ to
form the base of the Binder environments.
