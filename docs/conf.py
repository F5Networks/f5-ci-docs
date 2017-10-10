# -*- coding: utf-8 -*-
#
# F5 Container Integration documentation build configuration file, created by
# sphinx-quickstart on Wed Aug 10 14:05:28 2016.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('../'))


import f5_sphinx_theme
import recommonmark
import CommonMark


from recommonmark.parser import CommonMarkParser

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
#needs_sphinx = '1.5.1'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.ifconfig',
    'sphinx.ext.doctest',
    'sphinxjp.themes.basicstrap',
    'cloud_sptheme.ext.table_styling',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = ['.rst', '.md']

source_parsers = {
    '.md': CommonMarkParser,
}


# The encoding of source files.
#
source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'F5 Container Integrations'
copyright = u'2017 F5 Networks Inc'
author = u'F5 Networks'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = 'v1'
# The full version, including alpha/beta/rc tags.
release = 'v1.3'

# All substitutions

rst_epilog = """
.. |asp| replace:: Application Services Proxy
.. |aspk-long| replace:: F5-proxy for Kubernetes
.. |aspk| replace:: F5-proxy
.. |cfctlr| replace:: BIG-IP Controller
.. |cf-long| replace:: BIG-IP Controller for Cloud Foundry
.. |kctlr-long| replace:: BIG-IP Controller for Kubernetes
.. |kctlr| replace:: BIG-IP Controller
.. |mctlr-long| replace:: BIG-IP Controller for Marathon
.. |mctlr| replace:: BIG-IP Controller
.. |aspm-long| replace:: ASP Controller for Marathon
.. |aspm| replace:: ASP Controller
.. |octlr-long| replace:: BIG-IP Controller for OpenShift
.. _BIG-IP: https://f5.com/products/big-ip
.. _BIG-IP System User Account Administration -> Administrative Partitions: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/bigip-user-account-administration-12-0-0/3.html
.. _system configuration: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/bigip-system-initial-configuration-12-0-0/2.html#conceptid
.. _local traffic management: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/ltm-basics-12-0-0.html
.. _F5 Docker registry: https://hub.docker.com/r/f5networks/
.. _Kubernetes: https://kubernetes.io/
.. _kubectl: https://kubernetes.io/docs/user-guide/kubectl-overview/
.. _kube-proxy: https://kubernetes.io/docs/admin/kube-proxy/
.. _namespace: https://kubernetes.io/docs/user-guide/namespaces/
.. _ConfigMap: https://kubernetes.io/docs/user-guide/configmap/
.. _Kubernetes Deployment: https://kubernetes.io/docs/user-guide/deployments/
.. _Deployment: https://kubernetes.io/docs/user-guide/deployments/
.. _Kubernetes Service: https://kubernetes.io/docs/user-guide/services/
.. _Service: https://kubernetes.io/docs/user-guide/services/
.. _Services: https://kubernetes.io/docs/user-guide/services/
.. _Kubernetes Cluster: https://kubernetes.io/docs/admin/
.. _Kubernetes DaemonSet: https://kubernetes.io/docs/admin/daemons/
.. _Daemonset: https://kubernetes.io/docs/admin/daemons/
.. _Kubernetes Dashboard: https://kubernetes.io/docs/user-guide/ui/
.. _Static Pod: https://kubernetes.io/docs/admin/static-pods/
.. _Kubernetes pod: https://kubernetes.io/docs/user-guide/pods/
.. _Kubernetes node: https://kubernetes.io/docs/admin/node/
.. _Kubernetes Secret: https://kubernetes.io/docs/user-guide/secrets/
.. _Secret: https://kubernetes.io/docs/user-guide/secrets/
.. _Ingress Resource: https://kubernetes.io/docs/concepts/services-networking/ingress/
.. _Kubernetes Ingress controller: https://kubernetes.io/docs/concepts/services-networking/ingress/#ingress-controllers
.. _Ingress controller: https://kubernetes.io/docs/concepts/services-networking/ingress/#ingress-controllers
.. _Local Traffic Policies: https://support.f5.com/csp/article/K04597703
.. _f5-kube-proxy reference documentation: %(base_url)s/products/connectors/f5-kube-proxy/latest/
.. _ASP reference documentation: %(base_url)s/products/asp/latest/
.. _Kubernetes namespace: https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/
.. _F5 virtual server properties: %(base_url)s/products/connectors/k8s-bigip-ctlr/latest/#virtualserver-configmap-properties
.. _Marathon: https://mesosphere.github.io/marathon/
.. _Express middleware: https://expressjs.com/en/guide/using-middleware.html
.. _Node.js: https://nodejs.org/en/
.. _Express: https://expressjs.com/
.. _Splunk: https://www.splunk.com/
.. _Apache Mesos: https://mesosphere.com/
.. _Marathon: https://mesosphere.github.io/marathon/
.. _Apache Mesos Marathon: https://mesosphere.github.io/marathon/
.. _Marathon Apps: https://mesosphere.github.io/marathon/docs/application-basics.html
.. _Marathon Applications: https://mesosphere.github.io/marathon/docs/application-basics.html
.. _Docker: https://www.docker.com/
.. _Marathon Web Interface: https://mesosphere.github.io/marathon/docs/marathon-ui.html
.. _BIG-IP partition: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/bigip-user-account-administration-13-0-0/2.html
.. _BIG-IP SSL profile: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/ltm-profiles-reference-12-1-0/6.html
.. _Pivotal Cloud Foundry: https://pivotal.io/platform
.. _Cloud Foundry: https://www.cloudfoundry.org/platform/
.. _Diego cell: https://docs.cloudfoundry.org/concepts/architecture/#diego-cell
.. _NATS bus: https://docs.cloudfoundry.org/concepts/architecture/router.html#use
.. _Cloud Foundry CLI: https://docs.cloudfoundry.org/cf-cli/getting-started.html
.. _Application Manifest: https://docs.pivotal.io/pivotalcf/1-7/devguide/deploy-apps/manifest.html
.. _f5-kube-proxy: %(base_url)s/products/connectors/f5-kube-proxy/latest/
.. _marathon-asp-ctlr: %(base_url)s/products/connectors/marathon-asp-ctlr/latest/
.. _marathon-bigip-ctlr: %(base_url)s/products/connectors/marathon-bigip-ctlr/latest/
.. _k8s-bigip-ctlr: %(base_url)s/products/connectors/k8s-bigip-ctlr/latest/
.. _cf-bigip-ctlr: %(base_url)s/products/connectors/cf-bigip-ctlr/latest/
.. _Application Services Proxy: %(base_url)s/products/asp/latest/
.. _Cluster network: https://kubernetes.io/docs/concepts/cluster-administration/networking/
.. _Better or Best license: https://f5.com/products/how-to-buy/simplified-licensing
.. _OpenShift route resources: /products/connectors/k8s-bigip-ctlr/latest/#openshift-route-resources
.. _Route annotations: /products/connectors/k8s-bigip-ctlr/latest/#supported-annotations
.. _ASP ephemeral store: %(base_url)s/products/asp/latest/#ephemeral-store
.. _ASP health monitor: %(base_url)s/products/asp/latest/#health-monitors
.. _ASP health check parameters: %(base_url)s/products/asp/latest/#health-check-types
.. _ASP virtual server configuration parameters: %(base_url)s/products/asp/latest/#virtual-server
.. _ASP event handlers: %(base_url)s/products/asp/latest/event-handlers.html
.. _ASP Middleware API: %(base_url)s/products/asp/latest/middleware-api.html
.. _k8s-bigip-ctlr configuration parameters: %(base_url)s/products/k8s-bigip-ctlr/latest/#controller-configuration-parameters
.. _k8s-bigip-ctlr reference documentation: %(base_url)s/products/k8s-bigip-ctlr/latest/
.. _k8s-bigip-ctlr virtual server parameters: %(base_url)s/products/connectors/k8s-bigip-ctlr/latest/index.html#virtualserver
.. _k8s-bigip-ctlr iApp parameters: %(base_url)s/products/connectors/k8s-bigip-ctlr/latest/index.html#iapps
.. _iApp Pool Member table: %(base_url)s/products/connectors/k8s-bigip-ctlr/latest/index.html#iapp-pool-member-table
.. _configuration parameters specific to OpenShift: %(base_url)s/products/connectors/k8s-bigip-ctlr/latest/index.html#openshift-sdn
.. _Cluster Role: https://kubernetes.io/docs/admin/authorization/rbac/#role-and-clusterrole
.. _Cluster Role Binding: https://kubernetes.io/docs/admin/authorization/rbac/#rolebinding-and-clusterrolebinding
.. _ReplicaSet: https://kubernetes.io/docs/user-guide/replicasets/
.. _Pod: https://kubernetes.io/docs/user-guide/pods/
.. _Pods: https://kubernetes.io/docs/user-guide/pods/
.. _marathon-bigip-ctlr reference documentation: %(base_url)s/products/connectors/marathon-bigip-ctlr/latest/
.. _marathon-bigip-ctlr iApp configuration parameters: %(base_url)s/products/connectors/marathon-bigip-ctlr/latest/index.html#iApp
.. _ServiceAccount: https://kubernetes.io/docs/admin/service-accounts-admin/
.. _Create a new partition: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/tmos-implementations-12-1-0/29.html
.. _Create a Kubernetes Secret containing your Docker login credentials: https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/
.. _supported Ingress annotations: %(base_url)s/products/connectors/k8s-bigip-ctlr/latest/#supported-annotations
.. _store your Docker login credentials as a Secret: https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/
.. _Route configuration parameters: %(base_url)s/products/connectors/k8s-bigip-ctlr/latest/#openshift-routes
.. _BIG-IP Controller for Cloud Foundry configuration parameters: %(base_url)s//products/connectors/cf-bigip-ctlr/v1.0/#configuration-parameters
.. _supported OpenShift Route annotations: %(base_url)s/products/connectors/k8s-bigip-ctlr/latest/#supported-route-configurations
.. _Create a new partition: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/tmos-implementations-12-1-0/29.html
.. _BIG-IP Controller for Kubernetes: %(base_url)s/products/connectors/k8s-bigip-ctlr/latest
"""% {
    'base_url': 'http://clouddocs.f5.com'
}

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#
# today = ''
#
# Else, today_fmt is used as the format for a strftime call.
#
# today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build',
                    '_static/reuse',
                    'drafts',
                    'Thumbs.db',
                    '.DS_Store',
                    'venv',
                    '.github'
                    ]

