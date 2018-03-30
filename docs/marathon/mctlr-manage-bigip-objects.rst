:product: BIG-IP Controller for Marathon
:type: task

.. _mctlr-manage-bigip-objects:

Manage BIG-IP Objects
=====================

The |mctlr-long| watches the Mesos/Marathon API for Applications with associated :ref:`F5 Application Labels <app-labels>`.
These Application Labels define the BIG-IP LTM objects |mctlr| creates/manages.

The example JSON blob shown below tells |mctlr| to create one (1) virtual server - with one (1) health monitor and one (1) pool - in the ``/mesos`` partition on the BIG-IP device.

.. literalinclude:: /marathon/config_examples/hello-marathon-example.json
   :caption: Example F5 Application Labels defining a BIG-IP virtual server
   :lines: 8,10,14-17

.. tip::

   You can also :ref:`deploy iApps with the marathon-bigip-ctlr <mctlr-deploy-iapps>`.

.. _mctlr-create-vs:

Create a BIG-IP virtual server for a Marathon Application
---------------------------------------------------------

.. note::

   The code samples below use the `basic Hello Marathon App`_.


#. Create a JSON file containing the App service definitions and F5 labels.

   .. note:: This sample App definition shows labels that use the default :ref:`port index <port-mappings>` (``0``).

   .. literalinclude:: /marathon/config_examples/hello-marathon-example.json

   :fonticon:`fa fa-download` :download:`hello-marathon-example.json </marathon/config_examples/hello-marathon-example.json>`


#. Deploy the application in Marathon via the REST API using the JSON file.

   .. code-block:: shell

      curl -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' http://10.190.25.75:8080/v2/apps -d @hello-marathon-example.json

#. Verify creation of the virtual server, pool, and member in the App's BIG-IP partition via ``tmsh`` or the configuration utility.

   .. code-block:: console

      admin@(bigip)(cfg-sync Standalone)(Active)(/mesos)(tmos)$ show ltm virtual
      ------------------------------------------------------------------
      Ltm::Virtual Server: basic-0_8080
      ------------------------------------------------------------------
      Status
        Availability     : unknown
        State            : enabled
        Reason           : The children pool member(s) either don't have service checking enabled, or service check results are not available yet
        CMP              : enabled
        CMP Mode         : all-cpus
        Destination      : 10.190.25.70:8080
      ...

.. tip::

   In the above example, the "Availability" is "unknown" because there are no health monitors associated with the virtual server.
   When you add :ref:`health checks <health-checks>` to the App in Marathon, the |mctlr| creates corresponding BIG-IP health monitors.

.. _mctlr-update-vs:

Update a BIG-IP front-end virtual server
----------------------------------------

#. Edit the Application's JSON service definition.

#. Send the updated file to the Marathon API server.

   .. code-block:: console

      curl -X PUT http://10.190.25.75:8080/v2/apps/basic-0 -d @hello-marathon-example.json -H "Content-type: application/json"
      {"version":"2017-02-21T21:48:12.755Z","deploymentId":"02529d16-258b-41d4-ba06-9765c4d1f8d3"}

#. Verify your changes on the BIG-IP via ``tmsh`` or the configuration utility.

   .. code-block:: console

      tmsh show ltm virtual

.. _mctlr-delete-objects:

Delete BIG-IP LTM objects
-------------------------

#. Remove the F5 Application Labels from the Application's service definition.

#. Send the updated Application to the Marathon API server.

   .. code-block:: console

      curl -X PUT http://10.190.25.75:8080/v2/apps/basic-0 -d @hello-marathon-example.json -H "Content-type: application/json"
      {"version":"2017-02-21T21:58:11.111Z","deploymentId":"8bdf03d2-8568-46b3-a5a3-61cc397185a1"}

#. Verify the BIG-IP LTM object(s) no longer exist.

   .. code-block:: console

      admin@(bigip)(cfg-sync Standalone)(Active)(/mesos)(tmos)$ show ltm virtual
      admin@(bigip)(cfg-sync Standalone)(Active)(/mesos)(tmos)$

.. _mctlr-ipam:

Use IPAM to assign IP addresses to BIG-IP virtual servers
---------------------------------------------------------

.. include:: /_static/reuse/marathon-version-added-1_1.rst

The |mctlr-long| has a built-in hook that allows you to integrate an IPAM system using a custom plugin.
The basic elements required are:

#. Add the F5 application labels for :ref:`unattached pools <mctlr-pool-only>` to the App definition.
   The |mctlr-long| creates a BIG-IP pool that isn't attached to a virtual server.

#. Set your IPAM system to add the ``F5_{n}_BIND_ADDR`` label and IP address to the Application definition.
   This tells the |mctlr-long| to create a BIG-IP virtual server with the designated IP address and attach the pool to it.

