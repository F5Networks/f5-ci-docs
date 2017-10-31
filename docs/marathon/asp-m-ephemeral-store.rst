.. include:: /_static/reuse/asp-version-added-1_1.rst

.. sidebar:: Docs test matrix

   We tested this documentation with:

   - Mesos 1.0.3, Marathon 1.3.9, Ubuntu 16.04, ASP 1.1.0, ASP Controller 1.0.0

.. _install-ephemeral-store-marathon:

Set up the ASP ephemeral store - Marathon
=========================================

The |asp| (ASP) shares non-persistent, or ephemeral, data across instances.
It does so by way of a distributed, secure, key-value store called the Ephemeral Store.
The ephemeral store is a Docker-based Marathon `Application`_ .

You can set up the ASP ephemeral store *before* you `deploy the ASP in Marathon <install-asp-marathon>`_ -- OR --
add the ephemeral store configurations to an existing ASP running v1.1.0.

.. warning::

   The ephemeral store is not compatible with ASP v1.0.0.
   If you have a previous version of the ASP running, remove it and :ref:`deploy a new Application <deploy-asp-marathon>` running v1.1.0.

Set up authentication to the ephemeral store
--------------------------------------------

All communications between clients and the ASP ephemeral store use SSL encryption.
Perform the tasks in this section to set up the certificates required for authentication to the ephemeral store.

.. _generate_ephemeral_store_certs-marathon:

Generate root and user certificates
```````````````````````````````````

.. include:: /_static/reuse/generate-ephemeral-store-certs.rst


Deploy the ephemeral store
--------------------------

.. important::

   - Each ephemeral store instance requires a dedicated node with 1 CPU and at least 1GB memory.
   - By default, the ephemeral store app deploys a cluster of five (5) instances.
     **Do not deploy the ephemeral store with fewer than five instances or you may experience data loss.**
   - The instances use ``HOST`` networking mode and connect to ports 8087, 4369, and 8099.

#. Define the ephemeral store configurations in a JSON file.

   .. literalinclude:: /_static/config_examples/f5-ephemeral-store-marathon-example.json
      :linenos:

   :download:`f5-ephemeral-store-marathon-example.json </_static/config_examples/f5-ephemeral-store-marathon-example.json>`

#. Upload the config file to the Marathon API server.

   .. code-block:: bash

      $ curl -X POST -H "Content-Type: application/json" http://<marathon-uri>:8080/v2/apps -d @f5-ephemeral-store-marathon-example.json


#. To verify creation, send a GET request to the Marathon API server.

   .. tip::

      You can pass the response through a pretty-print tool like `jq <https://github.com/stedolan/jq>`_ for better readability.

   .. code-block:: bash
      :linenos:
      :emphasize-lines: 1

      $ curl -X GET http://<marathon-uri>:8080/v2/apps/ephemeral-store | jq .
        % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                       Dload  Upload   Total   Spent    Left  Speed
      100  4079    0  4079    0     0   332k      0 --:--:-- --:--:-- --:--:--  362k
      {
        "app": {
          "id": "/ephemeral-store",
          "cmd": null,
          "args": null,
          "user": null,
          "env": {
            "ORCHESTRATION": "marathon",
            "EPHEMERAL_STORE_USER": "{ \"name\" : \"myuser\", \"auth_mode\" : \"certificate\" }",
            "EPHEMERAL_STORE_ROOT_CA_CERT": "-----BEGIN CERTIFICATE-----<redacted>-----END CERTIFICATE-----",
            "EPHEMERAL_STORE_ROOT_CA_KEY": "-----BEGIN RSA PRIVATE KEY-----<redacted>-----END RSA PRIVATE KEY-----"
          },
          "instances": 1,
          "cpus": 1,
          "mem": 1024,
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
              "image": "f5networks/ephemeral-store:latest",
              "network": "HOST",
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
          "version": "2017-10-02T18:56:43.319Z",
          "residency": null,
          "secrets": {},
          "taskKillGracePeriodSeconds": null,
          "ports": [
            8087,
            4369,
            8099
          ],
          "portDefinitions": [
            {
              "port": 8087,
              "protocol": "tcp",
              "name": "proto",
              "labels": {
                "VIP_0": "ephemeral-store:8087"
              }
            },
            {
              "port": 4369,
              "protocol": "tcp",
              "name": "epmd",
              "labels": {}
            },
            {
              "port": 8099,
              "protocol": "tcp",
              "name": "handoff",
              "labels": {}
            }
          ],
          "requirePorts": true,
          "versionInfo": {
            "lastScalingAt": "2017-10-02T18:56:43.319Z",
            "lastConfigChangeAt": "2017-10-02T18:36:25.016Z"
          },
          "tasksStaged": 0,
          "tasksRunning": 0,
          "tasksHealthy": 0,
          "tasksUnhealthy": 0,
          "deployments": [
            {
              "id": "cceb4265-b60f-4b7a-bb76-96227a35ebb0"
            }
          ],
          "tasks": []
        }
      }


Next Steps
----------

Once you've set up the ephemeral store, you can :ref:`install and deploy the ASP <install-asp-marathon>`.


Learn More
----------

See the `ASP ephemeral store`_ and `ASP health monitor`_ documentation.


.. _Application: https://mesosphere.github.io/marathon/docs/application-basics.html
.. _Marathon Web Interface: https://mesosphere.github.io/marathon/docs/marathon-ui.html
