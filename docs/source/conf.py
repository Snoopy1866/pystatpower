# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys
from pathlib import Path

sys.path.insert(0, str(Path("../..", "src").resolve()))

import pystatpower

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "PyStatPower"
copyright = "%Y, Snoopy1866"
author = "Snoopy1866"
version = release = pystatpower.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx_copybutton",
    "sphinx_issues",
    "sphinx_togglebutton",
    "autodoc2",
    "myst_parser",
    "notfound.extension",
    "sphinx_tippy",
]

maximum_signature_line_length = 79

templates_path = ["_templates"]
exclude_patterns = []

language = "en"

nitpicky = True

# -- Options for sphinx.ext.autodoc ------------------------------------------
autoclass_content = "class"
autodoc_class_signature = "mixed"
autodoc_member_order = "bysource"

# -- Options for sphinx.ext.napoleon -----------------------------------------
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_rtype = False
napoleon_preprocess_types = True

# -- Options for sphinx.ext.intersphinx --------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master", None),
}

# -- Options for sphinx_issues -----------------------------------------------
issues_github_path = "PyStatPower/PyStatPower"

# -- Options for autodoc2 ----------------------------------------------------
autodoc2_packages = [
    {
        "path": "../../src/pystatpower",
        "auto_mode": False,
    },
]
autodoc2_docstring_parser_regexes = [
    (r".*", "myst"),
]
autodoc2_output_dir = "api"

# -- Options for myst_parser -------------------------------------------------
myst_enable_extensions = [
    "colon_fence",
    "dollarmath",
    "tasklist",
]
myst_heading_anchors = 3

# --Options for sphinx_tippy -------------------------------------------------
tippy_props = {
    "theme": "light",
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_static_path = ["_static"]

html_theme = "sphinx_book_theme"
html_theme_options = {
    "repository_url": "https://github.com/PyStatPower/PyStatPower",
    "repository_branch": "main",
    "path_to_docs": "docs",
    "use_repository_button": True,
    "use_issues_button": True,
    "use_edit_page_button": True,
    "use_download_button": True,
}
html_css_files = ["tippy.css"]
