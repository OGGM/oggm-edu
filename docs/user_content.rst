.. _user_content:

Use your own content in OGGM-Edu
================================

Ideally, we would like all the educational content to be bundled here, on this
open platform. However, you might be interested in running your own notebooks
in an OGGM-Edu environment, for example during the development phase, or
for a very specific class.

Fortunately, this is very easy to do! All you need to do is to provide the
notebooks you would like to run on MyBinder in an online git repository
(e.g. GitHub, Gitlab, Bitbucket). For example, we have created an
`oggm-edu-contrib <https://github.com/OGGM/oggm-edu-contrib>`_ with one single
notebook to get you started.

Once your notebooks are online, you simply have to provide the correct
link to your students. The syntax is following::

    https://mybinder.org/v2/gh/OGGM/oggm-edu-r2d/master?urlpath=git-pull?repo=<PATH/TO/YOUR/REPO>

For example, a link to our contrib repository looks like:

`<https://mybinder.org/v2/gh/OGGM/oggm-edu-r2d/master?urlpath=git-pull?repo=https://github.com/OGGM/oggm-edu-contrib>`_

What is happening here? The first part of the link (up to `?`) is telling
MyBinder to use the OGGM-Edu environment we are maintaining
`here <https://github.com/OGGM/oggm-edu-r2d>`_. The second part of the link
is using `nbgitpuller <https://jupyterhub.github.io/nbgitpuller/>`_ to fetch
the provided online repository and it's content. That's all!

This was the most basic example. If you want to use other features, like using
the Jupyter Lab interface (instead of the simple notebooks interface), and if
you want to start at an arbitrary location in the repository (for example
within a folder), the syntax is::


    https://mybinder.org/v2/gh/OGGM/oggm-edu-r2d/master?urlpath=git-pull?repo=<PATH/TO/YOUR/REPO>%26amp%3Burlpath=lab/tree/<YOUR_REPO_NAME>/<PATH/TO/FILE>%3Fautodecode

For example, we start the OGGM-Edu tutorials with this link:

`<https://mybinder.org/v2/gh/OGGM/oggm-edu-r2d/master?urlpath=git-pull?repo=https://github.com/OGGM/oggm-edu-notebooks%26amp%3Bbranch=master%26amp%3Burlpath=lab/tree/oggm-edu-notebooks/oggm-edu/welcome.ipynb%3Fautodecode>`_

It's getting quite long, I know! What's best therefore is to hide the links
`behind a badge <https://mybinder.readthedocs.io/en/latest/howto/badges.html>`_.
For example:

.. image:: https://img.shields.io/badge/launch-Edu%20Notebooks-579ACA.svg?style=popout&logo=     data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAC4jAAAuIwF4pT92AAAAB3RJTUUH4wEeDC0U4ki9ZgAAABl0RVh0Q29tbWVudABDcmVhdGVkIHdpdGggR0lNUFeBDhcAAAQFSURBVFjD7ZddaBxVGIafc2Y22+1u0qSxyaZJbBMTxLapUseUIsWWWrRIFhYL9bfgjdirQgX1qhUUb7zwQnqhghZ7IYo4MKJoo1YUtcQxlTRpWkyWGEp+l+zmZ5vs7swcL9yENeruxhi9yXc358z5nvfM9853ZgT/X/gAyXqsx3r8W2FHI9jRyNpDll1X2dFIVbH7CoVYCdgwLexoZA/wDHA34M/lSAE9wNuGaX2/fM2qBCyDnwFOCKU2S9fxCaUAUEKgpHQ8qc0BJvC8YVqTpYjQS3kCOfgrwEnheRvnqrYwuHMv09V1eEISnE2wdahfDw9fr9SczFNKyDvsaOSYYVrDxcohiu0+Bz8CnBeeVz1y2y6utD+AEmIpgRDgIqkeH2aH/QWhZBwl5SfAE4ZpJRfzrMYDF4XnHUjUNtJ16BgqN66UIlxVjtFSzzd9Q0ylXcKjMXb+2MnG2SRKiCeB9wzTcv8utywBbgBNUnn07zmIAny6JBTwo3DZFMpyZ3MYo7Uezc0y1thKvK4JT2oAJ4CyQvlLOQ7bhPJCc5XVpCo2A3BPawOHdjdzIxHj3LdnSaQSNIcrqa0MQNYhXredrD8ASrUX81kpAiqFUr754CZQCp8uOdDWREt9JRv8ccaTE3THekllphhJ/oLrZkgHQniatmhyXyEjliIgpRBuWXoeIXXiswN0DXTj18t45N7DzMyn+CnWw+R0nK7YV8RTN/C5DsLzFterQslLeQ17lBSp8mS8SkyPcmHwQ77sf58zR0/RUL0Vv17G11d/YDw5yeDENbRAI/uSG9CzGRBiCEivqg8YpnXJjkauStdtaLjcyUJgBkcpXvroNVrDzWRdh9j4rwyMDZERkBnto2LMh8/J4sEHgPOPPbBUOyFedGGiZXyC44kgITTG5mf4bqAbD3AFpHVBrSrjyMgs4dk5FGoGOA9kCjG0EpqQnPn5cnzLQx1pJx4/uH1earendSrQUJpECMEtjmTfTT8PJwPctVCGD4GCU8Dnhml5djTCm9eul16CZa49Wb6r7bi/pubizWDwsDY9/fKOBX3/toxGSvrJCtAUBD1ByBMACwpeAM4ZpuUUOwtEkd13AK8D24TuQ7nOgyhlA3sFPAbsB27NOT2m4GPgXeDKIrxQG/5LAXnw3cBbQHtuqhe4zzCtKTsakbnvej3PRx6QBbKGaalS4H8SkAevAc4CR3NTidxu+4olXMm3wJKAfKV2NBIATvN7HRcbSQfwqWFaqpRdrSTkMuUSeDwPDvAscGEt4AAy77EL4H7g1bz5N4B3DNPKrgX8Dx6wo5Fm4DOgNTfUCTxtmNbQWsGXSpAzTSivL/QCp9caDqDnAXrsaORR4DnAMkzr0n/xP/Ebgv/Oed8KI9UAAAAASUVORK5CYII=
    :target: https://mybinder.org/v2/gh/OGGM/oggm-edu-r2d/master?urlpath=git-pull?repo=https://github.com/OGGM/oggm-edu-notebooks%26amp%3Bbranch=master%26amp%3Burlpath=lab/tree/oggm-edu-notebooks/oggm-edu/welcome.ipynb%3Fautodecode

If you are making educational resources based on OGGM-Edu, please :ref:`title_contact`!
