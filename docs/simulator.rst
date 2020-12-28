.. _simulator:

Glacier Simulator
=================

.. figure:: _static/simulator_thumbnail.png
    :width: 100%
    :target: https://bokeh.oggm.org/simulator/app

The glacier simulator is an **interactive web application** with which
you can learn (and teach) about glacier flow, how glaciers grow and shrink,
what parameters influence their size, and a lot more!

You can start the app by clicking on this link: |badge_bokeh_en|_

.. _badge_bokeh_en: https://bokeh.oggm.org/simulator/app

.. important::

  The glacier simulator app runs a numerical glacier model in the background,
  using computer resources on the cloud. If several people are using the app at
  the same time, the server might become slow or unresponsive. In this case,
  we recommend to use the app
  `on MyBinder <https://mybinder.org/v2/gh/OGGM/glacier_simulator/v1.1?urlpath=panel/app>`_
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

Surging glaciers
~~~~~~~~~~~~~~~~

Some of the world's glaciers experience "surges" during which they flow much faster than usual 
and can advance dramatically. For an introduction see `antarcticglaciers.org (surging-glaciers)`_ ,
or `this video`_ of surging Karakorum glaciers seen from space.
 
We will use the simulator app to explore the characteristics of a surging glacier.

**Experiment:**

Use the "beginner mode" with standard settings (constant width, mass balance gradient of 4 and ELA of 3000) and run the 
model to create a glacier in equilibrium.
This glacier should now experience a surge which lasts for ten years:
Switch into the "advanced mode". Turn on "sliding", i.e. the glacier will "slip" on the 
bedrock, and let the model advance for 10 years. Between surge events long periods of 
quiescence happen: simulate one by advancing your glacier without sliding for 100 years. 
Repeat the surge event and the period of quiescence. Use the timeseries plots and the 
timeseries options to show the maximum velocity as well as the maximum thickness.

**Questions to answer:**

*Beginners:*

During a surge event:

- How much faster is the glacier during a surge in comparison to a "normal" (quiescence) period?
- How much gains the glacier in length? 

After a surge event:

- How can you explain the glacier retreat?

*Advanced:*

- Why is the glacier thinning during a surge?
- How can you explain the opposing behaviours of length and volume during a surge?
- Why is the glacier thickening after the surge?


..  admonition:: Take home messages
    :class: toggle

    - during a surge event: The glacier flows faster and reaches lower in the valley. 
      In the upper parts the accumulation of snow does change, but not much 
      (accumulation is slightly less since the glacier is thinner: a process called mass-balance / elevation feedback).
      At the same time, a much larger area than usual of the glacier is exposed to melt below 
      the ELA. Therefore the glacier thins and looses volume, although it is still advancing.
    - after a surge event: The glacier flow recovers its usual "slow" velocity. The glacier 
      will retreat until it accumulated enough ice to advance again.

**Going further:**

In the Notebook :ref:`notebooks_surging_glaciers` you can use OGGM to simulate surging events in Python yourself.

Velocity and Thickness along the glacier
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Experiments:**

- *Beginners*: Use "Beginner mode" to simulate a glacier in equilibrium with *Width* = *Constant*, *ELA* = 3000, *Mass-Balance gradient* = 4 and *Slope* = 11°.
- *Advanced*: Use "Beginner mode" to simulate a glacier with *Width* = *Wide top, narrow bottom*, *ELA* = 3500, *Mass-Balance gradient* = 4 and *Slope* = 11°.

**Questions to answer:**

- What do you think where the ice velocity/thickness along the glacier is the largest?
- *Advanced*: How is the narrowing effecting the velocity?
- When you made your guess go to "Geometry opt." and tick the box *Ice velocity (top left)* and *Ice thickness (bottom left)*. Now the red/blue colors are showing the velocity/thickness distribution along the glacier. Did you guess right?
- Why is the velocity/thickness distribution as it is?

..  admonition:: Take home messages
    :class: toggle

    - *Beginners*:
        - starting at the top of the glacier and going downward to the ELA there is constantly mass accumulated (positive mass-balance)
        - all this mass must be transported downwards and so the ice flux is largest at the ELA
        - from the ELA going further downward mass is constantly ablated and the ice flux decreases
        - larger ice flux means thicker and faster glacier flow
    - *Advanced*:
        - additionaly to the effect explained in *Beginners* we see that a narrowing of the along glacier widths can also lead to an increase in the ice flux (velocity/thickness)
        - in this case the maximum velocity is no longer located around the ELA but further downwards at the narrowing of the valley

