.. figure:: _static/oggm.gif
   :align: left

Welcome to OGGM-Edu!
====================

OGGM-Edu is an educational website about glaciers.

Our main goal is to **provide tools and materials for instructors** who
want to teach about glaciers at school, in workshops or at the university.

For a general introduction and an overview, visit this recent 
`EGU cryoblog post <https://blogs.egu.eu/divisions/cr/2021/03/12/do-you-know-about-oggm-edu-an-open-source-educational-platform-about-glaciers-and-glacier-modelling/>`_!

**OGGM-Edu has four independent and complementary components**:

1. :ref:`title_apps`, to illustrate glaciological processes with the
   help of interactive graphics on the web. The targeted audience is very
   broad, from school children to adults, with or without scientific background.
2. :ref:`title_graphics`, open access images and graphics that can be used
   for lectures or presentations.
3. :ref:`title_notebooks`, for students willing to run and develop
   their own experiments. The targeted audience are students at the undergrad
   or graduate level with some programming experience, or under the supervision
   of an instructor who can show them how to run the experiments.
4. :ref:`title_tuto`, for current and future users of the Open Global Glacier
   Model. These notebooks are targetting graduate students or scientists aiming
   to learn how the model works.

OGGM-Edu focuses on interactive content and numerical glacier experiments.
We do not provide teaching resources about fundamentals in glaciology or
climate science: for fundamental textbook material, refer to
:ref:`other_resources`, which OGGM-Edu intends to complement.

.. _title_apps:

Interactive apps
^^^^^^^^^^^^^^^^

These interactive apps can be run on any computer with an internet connection.

* :doc:`gallery`
* :doc:`explorer`
* :doc:`simulator`
* :doc:`mb_simulator`
* :doc:`alps_future`

.. toctree::
    :maxdepth: 1
    :hidden:
    :caption: Interactive apps

    gallery.rst
    explorer.rst
    simulator.rst
    mb_simulator.rst
    alps_future.rst

.. _title_graphics:

Graphics
^^^^^^^^

Open access images and graphics that can be used for lectures or presentations.

* :doc:`glacier_basics`
* :doc:`glacier_debriscovered`
* :doc:`glacier_lowpass`

.. toctree::
    :maxdepth: 1
    :hidden:
    :caption: Graphics

    glacier_basics.rst
    glacier_debriscovered.rst
    glacier_lowpass.rst


.. _title_notebooks:

Interactive Notebooks
^^^^^^^^^^^^^^^^^^^^^

Collection of notebooks with simple experiments explaining one or more
glaciological concepts. They are relatively easy to follow and adapt with some
background in programming, and we are working to make them as accessible as
possible. Read our :ref:`notebooks_howto` first if you are new to these things.

|badge_edu_notebooks|

.. toctree::
    :maxdepth: 1
    :hidden:
    :caption: Interactive Notebooks

    notebooks_howto.rst
    OGGM-Edu notebooks <https://oggm.org/oggm-edu-notebooks>


.. _title_tuto:

OGGM tutorials
^^^^^^^^^^^^^^

These are more advanced notebooks, for users of the OGGM model.

|badge_tutorial_notebooks|

.. toctree::
    :maxdepth: 1
    :hidden:
    :caption: OGGM tutorials

    OGGM tutorials <https://oggm.org/tutorials/stable>


For instructors and teachers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Thanks for considering OGGM-Edu for your classes! We've gathered some
recommendations and guidelines here.

* :doc:`why_oggmedu`
* :doc:`classes_howto`
* :doc:`examples`
* :doc:`charter`
* :doc:`roadmap`

.. toctree::
    :maxdepth: 1
    :hidden:
    :caption: For instructors and teachers

    why_oggmedu.rst
    classes_howto.rst
    other_resources.rst
    charter.rst
    roadmap.rst

.. _title_contact:

Get in touch
^^^^^^^^^^^^

Interested in OGGM-Edu? We would love to hear from you!

- All of this website and notebooks are located `on GitHub`_.
- Report bugs or share your ideas on the `issue tracker`_.
- Improve the website by submitting a `pull request`_.
- Follow us on `Twitter`_.
- Or you can always send us an `e-mail`_ the good old way.

.. _e-mail: info@oggm.org
.. _on GitHub: https://github.com/OGGM/oggm-edu
.. _issue tracker: https://github.com/OGGM/oggm-edu/issues
.. _pull request: https://github.com/OGGM/oggm-edu/pulls
.. _Twitter: https://twitter.com/OGGM_org

Acknowledgements
^^^^^^^^^^^^^^^^

OGGM-Edu is an affiliated project of the larger OGGM consortium
(`oggm.org <https://oggm.org>`_). It is mainly the work of volunteers, but we
also had support from various sources:

- the University of Innsbruck, Förderkreis **1669** – **Wissen** schafft
  Gesell **schaft** (2019-2020).
- the German BMBF (project FKZ 01LS1602A, 2017-2019).
- `Google Cloud | Data Solutions for Change`_ who provided cloud computing
  and hosting credits (2019-2020).
- the University of Innsbruck, department of
  `Digital Sciences <https://www.uibk.ac.at/zid/abteilungen/lt/>`_
  (Neue Medien Projekte, 2018).
- the OGGM e.V. organisation, who supported the creation of the OGGM-Edu logo
  and of the glacier graphics.

.. raw:: html

    <a href="https://www.uibk.ac.at/foerderkreis1669/" >
    <img src="_static/logo_1669_uibk.jpg" alt="Image missing" width="40%" />
    </a>
    <a href="https://www.bmbf.de/en/index.html" >
    <img src="_static/logo_bmbf.jpg" alt="Image missing" width="40%" />
    </a>
    <a href="https://cloud.google.com/data-solutions-for-change" >
    <img src="_static/feature-google-for-nonprofits-logo.svg" alt="Image missing" width="40%" />
    </a>
    <a href="http://holoviz.org/" >
    <img src="https://discourse.holoviz.org/uploads/default/original/1X/59aba5e11167d6b8742e01fc9d6bb60ddd4df55e.png" alt="Image missing" width="40%" />
    </a>
    <a href="https://jupyter.org" >
    <img src="https://jupyter.org/assets/hublogo.svg" alt="Jupyter logo" width="40%" />
    </a>
    <a href="https://mybinder.org" >
    <img src="https://mybinder.org/static/logo.svg" alt="MyBinder logo" width="40%" />
    </a>
    <br>

|

We rely on awesome open source tools to run OGGM-Edu! Most notably:

- `Jupyter <https://jupyter.org>`_
- `MyBinder <https://mybinder.org>`_
- `HoloViz <http://holoviz.org/>`_
- `ReadTheDocs <https://readthedocs.org>`_
- and many (many) other packages of the scientific python ecosytem

Last but not least: thanks to all OGGM-Edu friends and contributors!
For a full list, see our
`github repository <https://github.com/OGGM/oggm-edu/graphs/contributors>`_.

.. _Google Cloud | Data Solutions for Change: https://cloud.google.com/data-solutions-for-change
