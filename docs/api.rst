.. _api:

###########################
The oggm-edu python package
###########################
 
.. currentmodule:: oggm_edu

The ``oggm-edu`` python package is a "simplification layer" meant to hide many
of the complex OGGM internals to the students. In fact, it can be seen as a
fully functional glacier flow model optimized for education.

To see it in action, visit our dedicated
`oggm-edu notebooks website <https://oggm.org/oggm-edu-notebooks/oggm-edu/edu_intro.html>`_,
or run them yourself on MyBinder:

|badge_edu_notebooks|

For a complete documentation, visit the full :ref:`api_detailed`.

.. important::

    This programming interface is relatively new (2022). It replaces a
    much simpler previous interface, which is still accessible to our users
    with::

        from oggm_edu import legacy

    Don't hesitate to `let us know <https://github.com/OGGM/oggm-edu/issues>`_
    if you encounter any problem with the change!

A 2 minutes introduction to the package
---------------------------------------

The main objective of package is to propose an expressive syntax and preconfigured
plotting functions:

.. code-block:: python

    from oggm_edu import MassBalance, GlacierBed, Glacier

    # Create the bed
    bed = GlacierBed(top=3400, bottom=1500, width=300)
    # And the mass balance
    mass_balance = MassBalance(ela=3000, gradient=4)
    # And finally the glacier!
    glacier = Glacier(bed=bed, mass_balance=mass_balance)
    glacier.plot()

.. image:: https://oggm.org/img/blog/oggm-edu-new/edu_intro_26_0.png

To grow the glacier we can either progress the glacier to a specified year:

.. code-block:: python

    glacier.progress_to_year(150)
    glacier.plot()

.. image:: https://oggm.org/img/blog/oggm-edu-new/edu_intro_31_0.png

Or progress the glacier to equilibrium:

.. code-block:: python

    glacier.progress_to_equilibrium()
    glacier.plot()

.. image:: https://oggm.org/img/blog/oggm-edu-new/edu_intro_37_0.png

It is just as easy to inspect the history of the length, volume and area of the glacier:

.. code-block:: python

    glacier.plot_history()

.. image:: https://oggm.org/img/blog/oggm-edu-new/edu_intro_43_0.png

This is just a small part of what is possible with the new interface.

For a complete documentation, visit the full :ref:`api_detailed`.

We hope that you will find this interesting, and are waiting for your feedback!
