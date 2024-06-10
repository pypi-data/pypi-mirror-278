# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import datetime

from dtu_config import __version__

# -- Project information -----------------------------------------------------

project = "dtu_config"
copyright = str(datetime.datetime.now().year) + ", DTU Wind Energy"
author = "<AUTHORS>"

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = __version__
# The full version, including alpha/beta/rc tags
release = __version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.imgmath",
    # Allow inclusion of dot graphics
    "sphinx.ext.graphviz",
    # Document across sphinx instances
    "sphinx.ext.intersphinx",
    # Use Numpy or Google docstrings
    "sphinx.ext.napoleon",
    # Add links to sourcecode
    "sphinx.ext.viewcode",
    # Create a table with documentation
    "sphinx.ext.autosummary",
    # Document command line tools
    "sphinxarg.ext",
]

# Custom configuration for autosummary
autosummary_generate = True
imported_members = True


# Custom configuration of coverage
coverage_skip_undoc_in_source = False
coverage_write_headline = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Mapping to include common python libraries
intersphinx_mapping = {
    "numpy": ("https://docs.scipy.org/doc/numpy-1.16.0", None),
    "python": ("https://docs.python.org/3.8", None),
}
