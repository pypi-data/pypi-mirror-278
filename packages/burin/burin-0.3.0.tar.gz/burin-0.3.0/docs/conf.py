"""
Sphinx documentation build configuration for Burin project.

Copyright (c) 2024 William Foster with BSD 3-Clause License
See included LICENSE file for details.
"""

# -- Path setup --------------------------------------------------------------

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join("..", "src")))

onRTD = os.environ.get("READTHEDOCS") == "True"

# -- Project information -----------------------------------------------------

import burin
from datetime import datetime

docBuildDatetime = datetime.now()

project = burin.__title__
copyright = f"{docBuildDatetime.strftime('%Y')}, {burin.__author__}"
author = burin.__author__
release = burin.__version__
version = release.rpartition(".")[1]

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx_rtd_theme"
]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "__pycache__"]
highlight_language = "none"
suppress_warnings = []

# -- Options for EPUB output -------------------------------------------------

epub_show_urls = "no"

# -- Options for HTML output -------------------------------------------------

html_theme_options = {}
html_theme = "sphinx_rtd_theme"

# -- Options for LaTeX output -------------------------------------------------

latex_engine = "xelatex"
latex_show_pagerefs = True
latex_show_urls = "no"

# -- Options for autodoc -----------------------------------------------------

autoclass_content = "both"

# -- Options for autosectionlabel --------------------------------------------

autosectionlabel_prefix_document = True
suppress_warnings.append("autosectionlabel.*")

# -- Options for autosummary -------------------------------------------------

autosummary_generate = False

# -- Options for intersphinx -------------------------------------------------

intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}
