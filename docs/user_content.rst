.. _user_content:

Use your own content in OGGM-Edu
================================

You might be interested in running your own notebooks
in an OGGM-Edu environment, for example during the development phase or
for a specific class.

Fortunately, this is very easy to do! All you need to do is to provide the
notebooks you would like to run in an online git repository
(e.g. GitHub, Gitlab, Bitbucket). For example, we have created an
`oggm-edu-contrib <https://github.com/OGGM/oggm-edu-contrib>`_ with one single
notebook to get you started. See also
`Lizz' class (in spanish) <https://github.com/ehultee/CdeC-glaciologia>`_ for
a real-world example.

Ideally, we would like all OGGM-Edu related content to be bundled here on this
open platform: if you feel comfortable sharing your content to others,
please let us know!

On MyBinder
-----------

Using your own notebooks in an OGGM-Edu Binder environment is super easy!
Once your notebooks are online, you simply have to provide the correct
link to your students. The syntax is following::

    https://mybinder.org/v2/gh/OGGM/binder/master?urlpath=git-pull?repo=<PATH/TO/YOUR/REPO>

For example, a link to our contrib repository looks like:

`<https://mybinder.org/v2/gh/OGGM/binder/master?urlpath=git-pull?repo=https://github.com/OGGM/oggm-edu-contrib>`_

What is happening here? The first part of the link (up to the question mark)
is telling MyBinder to use the OGGM environment we are maintaining
`here <https://github.com/OGGM/binder>`_. The second part of the link
is using `nbgitpuller <https://jupyterhub.github.io/nbgitpuller/>`_ to fetch
the provided online repository and it's content. That's all!

This was the most basic example. If you want to use other features, like using
the Jupyter Lab interface (instead of the simple notebooks interface), and if
you want to start at an arbitrary location in the repository (for example
within a folder), the syntax is::


    https://mybinder.org/v2/gh/OGGM/binder/master?urlpath=git-pull?repo=<PATH/TO/YOUR/REPO>%26amp%3Burlpath=lab/tree/<YOUR_REPO_NAME>/<PATH/TO/FILE>%3Fautodecode

For example, we start the OGGM-Edu tutorials with this link:

`<https://mybinder.org/v2/gh/OGGM/binder/master?urlpath=git-pull?repo=https://github.com/OGGM/oggm-edu-notebooks%26amp%3Bbranch=master%26amp%3Burlpath=lab/tree/oggm-edu-notebooks/oggm-edu/welcome.ipynb%3Fautodecode>`_

It's getting quite long, I know! What's best therefore is to hide the links
`behind a badge <https://mybinder.readthedocs.io/en/latest/howto/badges.html>`_.

If you are creating educational resources based on OGGM-Edu,
please :ref:`title_contact` so that we can adverstise them!


On JupyterHub
-------------

If you are using `hub.oggm.org <https://hub.oggm.org>`_ or your own hub deployment, visit
`the OGGM documentation <https://docs.oggm.org/en/latest/cloud.html#oggm-hub>`_.
