# -*- coding: utf-8 -*-
#
# OGGM-Edu documentation build configuration file, created by
# sphinx-quickstart on Tue Oct 23 11:26:03 2018.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys
import os
import shutil
import datetime


print("python version:", sys.version)
print("python exec:", sys.executable)
print("sys.path:", sys.path)
try:
    import IPython
    print("ipython: %s, %s" % (IPython.__version__, IPython.__file__))
except ImportError:
    print("no ipython")
try:
    import numpy
    print("numpy: %s, %s" % (numpy.__version__, numpy.__file__))
except ImportError:
    print("no numpy")
try:
    import scipy
    print("scipy: %s, %s" % (scipy.__version__, scipy.__file__))
except ImportError:
    print("no scipy")
try:
    import pandas
    print("pandas: %s, %s" % (pandas.__version__, pandas.__file__))
except ImportError:
    print("no pandas")
try:
    import geopandas
    print("geopandas: %s, %s" % (geopandas.__version__, geopandas.__file__))
except ImportError:
    print("no geopandas")
try:
    import xarray
    print("xarray: %s, %s" % (xarray.__version__, xarray.__file__))
except ImportError:
    print("no xarray")
try:
    import matplotlib
    matplotlib.use('Agg')
    print("matplotlib: %s, %s" % (matplotlib.__version__, matplotlib.__file__))
except ImportError:
    print("no matplotlib")
try:
    import rasterio
    print("rasterio: %s, %s" % (rasterio.__version__, rasterio.__file__))
except ImportError:
    print("no rasterio")
try:
    import gdal
    import osgeo.gdal
    print("gdal: %s, %s" % (osgeo.gdal.__version__, gdal.__file__))
except ImportError:
    print("no gdal")
try:
    import pyproj
    print("pyproj: %s, %s" % (pyproj.__version__, pyproj.__file__))
except ImportError:
    print("no pyproj")
try:
    import netCDF4
    print("netCDF4: %s, %s" % (netCDF4.__version__, netCDF4.__file__))
except ImportError:
    print("no netCDF4")
try:
    import skimage
    print("skimage: %s, %s" % (skimage.__version__, skimage.__file__))
except ImportError:
    print("no skimage")

# Remove some warnings
try:
    import warnings
    from fiona.errors import FionaDeprecationWarning
    warnings.filterwarnings('ignore', category=FionaDeprecationWarning)
except ImportError:
    pass

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx.ext.extlinks',
    'sphinx.ext.mathjax',
    'numpydoc',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'IPython.sphinxext.ipython_directive',
    'IPython.sphinxext.ipython_console_highlighting',
]

extlinks = {'issue': ('https://github.com/OGGM/oggm-edu/issues/%s', 'GH'),
            'pull': ('https://github.com/OGGM/oggm-edu/pull/%s', 'PR'),
            }

autosummary_generate = True

numpydoc_class_members_toctree = True
numpydoc_show_class_members = False

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The encoding of source files.
# source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'OGGM-Edu'
copyright = u'2018, OGGM Developers'
author = u'OGGM Developers'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = u'0.1'
# The full version, including alpha/beta/rc tags.
release = u'0.1a'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
# today = ''
# Else, today_fmt is used as the format for a strftime call.
# today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']

# The reST default role (used for this markup: `text`) to use for all
# documents.
# default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
# add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
# add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
# show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
# modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
# keep_warnings = False

# If true, `todo` and `todoList` produce output, else they produce nothing.
# todo_include_todos = True


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    'logo_only': True,
    'display_version': False,
}

# Add any paths that contain custom themes here, relative to this directory.
# html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
# html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = '_static/logo.png'

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = '_static/favicon.ico'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
html_extra_path = ['gallery-app_en.html', 'gallery-app_de.html', 'alps_future-app.html']

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
# html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
# html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
# html_additional_pages = {}

# If false, no module index is generated.
# html_domain_indices = True

# If false, no index is generated.
# html_use_index = True

# If true, the index is split into individual pages for each letter.
# html_split_index = False

# If true, links to the reST sources are added to the pages.
# html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
# html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
# html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
# html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
# html_file_suffix = None

# Language to be used for generating the HTML full-text search index.
# Sphinx supports the following languages:
#   'da', 'de', 'en', 'es', 'fi', 'fr', 'h', 'it', 'ja'
#   'nl', 'no', 'pt', 'ro', 'r', 'sv', 'tr'
# html_search_language = 'en'

