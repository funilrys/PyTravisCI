# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath("../../"))

from setup import PACKAGE_NAME, comp


def get_version():
    """
    Extract the version from our package.
    """

    to_match = comp(r'VERSION\s=\s"(.*)"\n')
    extracted = to_match.findall(
        open(f"../../{PACKAGE_NAME}/__init__.py", encoding="utf-8").read()
    )[0]

    return ".".join([x for x in extracted.split(".") if x.isdigit()])


# -- Project information -----------------------------------------------------

project = PACKAGE_NAME
copyright = "2019, Nissar Chababy (@funilrys)"
author = "Nissar Chababy (@funilrys)"

# The full version, including alpha/beta/rc tags
release = get_version()


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.ifconfig",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
]

intersphinx_mapping = {
    "requests": ("http://docs.python-requests.org/en/latest", None),
    "python": ("https://docs.python.org/3/", None),
}

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

# Configure the todo extension
todo_include_todos = True
todo_link_only = True

# Configure the autodoc extension
autodoc_member_order = "'alphabetical"

# The master toctree document.
master_doc = 'index'
