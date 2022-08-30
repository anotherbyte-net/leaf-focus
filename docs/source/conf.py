# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
# Problems with imports? Could try `export PYTHONPATH=$PYTHONPATH:`pwd`` from root project dir...
import os
import sys

# Source code dir relative to this file
sys.path.insert(0, os.path.abspath("../../src"))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Leaf Focus"
copyright = "2022, Mark C-F"
author = "Mark C-F"
release = "0.1a1"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    # Core Sphinx library for auto html doc generation from docstrings
    "sphinx.ext.autodoc",
    # Create neat summary tables for modules/classes/methods etc
    "sphinx.ext.autosummary",
    # Link to other project's documentation (see mapping below)
    "sphinx.ext.intersphinx",
    # Add a link to the Python source code for classes, functions etc.
    "sphinx.ext.viewcode",
    # Automatically document param types (less noise in class signature)
    "sphinx_autodoc_typehints",
    # allow using markdown
    "myst_parser",
]

# Mappings for sphinx.ext.intersphinx. Projects have to have Sphinx-generated doc! (.inv file)
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
}
# Turn on sphinx.ext.autosummary
autosummary_generate = True

# Add __init__ doc (ie. params) to class summaries
autoclass_content = "both"

# Remove 'view source code' from top of page (for html, not python)
html_show_sourcelink = False

# If no docstring, inherit from base class
autodoc_inherit_docstrings = True

# Enable 'expensive' imports for sphinx_autodoc_typehints
set_type_checking_flag = True

# Sphinx-native method. Not as good as sphinx_autodoc_typehints
# autodoc_typehints = "description"

# Remove namespaces from class/method signatures
add_module_names = False

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