Mass-Balance gradient
~~~~~~~~~~~~~~~~~~~~~

See `antarcticglaciers.org (mass-balance)`_
for an introduction about glacier Mass-Balance and the Mass-Balance gradient.

In short: The climatic regime determines the glacier Mass-Balance gradient. Discovering global glacier locations using the `World Glaciers Explorer`_ reveals that glaciers can be found in quite different places around the world. Here now discover how different Mass-Balance gradients are shaping glaciers.

**Experiments:**

- First simulate a glacier in a maritime climate in temperate latitudes (larger Mass-Balance gradient, e.g. 10). For this use the "Beginner mode" (*ELA* = 3000, *Width* = *Constant* and *Slope* = 11°) and let the glacier grow until it reaches equilibrium and note on a piece of paper: the equilibrium *Time*, *Length*, *Area*, *Volume*, *Max ice thickness* and *Max ice velocity* of the glacier.
- Next simulate a glacier in a continental climate in polar latitudes (smaller Mass Balance gradient, e.g. 3) and again take some notes.

**Questions to answer:**

- *Beginners*:
    - Which one is thicker (*Max ice thickness*)?
    - Which one is flowing faster (*Max ice velocity*)?
    - Which one reaches the equilibrium faster (*Time*)?
- *Advanced*:
    - How are *Length*, *Area* and *Volume* effected?

..  admonition:: Take home messages
    :class: toggle

    - the larger the Mass-Balance gradient the larger the accumulation of mass (ice) at the top
    - more accumulation leads to a thicker glacier and a larger downslope component of the gravitational force (see `Glacier slope`_ experiment)
    - this larger force causes a larger ice flux and further a larger ice velocity
    - the larger the ice velocity the faster ice is transported downwards and the faster the equilibrium is reached
    - length and area are not much effected due to the unchanged **linear** Mass-Balance profile: no matter which gradient is selected the total ice gain/loss at a certain height is only determined by the distance away from the ELA (e.g. the same amount of mass is accumulated 100 m above the ELA as there is mass ablated 100 m below the ELA, with a constant width)
    - whereas the volume is increasing with a increasing Mass-Balance gradient due to a larger ice thickness

AAR (Accumulation Area Ratio)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The AAR is the ratio of the accumulation area (= area above ELA) to the total glacier area. Lets make some experiments to see what the AAR can tell us about glaciers. Note for the interpretation of the experiments that the total ice gain/loss at a certain height equals the Mass-Balance (black line in top right figure) times the area (resp. width) at the same height.

**Experiments:**

- *Beginners*: Use "Beginner mode" and conduct runs with *Width* = *Constant* and *Width* = *Wide top, narrow bottom* and note down the different AARs (*ELA* = 3300, *Mass-Balance gradient* = 4, *Slope* = 11°).
- *Advanced*: Conduct experiments with *Constant* width and different Mass-Balance gradients (e.g. *Mass-Balance gradient below ELA* = 4, *Mass-Balance gradient above ELA* = 2 and vice versa) in "Advanced mode". Note down the different AARs.

**Questions to answer:**

- *Beginners*:
    - Explaine the observed AARs for *Constant* width and for *Wide top, narrow bottom*?
    - For *Constant* width what values of AAR (below or above 0.5) do you expect for a advancing and a retreating glacier?
- *Advanced*:
    - How is the AAR changing with a different Mass-Balance gradients below and above the ELA?
    - What can you conclulde from the experiments for real valley glaciers when assuming an AAR between 0.5 and 0.8 for a glacier in equilibrium (see for example `Hawkins 1985 <https://www.cambridge.org/core/journals/journal-of-glaciology/article/equilibriumline-altitudes-and-paleoenvironment-in-the-merchants-bay-area-baffin-island-nwt-canada/21991E0893BCCF88D611103F397D73D1>`_)?

