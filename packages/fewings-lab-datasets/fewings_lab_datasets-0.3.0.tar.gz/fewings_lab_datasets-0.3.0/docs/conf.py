# Configuration file for the Sphinx documentation builder.

import sys
import os

sys.path.insert(0, os.path.abspath('..'))

# -- Project information

project = 'fewings-lab-datasets'
author = 'Andrew Scherer'

release = '1'
version = '0.1.0'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx_search.extension',
    'sphinx_copybutton',
    'IPython.sphinxext.ipython_directive',
    'IPython.sphinxext.ipython_console_highlighting',
    'matplotlib.sphinxext.plot_directive',
]

autodoc_typehints = "none"

autodoc_member_order = "alphabetical"
toc_object_entries_show_parents = "hide"

copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True

plot_include_source = True

source_suffix = {
    '.rst': 'restructuredtext'
}

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}

intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output ----------------------------------------------
# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "sphinx_book_theme"
html_title = "Fewings Lab Datasets"

html_context = {
    "github_user": "andrew-s28",
    "github_repo": "fewings-lab-datasets",
    "github_version": "main",
    "doc_path": "docs",
}

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = dict(
    repository_url="https://github.com/andrew-s28/fewings-lab-datasets",
    repository_branch="main",
    html_title="Fewings Lab Datasets",
    navigation_with_keys=False,
    path_to_docs="doc",
    use_edit_page_button=True,
    use_repository_button=True,
    use_issues_button=True,
    icon_links=[],
    show_toc_level=3,
    max_navbar_depth=5,
    home_page_in_toc=False,
)
