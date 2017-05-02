.. _mctlr-pool-only:

Manage BIG-IP LTM pools without virtual servers
===============================================

.. versionadded:: marathon-bigip-ctlr_v1.1.0

The |mctlr-long| can create and manage BIG-IP Local Traffic Manager (LTM) pools that aren't attached to a front-end BIG-IP virtual server (also called, simply, "unattached pools").
To create unattached pools for a Marathon Application, leave the ``F5_{n}_BIND_ADDR`` Application Label out of the Application's service definition.

When you create unattached pools, the |mctlr-long| applies the following naming convention to BIG-IP pool members: ``<application-name>_<F5_{n}_PORT>``. For example, ``pool-only-0_8080``.

.. important::

   Your BIG-IP device must have a virtual server with an `iRule`_ or `local traffic policy`_ in effect that can direct traffic to the unattached pool.
   Add the pool member to the iRule or policy to ensure proper handling of client connections to back-end applications.

.. _mctlr-create-unattached-pool:

Create an unattached pool for a Marathon Application
----------------------------------------------------

#. Create a JSON file containing the App service definitions and F5 application labels.

   .. note::

      This sample App definition uses the default :ref:`port index <port-mappings>` (``0``).

   .. literalinclude:: /_static/config_examples/hello-marathon-pool-only-example.json

   :download:`hello-marathon-pool-only-example.json </_static/config_examples/hello-marathon-pool-only-example.json>`

#. Deploy the application in Marathon via the REST API.

   .. code-block:: shell

      curl -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' http://10.190.25.75:8080/v2/apps -d @hello-marathon-pool-only-example.json


.. _mctlr-attach-pool-vs:

Attach pools to a BIG-IP virtual server
---------------------------------------

#. Add the the ``F5_{n}_BIND_ADDR`` label to the Application's JSON service definition using the `Marathon Web Interface`_.

   - :menuselection:`Applications --> <App name> --> Configuration --> Edit --> Labels`
   - Click the :guilabel:`plus sign` (+).
   - Add ``F5_{n}_BIND_ADDR`` and the desired IP address.
   - Click :guilabel:`Change and deploy configuration`.

#. Use the BIG-IP configuration utility to verify the pool attached to the virtual server.

   :menuselection:`Local Traffic --> Virtual Servers`

.. tip::

   You can :ref:`use an IPAM system <mctlr-ipam>` to populate the ``F5_{n}_BIND_ADDR`` label and attach a pool to a virtual server automatically.


.. _mctlr-delete-unattached-pool:

Delete an unattached pool
-------------------------

#. Remove the F5 Application Labels from the Application's service definition using the `Marathon Web Interface`_.

   - :menuselection:`Applications --> <App name> --> Configuration --> Edit --> Labels`
   - Click the :guilabel:`minus sign` (-) next to each F5 App Label.
   - Click :guilabel:`Change and deploy configuration`.

#. Use the BIG-IP configuration utility to verify deletion of the pool.

   :menuselection:`Local Traffic --> Pools`


.. _mctlr-detach-pool:

Detach a pool from a virtual server
-----------------------------------

If you want to delete a front-end BIG-IP virtual server and retain its associated pool(s)/pool member(s):

#. Remove the ``F5_{n}_BIND_ADDR`` label from the App's service definition using the `Marathon Web Interface`_.

   - :menuselection:`Applications --> <App name> --> Configuration --> Edit --> Labels`
   - Click the :guilabel:`minus sign` (-) next to ``F5_{n}_BIND_ADDR``.
   - Click :guilabel:`Change and deploy configuration`.


#. Use the BIG-IP configuration utility to verify the virtual server no longer exists.

   :menuselection:`Local Traffic --> Virtual Servers`

.. _local traffic policy: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/bigip-local-traffic-policies-getting-started-13-0-0/1.html
.. _iRule: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/bigip-system-irules-concepts-11-6-0/1.html