# The reST default role (used for this markup: `text`) to use for all
# documents.
#
# default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#
# add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#
# add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#
# show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
# modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
# keep_warnings = False

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'f5_sphinx_theme'

# Add any paths that contain custom themes here, relative to this directory.
html_theme_path = f5_sphinx_theme.get_html_theme_path()

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    'next_prev_link': False
}

html_sidebars = {
    '**': ['searchbox.html', 'localtoc.html', 'globaltoc.html' ]
}


# The name for this set of Sphinx documents.
# "<project> v<release> documentation" by default.
#
#html_title = 'F5 Container Integrations'

# A shorter title for the navigation bar.  Default is the same as html_title.
#
html_short_title = 'Home'

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#
html_logo = '_static/f5-logo-solid-rgb_small.png'

# The name of an image file (relative to this directory) to use as a favicon of
# the docs.  This file should be a Windows icon file (.ico) being 16x16 or
# 32x32 pixels large.
#
# html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static/']

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
#
# html_extra_path = []

# If not None, a 'Last updated on:' timestamp is inserted at every page
# bottom, using the given strftime format.
# The empty string is equivalent to '%b %d, %Y'.
#
html_last_updated_fmt = ''

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#
# html_use_smartypants = True

# Additional templates that should be rendered to pages, maps page names to
# template names.
#
# html_additional_pages = {}

