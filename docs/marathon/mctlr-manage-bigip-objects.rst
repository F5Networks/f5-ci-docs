.. _mctlr-manage-bigip-objects:

Manage BIG-IP objects with |mctlr-long|
=======================================

.. table:: Docs test matrix

    +-----------------------------------------------------------+
    | marathon-1.3.9                                            |
    +-----------------------------------------------------------+
    | mesos-1.0.3                                               |
    +-----------------------------------------------------------+
    | |mctlr| v1.0.0                                            |
    +-----------------------------------------------------------+


Include the |mctlr| F5 :ref:`Application Labels <app-labels>` in a Marathon Application's definition. These Application Labels define the BIG-IP objects |mctlr| manages.

The example JSON blob shown below uses the F5 Application Labels to tell |mctlr| to create one (1) virtual server - with one (1) health monitor and one (1) pool - in the ``/mesos`` partition on the BIG-IP.

.. literalinclude:: /_static/config_examples/hello-marathon-example.json
    :caption: Example F5 Application Labels defining a BIG-IP virtual server
    :lines: 7-12

.. tip::

    You can also :ref:`deploy iApps with the marathon-bigip-ctlr <mctlr-deploy-iapps>`.

Create a virtual server for a Marathon Application
--------------------------------------------------

.. note:: The below code samples use the `basic Hello Marathon App`_.


#. Create a JSON file containing the App service definitions and F5 labels.

    .. note:: This sample App definition shows labels that use the default :ref:`port index <port-mappings>` (``0``).

    .. literalinclude:: /_static/config_examples/hello-marathon-example.json

    :download:`hello-marathon-example.json </_static/config_examples/hello-marathon-example.json>`


#. Deploy the application in Marathon via the REST API using the JSON file.

    .. code-block:: shell

        curl -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' http://10.190.25.75:8080/v2/apps -d @hello-marathon-example.json




#. Verify creation of the virtual server, pool, and member on the BIG-IP via ``tmsh`` or the configuration utility.

    .. code-block:: text

        root@(bigip)(cfg-sync Standalone)(Active)(/mesos)(tmos)# show ltm virtual
        ------------------------------------------------------------------
        Ltm::Virtual Server: basic-0_10.190.25.70_8080
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

    In the above example, the "Availability" is "unknown" because there are no health monitors associated with the virtual server. You can add :ref:`health checks <health-checks>` to the App in Marathon; the |mctlr| will create corresponding health monitors on the BIG-IP.

Update a virtual server
-----------------------

#. Edit the Application's JSON service definition as needed.

#. Send the updated file to the Marathon API server.

    .. code-block:: bash

        user@mesos-master:~$ curl -X PUT http://10.190.25.75:8080/v2/apps/basic-0 -d @hello-marathon-example.json -H "Content-type: application/json"
        {"version":"2017-02-21T21:48:12.755Z","deploymentId":"02529d16-258b-41d4-ba06-9765c4d1f8d3"}


#. Verify your changes on the BIG-IP via ``tmsh`` or the configuration utility.

    .. code-block:: bash

        root@(bigip)(cfg-sync Standalone)(Active)(/mesos)(tmos)# show ltm virtual


Delete a virtual server
-----------------------

#. Remove the Application Labels from the Application's service definition.

#. Update the Application on the Marathon API server to delete the corresponding virtual server from the BIG-IP.

    .. code-block:: bash

        user@mesos-master:~$ curl -X PUT http://10.190.25.75:8080/v2/apps/basic-0 -d @hello-marathon-example.json -H "Content-type: application/json"
        {"version":"2017-02-21T21:58:11.111Z","deploymentId":"8bdf03d2-8568-46b3-a5a3-61cc397185a1"}


#. Verify the virtual server no longer exists on the BIG-IP via the configuration utility.

    .. code-block:: bash

        root@(bigip)(cfg-sync Standalone)(Active)(/mesos)(tmos)# show ltm virtual
        root@(bigip)(cfg-sync Standalone)(Active)(/mesos)(tmos)#



.. _basic Hello Marathon App: https://mesosphere.github.io/marathon/docs/application-basics.html#hello-marathon-an-inline-shell-script
