.. _simulator:

Glacier Simulator (beta)
========================

.. figure:: _static/simulator_thumbnail.png
    :width: 100%
    :target: https://bokeh.oggm.org/simulator/app

The glacier simulator is an **interactive web application** with which
you can learn (and teach) about how glaciers grow and shrink, how fast they
flow, what parameters influence their size, and a lot more.

The application is still in beta version, which means that we are working on
the last details before release.

You can start the app by clicking on this link: |badgelink|_

.. |badgelink| image::  https://img.shields.io/badge/launch-bokeh%20app-579ACA.svg?style=popout&logo=     data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAC4jAAAuIwF4pT92AAAAB3RJTUUH4wEeDC0U4ki9ZgAAABl0RVh0Q29tbWVudABDcmVhdGVkIHdpdGggR0lNUFeBDhcAAAQFSURBVFjD7ZddaBxVGIafc2Y22+1u0qSxyaZJbBMTxLapUseUIsWWWrRIFhYL9bfgjdirQgX1qhUUb7zwQnqhghZ7IYo4MKJoo1YUtcQxlTRpWkyWGEp+l+zmZ5vs7swcL9yENeruxhi9yXc358z5nvfM9853ZgT/X/gAyXqsx3r8W2FHI9jRyNpDll1X2dFIVbH7CoVYCdgwLexoZA/wDHA34M/lSAE9wNuGaX2/fM2qBCyDnwFOCKU2S9fxCaUAUEKgpHQ8qc0BJvC8YVqTpYjQS3kCOfgrwEnheRvnqrYwuHMv09V1eEISnE2wdahfDw9fr9SczFNKyDvsaOSYYVrDxcohiu0+Bz8CnBeeVz1y2y6utD+AEmIpgRDgIqkeH2aH/QWhZBwl5SfAE4ZpJRfzrMYDF4XnHUjUNtJ16BgqN66UIlxVjtFSzzd9Q0ylXcKjMXb+2MnG2SRKiCeB9wzTcv8utywBbgBNUnn07zmIAny6JBTwo3DZFMpyZ3MYo7Uezc0y1thKvK4JT2oAJ4CyQvlLOQ7bhPJCc5XVpCo2A3BPawOHdjdzIxHj3LdnSaQSNIcrqa0MQNYhXredrD8ASrUX81kpAiqFUr754CZQCp8uOdDWREt9JRv8ccaTE3THekllphhJ/oLrZkgHQniatmhyXyEjliIgpRBuWXoeIXXiswN0DXTj18t45N7DzMyn+CnWw+R0nK7YV8RTN/C5DsLzFterQslLeQ17lBSp8mS8SkyPcmHwQ77sf58zR0/RUL0Vv17G11d/YDw5yeDENbRAI/uSG9CzGRBiCEivqg8YpnXJjkauStdtaLjcyUJgBkcpXvroNVrDzWRdh9j4rwyMDZERkBnto2LMh8/J4sEHgPOPPbBUOyFedGGiZXyC44kgITTG5mf4bqAbD3AFpHVBrSrjyMgs4dk5FGoGOA9kCjG0EpqQnPn5cnzLQx1pJx4/uH1earendSrQUJpECMEtjmTfTT8PJwPctVCGD4GCU8Dnhml5djTCm9eul16CZa49Wb6r7bi/pubizWDwsDY9/fKOBX3/toxGSvrJCtAUBD1ByBMACwpeAM4ZpuUUOwtEkd13AK8D24TuQ7nOgyhlA3sFPAbsB27NOT2m4GPgXeDKIrxQG/5LAXnw3cBbQHtuqhe4zzCtKTsakbnvej3PRx6QBbKGaalS4H8SkAevAc4CR3NTidxu+4olXMm3wJKAfKV2NBIATvN7HRcbSQfwqWFaqpRdrSTkMuUSeDwPDvAscGEt4AAy77EL4H7g1bz5N4B3DNPKrgX8Dx6wo5Fm4DOgNTfUCTxtmNbQWsGXSpAzTSivL/QCp9caDqDnAXrsaORR4DnAMkzr0n/xP/Ebgv/Oed8KI9UAAAAASUVORK5CYII=
.. _badgelink: https://bokeh.oggm.org/simulator/app

.. important::

  The glacier simulator app runs a numerical glacier model in the background,
  using computer resources on the cloud. If several people are using the app at
  the same time, the server might become slow or unresponsive. In this case,
  we recommend to use the app on MyBinder or (even better) locally on your
  own computer (see below).

Alternatively, you can start the app `on mybinder <https://mybinder.org/v2/gh/OGGM/glacier_simulator/master?urlpath=panel/app>`_
(slightly slower in general, but a good alternative if our server is saturated).
If you want to run the app on your own computer, see :ref:`docker-launch-simulator` below.

Demo
----

(in construction)

Questions to explore with this app
----------------------------------

With this app, you can address many questions, by yourself or in class!

Equilibrium Line Altitude (ELA)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

See `antarcticglaciers.org <http://www.antarcticglaciers.org/glacier-processes/introduction-glacier-mass-balance/>`_
for an intrudction about glacier mass-balance and the ELA, or our
:ref:`glacier_basics` graphics for an illustration.

We are going to show that the ELA is determinant in shaping glaciers.

**In "beginner mode", start by setting the ELA to 2500m a.s.l**, and note
on a piece of paper: the equilibrium volume of the glacier,
its lenght and maximal thickness.
**Now change the ELA up to 3500m a.s.l in 200m increments** and, at each
step, note the equilibrium volume of the glacier, its lenght and maximal thickness.

**Now draw these variables on a graph, as a function of the ELA.**
How does glacier volume change with ELA? Can you explain why?
What about glacier length and thickness? Are these changes linear, or more
complex?

An example graphic that students could come up with by varying the ELA
with different shapes can be found `here <_static/simulator_ela_example.png>`_.

Glacier shape
~~~~~~~~~~~~~

**In "beginner mode", start by setting the ELA to 3000m a.s.l**, and note
on a piece of paper: the equilibrium volume of the glacier,
its lenght and maximal thickness. **Now choose the "wider top" glacier shape**
and run the model again. Is the new glacier larger or smaller than before? Why?


Glacier slope
~~~~~~~~~~~~~

(in construction)

Mass-balance gradient
~~~~~~~~~~~~~~~~~~~~~

(in construction)


Authors
-------

`Patrick Schmitt <https://github.com/pat-schmitt>`_ and
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

    docker run -e BOKEH_ALLOW_WS_ORIGIN=127.0.0.1 -p 8080:8080 oggm/bokeh:20200202 git+https://github.com/OGGM/glacier_simulator.git app.ipynb

Once running, you should be able to start the app in your browser at this
address: `http://127.0.0.1:8080/ <http://127.0.0.1:8080/>`_.
