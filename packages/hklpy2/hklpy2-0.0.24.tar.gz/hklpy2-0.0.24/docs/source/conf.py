# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# flake8: noqa

import pathlib
import sys

docs_source = pathlib.Path(__file__).parent
sys.path.insert(0, str(docs_source.parent.parent))

# imports here for sphinx to build the documents without many WARNINGS.
import hklpy2

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "hklpy2"
copyright = "2023-2024, Argonne National Laboratory"
# author = 'Bluesky team'
release = hklpy2.__version__
version = ".".join(release.split(".")[:2])
today_fmt = "%Y-%m-%d %H:%M"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_design",
    "myst_parser",
    "nbsphinx",
]
extensions.append("sphinx_tabs.tabs")  # this must be last

exclude_patterns = ["**.ipynb_checkpoints"]
myst_enable_extensions = ["colon_fence"]
source_suffix = ".rst .md".split()
templates_path = ["_templates"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_title = f"{project} {version}"
html_static_path = ["_static"]


# -- Options for autodoc ---------------------------------------------------

autodoc_exclude_members = ",".join(
    """
    __weakref__
    _component_kinds
    _device_tuple
    _required_for_connection
    _sig_attrs
    _sub_devices
    calc_class
    component_names
    """.split()
)
autodoc_default_options = {
    # 'members': 'var1, var2',
    # 'member-order': 'bysource',
    "private-members": True,
    # "special-members": "__init__",
    # 'undoc-members': True,
    "exclude-members": autodoc_exclude_members,
}
autodoc_mock_imports = """
    gi
    ophyd
    pint
""".split()

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}
inheritance_graph_attrs = {"rankdir": "LR"}
inheritance_node_attrs = {"fontsize": 24}
autosummary_generate = True
