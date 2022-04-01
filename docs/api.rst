#######################
oggm-edu python package
#######################
 
.. currentmodule:: oggm_edu

This page lists all classes, their methods and attributes available in the
``oggm-edu`` python package.

.. important::

    This programming interface is relatively new (2022). It replaces a
    much simpler previous interface which is now accessible via
    ``from oggm_edu import legacy``.

    Don't hesitate to `let us know <https://github.com/OGGM/oggm-edu/issues>`_
    if you find any mistakes!.

Glacier bed
-----------

.. autosummary::
   :toctree: generated/

   GlacierBed
   GlacierBed.plot

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


