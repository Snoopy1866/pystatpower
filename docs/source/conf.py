# Configuration file for the Sphinx documentation builder.

import os
import sys

sys.path.insert(0, os.path.abspath("../../src"))

import pystatpower

# -- Project information -----------------------------------------------------
project = "PyStatPower"
author = "Snoopy1866"
copyright = "%Y, Snoopy1866"
version = release = pystatpower.__version__

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.duration",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_copybutton",
    "sphinx_issues",
    "sphinx_tippy",
    "sphinx_togglebutton",
    "autodoc2",
    "myst_parser",
    "notfound.extension",
]

# internationalisation
language = "zh_CN"

# markup
trim_footnote_reference_space = True

# nitpicky mode
nitpicky = True

# templating
templates_path = ["_templates"]


# -- Builder options ---------------------------------------------------------

# HTML
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
    "use_source_button": True,
    "announcement": "本项目处于 alpha 阶段，API 可能随时更改。",
}
html_css_files = ["css/tippy.css"]

import jieba

html_search_language = "zh"
html_search_options = {
    "dict": os.path.join(os.path.dirname(jieba.__file__), jieba.DEFAULT_DICT_NAME),
}


# -- Domain options ----------------------------------------------------------

# Python
add_module_names = False
modindex_common_prefix = ["pystatpower."]


# -- Extension options -------------------------------------------------------

# sphinx.ext.autodoc
autoclass_content = "class"
autodoc_class_signature = "separated"
autodoc_member_order = "bysource"
autodoc_default_options = {
    "members": None,
    "member-order": "bysource",
    "class-doc-from": "class",
    "show-inheritance": None,
}
autodoc_docstring_signature = True
autodoc_typehints = "none"
autodoc_typehints_description_target = "all"
autodoc_type_aliases = {}
autodoc_typehints_format = "short"
autodoc_preserve_defaults = False
autodoc_warningiserror = True
autodoc_inherit_docstrings = False

# sphinx.ext.intersphinx
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master", None),
}

# sphinx.ext.napoleon
napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_keyword = True
napoleon_use_rtype = False
napoleon_preprocess_types = False
napoleon_type_aliases = {}
napoleon_attr_annotations = True

# sphinx_ext_viewcode
viewcode_follow_imported_members = True
viewcode_line_numbers = True

# sphinx_copybutton
copybutton_prompt_text = r">>> |\.\.\. "
copybutton_prompt_is_regexp = True
copybutton_line_continuation_character = "\\"

# sphinx_issues
issues_github_path = "PyStatPower/PyStatPower"

# autodoc2
autodoc2_packages = [
    {
        "path": "../../src/pystatpower",
        "auto_mode": False,
    },
]
# autodoc2_docstring_parser_regexes = [
#     (r".*", "myst"),
# ]
autodoc2_output_dir = "api"
autodoc2_hidden_objects = [
    "dunder",
    "private",
    "inherited",
]

# myst_parser
myst_enable_extensions = [
    "attrs_block",
    "attrs_inline",
    "colon_fence",
    "dollarmath",
    "tasklist",
]
myst_heading_anchors = 3
myst_links_external_new_tab = True

# sphinx_tippy
tippy_props = {
    "theme": "light",
}
