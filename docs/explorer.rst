.. _explorer:

World Glaciers Explorer
=======================

.. figure:: _static/explorer.png
    :width: 100%
    :target: https://dash.klima.uni-bremen.de/bokeh/app

The world glacier explorer is an interactive application allowing to explore
the location of the world's glaciers, their climate, and their volume.

You can start the app by clicking on this link: |badgelink|_

.. |badgelink| image::  https://img.shields.io/badge/launch-bokeh%20app-579ACA.svg?style=popout&logo=     data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAC4jAAAuIwF4pT92AAAAB3RJTUUH4wEeDC0U4ki9ZgAAABl0RVh0Q29tbWVudABDcmVhdGVkIHdpdGggR0lNUFeBDhcAAAQFSURBVFjD7ZddaBxVGIafc2Y22+1u0qSxyaZJbBMTxLapUseUIsWWWrRIFhYL9bfgjdirQgX1qhUUb7zwQnqhghZ7IYo4MKJoo1YUtcQxlTRpWkyWGEp+l+zmZ5vs7swcL9yENeruxhi9yXc358z5nvfM9853ZgT/X/gAyXqsx3r8W2FHI9jRyNpDll1X2dFIVbH7CoVYCdgwLexoZA/wDHA34M/lSAE9wNuGaX2/fM2qBCyDnwFOCKU2S9fxCaUAUEKgpHQ8qc0BJvC8YVqTpYjQS3kCOfgrwEnheRvnqrYwuHMv09V1eEISnE2wdahfDw9fr9SczFNKyDvsaOSYYVrDxcohiu0+Bz8CnBeeVz1y2y6utD+AEmIpgRDgIqkeH2aH/QWhZBwl5SfAE4ZpJRfzrMYDF4XnHUjUNtJ16BgqN66UIlxVjtFSzzd9Q0ylXcKjMXb+2MnG2SRKiCeB9wzTcv8utywBbgBNUnn07zmIAny6JBTwo3DZFMpyZ3MYo7Uezc0y1thKvK4JT2oAJ4CyQvlLOQ7bhPJCc5XVpCo2A3BPawOHdjdzIxHj3LdnSaQSNIcrqa0MQNYhXredrD8ASrUX81kpAiqFUr754CZQCp8uOdDWREt9JRv8ccaTE3THekllphhJ/oLrZkgHQniatmhyXyEjliIgpRBuWXoeIXXiswN0DXTj18t45N7DzMyn+CnWw+R0nK7YV8RTN/C5DsLzFterQslLeQ17lBSp8mS8SkyPcmHwQ77sf58zR0/RUL0Vv17G11d/YDw5yeDENbRAI/uSG9CzGRBiCEivqg8YpnXJjkauStdtaLjcyUJgBkcpXvroNVrDzWRdh9j4rwyMDZERkBnto2LMh8/J4sEHgPOPPbBUOyFedGGiZXyC44kgITTG5mf4bqAbD3AFpHVBrSrjyMgs4dk5FGoGOA9kCjG0EpqQnPn5cnzLQx1pJx4/uH1earendSrQUJpECMEtjmTfTT8PJwPctVCGD4GCU8Dnhml5djTCm9eul16CZa49Wb6r7bi/pubizWDwsDY9/fKOBX3/toxGSvrJCtAUBD1ByBMACwpeAM4ZpuUUOwtEkd13AK8D24TuQ7nOgyhlA3sFPAbsB27NOT2m4GPgXeDKIrxQG/5LAXnw3cBbQHtuqhe4zzCtKTsakbnvej3PRx6QBbKGaalS4H8SkAevAc4CR3NTidxu+4olXMm3wJKAfKV2NBIATvN7HRcbSQfwqWFaqpRdrSTkMuUSeDwPDvAscGEt4AAy77EL4H7g1bz5N4B3DNPKrgX8Dx6wo5Fm4DOgNTfUCTxtmNbQWsGXSpAzTSivL/QCp9caDqDnAXrsaORR4DnAMkzr0n/xP/Ebgv/Oed8KI9UAAAAASUVORK5CYII=
.. _badgelink: https://bokeh.oggm.org/explorer/app

Alternatively, you can start the app `on mybinder <https://mybinder.org/v2/gh/OGGM/world-glacier-explorer/master?urlpath=panel/app>`_
(slightly slower in general, but possibly better if our server is saturated).
If you want to run the app locally, see :ref:`docker-launch` below.

**The app contains five elements**:

- the **world map** (upper right) displaying thg glacier locations, the color
  indicating the total area of each pixel. Moving the mouse over a glacier
  pixel indicates its glaciated area in a box. When selecting a box on the map,
  the other elements in the app will update accordingly. Above the map, there is
  a toolbar: with the "Box Zoom" button, you can also zoom into a specific
  region. Click on "Reset" to set the map back to defaults (see video below
  for a demo). *Be aware that
  the map projection is slightly misleading: high latitudes appear much
  bigger on the map than they really are.*
- the **clear selection button** on the left below the logos resets the
  current glacier selection.
- the **bar plots** (center) indicate various statistics about the current
  glacier selection (default: all glaciers). The upper blue bar (and text)
  indicates the number of glaciers selected, the middle blue bar their total
  area, and the lower blue bar their estimated volume. This volume can be
  converted to its *sea-level rise equivalent* (in mm), which is the global
  sea-level rise to be expected if all glacier melted. Only glaciers *above*
  sea-level are contributing to this number, therefore there are two bars:
  *asl* (above sea-level) and *bsl* (below sea-level). See the demo and
  explanations below on how to use this information.
- the three **climate histograms plots** (lower row) display the distribution
  of the selected glaciers' climate conditions. The y-axis is given in number
  of glaciers per bin, and the x-axis in the unit of the target variable
  (temperature trend, average temperature, average precipitation at the glacier
  location). Selecting a range of data in these plots also actualises the map
  and the rest of the plot (see demo below).
- the **glacier elevation/altitude scatter plot** (lower right) displays the
  average elevation of the glaciers on the map as a function of latitude (y-axis).


Demo
----

.. raw:: html

  <video width="700" height="360" controls>
   <source src="_static/explorer_demo.mp4" type="video/mp4">
  Your browser does not support the video tag.
  </video>

*In this video, we start by selecting all glaciers in Antarctica and show that
although these are few glaciers in number, they represent a large portion of
the total volume, but mostly below sea-level. Then, we reset the selection
and try to find out where the glaciers with the warmest
climate are located. Then, we show that the wettest glacier climates tend to be
among the warmests. Then, we select the glaciers with the most dramatic
warming trend, and show that these are located in the arctic. Finally, we
illustrate that we can zoom into the map and do multiple selections from
there. To reset the map view, click on the reset button above the map.*

The questions to explore
------------------------

With this app, you can address many questions, by yourself or in class! For example:

- where are the wettest glaciers located? And the driests?
- is there a relationship between temperature and precipitation?
- how much glacier area is found on Greenland? In the European Alps?
- does the number of glaciers always correlate with their volume?
- what regions are most likely to contribute to sea-level rise? Where do we
  find glaciers with ice below sea-level?
- what is the relationship between latitude and glacier elevation? Why?
- where are the glaciers which are warming the fastest?
  `why <https://fabienmaussion.info/2019/08/29/era5/>`_?
- and many more!

Authors
-------

`Philipp Rudiger <https://github.com/philippjfr>`_ and
`James Bednar <https://github.com/jbednar>`_ from
`HoloViz <http://holoviz.org//>`_ and Anaconda Inc., based on an original
Dash application by `Fabien Maussion <https://fabienmaussion.info/>`_.
`Zora Schirmeister <https://github.com/zschirmeister>`_ improved the app greatly
with new data and new plots.

Data sources
------------

Glacier location, elevation and area are obtained
from the `Randolph Glacier Inventory version 6 <https://www.glims.org/RGI/>`_.
The climate data (temperature, precipitation, trends) is extracted from
`ERA5 data <https://www.ecmwf.int/en/forecasts/datasets/reanalysis-datasets/era5>`_
provided by the `ECMWF <https://www.ecmwf.int/>`_.
The glacier volume was provided by `Farinotti et al., (2019) <https://www.nature.com/articles/s41561-019-0300-3>`_

.. _docker-launch:

Launching from Docker
---------------------

This application should work quite well online, either on our server or on
mybinder. But you can also start the app locally, which will make it
faster and less dependent on an internet connection (although you still
need one to download the app, display the logos and the map).

To start the app locally, all you'll need is to
have `Docker <https://www.docker.com/>`_ installed on your computer.
From there, run this command into a terminal:

    docker run -e BOKEH_ALLOW_WS_ORIGIN=127.0.0.1 -p 8080:80 oggm/bokeh:20191108 git+https://github.com/OGGM/world-glacier-explorer.git app.ipynb

Once running, you should be able to start the app in your browser at this
address: `http://127.0.0.1:8080/ <http://127.0.0.1:8080/>`_.

Possible future improvements
----------------------------

- With a category choice bar, it would be possible to differentiate glaciers
  from ice-caps or marine terminating glaciers from land-terminating ones.
