f5-ci-docs
==========

.. image:: https://readthedocs.com/projects/f5-networks-f5-ci-docs/badge/?version=master
    :target: https://f5-networks-f5-ci-docs.readthedocs-hosted.com/en/gitlab-ci/?badge=gitlab-ci
    :alt: Documentation Status

.. image:: https://travis-ci.com/F5Networks/f5-ci-docs.svg?token=9DzDpZ48B74dRXvdFxM2&branch=master
    :target: https://travis-ci.com/F5Networks/f5-ci-docs

Overview
--------

This repository houses the end-user documentation for F5 Networks' Container Connectors (CC) and Application Services Proxy (ASP).

We write documentation in `reStructuredText <http://docutils.sourceforge.net/rst.html>`_ (rST); build with `Sphinx <http://www.sphinx-doc.org/>`_ ; test with `Travis-CI <https://travis-ci.com/>`_ ; and publish with `Read The Docs Business <https://readthedocs.com/>`_.


Documentation
-------------

View the documentation online at https://f5-networks-f5-ci-docs.readthedocs-hosted.com/en/master/.


Contributing
------------

If you want to contribute to this documentation set, please consult the `F5 Open Source Style Guide <http://f5-docs-training.readthedocs.io/en/latest/docs/style_guide.html>`_ and `training <http://f5-docs-training.readthedocs.io/en/latest/>`_ first. Once you've completed the training and are ready to start writing, fork this repo.

* Create an `Issue <https://github.com/F5Networks/f5-ci-docs/issues>`_ corresponding to the changes/additions you plan to make. When your work is complete, `open a pull request <https://github.com/F5Networks/f5-ci-docs/pulls>`_.
* Be sure to fetch and rebase your work to ensure your fork stays up-to-date!


Build and Test
~~~~~~~~~~~~~~

The `scripts <scripts/>`_ directory contains resources for building and testing documentation in a Docker container. We recommend running the build and test scripts **before** opening a pull request; if your PR doesn't pass, it won't be accepted.

The build and test scripts can be run in a container using an `image <https://hub.docker.com/r/thejodesterf5/containthedocs/>`_ that has all of the sphinx and Read the Docs dependencies. You can also just run the scripts, provided you have the `requirements <requirements.docs.txt>`_ installed.

- scripts/run-in-docker.sh -- runs a Docker container with the 'containthedocs' image.
- scripts/build-docs.sh -- builds the documentation and checks grammar with `write-good <https://github.com/btford/write-good>`_.
- scripts/sphinx-test-suite -- these tests run in travis-ci and must pass before we can accept a pull request; the highlighted section at the end shows what you need to fix.

To run the script(s) in the Docker container:

::

    $ ./scripts/run-in-docker.sh ./scripts/build-docs.sh
    $ ./scripts/run-in-docker.sh ./scripts/sphinx-test-suite.sh

To run the script(s) without using Docker:

::

    $ pip install -r requirements.docs.txt
    $ ./scripts/build-docs.sh
    $ ./scripts/sphinx-test-suite.sh



Contributor License Agreement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Individuals or business entities who contribute to this project must
have completed and submitted the `F5 Contributor License
Agreement <#>`_ prior to their code submission being included in this project.

Issues
------
To report an issue or request additional guides, please open an `Issue <https://github.com/F5Networks/f5-ci-docs/issues>`_. Use the issue template provided and, please, be specific!


Support
-------
See `Support <SUPPORT>`_.


Copyright and License
---------------------

Copyright 2015-2017 F5 Networks Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


