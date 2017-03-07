.. _install-asp-marathon:

Install the |asp| in Marathon
=============================

.. table:: Docs test matrix

    +-----------------------------------------------------------+
    | marathon-1.3.9                                            |
    +-----------------------------------------------------------+
    | mesos-1.0.3                                               |
    +-----------------------------------------------------------+
    | |aspm| v1.0.0                                             |
    +-----------------------------------------------------------+
    | ``asp`` v1.0.0                                            |
    +-----------------------------------------------------------+


The |aspm-long| installs as a Marathon `Application`_. You can do so via the Marathon REST API, or via the `Marathon Web Interface`_.

Before you begin
----------------

* :ref:`Set up authentication to your secure DC/OS cluster <mesos-authentication>` (optional).


Deploy the |aspm-long| using the Marathon REST API
--------------------------------------------------

#. Create a JSON config file defining the default configurations for the :ref:`ASP <tbd>`.

    .. literalinclude:: /_static/config_examples/f5-marathon-asp-ctlr-example.json
        :linenos:
        :emphasize-lines: 9, 17-31

    .. tip::

        You can download the example config file below and modify it to suit your environment.

        :download:`f5-marathon-asp-ctlr-example.json </_static/config_examples/f5-marathon-asp-ctlr-example.json>`


#. Upload the config file to the Marathon API server.

    .. code-block:: bash
        :linenos:
        :emphasize-lines: 1, 2

        user@mesos-master:~$ curl -X POST -H "Content-Type: application/json" //
        http://10.190.25.75:8080/v2/apps -d @f5-marathon-asp-ctlr.json
        {"id":"/marathon-asp-ctlr","cmd":null,"args":null,"user":null, //
        "env":{"ASP_DEFAULT_MEM":"256", "MARATHON_URL":"http://10.190.25.75:8080", //
        "ASP_DEFAULT_CONTAINER":"docker-registry.pdbld.f5net .com/velcro/asp:master", //
        "ASP_DEFAULT_STATS_FLUSH_INTERVAL":"10000","ASP_DEFAULT_CPU":"1", //
        "ASP_ENABLE_LABEL":"ASP","ASP_DEFAULT_LOG_LEVEL":"debug"},"instances":1, //
        "cpus":1,"mem":128,"disk":0, "executor":"","constraints":[],"uris":[], //
        "fetch":[],"storeUrls":[],"ports":[],"requirePorts":false, "backoffSeconds":1, //
        "backoffFactor":1.15,"maxLaunchDelaySeconds":3600,"container":{"type":"DOCKER", //
         "volumes":[], "docker":{"image":"f5networks/marathon-asp-ctlr:master", //
         "network":"BRIDGE", "portMappings":[],"privileged":false,"parameters":[], //
         "forcePullImage":true}},"healthChecks":[], "dependencies":[], //
         "upgradeStrategy":{"minimumHealthCapacity":1,"maximumOverCapacity":1}, //
         "labels":{}, "acceptedResourceRoles":null, "ipAddress":null, //
         "version":"2017-02-23T17:51:50.608Z","tasksStaged":0, "tasksRunning":0, //
         "tasksHealthy":0, "tasksUnhealthy":0,"deployments":[ //
         {"id":"b644ea55-99dd-41af-87ee-477e73b326d4"}],"tasks":[]} //



Verify creation
---------------

Send a GET request to the Marathon API server to verify successful creation of the |aspm| App.

.. code-block:: bash
    :linenos:
    :emphasize-lines: 1

    user@mesos-master:~$ curl -X GET http://10.190.25.75:8080/v2/apps/marathon-asp-ctlr
    {"app":{"id":"/marathon-asp-ctlr","cmd":null,"args":null,"user":null, //
    "env":{"ASP_DEFAULT_MEM":"256","MARATHON_URL":"http://10.190.25.75:8080", //
    "ASP_DEFAULT_CONTAINER":"f5networks/asp:master","ASP_DEFAULT_STATS_FLUSH_INTERVAL":"10000", //
    "ASP_DEFAULT_CPU":"1","ASP_ENABLE_LABEL":"ASP","ASP_DEFAULT_LOG_LEVEL":"debug"}, //
    "instances":1,"cpus":1,"mem":128,"disk":0,"executor":"","constraints":[],"uris":[], //
    "fetch":[],"storeUrls":[],"ports":[],"requirePorts":false,"backoffSeconds":1, //
    "backoffFactor":1.15,"maxLaunchDelaySeconds":3600,"container":{"type":"DOCKER", //
    "volumes":[],"docker":{"image":"f5networks/marathon-asp-ctlr:master","network":"BRIDGE", //
    "privileged":false,"parameters":[],"forcePullImage":true}},"healthChecks":[], //
    "dependencies":[],"upgradeStrategy":{"minimumHealthCapacity":1,"maximumOverCapacity":1}, //
    "labels":{},"acceptedResourceRoles":null,"ipAddress":null,"version":"2017-02-23T17:51:50.608Z", //
    "versionInfo":{"lastScalingAt":"2017-02-23T17:51:50.608Z", //
    "lastConfigChangeAt":"2017-02-23T17:51:50.608Z"},"tasksStaged":0,"tasksRunning":1, //
    "tasksHealthy":0,"tasksUnhealthy":0,"deployments":[],"tasks":[ //
    {"id":"marathon-asp-ctlr.c0fd94aa-f9f0-11e6-b795-fa163eb3c6bc","host":"172.16.1.11", //
    "ipAddresses":[],"ports":[],"startedAt":"2017-02-23T17:52:06.982Z", //
    "stagedAt":"2017-02-23T17:51:50.669Z","version":"2017-02-23T17:51:50.608Z", //
    "slaveId":"28f24575-ca18-4e99-a2fb-a64544c0c67c-S0","appId":"/marathon-asp-ctlr"}]}}


.. _Application: https://mesosphere.github.io/marathon/docs/application-basics.html
.. _Marathon Web Interface: https://mesosphere.github.io/marathon/docs/marathon-ui.html
