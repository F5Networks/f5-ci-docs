f5-ci-docs
==========

.. image:: https://travis-ci.com/F5Networks/f5-ci-docs.svg?token=9DzDpZ48B74dRXvdFxM2&branch=master
    :target: https://travis-ci.com/F5Networks/f5-ci-docs

Overview
--------

This repository houses the end-user documentation for F5 Networks' Container Connectors (CC) and Application Services Proxy (ASP).

We write documentation in `reStructuredText <http://docutils.sourceforge.net/rst.html>`_ (rST); build with `Sphinx <http://www.sphinx-doc.org/>`_ ; test with `Travis-CI <https://travis-ci.com/>`_ ; and host the docs website in `Amazon s3 <https://aws.amazon.com/s3/>`_.

Contributing
------------

If you want to contribute to this documentation set, please consult the `F5 Open Source Style Guide <https://s3-us-west-2.amazonaws.com/staging-c2ub89n2qjgt1/docs-training/style_guide/index.html>`_ and `training <https://gitlab.pdbld.f5net.com/tools/f5-docs-training/>`_ first (NOTE: training repo is only accessible by F5 employees). Once you've completed the training and are ready to start writing, fork this repo.

* Create an `issue <https://github.com/F5Networks/f5-ci-docs/issues>`_ corresponding to the changes/additions you plan to make. When your work is complete, `open a pull request <https://github.com/F5Networks/f5-ci-docs/pulls>`_.
* Be sure to fetch often so your fork stays up-to-date!


Build and Test
~~~~~~~~~~~~~~

The `scripts </scripts>`_ directory contains documentation testing resources. We recommend running the test script **before** opening a pull request; if the build associated with your PR doesn't pass, the request won't be accepted.

The test script can be run locally or in a Docker container, which uses an image developed by F5 (https://hub.docker.com/r/f5devcentral/containthedocs/ ). The Ubuntu-based Docker image has all of the dependencies required to build the project documentation pre-installed. If you want to run the test script locally, you'll need to install the `requirements <requirements.txt>`_ first.

- scripts/docker-docs.sh -- runs a Docker container with the 'containthedocs' image.
- scripts/test-docs.sh -- builds the documentation (``make -C docs/ html``); runs ``make linkcheck`` to check internal and external links; and checks grammar with ``write-good``. These tests run in travis-ci and must pass before we can accept a pull request.

To run the test script in the Docker container: ::

    $ ./scripts/docker-docs.sh ./scripts/test-docs.sh

To run the script without using Docker: ::

    $ pip install -r requirements.txt
    $ npm install -g write-good
    $ ./scripts/test-docs.sh


Contributor License Agreement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Individuals or business entities who contribute to this project must have completed and submitted the `F5 Contributor License Agreement </_static/F5-contributor-license-agreement.pdf>`_ prior to their code submission being included in this project.

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