# If false, no module index is generated.
#
html_domain_indices = True

# If false, no index is generated.
#
html_use_index = True

# If true, the index is split into individual pages for each letter.
#
html_split_index = False

# If true, links to the reST sources are added to the pages.
#
html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
#
html_show_sphinx = False

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
#
html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#
# html_use_opensearch = 'http://clouddocs.f5.com'

# This is the file name suffix for HTML files (e.g. ".xhtml").
# html_file_suffix = None

# Language to be used for generating the HTML full-text search index.
# Sphinx supports the following languages:
#   'da', 'de', 'en', 'es', 'fi', 'fr', 'hu', 'it', 'ja'
#   'nl', 'no', 'pt', 'ro', 'ru', 'sv', 'tr', 'zh'
#
# html_search_language = 'en'

# A dictionary with options for the search language support, empty by default.
# 'ja' uses this config value.
# 'zh' user can custom change `jieba` dictionary path.
#
# html_search_options = {'type': 'default'}

# The name of a javascript file (relative to the configuration directory) that
# implements a search results scorer. If empty, the default will be used.
#
# html_search_scorer = 'scorer.js'

# Output file base name for HTML help builder.
htmlhelp_basename = 'F5_Container Integrations_doc'

# -- Options for linkcheck ------------------------------------------------
# A list of regular expressions that match URIs that should not be checked when doing a linkcheck build. Example:
#linkcheck_ignore = [r'http://localhost:\d+/']

