.. _MBsimulator:

Mass-Balance Simulator
======================

.. figure:: _static/MBsimulator_thumbnail.png
    :width: 100%
    :target: https://bokeh.oggm.org/mb_simulator/app

The Mass-Balance simulator is an **interactive web application** with which you can learn (and teach) about the glacier Mass-Balance, including the influence of different climate environments and different parameter settings.

You can start the app by clicking on this link: |badge_bokeh_en|_

.. _badge_bokeh_en: https://bokeh.oggm.org/mb_simulator/app

.. important::

  The Mass-Balance simulator app using computer resources on the cloud. If several people are using the app at
  the same time, the server might become slow or unresponsive. In this case,
  we recommend to use the app
  `on MyBinder <https://mybinder.org/v2/gh/OGGM/mb_simulator/stable?urlpath=panel/app>`_
  or even locally on your own computer (see :ref:`docker-launch-mb-simulator` below).

Getting started with the app
----------------------------

The Mass-Balance simulator is in principle structured in three parts:

- under 'Mass Balance 1' and 'Mass Balance 2', individual Mass-Balance models can be defined (with their particular climate configuration and model parameter settings) and explored (up to the monthly contributions).
- under 'Compare mass balances', the two individual Mass-Balance models are compared to each other.

For an introduction on how to interact with the app and what the individual figures show you should watch the tutorial video below!

Video tutorial
---------------

Watch this video for an introduction to the app's features and how to use it!

.. raw:: html

  <iframe src="https://player.vimeo.com/video/645151831" width="640" height="357" frameborder="0" allow="autoplay; fullscreen" allowfullscreen></iframe>
  <p><a href="https://vimeo.com/645151831">OGGM-Edu app: Mass Balance Simulator tutorial on Vimeo</a></p>

Theoretical Background
----------------------

The Mass-Balance describes the ice gain and loss of a glacier system. For a good general introduction visit `antarcticglaciers.org (mass-balance)`_.

The actual equation in the background of the App is a so-called Temperature-index model briefly explained in the `OGGM Docs`_ or in more detail in `Marzeion et al. (2012)`_. And the climate data for the different locations is from the `CRU TS v4 Dataset`_.

Questions to explore with this app
----------------------------------

With this app, you can address many questions, by yourself or in class! This list will grow in the future (documentation takes time!).

Monthly contributions to annual Mass Balance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Experiment:**

- Choose as a Base Climate 'Hintereisferner (Alps, continental)' and let all the other settings unchanged.
- Now look at the climograph (showing precipitation and temperature at each month) and try to answer the questions below.

**Questions to answer:**

By only looking at (or moving with your mouse over) the climograph try to guess:

- In which month do you think the accumulation is largest at 4000 m?
- In which month do you think the ablation is largest at 2000 m?
- Which month has the lowest altitude with a Mass Balance of 0 kg m⁻² month⁻¹ (lowest monthly Equilibrium Line Altitude ELA)?

After you made your guess you can compare the different months by switching them on and off at the left of the Accumulation plot. Tip: Move your mouse over the plots to get exact values.

.. admonition:: Take home messages
    :class: toggle

    - Largest Accumulation at 4500 m in June, the month with the largest precipitation amount
    - Largest Ablation at 2000 m in July, the month with the largest temperature
    - Lowest monthly ELA in December, even January has the lowest temperature, but in December more precipitation
    - Advanced comment: Comparing Ablation of December and January in 1600 m shows slightly more negative value in January than December. But from the definition of the Ablation we would expect a more negative value for December when only looking at the mean temperature shown in the climograph (the lower the temperature the smaller the Ablation). This is an example showing the difference of calculating the monthly mass balance at each month and then calculating the mean (as it is done in the background) or first calculating a mean temperature for a month and then using this for the calculation of the monthly Mass-Balance, for more information look at this `OGGM Blogpost`_.


Compare different locations/climates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Experiment:**