# A dictionary with options for the search language support, empty by default.
# Now only 'ja' uses this config value
# html_search_options = {'type': 'default'}

# The name of a javascript file (relative to the configuration directory) that
# implements a search results scorer. If empty, the default will be used.
# html_search_scorer = 'scorer.js'

# Output file base name for HTML help builder.
htmlhelp_basename = 'OGGM-Edudoc'

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    # 'preamble': '',

    # Latex figure (float) alignment
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'OGGM-Edu.tex', u'OGGM-Edu Documentation',
     u'OGGM Developers', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
# latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
# latex_use_parts = False

# If true, show page references after internal links.
# latex_show_pagerefs = False

# If true, show URL addresses after external links.
# latex_show_urls = False

# Documents to append as an appendix to all manuals.
# latex_appendices = []

# If false, no module index is generated.
# latex_domain_indices = True


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'oggm-edu', u'OGGM-Edu Documentation',
     [author], 1)
]

# If true, show URL addresses after external links.
# man_show_urls = False


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'OGGM-Edu', u'OGGM-Edu Documentation',
     author, 'OGGM-Edu', 'One line description of project.',
     'Miscellaneous'),
]

# Documents to append as an appendix to all manuals.
#texinfo_appendices = []

# If false, no module index is generated.
#texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
#texinfo_show_urls = 'footnote'

# If true, do not generate a @detailmenu in the "Top" node's menu.
#texinfo_no_detailmenu = False


# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {}

