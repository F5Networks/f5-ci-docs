.. _mctlr-manage-bigip-objects:

Manage BIG-IP LTM objects in Marathon
=====================================

.. sidebar:: Docs test matrix

   We tested this documentation with:

   - ``marathon-1.3.9``
   - ``mesos-1.0.3``
   - ``|mctlr| v1.0.0``


The |mctlr-long| watches the Mesos/Marathon API for Applications with associated :ref:`F5 Application Labels <app-labels>`.
 These Application Labels define the BIG-IP LTM objects |mctlr| creates/manages.

The example JSON blob shown below tells |mctlr| to create one (1) virtual server - with one (1) health monitor and one (1) pool - in the ``/mesos`` partition on the BIG-IP device.

.. literalinclude:: /_static/config_examples/hello-marathon-example.json
   :caption: Example F5 Application Labels defining a BIG-IP virtual server
   :lines: 7-12

.. tip::

   You can also :ref:`deploy iApps with the marathon-bigip-ctlr <mctlr-deploy-iapps>`.

.. _mctlr-create-vs:

Create a virtual server for a Marathon Application
--------------------------------------------------

.. note::

   The code samples below use the `basic Hello Marathon App`_.


#. Create a JSON file containing the App service definitions and F5 labels.

   .. note:: This sample App definition shows labels that use the default :ref:`port index <port-mappings>` (``0``).

   .. literalinclude:: /_static/config_examples/hello-marathon-example.json

   :download:`hello-marathon-example.json </_static/config_examples/hello-marathon-example.json>`


#. Deploy the application in Marathon via the REST API using the JSON file.

   .. code-block:: shell

      curl -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' http://10.190.25.75:8080/v2/apps -d @hello-marathon-example.json

#. Verify creation of the virtual server, pool, and member on the BIG-IP via ``tmsh`` or the configuration utility.

   .. code-block:: text

      admin@(bigip)(cfg-sync Standalone)(Active)(/mesos)(tmos)# show ltm virtual
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

Update a BIG-IP virtual server
------------------------------

#. Edit the Application's JSON service definition.

#. Send the updated file to the Marathon API server.

   .. code-block:: bash

      user@mesos-master:~$ curl -X PUT http://10.190.25.75:8080/v2/apps/basic-0 -d @hello-marathon-example.json -H "Content-type: application/json"
      {"version":"2017-02-21T21:48:12.755Z","deploymentId":"02529d16-258b-41d4-ba06-9765c4d1f8d3"}

#. Verify your changes on the BIG-IP via ``tmsh`` or the configuration utility.

   .. code-block:: bash

      admin@(bigip)(cfg-sync Standalone)(Active)(/mesos)(tmos)$ show ltm virtual

.. _mctlr-delete-objects:

Delete BIG-IP LTM objects
-------------------------

#. Remove the F5 Application Labels from the Application's service definition.

#. Send the updated Application to the Marathon API server.

   .. code-block:: bash

      user@mesos-master:~$ curl -X PUT http://10.190.25.75:8080/v2/apps/basic-0 -d @hello-marathon-example.json -H "Content-type: application/json"
      {"version":"2017-02-21T21:58:11.111Z","deploymentId":"8bdf03d2-8568-46b3-a5a3-61cc397185a1"}

#. Verify the BIG-IP LTM object(s) no longer exist.

   .. code-block:: bash

      admin@(bigip)(cfg-sync Standalone)(Active)(/mesos)(tmos)$ show ltm virtual
      admin@(bigip)(cfg-sync Standalone)(Active)(/mesos)(tmos)$

.. _mctlr-ipam:

Use IPAM to assign IP addresses to BIG-IP virtual servers
---------------------------------------------------------

.. versionadded:: marathon-bigip-ctlr_v1.1.0

You can use IPAM to assign IP addresses to BIG-IP virtual server objects managed by the |mctlr-long|.
To do so, configure your IPAM system to set the ``F5_{0}_BIND_ADDR`` F5 Application Label with a chosen IP address.
The |mctlr| will assign the IP address specific in the application label to the BIG-IP virtual server object associated with the Application.

#. Add the F5 application labels for :ref:`unattached pools <mctlr-pool-only>` to the App definition.

#. Set up your IPAM system to add the ``F5_{0}_BIND_ADDR`` and IP address key-value pair to the Application definition as a Label.

The |mctlr-long| discovers the updated App definition, creates a BIG-IP virtual server object for the App, and attaches the pool to the virtual server.

.. _mctlr-downed-apps:

Connectivity for down or replaced Applications
----------------------------------------------

If you need to take down a`Marathon Application  temporarily and want to keep the associated BIG-IP LTM objects, keep the F5 Application Labels in the application's service definition.
The |mctlr| will continue to manage the associated BIG-IP LTM objects when the App comes back up.
If you deploy a new App with the same name as the one you took down, the |kctlr| associates the existing BIG-IP LTM objects with the new Service.

If you take down an Application and want to remove its corresponding BIG-IP LTM objects, :ref:`delete the F5 Application Labels <mctlr-delete-objects>` from its service definition.

.. _basic Hello Marathon App: https://mesosphere.github.io/marathon/docs/application-basics.html#hello-marathon-an-inline-shell-script
