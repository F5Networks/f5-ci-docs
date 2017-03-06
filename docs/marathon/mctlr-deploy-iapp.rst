.. _mctlr-deploy-iapps:

Deploy iApps with |mctlr-long|
==============================

.. table:: Docs test matrix

    +-----------------------------------------------------------+
    | marathon-1.3.9                                            |
    +-----------------------------------------------------------+
    | mesos-1.0.3                                               |
    +-----------------------------------------------------------+
    | |mctlr| v1.0.0                                            |
    +-----------------------------------------------------------+
    | Marathon `basic-3 example app`_                           |
    +-----------------------------------------------------------+

The |mctlr| can deploy any iApp on the BIG-IP via a set of `iApp configuration parameters </products/connectors/marathon-bigip-ctlr/latest/index.html#iApp>`_. The iApp must exist on your BIG-IP before |mctlr| attempts to deploy it. The steps presented here apply to any built-in or custom iApp.

If you prefer not to use iApps, you can also :ref:`manage BIG-IP objects directly <mctlr-manage-bigip-objects>` with |mctlr|.

Define the F5 iApp Application Labels
-------------------------------------

.. _f5-app-labels-iapp-blob:

The example JSON blob shown below defines the ``f5.http`` iApp for a Marathon Application using :ref:`F5 Application Labels <app-labels>`. The ``F5_IAPP_VARIABLE`` labels correspond to fields in the `iApp template <https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/bigip_iapps_developer_11_0_0/2.html#unique_1762445433>`_ 's presentation section. You can :ref:`create iApp variables <tbd>` for any built-in or custom iApp.

.. literalinclude:: /_static/config_examples/f5-marathon-bigip-ctlr-vs-iApp-example.json
    :caption: Example F5 iApp Application Labels
    :lines: 21-34


.. tip::

    You can download the example iApp JSON blob below and modify it to suit your needs.

    :download:`f5-marathon-bigip-ctlr-vs-iApp-example.json </_static/config_examples/f5-marathon-bigip-ctlr-vs-iApp-example.json>`


Deploy the iApp
---------------

#. Add the iApp labels section to the service definition of your Marathon Application.

    .. literalinclude:: /_static/config_examples/f5-marathon-bigip-ctlr-vs-iApp-example.json


#. Send a PUT request to the Marathon API server to update the Application definition.

    .. code-block:: bash

        user@mesos-master:~$ curl -X PUT -H 'Content-Type: application/json' http://10.190.25.75:8080/v2/apps/basic-3 -d @marathon-iapp-example.json


#. Verify creation of the iApp, and its related objects, on the BIG-IP. This is most easily done via the configuration utility:

    - Log in to the BIG-IP configuration utility.
    - Go to :menuselection:`iApps --> Application Services`.
    - Verify that a new item prefixed with the name of your Marathon Application appears in the list, in the correct partition.

Delete iApp objects
-------------------

#. Delete the F5 Application Labels from the Application definition.

#. Send a PUT request to the Marathon API server to update the Application definition.

    .. code-block:: bash

        user@mesos-master:~$ curl -X PUT -H 'Content-Type: application/json' http://10.190.25.75:8080/v2/apps/basic-3 -d @marathon-iapp-example.json

#. Verify the iApp and its related objects no longer exist on the BIG-IP.

    - Log in to the BIG-IP configuration utility.
    - Go to :menuselection:`iApps --> Application Services`.
    - Verify that the item prefixed with the name of your Marathon Application no longer appears in the list for your partition.



.. _basic-3 example app: https://mesosphere.github.io/marathon/docs/application-basics.html#a-simple-docker-based-application