.. _mctlr-downed-apps:

Connectivity for down or replaced Applications
----------------------------------------------

If you need to take down a `Marathon Application`_ temporarily and want to keep the associated BIG-IP LTM objects, keep the F5 Application Labels in the application's service definition.
The |mctlr| will continue to manage the associated BIG-IP LTM objects when the App comes back up.
If you deploy a new App with the same name as the one you took down, the |kctlr| associates the existing BIG-IP LTM objects with the new Service.

If you take down an Application and want to remove its corresponding BIG-IP LTM objects, :ref:`delete the F5 Application Labels <mctlr-delete-objects>` from its service definition.

.. _mctlr-pool-only:

Manage pools without virtual servers
------------------------------------

.. include:: /_static/reuse/marathon-version-added-1_1.rst

The |mctlr-long| can create and manage BIG-IP Local Traffic Manager (LTM) pools that aren't attached to a front-end BIG-IP virtual server (also referred to as "unattached pools").
When you create unattached pools, the |mctlr-long| applies the following naming convention to BIG-IP pool members: ``<application-name>_<F5_{n}_PORT>``.
For example, ``pool-only-0_8080``.

.. important::

   Your BIG-IP device must have a virtual server with an `iRule`_, or a `local traffic policy`_, that can direct traffic to the unattached pool.
   After creating an unattached pool, add its member(s) to the iRule or traffic policy to ensure proper handling of client connections to your back-end applications.

.. _mctlr-create-unattached-pool:

Create a pool without a virtual server
``````````````````````````````````````

#. Create a JSON file containing the App service definitions and F5 application labels, **without the** ``F5_{n}_BIND_ADDR`` **application label**.

   .. note::

      This sample App definition uses the default :ref:`port index <port-mappings>` (``0``).

   .. literalinclude:: /marathon/config_examples/hello-marathon-pool-only-example.json

   :fonticon:`fa fa-download` :download:`hello-marathon-pool-only-example.json </marathon/config_examples/hello-marathon-pool-only-example.json>`

#. Deploy the application in Marathon via the REST API.

   .. code-block:: shell

      curl -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' http://10.190.25.75:8080/v2/apps -d @hello-marathon-pool-only-example.json


.. _mctlr-attach-pool-vs:

Attach a pool to a virtual server
`````````````````````````````````

#. Add the the ``F5_{n}_BIND_ADDR`` label to the Application's JSON service definition using the `Marathon Web Interface`_.

   - :menuselection:`Applications --> <App name> --> Configuration --> Edit --> Labels`
   - Click the :guilabel:`plus sign` (+).
   - Add ``F5_{n}_BIND_ADDR`` and the desired IP address.
   - Click :guilabel:`Change and deploy configuration`.

#. Use the BIG-IP configuration utility to verify the pool attached to the virtual server.

   :menuselection:`Local Traffic --> Virtual Servers`

.. tip::

   You can :ref:`use an IPAM system <mctlr-ipam>` to populate the ``F5_{n}_BIND_ADDR`` label automatically.


.. _mctlr-delete-unattached-pool:

Delete an unattached pool
`````````````````````````

#. Remove the F5 Application Labels from the Application's service definition using the `Marathon Web Interface`_.

   - :menuselection:`Applications --> <App name> --> Configuration --> Edit --> Labels`
   - Click the :guilabel:`minus sign` (-) next to each F5 App Label.
   - Click :guilabel:`Change and deploy configuration`.

#. Use the BIG-IP configuration utility to verify deletion of the pool.

   :menuselection:`Local Traffic --> Pools`


.. _mctlr-detach-pool:

Detach a pool from a virtual server
```````````````````````````````````

If you want to delete a front-end BIG-IP virtual server, but keep its associated pool(s)/pool member(s):

#. Remove the ``F5_{n}_BIND_ADDR`` label from the App's service definition using the `Marathon Web Interface`_.

   - :menuselection:`Applications --> <App name> --> Configuration --> Edit --> Labels`
   - Click the :guilabel:`minus sign` (-) next to ``F5_{n}_BIND_ADDR``.
   - Click :guilabel:`Change and deploy configuration`.


#. Use the BIG-IP configuration utility to verify the virtual server no longer exists.

   :menuselection:`Local Traffic --> Virtual Servers`

.. _Marathon Application: https://mesosphere.github.io/marathon/docs/application-basics.html
.. _local traffic policy: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/bigip-local-traffic-policies-getting-started-13-0-0/1.html
.. _iRule: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/bigip-system-irules-concepts-11-6-0/1.html
.. _basic Hello Marathon App: https://mesosphere.github.io/marathon/docs/application-basics.html#hello-marathon-an-inline-shell-script
