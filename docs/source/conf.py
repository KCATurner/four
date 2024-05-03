# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys
sys.path.insert(0, os.path.abspath('../..'))
sys.path.insert(0, os.path.abspath('../../four'))


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Four'
copyright = '2023'
author = 'Kevin Turner'
release = '0.0'


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.napoleon',
    'sphinx.ext.autodoc',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'sphinx.ext.graphviz',
    'sphinx.ext.imgmath',
    'sphinx.ext.autosummary',
    'sphinxcontrib.autoprogram',
    'sphinx_rtd_theme',
]

templates_path = ['_templates']
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
thml_theme_options = {
    'navigation_depth': -1,
}


# -- Extension configuration -------------------------------------------------

todo_include_todos = True
graphviz_output_format = 'svg'
imgmath_image_format = 'svg'
imgmath_latex_preamble = r'\usepackage{newtxsf}'
autosummary_generate = True
autosummary_generate_overwrite = True
autoclass_content = 'both'
autodoc_module_first = True
autodoc_typehints = 'both'
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'no-value': True,
}


def setup(app):
    # for wrapping long table cells.
    app.add_css_file('custom.css')
