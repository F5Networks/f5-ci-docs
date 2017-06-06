.. _install-mctlr:

Install the |mctlr-long|
========================

.. sidebar:: Docs test matrix

   We tested this documentation with:

   - ``marathon-1.3.9``
   - ``mesos-1.0.3``
   - |mctlr| ``v1.0.0``

The |mctlr-long| installs as a Marathon `Application`_.
You can do this via the Marathon REST API, or via the `Marathon Web Interface`_.

Before you begin
----------------

* :ref:`Set up authentication to your secure DC/OS cluster <mesos-authentication>`.
* `Create a new partition`_ for Marathon on your BIG-IP device.
  The |mctlr-long| cannot manage objects in the ``/Common`` partition.

Launch the |mctlr| App using the Marathon REST API
--------------------------------------------------

#. Create a JSON config file containing the :ref:`required configuration parameters <mctlr-configuration>`.

   .. literalinclude:: /_static/config_examples/f5-marathon-bigip-ctlr-example.json
      :linenos:
      :emphasize-lines: 12, 16-27

   .. tip::

      You can download the example config file below and modify it to suit your environment.

   :download:`f5-marathon-bigip-ctlr-example.json </_static/config_examples/f5-marathon-bigip-ctlr-example.json>`


#. Upload the config file to the Marathon API server.

   .. code-block:: bash
      :linenos:
      :emphasize-lines: 1

      user@mesos-master:~$ curl -X POST -H "Content-Type: application/json" //
      http://10.190.25.75:8080/v2/apps -d @marathon-bigip-ctlr.json
      {"id": "/marathon-bigip-ctlr","cmd": null,"args": null,"user": null, //
      "env":{"MARATHON_URL": "http://10.190.25.75:8080","F5_CC_BIGIP_PASSWORD": "admin", //
      "F5_CC_BIGIP_USERNAME": "admin","F5_CC_BIGIP_HOSTNAME": "10.190.25.80", //
      "F5_CC_PARTITIONS": "mesos"},"instances": 1,"cpus": 0.5,"mem": 64, //
      "disk": 0,"executor": "","constraints": [],"uris": [],"fetch": [], //
      "storeUrls": [],"ports": [0],"requirePorts": false,"backoffSeconds": 1, //
      "backoffFactor": 1.15,"maxLaunchDelaySeconds": 3600,"container":{"type": "DOCKER", //
      "volumes": [],"docker": {"image": "f5networks/marathon-bigip-ctlr:1.0.0", //
      "network": "BRIDGE","privileged": false,"parameters": [],"forcePullImage": false}}, //
      "healthChecks": [],"dependencies": [],"upgradeStrategy": {"minimumHealthCapacity": 1, //
      "maximumOverCapacity": 1},"labels": {},"acceptedResourceRoles": null, //
      "ipAddress": null,"version": "2017-02-21T18:46:19.589Z","tasksStaged": 0, //
      "tasksRunning": 0,"tasksHealthy": 0,"tasksUnhealthy": 0,"deployments":  //
      [{"id": "56b6356d-65ac-478c-aa86-9b3480bd0df4"}],"tasks": []}


Verify creation
---------------

Send a GET request to the Marathon API server to verify successful creation of the |mctlr| App.

.. code-block:: bash
   :emphasize-lines: 1

   user@mesos-master:~$ curl -X GET http://10.190.25.75:8080/v2/apps/marathon-bigip-ctlr
   {"app":{"id":"/marathon-bigip-ctlr","cmd":null,"args":null,"user":null, //
   "env":{"F5_CC_LOG_LEVEL":"DEBUG","MARATHON_URL":"http://10.190.25.75:8080", //
   "F5_CC_BIGIP_PASSWORD":"admin","F5_CC_BIGIP_USERNAME":"admin", //
   "F5_CC_BIGIP_HOSTNAME":"10.190.25.80","F5_CC_PARTITIONS":"mesos"}, //
   "instances":1,"cpus":0.5,"mem":64,"disk":0,"executor":"","constraints":[], //
   "uris":[],"fetch":[],"storeUrls":[],"ports":[10000],"requirePorts":false, //
   "backoffSeconds":1,"backoffFactor":1.15,"maxLaunchDelaySeconds":3600, //
   "container":{"type":"DOCKER","volumes":[],"docker":{"image":"f5networks/marathon-bigip-ctlr:master", //
   "network":"BRIDGE","privileged":false,"parameters":[],"forcePullImage":false}}, //
   "healthChecks":[],"dependencies":[],"upgradeStrategy":{"minimumHealthCapacity":1, //
   "maximumOverCapacity":1},"labels":{},"acceptedResourceRoles":null,"ipAddress":null, //
   "version":"2017-02-21T20:49:53.630Z","versionInfo":{"lastScalingAt":"2017-02-21T20:49:53.630Z", //
   "lastConfigChangeAt":"2017-02-21T20:49:53.630Z"},"tasksStaged":0,"tasksRunning":1, //
   "tasksHealthy":0,"tasksUnhealthy":0,"deployments":[],"tasks":[ //
   {"id":"marathon-bigip-ctlr.4bfb0f85-f877-11e6-b795-fa163eb3c6bc","host":"172.16.1.11", //
   "ipAddresses":[],"ports":[11467],"startedAt":"2017-02-21T20:49:54.925Z", //
   "stagedAt":"2017-02-21T20:49:54.092Z","version":"2017-02-21T20:49:53.630Z"  //
   "slaveId":"28f24575-ca18-4e99-a2fb-a64544c0c67c-S0","appId":"/marathon-bigip-ctlr"}], //
   "lastTaskFailure":{}}}


.. _Create a new partition: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/tmos-implementations-12-1-0/29.html
.. _Application: https://mesosphere.github.io/marathon/docs/application-basics.html
.. _Marathon Web Interface: https://mesosphere.github.io/marathon/docs/marathon-ui.html
