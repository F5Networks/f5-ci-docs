.. _install-ephemeral-store-marathon:

Set up ephemeral data storage for the Application Services Proxy
================================================================

.. sidebar: Docs test matrix
   We tested this documentation with:
   - ``marathon-1.3.9``
   - ``mesos-1.0.3``
   - |asp| ``v1.1.0``

.. include:: /_static/reuse/asp-version-added.rst

The |asp| (ASP) shares non-persistent, or ephemeral, data across instances.
It does so by way of a distributed, secure, key-value store called the Ephemeral Store.
The ephemeral store is a Docker-based Marathon `Application`_ .

You can set up the ASP ephemeral store *before* you `deploy the ASP in Marathon <install-asp-marathon>`_, or add the ephemeral store configurations to an existing ASP.

Set up authentication to the ephemeral store
--------------------------------------------

All communications between clients and the ASP ephemeral store use SSL encryption.
Perform the tasks in this section to set up the certificates required for authentication to the ephemeral store.

.. _generate_ephemeral_store_certs-marathon:

Generate root and user certificates
```````````````````````````````````

.. include:: /_static/reuse/generate-ephemeral-store-certs.rst


Deploy the ephemeral store using the Marathon REST API
------------------------------------------------------

#. Define ephemeral store configurations in a JSON file.

   .. important::

      - The ephemeral store app deploys a cluster of 5 tasks; each task requires 1 CPU and 1GB memory.
      - The tasks use ``HOST`` networking mode and connect to ports 8087, 4369, and 8099.

   .. literalinclude:: /_static/config_examples/f5-ephemeral-store-marathon-example.json
      :linenos:

   :download:`f5-ephemeral-store-marathon-example.json </_static/config_examples/f5-ephemeral-store-marathon-example.json>`

#. Upload the config file to the Marathon API server.

   .. code-block:: bash

      user@mesos-master:~$ curl -X POST -H "Content-Type: application/json" //
      http://10.190.25.75:8080/v2/apps -d @f5-ephemeral-store-marathon-example.json

#. To verify creation, send a GET request to the Marathon API server.

   .. code-block:: bash
      :linenos:
      :emphasize-lines: 1

      user@mesos-master:~$ curl -X GET http://10.190.25.75:8080/v2/apps/ephemeral-store | jq.
      {
        "app": {
          "id": "/ephemeral-store",
          "cmd": null,
          "args": null,
          "user": null,
          "env": {
            "ORCHESTRATION": "marathon",
            "EPHEMERAL_STORE_USER": "{ \"name\" : \"myUser\", \"auth_mode\" : \"certificate\" }",
            "EPHEMERAL_STORE_ROOT_CA_CERT": "<root-ca-cert-in-PEM-format>",
            "EPHEMERAL_STORE_ROOT_CA_KEY": "<root-ca-key-in-PEM-format>"
          },
          "instances": 5,
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
              "image": "docker-registry.pdbld.f5net.com/systest-common/ephemeral-store:latest",
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
          "version": "2017-06-20T20:14:48.473Z",
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
            "lastScalingAt": "2017-06-20T20:14:48.473Z",
            "lastConfigChangeAt": "2017-06-20T20:14:48.473Z"
          },
          "tasksStaged": 0,
          "tasksRunning": 5,
          "tasksHealthy": 0,
          "tasksUnhealthy": 0,
          "deployments": [
            {
              "id": "d8baf459-4ae3-4b91-ab93-55014336b789"
            }
          ],
          "tasks": [...]
        }
      }

Learn More
----------

The ephemeral store is a distributed, secure, key-value store used by ASP instances to store and quickly share non-persistent data.
For example, if an :code:`asp` instance learns that a pool member it monitors is unhealthy, it needs to share that information with other instances monitoring the same pool.
The :code:`asp` instance adds the information to the ephemeral store so all other :code:`asp` instances immediately have access to the pool's updated health status.
When new data added to the ephmeral store marks the pool member as healthy, the stale information gets deleted.

The ASP also reports session data to the ephemeral store.
Sharing client session information across servers means, for example, that if multiple servers try to establish a session with a client, one will succeed and the others will fail.

Next Steps
----------

Once you've set up the ephemeral store, you can :ref:`install and deploy the ASP <install-asp-marathon>`.


.. _Application: https://mesosphere.github.io/marathon/docs/application-basics.html
.. _Marathon Web Interface: https://mesosphere.github.io/marathon/docs/marathon-ui.html
