.. _simulator:

Glacier Simulator
=================

.. figure:: _static/simulator_thumbnail.png
    :width: 100%
    :target: https://bokeh.oggm.org/simulator/app

The glacier simulator is an **interactive web application** with which
you can learn (and teach) about glacier flow, how glaciers grow and shrink,
what parameters influence their size, and a lot more!

You can start the app by clicking on this link: |badgelink|_

.. |badgelink| image::  https://img.shields.io/badge/launch-bokeh%20app-579ACA.svg?style=popout&logo=     data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAC4jAAAuIwF4pT92AAAAB3RJTUUH4wEeDC0U4ki9ZgAAABl0RVh0Q29tbWVudABDcmVhdGVkIHdpdGggR0lNUFeBDhcAAAQFSURBVFjD7ZddaBxVGIafc2Y22+1u0qSxyaZJbBMTxLapUseUIsWWWrRIFhYL9bfgjdirQgX1qhUUb7zwQnqhghZ7IYo4MKJoo1YUtcQxlTRpWkyWGEp+l+zmZ5vs7swcL9yENeruxhi9yXc358z5nvfM9853ZgT/X/gAyXqsx3r8W2FHI9jRyNpDll1X2dFIVbH7CoVYCdgwLexoZA/wDHA34M/lSAE9wNuGaX2/fM2qBCyDnwFOCKU2S9fxCaUAUEKgpHQ8qc0BJvC8YVqTpYjQS3kCOfgrwEnheRvnqrYwuHMv09V1eEISnE2wdahfDw9fr9SczFNKyDvsaOSYYVrDxcohiu0+Bz8CnBeeVz1y2y6utD+AEmIpgRDgIqkeH2aH/QWhZBwl5SfAE4ZpJRfzrMYDF4XnHUjUNtJ16BgqN66UIlxVjtFSzzd9Q0ylXcKjMXb+2MnG2SRKiCeB9wzTcv8utywBbgBNUnn07zmIAny6JBTwo3DZFMpyZ3MYo7Uezc0y1thKvK4JT2oAJ4CyQvlLOQ7bhPJCc5XVpCo2A3BPawOHdjdzIxHj3LdnSaQSNIcrqa0MQNYhXredrD8ASrUX81kpAiqFUr754CZQCp8uOdDWREt9JRv8ccaTE3THekllphhJ/oLrZkgHQniatmhyXyEjliIgpRBuWXoeIXXiswN0DXTj18t45N7DzMyn+CnWw+R0nK7YV8RTN/C5DsLzFterQslLeQ17lBSp8mS8SkyPcmHwQ77sf58zR0/RUL0Vv17G11d/YDw5yeDENbRAI/uSG9CzGRBiCEivqg8YpnXJjkauStdtaLjcyUJgBkcpXvroNVrDzWRdh9j4rwyMDZERkBnto2LMh8/J4sEHgPOPPbBUOyFedGGiZXyC44kgITTG5mf4bqAbD3AFpHVBrSrjyMgs4dk5FGoGOA9kCjG0EpqQnPn5cnzLQx1pJx4/uH1earendSrQUJpECMEtjmTfTT8PJwPctVCGD4GCU8Dnhml5djTCm9eul16CZa49Wb6r7bi/pubizWDwsDY9/fKOBX3/toxGSvrJCtAUBD1ByBMACwpeAM4ZpuUUOwtEkd13AK8D24TuQ7nOgyhlA3sFPAbsB27NOT2m4GPgXeDKIrxQG/5LAXnw3cBbQHtuqhe4zzCtKTsakbnvej3PRx6QBbKGaalS4H8SkAevAc4CR3NTidxu+4olXMm3wJKAfKV2NBIATvN7HRcbSQfwqWFaqpRdrSTkMuUSeDwPDvAscGEt4AAy77EL4H7g1bz5N4B3DNPKrgX8Dx6wo5Fm4DOgNTfUCTxtmNbQWsGXSpAzTSivL/QCp9caDqDnAXrsaORR4DnAMkzr0n/xP/Ebgv/Oed8KI9UAAAAASUVORK5CYII=
.. _badgelink: https://bokeh.oggm.org/simulator/app

.. important::

  The glacier simulator app runs a numerical glacier model in the background,
  using computer resources on the cloud. If several people are using the app at
  the same time, the server might become slow or unresponsive. In this case,
  we recommend to use the app
  `on MyBinder <https://mybinder.org/v2/gh/OGGM/glacier_simulator/master?urlpath=panel/app>`_
  or even locally on your own computer (see :ref:`docker-launch-simulator` below).

Getting started with the app
----------------------------

The upper panel in the app is a guided tutorial about the app's functionalities.
You can navigate it with the "Next" and "Previous" buttons, or use the
"Find help here" overview.


Questions to explore with this app
----------------------------------

With this app, you can address many questions, by yourself or in class!
This list will grow in the future (documentation takes time!).

Glacier shape
~~~~~~~~~~~~~