# Will be included at the beginning of every source file that is read.
rst_prolog = """

.. |badge_bokeh_en| image::  https://img.shields.io/badge/launch-bokeh%20app-579ACA.svg?style=popout&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAC4jAAAuIwF4pT92AAAAB3RJTUUH4wEeDC0U4ki9ZgAAABl0RVh0Q29tbWVudABDcmVhdGVkIHdpdGggR0lNUFeBDhcAAAQFSURBVFjD7ZddaBxVGIafc2Y22+1u0qSxyaZJbBMTxLapUseUIsWWWrRIFhYL9bfgjdirQgX1qhUUb7zwQnqhghZ7IYo4MKJoo1YUtcQxlTRpWkyWGEp+l+zmZ5vs7swcL9yENeruxhi9yXc358z5nvfM9853ZgT/X/gAyXqsx3r8W2FHI9jRyNpDll1X2dFIVbH7CoVYCdgwLexoZA/wDHA34M/lSAE9wNuGaX2/fM2qBCyDnwFOCKU2S9fxCaUAUEKgpHQ8qc0BJvC8YVqTpYjQS3kCOfgrwEnheRvnqrYwuHMv09V1eEISnE2wdahfDw9fr9SczFNKyDvsaOSYYVrDxcohiu0+Bz8CnBeeVz1y2y6utD+AEmIpgRDgIqkeH2aH/QWhZBwl5SfAE4ZpJRfzrMYDF4XnHUjUNtJ16BgqN66UIlxVjtFSzzd9Q0ylXcKjMXb+2MnG2SRKiCeB9wzTcv8utywBbgBNUnn07zmIAny6JBTwo3DZFMpyZ3MYo7Uezc0y1thKvK4JT2oAJ4CyQvlLOQ7bhPJCc5XVpCo2A3BPawOHdjdzIxHj3LdnSaQSNIcrqa0MQNYhXredrD8ASrUX81kpAiqFUr754CZQCp8uOdDWREt9JRv8ccaTE3THekllphhJ/oLrZkgHQniatmhyXyEjliIgpRBuWXoeIXXiswN0DXTj18t45N7DzMyn+CnWw+R0nK7YV8RTN/C5DsLzFterQslLeQ17lBSp8mS8SkyPcmHwQ77sf58zR0/RUL0Vv17G11d/YDw5yeDENbRAI/uSG9CzGRBiCEivqg8YpnXJjkauStdtaLjcyUJgBkcpXvroNVrDzWRdh9j4rwyMDZERkBnto2LMh8/J4sEHgPOPPbBUOyFedGGiZXyC44kgITTG5mf4bqAbD3AFpHVBrSrjyMgs4dk5FGoGOA9kCjG0EpqQnPn5cnzLQx1pJx4/uH1earendSrQUJpECMEtjmTfTT8PJwPctVCGD4GCU8Dnhml5djTCm9eul16CZa49Wb6r7bi/pubizWDwsDY9/fKOBX3/toxGSvrJCtAUBD1ByBMACwpeAM4ZpuUUOwtEkd13AK8D24TuQ7nOgyhlA3sFPAbsB27NOT2m4GPgXeDKIrxQG/5LAXnw3cBbQHtuqhe4zzCtKTsakbnvej3PRx6QBbKGaalS4H8SkAevAc4CR3NTidxu+4olXMm3wJKAfKV2NBIATvN7HRcbSQfwqWFaqpRdrSTkMuUSeDwPDvAscGEt4AAy77EL4H7g1bz5N4B3DNPKrgX8Dx6wo5Fm4DOgNTfUCTxtmNbQWsGXSpAzTSivL/QCp9caDqDnAXrsaORR4DnAMkzr0n/xP/Ebgv/Oed8KI9UAAAAASUVORK5CYII=

.. |badge_bokeh_de| image::  https://img.shields.io/badge/bokeh%20app-starten-579ACA.svg?style=popout&logo=     data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAC4jAAAuIwF4pT92AAAAB3RJTUUH4wEeDC0U4ki9ZgAAABl0RVh0Q29tbWVudABDcmVhdGVkIHdpdGggR0lNUFeBDhcAAAQFSURBVFjD7ZddaBxVGIafc2Y22+1u0qSxyaZJbBMTxLapUseUIsWWWrRIFhYL9bfgjdirQgX1qhUUb7zwQnqhghZ7IYo4MKJoo1YUtcQxlTRpWkyWGEp+l+zmZ5vs7swcL9yENeruxhi9yXc358z5nvfM9853ZgT/X/gAyXqsx3r8W2FHI9jRyNpDll1X2dFIVbH7CoVYCdgwLexoZA/wDHA34M/lSAE9wNuGaX2/fM2qBCyDnwFOCKU2S9fxCaUAUEKgpHQ8qc0BJvC8YVqTpYjQS3kCOfgrwEnheRvnqrYwuHMv09V1eEISnE2wdahfDw9fr9SczFNKyDvsaOSYYVrDxcohiu0+Bz8CnBeeVz1y2y6utD+AEmIpgRDgIqkeH2aH/QWhZBwl5SfAE4ZpJRfzrMYDF4XnHUjUNtJ16BgqN66UIlxVjtFSzzd9Q0ylXcKjMXb+2MnG2SRKiCeB9wzTcv8utywBbgBNUnn07zmIAny6JBTwo3DZFMpyZ3MYo7Uezc0y1thKvK4JT2oAJ4CyQvlLOQ7bhPJCc5XVpCo2A3BPawOHdjdzIxHj3LdnSaQSNIcrqa0MQNYhXredrD8ASrUX81kpAiqFUr754CZQCp8uOdDWREt9JRv8ccaTE3THekllphhJ/oLrZkgHQniatmhyXyEjliIgpRBuWXoeIXXiswN0DXTj18t45N7DzMyn+CnWw+R0nK7YV8RTN/C5DsLzFterQslLeQ17lBSp8mS8SkyPcmHwQ77sf58zR0/RUL0Vv17G11d/YDw5yeDENbRAI/uSG9CzGRBiCEivqg8YpnXJjkauStdtaLjcyUJgBkcpXvroNVrDzWRdh9j4rwyMDZERkBnto2LMh8/J4sEHgPOPPbBUOyFedGGiZXyC44kgITTG5mf4bqAbD3AFpHVBrSrjyMgs4dk5FGoGOA9kCjG0EpqQnPn5cnzLQx1pJx4/uH1earendSrQUJpECMEtjmTfTT8PJwPctVCGD4GCU8Dnhml5djTCm9eul16CZa49Wb6r7bi/pubizWDwsDY9/fKOBX3/toxGSvrJCtAUBD1ByBMACwpeAM4ZpuUUOwtEkd13AK8D24TuQ7nOgyhlA3sFPAbsB27NOT2m4GPgXeDKIrxQG/5LAXnw3cBbQHtuqhe4zzCtKTsakbnvej3PRx6QBbKGaalS4H8SkAevAc4CR3NTidxu+4olXMm3wJKAfKV2NBIATvN7HRcbSQfwqWFaqpRdrSTkMuUSeDwPDvAscGEt4AAy77EL4H7g1bz5N4B3DNPKrgX8Dx6wo5Fm4DOgNTfUCTxtmNbQWsGXSpAzTSivL/QCp9caDqDnAXrsaORR4DnAMkzr0n/xP/Ebgv/Oed8KI9UAAAAASUVORK5CYII=

.. |badge_edu_notebooks| image:: https://img.shields.io/badge/launch-Edu%20Notebooks-579ACA.svg?style=popout&logo=     data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAC4jAAAuIwF4pT92AAAAB3RJTUUH4wEeDC0U4ki9ZgAAABl0RVh0Q29tbWVudABDcmVhdGVkIHdpdGggR0lNUFeBDhcAAAQFSURBVFjD7ZddaBxVGIafc2Y22+1u0qSxyaZJbBMTxLapUseUIsWWWrRIFhYL9bfgjdirQgX1qhUUb7zwQnqhghZ7IYo4MKJoo1YUtcQxlTRpWkyWGEp+l+zmZ5vs7swcL9yENeruxhi9yXc358z5nvfM9853ZgT/X/gAyXqsx3r8W2FHI9jRyNpDll1X2dFIVbH7CoVYCdgwLexoZA/wDHA34M/lSAE9wNuGaX2/fM2qBCyDnwFOCKU2S9fxCaUAUEKgpHQ8qc0BJvC8YVqTpYjQS3kCOfgrwEnheRvnqrYwuHMv09V1eEISnE2wdahfDw9fr9SczFNKyDvsaOSYYVrDxcohiu0+Bz8CnBeeVz1y2y6utD+AEmIpgRDgIqkeH2aH/QWhZBwl5SfAE4ZpJRfzrMYDF4XnHUjUNtJ16BgqN66UIlxVjtFSzzd9Q0ylXcKjMXb+2MnG2SRKiCeB9wzTcv8utywBbgBNUnn07zmIAny6JBTwo3DZFMpyZ3MYo7Uezc0y1thKvK4JT2oAJ4CyQvlLOQ7bhPJCc5XVpCo2A3BPawOHdjdzIxHj3LdnSaQSNIcrqa0MQNYhXredrD8ASrUX81kpAiqFUr754CZQCp8uOdDWREt9JRv8ccaTE3THekllphhJ/oLrZkgHQniatmhyXyEjliIgpRBuWXoeIXXiswN0DXTj18t45N7DzMyn+CnWw+R0nK7YV8RTN/C5DsLzFterQslLeQ17lBSp8mS8SkyPcmHwQ77sf58zR0/RUL0Vv17G11d/YDw5yeDENbRAI/uSG9CzGRBiCEivqg8YpnXJjkauStdtaLjcyUJgBkcpXvroNVrDzWRdh9j4rwyMDZERkBnto2LMh8/J4sEHgPOPPbBUOyFedGGiZXyC44kgITTG5mf4bqAbD3AFpHVBrSrjyMgs4dk5FGoGOA9kCjG0EpqQnPn5cnzLQx1pJx4/uH1earendSrQUJpECMEtjmTfTT8PJwPctVCGD4GCU8Dnhml5djTCm9eul16CZa49Wb6r7bi/pubizWDwsDY9/fKOBX3/toxGSvrJCtAUBD1ByBMACwpeAM4ZpuUUOwtEkd13AK8D24TuQ7nOgyhlA3sFPAbsB27NOT2m4GPgXeDKIrxQG/5LAXnw3cBbQHtuqhe4zzCtKTsakbnvej3PRx6QBbKGaalS4H8SkAevAc4CR3NTidxu+4olXMm3wJKAfKV2NBIATvN7HRcbSQfwqWFaqpRdrSTkMuUSeDwPDvAscGEt4AAy77EL4H7g1bz5N4B3DNPKrgX8Dx6wo5Fm4DOgNTfUCTxtmNbQWsGXSpAzTSivL/QCp9caDqDnAXrsaORR4DnAMkzr0n/xP/Ebgv/Oed8KI9UAAAAASUVORK5CYII=
    :target: https://mybinder.org/v2/gh/OGGM/binder/master?urlpath=git-pull?repo=https://github.com/OGGM/oggm-edu-notebooks%26amp%3Bbranch=master%26amp%3Burlpath=lab/tree/oggm-edu-notebooks/oggm-edu/welcome.ipynb%3Fautodecode

.. |badge_edu_intro_notebooks| image:: https://img.shields.io/badge/launch-Edu%20Notebooks-579ACA.svg?style=popout&logo=     data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAC4jAAAuIwF4pT92AAAAB3RJTUUH4wEeDC0U4ki9ZgAAABl0RVh0Q29tbWVudABDcmVhdGVkIHdpdGggR0lNUFeBDhcAAAQFSURBVFjD7ZddaBxVGIafc2Y22+1u0qSxyaZJbBMTxLapUseUIsWWWrRIFhYL9bfgjdirQgX1qhUUb7zwQnqhghZ7IYo4MKJoo1YUtcQxlTRpWkyWGEp+l+zmZ5vs7swcL9yENeruxhi9yXc358z5nvfM9853ZgT/X/gAyXqsx3r8W2FHI9jRyNpDll1X2dFIVbH7CoVYCdgwLexoZA/wDHA34M/lSAE9wNuGaX2/fM2qBCyDnwFOCKU2S9fxCaUAUEKgpHQ8qc0BJvC8YVqTpYjQS3kCOfgrwEnheRvnqrYwuHMv09V1eEISnE2wdahfDw9fr9SczFNKyDvsaOSYYVrDxcohiu0+Bz8CnBeeVz1y2y6utD+AEmIpgRDgIqkeH2aH/QWhZBwl5SfAE4ZpJRfzrMYDF4XnHUjUNtJ16BgqN66UIlxVjtFSzzd9Q0ylXcKjMXb+2MnG2SRKiCeB9wzTcv8utywBbgBNUnn07zmIAny6JBTwo3DZFMpyZ3MYo7Uezc0y1thKvK4JT2oAJ4CyQvlLOQ7bhPJCc5XVpCo2A3BPawOHdjdzIxHj3LdnSaQSNIcrqa0MQNYhXredrD8ASrUX81kpAiqFUr754CZQCp8uOdDWREt9JRv8ccaTE3THekllphhJ/oLrZkgHQniatmhyXyEjliIgpRBuWXoeIXXiswN0DXTj18t45N7DzMyn+CnWw+R0nK7YV8RTN/C5DsLzFterQslLeQ17lBSp8mS8SkyPcmHwQ77sf58zR0/RUL0Vv17G11d/YDw5yeDENbRAI/uSG9CzGRBiCEivqg8YpnXJjkauStdtaLjcyUJgBkcpXvroNVrDzWRdh9j4rwyMDZERkBnto2LMh8/J4sEHgPOPPbBUOyFedGGiZXyC44kgITTG5mf4bqAbD3AFpHVBrSrjyMgs4dk5FGoGOA9kCjG0EpqQnPn5cnzLQx1pJx4/uH1earendSrQUJpECMEtjmTfTT8PJwPctVCGD4GCU8Dnhml5djTCm9eul16CZa49Wb6r7bi/pubizWDwsDY9/fKOBX3/toxGSvrJCtAUBD1ByBMACwpeAM4ZpuUUOwtEkd13AK8D24TuQ7nOgyhlA3sFPAbsB27NOT2m4GPgXeDKIrxQG/5LAXnw3cBbQHtuqhe4zzCtKTsakbnvej3PRx6QBbKGaalS4H8SkAevAc4CR3NTidxu+4olXMm3wJKAfKV2NBIATvN7HRcbSQfwqWFaqpRdrSTkMuUSeDwPDvAscGEt4AAy77EL4H7g1bz5N4B3DNPKrgX8Dx6wo5Fm4DOgNTfUCTxtmNbQWsGXSpAzTSivL/QCp9caDqDnAXrsaORR4DnAMkzr0n/xP/Ebgv/Oed8KI9UAAAAASUVORK5CYII=
    :target: https://mybinder.org/v2/gh/OGGM/binder/master?urlpath=git-pull?repo=https://github.com/OGGM/oggm-edu-notebooks%26amp%3Bbranch=master%26amp%3Burlpath=lab/tree/oggm-edu-notebooks/oggm-edu/getting_started_with_notebooks.ipynb%3Fautodecode

.. |badge_tutorial_notebooks| image:: https://img.shields.io/badge/Launch-OGGM%20tutorials-579ACA.svg?style=popout&logo=data:image/png;base64,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
    :target: https://mybinder.org/v2/gh/OGGM/binder/master?urlpath=git-pull?repo=https://github.com/OGGM/oggm-edu-notebooks%26amp%3Bbranch=master%26amp%3Burlpath=lab/tree/oggm-edu-notebooks/oggm-tuto/welcome.ipynb%3Fautodecode

.. |badge_hub| image:: https://img.shields.io/badge/Launch-OGGM%20hub-F37524.svg?style=popout&logo=data:image/png;base64,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
    :target: https://hub.oggm.org
"""

# Add toggle container https://stackoverflow.com/questions/2454577/sphinx-restructuredtext-show-hide-code-snippets
def setup(app):
    app.add_stylesheet('custom.css')
