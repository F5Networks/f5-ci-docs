:product: BIG-IP Controller for Marathon
:type: task

.. _install-mctlr:

Install the BIG-IP Controller: Marathon
========================================

The |mctlr-long| installs as a Marathon `Application`_.

.. table:: Task Summary

   =======  ===================================================================
   Step     Task
   =======  ===================================================================
   1.       :ref:`mctlr initial setup`
   2.       :ref:`mctlr rbac`
   3.       :ref:`mctlr deploy`
   4.       :ref:`upload mctlr app`
   5.       :ref:`mctlr verify`
   =======  ===================================================================

.. _mctlr initial setup:

Initial Setup
-------------

.. include:: /_static/reuse/kctlr-initial-setup.rst
   :end-line: 10

.. _mctlr rbac:

Set up RBAC Authentication
--------------------------

:ref:`Set up authentication to your secure DC/OS cluster <mesos-authentication>`.

See the `Mesosphere DC/OS Security documentation <https://docs.mesosphere.com/1.10/security/>`_ for more information.

.. _mctlr deploy:

Launch the BIG-IP Controller for Marathon
-----------------------------------------

Define a Marathon Application using valid JSON. See the `marathon-bigip-ctlr configuration parameters`_ reference for all supported configuration options.

.. include:: /_static/reuse/bigip-permissions-ctlr.rst

.. literalinclude:: /marathon/config_examples/f5-marathon-bigip-ctlr-example.json

:fonticon:`fa fa-download` :download:`f5-marathon-bigip-ctlr-example.json </marathon/config_examples/f5-marathon-bigip-ctlr-example.json>`

.. _mctlr snat deploy:

Use BIG-IP SNAT Pools and SNAT automap
``````````````````````````````````````

.. include:: /_static/reuse/marathon-version-added-1_3.rst

.. include:: /_static/reuse/mctlr-snat-note.rst

See :ref:`bigip snats` for more information.

To use a specific SNAT pool, add the following label to the |mctlr| Application file:

.. code-block:: bash

   "F5_CC_VS_SNAT_POOL_NAME": "<name-of-snat-pool>"

Replace :code:`<snat-pool>` with the name of any SNAT pool that already exists in the :code:`/Common` partition on the BIG-IP device. The |mctlr| cannot define a new SNAT pool for you.

:fonticon:`fa fa-download` :download:`f5-marathon-bigip-ctlr-example_snat.json </marathon/config_examples/f5-marathon-bigip-ctlr-example_snat.json>`

.. _upload mctlr app:

Upload the App to the Marathon API server
-----------------------------------------

You can use a :command:`curl` command to upload the App definition to the Marathon API server.

.. code-block:: bash

   curl -X POST -H "Content-Type: application/json" http://<marathon_uri>/v2/apps -d @marathon-bigip-ctlr.json

.. _mctlr verify:

Verify creation
---------------

Send a :code:`GET` request to the Marathon API server to verify successful creation of the |mctlr| App.

.. tip::

   You can pass the response through a pretty-print tool like `jq <https://github.com/stedolan/jq>`_ for better readability.

.. code-block:: bash

   curl -X GET http://<marathon_uri>/v2/apps/marathon-bigip-ctlr | jq .

.. _Application: https://mesosphere.github.io/marathon/docs/application-basics.html
.. _Marathon Web Interface: https://mesosphere.github.io/marathon/docs/marathon-ui.html
