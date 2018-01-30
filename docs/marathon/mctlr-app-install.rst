:product: BIG-IP Controller for Marathon
:type: task

.. _install-mctlr:

Install the BIG-IP Controller: Marathon
========================================

The |mctlr-long| installs as a Marathon `Application`_. You can do this via the Marathon REST API, or via the `Marathon Web Interface`_.

Initial Setup
-------------

#. :ref:`Set up authentication to your secure DC/OS cluster <mesos-authentication>`.

#. `Create a new partition`_ for Marathon on your BIG-IP device.
   The |mctlr-long| cannot manage objects in the ``/Common`` partition.

.. _mctlr-deploy:

Launch the |mctlr| App using the Marathon REST API
--------------------------------------------------

#. Create a JSON config file containing the :ref:`required configuration parameters <mctlr-configuration>`.

   .. literalinclude:: /marathon/config_examples/f5-marathon-bigip-ctlr-example.json
      :linenos:
      :emphasize-lines: 11, 16-25

   :fonticon:`fa fa-download` :download:`f5-marathon-bigip-ctlr-example.json </marathon/config_examples/f5-marathon-bigip-ctlr-example.json>`


#. Upload the config file to the Marathon API server.

   .. code-block:: bash

      curl -X POST -H "Content-Type: application/json" http://<marathon_uri>/v2/apps -d @marathon-bigip-ctlr.json

Verify creation
---------------

Send a GET request to the Marathon API server to verify successful creation of the |mctlr| App.

.. tip::

   You can pass the response through a pretty-print tool like `jq <https://github.com/stedolan/jq>`_ for better readability.

.. code-block:: bash

   curl -X GET http://<marathon_uri>/v2/apps/marathon-bigip-ctlr | jq .

.. _Application: https://mesosphere.github.io/marathon/docs/application-basics.html
.. _Marathon Web Interface: https://mesosphere.github.io/marathon/docs/marathon-ui.html
