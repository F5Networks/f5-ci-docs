Installation and Setup
----------------------

The instructions provided here demonstrate how to install the f5-marathon-lb service and configure your Mesos cluster to use your existing BIG-IP device for edge load balancing.

How to Deploy f5-marathon-lb in Marathon
````````````````````````````````````````

#. To deploy the f5-marathon-lb container, add the following JSON to a file named f5-marathon-lb.json:

    .. code-block:: javascript

      {
        "id": "f5-marathon-lb",
        "cmd": null,
        "cpus": 1,
        "mem": 128,
        "disk": 0,
        "instances": 1,
        "args": [
          "sse",
          "--marathon","<marathon_url>:8080",
          "--partition","<bigip_partition_for_mesos_apps>",
          "--hostname","<bigip_admin_console>",
          "--username","<bigip_username>",
          "--password","<bigip_password>"
        ],
        "labels": {},
        "uris": [
            "file:///etc/dockercfg.tgz"
        ],
        "container": {
          "docker": {
            "network": "BRIDGE",
            "parameters": [],
            "image": "<your_registry>/f5-marathon-lb:v0.1.2",
          },
          "type": "DOCKER",
          "volumes": []
        }
      }

    .. important::

        * All options enclosed with "<>" -- for example, "<your_registry>/f5-marathon-lb:v0.1.2" -- must be replaced with the appropriate information for your environment.
        * DC/OS users: Use http://mesos.master:8080 as the value for <marathon_url> in the example above.

#. Next, create the application in Marathon from the command line with the following command referencing the file created earlier:

    .. code-block:: bash

      $ curl -X POST -H "Content-Type: application/json" http://<marathon_url>:8080/v2/apps -d @f5-marathon-lb.json


.. tip:: If your Mesos cluster doesn't have internet access, take the steps below to store a copy of the image locally.

How to Save the Docker Image Locally (Optional)
```````````````````````````````````````````````

#. Pull the f5-marathon-lb image from Docker Hub:

    .. note::

         See :ref:`Docker Authorization` to enable access to the private beta repository.

    .. code-block:: bash

      docker pull f5networks/f5-ci-beta:f5-marathon-lb-v0.1.2

#. Push the image to your own Docker repository:

    .. code-block:: bash

        # Tag and push the downloaded image to your private Docker registry.
        docker tag f5networks/f5-ci-beta:f5-marathon-lb-v0.1.2 <your_registry>/f5-marathon-lb:v0.1.2
        docker push <your_registry>/f5-marathon-lb:v0.1.2