..  admonition:: Take home messages
    :class: toggle

    - *Beginners*:
        - In the case with *Constant* width and a linear Mass-Balance the AAR is around 0.5. The total ice gain/loss at a certain height is only determined by the distance away from the ELA (e.g. the same amount of mass is accumulated 100 m above the ELA as there is mass ablated 100 m below the ELA) and so the glacier area above the ELA equals approx. the glacier area below.
        - In the case with *Wide top, narrow bottom* and a linear Mass-Balance the AAR is around 0.6. In this case the total ice gain/loss at a certain height is not only determined by the distance away from the ELA but also from the width at a certain height (e.g. if the width 100 m above the ELA is double the width of 100 m below the ELA also the total ice gain is double of the total ice loss). In this case the glacier length is longer compared with the case of constant width and in the lower altitudes the more negative Mass-Balance lead to more melting ice. Overall the ablation area (area below ELA) stays smaller than the accumulation area, even with a longer glacier.
        - For a advancing glacier with constant width the AAR is well above 0.5, and in the retreating case well below 0.5.
    - *Advanced*:
        - With a Mass-Balance gradient below ELA twice the gradient above the ELA also the total ice loss is twice the total ice gain going the same distance away from the ELA. With this the ablation area (area below ELA) only needs to be half of the accumulation area. For the AAR this means a value of approx. 0.6 (AAR = Ablation Area / Total Area = Ablation Area / (Accumulation Area + Ablation Area) = Ablation Area / (0.5 * Ablation Area + Ablation Area) = 1 / 1.5 = 2 / 3).
        - For real glaciers in equilibrium with AAR between 0.5 and 0.8 we can assume wider tops and larger Mass-Balance gradients below the ELA

Balance Ratio, in the footsteps of a paleoclimatologist
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this experiment we are using knowledge of Balance Ratios to estimate the height of the ELA (and past climate conditions). The Balance Ratio is defined as the ratio of the Mass-Balance gradient below the ELA to the Mass-Balance gradient above the ELA (e.g. *Mass-Balance gradient below the ELA* = 4 and *Mass-Balance gradient above the ELA* = 2 gives a Balance Ratio of 2). See `antarcticglaciers.org (mass-balance)`_ for an introduction about glacier mass-balance and the ELA, or our
:ref:`glacier_basics` graphics for an illustration.

In short: the height of the ELA is determined among other things by the temperature. In a warming climate the ELA is increasing in height.

**Experiment:**

    - You made expeditions to the European Alps and Kamchatka to find two glacier areas of the last glaciological maximum, by using landmarks (e.g. abrasive erosion, moraines, ...). You want to use this two past glacier areas to approximate the ELA height and compare the past climates (note that this experiment is only fictional).
    - For the European Alps glacier you found an approximated past area of 3 km². The glacier geometry is a *Linear* bedrock profile with a slope of 11° and *wide top, narrow bottom* width along the glacier.
    - For the Kamchatka glacier the past area was also approx. 3 km². This glacier is *getting flatter* (bedrock profile) and *getting narrower* (width along glacier).
    - You know that a typical Balance Ratio for the European Alps is around 1.5 and for the Kamchatka around 3 (e.g. `Rea 2009 <https://www.sciencedirect.com/science/article/abs/pii/S0277379108002989?via%3Dihub>`_).

**Questions:**
    - Use the simulator to find the corresponding past ELAs.
    - Which glacier do you think was located in a warmer environment?
    - How do different absolute values of the Mass-Balance gradients change your result?
    - What additional information would be usefull to find absolute values of the gradients?

..  admonition:: Take home messages
    :class: toggle

    - Alps ELA = 3100 and Kamchatka ELA = 2000
    - From the ELA heights one can conlculde that the past (fictional) climate in the Alps was warmer than in Kamchatka.
    - Different magnitudes of the Mass-Balance gradients do not change the results a lot.
    - Additional information about the maximum thickness could help to find absolute gradient values.

.. _antarcticglaciers.org (mass-balance): http://www.antarcticglaciers.org/glacier-processes/introduction-glacier-mass-balance
.. _antarcticglaciers.org (glacier-flow): http://www.antarcticglaciers.org/glacier-processes/glacier-flow-2/glacier-flow
.. _World Glaciers Explorer: https://edu.oggm.org/en/latest/explorer.html
.. _Glacier slope: https://edu.oggm.org/en/latest/simulator.html#glacier-slope
.. _`antarcticglaciers.org (surging-glaciers)`: http://www.antarcticglaciers.org/glacier-processes/glacier-flow-2/surging-glaciers/
.. _`this video`: http://cdn.antarcticglaciers.org/wp-content/uploads/2012/10/Panmah_and_Choktoi_glaciers_large.gif

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
