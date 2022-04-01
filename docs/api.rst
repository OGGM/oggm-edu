#######################
oggm-edu python package
#######################
 
.. currentmodule:: oggm_edu

This page lists all classes, their methods and attributes available in the
``oggm-edu`` python package.

|badge_edu_notebooks|

Open a MyBinder interactive session to try them yourself!

.. important::

    This programming interface is relatively new (2022). It replaces a
    much simpler previous interface, which is still accessible to our users
    with::

        from oggm_edu import legacy

    Don't hesitate to `let us know <https://github.com/OGGM/oggm-edu/issues>`_
    if you find any mistakes in the tool or in the docs!

GlacierBed
----------

.. autosummary::
   :toctree: generated/

   GlacierBed
   GlacierBed.plot

GlacierBed example
~~~~~~~~~~~~~~~~~~

.. ipython:: python

    from oggm_edu import GlacierBed
    bed = GlacierBed(top=3400, bottom=1500, width=300)
    @savefig plot_bed.png width=100%
    bed.plot();

MassBalance
-----------

.. autosummary::
   :toctree: generated/

   MassBalance
   MassBalance.reset
   MassBalance.get_monthly_mb
   MassBalance.get_annual_mb
   MassBalance.gradient
   MassBalance.ela
   MassBalance.temp_bias

MassBalance example
~~~~~~~~~~~~~~~~~~~

.. ipython:: python

    from oggm_edu import MassBalance
    mass_balance = MassBalance(ela=3000, gradient=4)
    mass_balance

Glacier
-------

.. autosummary::
   :toctree: generated/

   Glacier

Glacier methods
~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: generated/

   Glacier.reset
   Glacier.copy
   Glacier.progress_to_year
   Glacier.progress_to_equilibrium
   Glacier.plot
   Glacier.plot_mass_balance
   Glacier.plot_history
   Glacier.plot_state_history
   Glacier.add_temperature_bias

Glacier attributes
~~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: generated/

   Glacier.ela
   Glacier.mb_gradient
   Glacier.mass_balance
   Glacier.annual_mass_balance
   Glacier.specific_mass_balance
   Glacier.age
   Glacier.history
   Glacier.state_history
   Glacier.creep
   Glacier.basal_sliding
   Glacier.eq_states
   Glacier.response_time

Glacier example
~~~~~~~~~~~~~~~

.. ipython:: python

    from oggm_edu import Glacier
    glacier = Glacier(bed=bed, mass_balance=mass_balance)
    glacier.progress_to_equilibrium()
    @savefig plot_glacier.png width=100%
    glacier.plot();

.. ipython:: python

    @savefig plot_glacier_equi.png width=100%
    glacier.plot_history();

SurgingGlacier
--------------

.. autosummary::
   :toctree: generated/

   SurgingGlacier
   SurgingGlacier.reset
   SurgingGlacier.progress_to_year
   SurgingGlacier.plot_history
   SurgingGlacier.normal_years
   SurgingGlacier.surging_years
   SurgingGlacier.basal_sliding_surge


GlacierCollection
-----------------

.. autosummary::
   :toctree: generated/

   GlacierCollection

GlacierCollection methods
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: generated/

   GlacierCollection.reset
   GlacierCollection.fill
   GlacierCollection.add
   GlacierCollection.change_attributes
   GlacierCollection.progress_to_year
   GlacierCollection.progress_to_equilibrium
   GlacierCollection.plot
   GlacierCollection.plot_history
   GlacierCollection.plot_mass_balance

GlacierCollection attributes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: generated/

   GlacierCollection.glaciers
   GlacierCollection.annual_mass_balance


GlacierCollection example
~~~~~~~~~~~~~~~~~~~~~~~~~

.. ipython:: python

    from oggm_edu import GlacierCollection
    wide_narrow_bed = GlacierBed(altitudes=[3400, 2800, 1500],
                                 widths=[600, 300, 300])
    wide_narrow_glacier = Glacier(bed=wide_narrow_bed,
                                  mass_balance=mass_balance)
    collection = GlacierCollection()
    collection.add([glacier, wide_narrow_glacier])
    collection.progress_to_year(600)
    @savefig plot_glacier_collection.png width=100%
    collection.plot()