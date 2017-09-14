.. _install-aspm-marathon:
.. _install-asp-marathon:

.. sidebar:: Docs test matrix

   We tested this documentation with:

   - Mesos 1.0.3, Marathon 1.3.9, Ubuntu 16.04, ASP 1.1.0, ASP Controller 1.0.0
   - Mesos 1.0.3, Marathon 1.3.9, Ubuntu 16.04, ASP 1.0.0, ASP Controller 1.0.0

Install the |aspm-long|
=======================

The |aspm-long| is a Docker container that runs as a Marathon `Application`_. You can install it via the Marathon REST API or the `Marathon Web Interface`_.

The |aspm-long| dynamically deploys the |asp| (ASP) in `Apache Mesos Marathon`_ when it discovers a Marathon Application that has the ``f5-asp:enable`` label.

When you launch the |aspm-long|, provide the global configuration parameter(s) you want the |aspm| to use when creating new ASP instances. You can `override the global configurations`_ on a per-Application basis.

Initial Setup
-------------

.. include:: /_static/reuse/asp-initial-setup.rst

#. `Set up Marathon to use a private Docker registry <https://mesosphere.github.io/marathon/docs/native-docker-private-registry.html>`_ so you can pull the ASP image from Docker Store.

   .. seealso::

      `How to use Docker Registry on DC/OS <https://github.com/dcos/examples/tree/master/registry/1.8>`_

#. :ref:`Set up the ASP ephemeral store <install-ephemeral-store-marathon>`. [#aspreq]_

.. ref:`Set up authentication to your secure DC/OS cluster <mesos-authentication>` (optional).

.. _deploy-asp-marathon:

Deploy the |aspm-long|
----------------------

#. Define the default `Marathon ASP configuration labels </products/connectors/marathon-asp-ctlr/latest/index.html#configuration-parameters>`_ in a JSON file.

   .. tip::

      Provide the URI for your Docker config file in the App definition using the ``ASP_DEFAULT_URIS`` in the App definition.
      Otherwise, Marathon won't be able to pull the ASP image from Docker Store.

   \

   .. literalinclude:: /_static/config_examples/f5-marathon-asp-ctlr-example.json
      :linenos:

   :fonticon:`fa fa-download` :download:`f5-marathon-asp-ctlr-example.json </_static/config_examples/f5-marathon-asp-ctlr-example.json>`

#. Upload the config file to the Marathon API server.

   .. code-block:: console
      :linenos:

      $ curl -X POST -H "Content-Type: application/json" http://<marathon-uri>:8080/v2/apps -d @f5-marathon-asp-ctlr.json

#. Send a GET request to the Marathon API server to verify successful creation of the |aspm| App.

.. tip::

   You can pass the response through a pretty-print tool like `jq <https://github.com/stedolan/jq>`_ for better readability.

.. code-block:: console
   :linenos:
   :emphasize-lines: 1

   $ curl -X GET http://10.190.25.75:8080/v2/apps/marathon-asp-ctlr | jq .
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
            "ASP_EPHEMERAL_STORE": "{\"host\": \"ephemeral-store.marathon.l4lb.thisdcos.directory\", \"port\": 8087, \"users\": {\"myUser\" : {\"key\": \"----REDACTED----\", \"cert\": \"----REDACTED----\"}}, \"root-ca\": \"----REDACTED----\"}",
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
              "image": "f5networks/marathon-asp-ctlr:1.1.0",
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

What's Next
-----------

- Learn how to :ref:`launch an ASP instance <marathon-asp-deploy>` and :ref:`override the global configurations <marathon-asp-custom-config>`.

.. rubric:: Footnotes
.. [#aspreq] *Required as of* ``asp v1.1.0``.

.. _Application: https://mesosphere.github.io/marathon/docs/application-basics.html
.. _Marathon Web Interface: https://mesosphere.github.io/marathon/docs/marathon-ui.html
