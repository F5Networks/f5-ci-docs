:product: BIG-IP Controller for Marathon
:type: task

.. _mctlr-deploy-iapps:

Create BIG-IP Objects with iApps
================================

The |mctlr| can deploy any iApp on a BIG-IP device via the `marathon-bigip-ctlr iApp configuration parameters`_. The iApp must exist on your BIG-IP device before |mctlr| attempts to deploy it.
The steps presented here apply to any built-in or custom iApp.

If you prefer not to use iApps, you can also :ref:`manage BIG-IP objects directly <mctlr-manage-bigip-objects>` with |mctlr|.

Define the F5 iApp Application Labels
-------------------------------------

.. _f5-app-labels-iapp-blob:

The example JSON blob shown below defines the ``f5.http`` iApp for a Marathon Application using :ref:`F5 Application Labels <app-labels>`.
The ``F5_IAPP_VARIABLE`` labels correspond to fields in the `iApp template <https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/bigip_iapps_developer_11_0_0/2.html#unique_1762445433>`_ 's presentation section.
You can create iApp variables for any built-in or custom iApp.

.. todo:: add link to iApp variable 'How-to'

.. seealso::

   The  `marathon-bigip-ctlr reference documentation`_ for detailed information about iApp labels.

Deploy the iApp
---------------

#. Add the iApp labels section to the service definition of your Marathon Application.

   .. literalinclude:: /marathon/config_examples/f5-marathon-bigip-ctlr-vs-iApp-example.json
      :caption: Example F5 iApp Application Labels
      :linenos:
      :emphasize-lines: 23-33

   :fonticon:`fa fa-download` :download:`Download f5-marathon-bigip-ctlr-vs-iApp-example.json </marathon/config_examples/f5-marathon-bigip-ctlr-vs-iApp-example.json>`

#. Send a PUT request to the Marathon API server to update the Application definition.

   .. code-block:: bash

      curl -X PUT -H 'Content-Type: application/json' http://10.190.25.75:8080/v2/apps/basic-3 -d @marathon-iapp-example.json

#. Verify creation of the iApp, and its related objects, on the BIG-IP. This is most easily done via the configuration utility:

   - Log in to the BIG-IP configuration utility.
   - Go to :menuselection:`iApps --> Application Services`.
   - Verify that a new item prefixed with the name of your Marathon Application appears in the list, in the correct partition.

Delete iApp objects
-------------------

#. Delete the F5 Application Labels from the Application definition.

#. Send a PUT request to the Marathon API server to update the Application definition.

   .. code-block:: bash

      curl -X PUT -H 'Content-Type: application/json' http://10.190.25.75:8080/v2/apps/basic-3 -d @marathon-iapp-example.json

#. Verify the iApp and its related objects no longer exist on the BIG-IP.

   - Log in to the BIG-IP configuration utility.
   - Go to :menuselection:`iApps --> Application Services`.
   - Verify that the item prefixed with the name of your Marathon Application no longer appears in the list for your partition.


.. _basic-3 example app: https://mesosphere.github.io/marathon/docs/application-basics.html#a-simple-docker-based-application