- Define two different Base Climates for 'Mass Balance 1' ('Hintereisferner (Alps, continental)') and 'Mass Balance 2' ('Echaurren Norte (Andes, mediterranean)') for the period 1990 - 2020, with the default MB settings.
- Go to 'Compare mass balances' and compare them ;).

**Questions to answer:**

- Compare the Accumulation and Ablation at the ELA.
- Compare the total Mass-Balance shape and the position of the ELA.
- *Advanced*: How do you believe these differences influence the glacier flow?

.. admonition:: Take home messages
    :class: toggle

    - Accumulation and Ablation at ELA appr. two times larger at Hintereisferner compared to Echaurren Norte.
    - *Advanced*: This results in a larger Mass-Balance gradient around the ELA for Hintereisferner. How this influences the glacier flow can be explored with the `Glacier Simulator (Mass-balance gradient)`_.
    - Higher ELA for Echauren Norte is a result of less annual precipitation and higher temperatures.


Compare different periods of the same base climate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Experiment:**

- Go to 'Mass Balance 1' and choose as base climate 'Lewis (Mount Kenya, tropical)' with period 1902 - 1932.
- Now go to 'Mass Balance 2' and choose the same base climate with the period 1990 - 2020.
- Additionally, you can go to 'Base climate timeseries' to explore the underlying climate dataset periods visually.
- For the comparison now switch to 'Compare mass balances'.

**Question to answer:**

- Interpret the resulting differences by comparing the climographs.
- How are glaciers affected by these differences?

.. admonition:: Take home messages
    :class: toggle

    - higher Temperatures results in a higher ELA in 1990 - 2020 compared to 1902 - 1932
    - but due to the larger precipitation amount ('total Prec.' when moving the mouse over a climograph) the mass gain is larger at high elevations (>5100 m) in 1990 - 2020 compared to 1902 - 1932

Influence of MB settings
~~~~~~~~~~~~~~~~~~~~~~~~

**Experiment (Suggestion):**

- Choose the same Base Climate for 'Mass Balance 1' and 'Mass Balance 2' with the same climate periods.
- Now go to 'MB settings' and change one of the settings for 'Mass Balance 2'.

**Questions to Answer:**

- What is the influence on the Accumulation, Ablation, Mass-Balance or ELA height?
- Is the influences the same for different Base Climates?

.. _antarcticglaciers.org (mass-balance): http://www.antarcticglaciers.org/glacier-processes/introduction-glacier-mass-balance
.. _OGGM Docs: https://docs.oggm.org/en/stable/mass-balance.html#temperature-index-model
.. _Marzeion et al. (2012): https://tc.copernicus.org/articles/6/1295/2012/tc-6-1295-2012.html
.. _CRU TS v4 Dataset: https://www.nature.com/articles/s41597-020-0453-3
.. _OGGM Blogpost: https://oggm.org/2021/08/05/mean-forcing/
.. _Glacier Simulator (Mass-balance gradient): https://edu.oggm.org/en/latest/simulator.html#mass-balance-gradient

Authors
-------

`Patrick Schmitt <https://github.com/pat-schmitt>`_ and
`Fabien Maussion <https://fabienmaussion.info/>`_.

Source code
-----------

Code and data are on `GitHub <https://github.com/OGGM/mb_simulator>`_, BSD3 licensed.

.. _docker-launch-mb-simulator:

Launching from Docker
---------------------

This application can keep a single processor quite busy when running. Fortunately,
you can also start the app locally, which will make it
faster and less dependent on an internet connection (although you still
need one to download the app and display the logos).

To start the app locally, all you'll need is to
have `Docker <https://www.docker.com/>`_ installed on your computer.
From there, run this command into a terminal::

    docker run -e BOKEH_ALLOW_WS_ORIGIN=0.0.0.0:8080 -p 8080:8080 oggm/bokeh:20211010 git+https://github.com/OGGM/mb_simulator.git@stable app.ipynb

Once running, you should be able to start the app in your browser at this
address: `http://0.0.0.0:8080/app <http://0.0.0.0:8080/app>`_.
