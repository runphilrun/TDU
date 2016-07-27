#!/usr/bin/env python3
import sys
import os
import sphinx_rtd_theme

# Add our modules to the system path.
sys.path.insert(0, os.path.abspath("../src"))

project = 'tdu'
copyright = '2016, Phil-Linden, Nate-Wilkins'
author = 'Phil-Linden, Nate-Wilkins'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.imgmath',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
source_suffix = ['.rst']

master_doc = 'index'

version = '0.0.1'
release = '0.0.1'

language = None

exclude_patterns = []

add_function_parentheses = True
add_module_names = False
pygments_style = 'sphinx'
todo_include_todos = True

html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_static_path = []
html_extra_path = []
html_sidebars = {}
html_additional_pages = {}
html_show_sourcelink = True
html_show_sphinx = True
html_show_copyright = True
html_search_language = 'en'
htmlhelp_basename = 'tdudoc'

# -- Options for LaTeX output ---------------------------------------------
latex_elements = {
     # The paper size ('letterpaper' or 'a4paper').
     #
     # 'papersize': 'letterpaper',

     # The font size ('10pt', '11pt' or '12pt').
     #
     # 'pointsize': '10pt',

     # Additional stuff for the LaTeX preamble.
     #
     # 'preamble': '',

     # Latex figure (float) alignment
     #
     # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'tdu.tex', 'tdu Documentation',
     'Phil-Linden,Nate-Wilkins', 'manual'),
]