# The number of times the linkcheck builder will attempt to check a URL before declaring it broken. Defaults to 1 attempt.
linkcheck_retries=2

# A timeout value, in seconds, for the linkcheck builder. The default is to use Python’s global socket timeout.
linkcheck_timeout=5


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
     # The paper size ('letterpaper' or 'a4paper').
     #
      'papersize': 'letterpaper',

     # The font size ('10pt', '11pt' or '12pt').
     #
      'pointsize': '12pt',

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
    (master_doc, 'F5_Container Integrations_doc.tex',
     u'F5 Container Integrations Documentation',
     'F5 Networks', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#
latex_logo = '_static/f5-logo-solid-rgb_small.png'

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#
# latex_use_parts = False

# replaces latex_use_parts
# determines the topmost sectioning unit. It should be chosen from part,
#  chapter or section. The default is None; the topmost sectioning unit is
#  switched by documentclass. section is used if documentclass will be howto,
#  otherwise chapter will be used.
#
latex_toplevel_sectioning = 'section'

# If true, show page references after internal links.
#
# latex_show_pagerefs = False

# If true, show URL addresses after external links.
#
# latex_show_urls = False

# Documents to append as an appendix to all manuals.
#
# latex_appendices = []

# If false, will not define \strong, \code, \titleref, \crossref ... but
# only \sphinxstrong, ..., \sphinxtitleref, ... To help avoid clash with user added
# packages.
#
# latex_keep_old_macro_names = True

# If false, no module index is generated.
#
# latex_domain_indices = True


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'F5_Container_Integrations_doc',
     'F5 Container Integrations Documentation',
     [author], 1)
]

# If true, show URL addresses after external links.
#
# man_show_urls = False


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'F5_Container_Integrations_doc',
     'F5 Container Integrations Documentation',
     author, 'F5 Container Integrations'),
]

# Documents to append as an appendix to all manuals.
#
# texinfo_appendices = []

# If false, no module index is generated.
#
# texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
#
texinfo_show_urls = 'footnote'

# If true, do not generate a @detailmenu in the "Top" node's menu.
#
# texinfo_no_detailmenu = False


# Example configuration for intersphinx: refer to the Python standard library.
#intersphinx_mapping = {'https://docs.python.org/': None}
