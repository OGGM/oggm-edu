Contributing to the documentation
=================================

Contributing to the documentation is of huge value. Something as simple as
rewriting small passages for clarity is a simple but effective way to
contribute.

About the documentation
-----------------------

The documentation is written in **reStructuredText**, which is almost like writing
in plain English, and built using `Sphinx <http://sphinx.pocoo.org/>`__. The
Sphinx Documentation has an excellent `introduction to reST
<http://sphinx.pocoo.org/rest.html>`__. Review the Sphinx docs to perform more
complex changes to the documentation as well.

How to build the documentation
------------------------------

Requirements
~~~~~~~~~~~~

There are some extra requirements to build the docs: you will need to
have ``sphinx``, ``sphinx-book-theme``, ``numpydoc`` and ``ipython`` installed.

We recommend to use conda (or mamba) to create an environment for oggm-edu. 
Create a text file called `oggm_edu_docs.yaml` with the following content 
in it::


  name: oggm_edu_docs
  channels:
    - conda-forge
  dependencies:
    - sphinx 
    - sphinx-book-theme
    - ipython
    - numpydoc
    - sphinx-intl

Then, from your `base` environment, do `mamba env create -f oggm_edu_docs.yml` 
(or `conda env create -f oggm_edu_docs.yml`). To activate the environment,
type: `conda activate oggm_edu_docs`.


Building the documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~

So how do you build the docs? Navigate to your local
``oggm-edu/docs/`` directory in the console and run::

    make html

Then you can find the HTML output in the folder ``oggm-edu/docs/_build/html/``.

The first time you build the docs, it might take a bit because it has to
run all the code examples and build all the generated docstring pages.
In subsequent evocations, sphinx will try to only build the pages that have
been modified.

If you want to do a full clean build, do::

    make clean
    make html

Open the following file in a web browser to see the full documentation you
just built::

    oggm-edu/docs/_build/html/index.html

And you'll have the satisfaction of seeing your new and improved documentation!

Update the translation files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

OGGM-Edu is available in other languages (although almost nothing is translated yet). 

Each time OGGM-Edu is updated in english, it is wize to also update the translation 
files (`.po`) files. After a `make html` build, simply run the `translate.sh`
script from the same `oggm-edu/docs` folder: it will update the `.po` files 
accordingly. 


Build the website in one of the available languages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

German::

    sphinx-build -b html -t language_de . _build/de

French::

    sphinx-build -b html -t language_fr . _build/fr

Spanish::

    sphinx-build -b html -t language_es . _build/es
