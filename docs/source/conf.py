# Configuration file for the Sphinx documentation builder.

# -- Project information

project = 'CoRAL'
copyright = '2025, Vega Waichman - Annett'
author = 'Vega Waichman - Annett'

release = '0.1.0'
version = '0.4.0'

# -- General configuration

master_doc = "index"

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx'
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

    
# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_css_files = ['css/custom.css']
#html_logo = "_static/img/Scanpy_Logo_BrightFG.svg"
html_title = "CoRAL"
# -- Options for EPUB output
epub_show_urls = 'footnote'

# def setup(app):
#     app.add_css_file('_static/custom.css')