See `antarcticglaciers.org (mass-balance)`_
for an introduction about glacier mass-balance and the ELA, or our
:ref:`glacier_basics` graphics for an illustration.

**In "beginner mode", start by setting the ELA to 3000m a.s.l**, and note
on a piece of paper: the equilibrium volume of the glacier,
its length and maximal thickness. **Now choose the "wider top" glacier shape**
and run the model again. Is the new glacier larger or smaller than before? Why?

..  admonition:: Take home messages
    :class: toggle

    A glacier with a wider top has a larger `accumulation area <https://en.wikipedia.org/wiki/Accumulation_zone>`_.
    It can therefore accumulate more mass (more ice) and flow further down.


Equilibrium Line Altitude (ELA)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

See `antarcticglaciers.org (mass-balance)`_
for an introduction about glacier mass-balance and the ELA, or our
:ref:`glacier_basics` graphics for an illustration.

We are going to show that the ELA is determinant in shaping glaciers.

**In "beginner mode", start by setting the ELA to 2500m a.s.l**, and note
on a piece of paper: the equilibrium volume of the glacier,
its length and maximal thickness.

**Now change the ELA up to 3500m a.s.l in 200m increments** and, at each
step, note the equilibrium volume of the glacier, its length and maximal thickness.

**Now draw these variables on a graph, as a function of the ELA.**
How does glacier volume change with ELA? Can you explain why?
What about glacier length and thickness? Are these changes linear, or more
complex?

..  admonition:: Take home messages
    :class: toggle

    An example graphic that students could come up with by varying the ELA
    with different shapes:

    .. figure:: _static/simulator_ela_example.png
        :width: 100%

    **The lower the ELA, the larger the equilibrium glacier**. The length,
    volume or maximal thickness are not necessarily linear functions of the
    ELA.

Glacier slope
~~~~~~~~~~~~~

The slope of a glacier bed is one key ingredient which determines glacier flow.
For a introduction, visit `antarcticglaciers.org (glacier-flow)`_.
In short: glaciers flow downslope driven by the gravitational force.
This force can be decomposed into an along-slope component and perpenticular to the slope component (see
`this illustration in wikipedia <https://en.wikipedia.org/wiki/Inclined_plane#/media/File:Free_body1.3.svg>`_).
The along-slope component "pulls" the glacier downwards and the perpendicular component "flattens" the glacier.

**Experiments:**

- *Beginners*: Use beginner mode with standard settings (constant width, mass
  balance gradient of 4 and ELA of 3000) and run the model with all different
  settings for the slope and use the geometry plot for inspection.
  Take notes on a piece of paper of the ice thickness, volume, area and length
  at the end of each model run.
- *Advanced*: Conduct the same experiment as for beginners, but additionally
  switch on the timeseries plot. Also take notes of the velocity and look how
  the parameters change with time in the timeseries plot.

**Questions to answer:**

- *Beginners*: which glaciers are thicker? Steep or flat ones? And why?
- *Advanced*: which glaciers are faster? Steep or flat ones? How and why does
  the velocity change with time?


..  admonition:: Take home messages
    :class: toggle

    - glaciers flow downslope
    - the steeper the slope the thinner the glacier (larger along-slope gravitational force)
    - the flatter the slope the larger the equilibrium velocity. When the glacier
      is thin (has not much mass) the along-slope component is more important.
      When the glacier is getting thicker the perpendicular component is getting
      more weight. This partly explains slower velocities for flatter slopes
      at the start of the model run, and higher velocities when the glacier is
      getting thicker. For steeper slopes the velocities at the start are
      large and so more ice is transported downwards, and the glacier stays
      relatively thin.

.. _antarcticglaciers.org (mass-balance): http://www.antarcticglaciers.org/glacier-processes/introduction-glacier-mass-balance
.. _antarcticglaciers.org (glacier-flow): http://www.antarcticglaciers.org/glacier-processes/glacier-flow-2/glacier-flow


Authors
-------

`Patrick Schmitt <https://github.com/pat-schmitt>`_ (main author) and
`Fabien Maussion <https://fabienmaussion.info/>`_.

Source code
-----------

Code and data are on `GitHub <https://github.com/OGGM/glacier_simulator>`_, BSD licensed.

.. _docker-launch-simulator:

Launching from Docker
---------------------

This application can keep a single processor quite busy when running. Fortunately,
you can also start the app locally, which will make it
faster and less dependent on an internet connection (although you still
need one to download the app and display the logos).

To start the app locally, all you'll need is to
have `Docker <https://www.docker.com/>`_ installed on your computer.
From there, run this command into a terminal:

    docker run -e BOKEH_ALLOW_WS_ORIGIN=127.0.0.1 -p 8080:8080 oggm/bokeh:20200406 git+https://github.com/OGGM/glacier_simulator.git app.ipynb

Once running, you should be able to start the app in your browser at this
address: `http://127.0.0.1:8080/ <http://127.0.0.1:8080/>`_.
