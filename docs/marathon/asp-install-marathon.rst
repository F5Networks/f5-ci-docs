.. _install-aspm-marathon:
.. _install-asp-marathon:

Install the |aspm-long|
=======================

.. sidebar:: Docs test matrix

   We tested this documentation with:

   - ``marathon-1.3.9``
   - ``mesos-1.0.3``
<<<<<<< f4c787611c8967679bcd00cb11e997f862e4373e
   - ``marathon-bigip-ctlr v1.0.0``
   - ``asp v1.0.0``

The |aspm-long| installs as a Marathon `Application`_.
You can do so via the Marathon REST API, or via the `Marathon Web Interface`_.
=======
   - |mctlr| ``v1.0.0``
   - ``asp v1.1.0``

The |aspm-long| is a docker container that runs as a Marathon `Application`_.
You can install it via the Marathon REST API or the `Marathon Web Interface`_.
>>>>>>> Ephemeral-store doc changes

Initial Setup
-------------

<<<<<<< f4c787611c8967679bcd00cb11e997f862e4373e
.. include:: /_static/reuse/asp-initial-setup.rst
=======
- :ref:`Set up the ASP ephemeral store <install-ephemeral-store-marathon>`. [#aspreq]_
- :ref:`Set up authentication to your secure DC/OS cluster <mesos-authentication>` (optional).
>>>>>>> Ephemeral-store doc changes

#. `Set up Marathon to use a private Docker registry <https://mesosphere.github.io/marathon/docs/native-docker-private-registry.html>`_.

   .. seealso::

      `How to use Docker Registry on DC/OS <https://github.com/dcos/examples/tree/master/registry/1.8>`_

.. ref:`Set up authentication to your secure DC/OS cluster <mesos-authentication>` (optional).

.. _deploy-asp-marathon:

Deploy the |aspm-long| using the Marathon REST API
--------------------------------------------------

#. Create a JSON config file defining the default `Marathon ASP configuration labels </products/connectors/marathon-asp-ctlr/latest/index.html#configuration-parameters>`_.

   .. tip::

      Be sure to include ``"ASP_DEFAULT_URIS": "<docker-config-file-URI>"`` in the App definition.
      Otherwise, Marathon won't be able to pull the ASP image from Docker Store.

   .. literalinclude:: /_static/config_examples/f5-marathon-asp-ctlr-example.json
      :linenos:
<<<<<<< f4c787611c8967679bcd00cb11e997f862e4373e
=======
      :emphasize-lines: 10, 20-49
>>>>>>> Ephemeral-store doc changes

   :fonticon:`fa fa-download` :download:`f5-marathon-asp-ctlr-example.json </_static/config_examples/f5-marathon-asp-ctlr-example.json>`

#. Upload the config file to the Marathon API server.

<<<<<<< f4c787611c8967679bcd00cb11e997f862e4373e
   .. code-block:: console
      :linenos:

      user@mesos-master:~$ curl -X POST -H "Content-Type: application/json" http://10.190.25.75:8080/v2/apps -d @f5-marathon-asp-ctlr.json
=======
   .. code-block:: bash

      user@mesos-master:~$ curl -X POST -H "Content-Type: application/json" //
      http://10.190.25.75:8080/v2/apps -d @f5-marathon-asp-ctlr.json
>>>>>>> Ephemeral-store doc changes


Verify creation
---------------

Send a GET request to the Marathon API server to verify successful creation of the |aspm| App.

.. code-block:: console
   :linenos:
<<<<<<< f4c787611c8967679bcd00cb11e997f862e4373e

   user@mesos-master:~$ curl -X GET http://10.190.25.75:8080/v2/apps/marathon-asp-ctlr | jq .
   {
      "app": {
         "id": "/marathon-asp-ctlr",
         "cmd": null,
         "args": null,
         "user": null,
         "env": {
            "ASP_DEFAULT_MEM": "256",
            "MARATHON_URL": "http://10.190.25.75:8080",
            "ASP_DEFAULT_CONTAINER": "store/f5networks/asp:1.0.0",
            "ASP_DEFAULT_URIS": "file:///etc/docker.tar.gz",
            "ASP_DEFAULT_STATS_FLUSH_INTERVAL": "10000",
            "ASP_DEFAULT_CPU": "1",
            "ASP_ENABLE_LABEL": "f5-asp",
            "ASP_DEFAULT_LOG_LEVEL": "debug"
         },
         "instances": 1,
         "cpus": 1,
         "mem": 128,
         "disk": 0,
         "executor": "",
         "constraints": [],
         "uris": [],
         "fetch": [],
         "storeUrls": [],
         "ports": [],
         "requirePorts": false,
         "backoffSeconds": 1,
         "backoffFactor": 1.15,
         "maxLaunchDelaySeconds": 3600,
         "container": {
            "type": "DOCKER",
            "volumes": [],
            "docker": {
               "image": "f5networks/marathon-asp-ctlr:master",
               "network": "BRIDGE",
               "privileged": false,
               "parameters": [],
               "forcePullImage": true
            }
         },
         "healthChecks": [],
         "dependencies": [],
         "upgradeStrategy": {
            "minimumHealthCapacity": 1,
            "maximumOverCapacity": 1
         },
         "labels": {},
         "acceptedResourceRoles": null,
         "ipAddress": null,
         "version": "2017-02-23T17:51:50.608Z",
         "versionInfo": {
            "lastScalingAt": "2017-02-23T17:51:50.608Z",
            "lastConfigChangeAt": "2017-02-23T17:51:50.608Z"
         },
         "tasksStaged": 0,
         "tasksRunning": 1,
         "tasksHealthy": 0,
         "tasksUnhealthy": 0,
         "deployments": [],
         "tasks": [{
            "id": "marathon-asp-ctlr.c0fd94aa-f9f0-11e6-b795-fa163eb3c6bc",
            "host": "172.16.1.11",
            "ipAddresses": [],
            "ports": [],
            "startedAt": "2017-02-23T17:52:06.982Z",
            "stagedAt": "2017-02-23T17:51:50.669Z",
            "version": "2017-02-23T17:51:50.608Z",
            "slaveId": "28f24575-ca18-4e99-a2fb-a64544c0c67c-S0",
            "appId": "/marathon-asp-ctlr"
         }]
      }
   }

=======
   :emphasize-lines: 1

   user@mesos-master:~$ curl -X GET http://10.190.25.75:8080/v2/apps/marathon-asp-ctlr | jq .
      {
        "app": {
          "id": "/marathon-asp-ctlr",
          "cmd": null,
          "args": null,
          "user": null,
          "env": {
            "ASP_DEFAULT_STATS_URL": "http://<splunk_url>:8088",
            "ASP_DEFAULT_MEM": "256",
            "MARATHON_URL": "http://10.190.25.75:8080",
            "ASP_DEFAULT_STATS_TOKEN": "<provide_stats_auth_token>",
            "ASP_DEFAULT_CONTAINER": "f5networks/asp:1.1",
            "ASP_EPHEMERAL_STORE": "{\"host\": \"ephemeral-store.marathon.l4lb.thisdcos.directory\", \"port\": 8087, \"users\": {\"myUser\" : {\"key\": \"<user-private-key-in-PEM-format>\", \"cert\": \"<user-cert-in-PEM-format>\"}}, \"root-ca\": \"<rootCA-cert-in-PEM-format>\"}",
            "ASP_DEFAULT_STATS_FLUSH_INTERVAL": "10000",
            "ASP_DEFAULT_CPU": "1",
            "ASP_DEFAULT_STATS_BACKEND": "splunk",
            "ASP_ENABLE_LABEL": "ASP",
            "ASP_DEFAULT_LOG_LEVEL": "debug"
          },
          "instances": 1,
          "cpus": 1,
          "mem": 128,
          "disk": 0,
          "gpus": 0,
          "executor": "",
          "constraints": [],
          "uris": [],
          "fetch": [],
          "storeUrls": [],
          "backoffSeconds": 1,
          "backoffFactor": 1.15,
          "maxLaunchDelaySeconds": 3600,
          "container": {
            "type": "DOCKER",
            "volumes": [],
            "docker": {
              "image": "f5networks/marathon-asp-ctlr:1.0.0",
              "network": "BRIDGE",
              "portMappings": null,
              "privileged": false,
              "parameters": [],
              "forcePullImage": true
            }
          },
          "healthChecks": [],
          "readinessChecks": [],
          "dependencies": [],
          "upgradeStrategy": {
            "minimumHealthCapacity": 1,
            "maximumOverCapacity": 1
          },
          "labels": {},
          "acceptedResourceRoles": null,
          "ipAddress": null,
          "version": "2017-06-20T20:27:03.548Z",
          "residency": null,
          "secrets": {},
          "taskKillGracePeriodSeconds": null,
          "ports": [
            10002
          ],
          "portDefinitions": [
            {
              "port": 10002,
              "protocol": "tcp",
              "labels": {}
            }
          ],
          "requirePorts": false,
          "versionInfo": {
            "lastScalingAt": "2017-06-20T20:27:03.548Z",
            "lastConfigChangeAt": "2017-06-20T20:27:03.548Z"
          },
          "tasksStaged": 0,
          "tasksRunning": 1,
          "tasksHealthy": 1,
          "tasksUnhealthy":0,
          "deployments": [],
          "tasks": [...],
        }
      }

.. rubric:: Footnotes
.. [#aspreq] *Required as of* ``asp v1.1.0``.
>>>>>>> Ephemeral-store doc changes

.. _Application: https://mesosphere.github.io/marathon/docs/application-basics.html
.. _Marathon Web Interface: https://mesosphere.github.io/marathon/docs/marathon-ui.html
