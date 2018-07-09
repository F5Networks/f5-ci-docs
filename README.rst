f5-ci-docs
==========

.. image:: https://travis-ci.org/F5Networks/f5-ci-docs.svg?branch=master
    :target: https://travis-ci.org/F5Networks/f5-ci-docs

Overview
--------

This repository houses the end-user documentation for F5 Networks' Container Connectors (CC). The documentation is published at https://clouddocs.f5.com/containers/latest.

We write documentation in `reStructuredText <http://docutils.sourceforge.net/rst.html>`_ (rST); build with `Sphinx <http://www.sphinx-doc.org/>`_ ; test with `Travis-CI <https://travis-ci.org/>`_ ; and publish to a static website hosted in `Amazon s3 <https://aws.amazon.com/s3/>`_.

Contributing
------------

If you want to contribute to this documentation set, please consult the `F5 Open Source Style Guide <tbd>`_ and `training <tbd>`_ first. Once you've completed the training and are ready to start writing, fork this repo.

* Create an `issue <https://github.com/F5Networks/f5-ci-docs/issues>`_ corresponding to the changes/additions you plan to make. When your work is complete, `open a pull request <https://github.com/F5Networks/f5-ci-docs/pulls>`_.
* Be sure to fetch and rebase often so your fork stays up-to-date!

How to Build, Test, and Deploy Documentation
````````````````````````````````````````````

This project uses CI/CD to build, test, and deploy documentation.

**Tools:**

- `sphinx`: builds HTML, checks syntax, and tests links.
- `f5-sphinx-theme <https://github.com/f5devcentral/f5-sphinx-theme>`_: F5 theme for sphinx projects.
- `write-good`: tests grammar.
- Travis-CI: builds, tests, and deploys documentation.
- AWS S3/CloudFront: website hosting.
- Docker image: `f5devcentral/containthedocs <https://hub.docker.com/r/f5devcentral/containthedocs/>`_

**Scripts:**

The `scripts </scripts>`_ directory contains documentation testing resources. We recommend running the test script **before** opening a pull request; if the build associated with your PR doesn't pass, the request won't be accepted.

The test script can be run locally or in a Docker container, which uses the F5 ``containthedocs`` image. The Ubuntu-based Docker image has all of the dependencies required to build the project documentation pre-installed. If you want to run the test script locally, you'll need to install the `requirements <requirements.txt>`_ first.

- *docker-docs*: Runs a Docker container mounted to your working directory.
- *test-docs*: Runs the HTML build, grammar check, and linkcheck.

Building and Testing
~~~~~~~~~~~~~~~~~~~~

You can use the commands below to build and test your work.
Commands beginning with `docker` run in a Docker container using the same image used in Travis-CI (`f5devcentral/containthedocs <https://hub.docker.com/r/f5devcentral/containthedocs/>`_).

You can view the documentation in a web browser on your local machine.

+------------------------+--------------------------------------------------------+----------------------------------+
| Command                | Description                                            | How to view docs                 |
+========================+========================================================+==================================+
| `make html`            | basic HTML build                                       | open docs/_build/html/index.html |
+------------------------+--------------------------------------------------------+----------------------------------+
| `make preview`         | builds docs as you write; view changes live in browser | open http://0.0.0.0:8000         |
+------------------------+--------------------------------------------------------+----------------------------------+
| `make test`            | run the docs quality tests                             | open docs/_build/html/index.html |
+------------------------+--------------------------------------------------------+----------------------------------+
| `make docker-html`     | Runs the docker-docs script with ``make HTML``;        | open docs/_build/html/index.html |
|                        | uses the same container image as production builds     |                                  |
+------------------------+--------------------------------------------------------+----------------------------------+
| `make docker-preview`  | Runs the docker-docs script with ``make preview``;     | open http://0.0.0.0:8000         |
|                        | uses the same container image as production builds     |                                  |
+------------------------+--------------------------------------------------------+----------------------------------+
| `make docker-test`     | Runs the docker-docs script with ``make test``;        | open docs/_build/html/index.html |
|                        | uses the same container image as production builds     |                                  |
+------------------------+--------------------------------------------------------+----------------------------------+

.. note:: If you don't use the Docker container, you need to install the project dependencies locally. You can find instructions for installing/using virtualenv and pip `here <https://packaging.python.org/guides/installing-using-pip-and-virtualenv>`_.

::

   virtualenv <my-venv>
   pip install -r requirements.txt
   npm install write-good

Tips and Tricks
```````````````

See the `F5 Open Source Documentation style guide <https://s3-us-west-2.amazonaws.com/staging-c2ub89n2qjgt1/docs-training/style_guide/index.html>`_ for rST and sphinx cheat sheets, as well as general guidelines for writers.

Contributor License Agreement
`````````````````````````````

Individuals or business entities who contribute to this project must have completed and submitted the `F5 Contributor License Agreement </_static/F5-contributor-license-agreement.pdf>`_ prior to their code submission being included in this project.

Issues
------

To report an issue or request additional guides, please open an `Issue <https://github.com/F5Networks/f5-ci-docs/issues>`_. Use the issue template provided and, please, be specific!

Support
-------

See `Support <SUPPORT>`_.


Copyright and License
---------------------

Copyright 2015-2018 F5 Networks Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
