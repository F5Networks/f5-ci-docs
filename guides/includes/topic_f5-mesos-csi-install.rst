F5 Container Service Integrator Installation
````````````````````````````````````````````

To install the f5-marathon-lb service to configure your BIG-IP for edge load balancing with Mesos and Marathon, you must first pull the proper docker image:

.. code:: bash

  $ docker pull f5networks/f5-ci-beta:f5-marathon-lb-v0.1.0

The following commands can be used to push the container service integrator image to your own docker repository:

.. code:: bash

    $ docker images | grep f5-ci-beta
    f5networks/f5-ci-beta  f5-marathon-lb-v0.1.0 a072bbd759e4 6 days ago 327.7 MB

    # Next tag and push the downloaded image to create the repository in your private registry.
    $ docker tag a072bbd759e4 <your_registry>/f5-marathon-lb:v0.1.0
    $ docker push <your_registry>/f5-marathon-lb:v0.1.0

Deploy the F5 Container Service Integrator
``````````````````````````````````````````

To deploy the f5-marathon-lb container, add the following JSON to a file named f5-marathon-lb.json:

.. code:: javascript

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
    "container": {
      "docker": {
        "network": "BRIDGE",
        "parameters": [],
        "image": "<your_registry>/f5-marathon-lb:v0.1.0",
        "portMappings": [
          {
            "containerPort": 0,
            "protocol": "tcp",
            "name": null,
            "labels": null
          }
        ]
      },
      "type": "DOCKER",
      "volumes": []
    }
  }

Replace all the options with the <> symbols with the corresponding information for your environment.

.. note::

  DC/OS users: Use http://mesos.master:8080 as your value for <marathon_url> in the example above.

Next, create the application in Marathon from the command line with the following command referencing the file created earlier:

.. code:: bash

  $ curl -X POST -H "Content-Type: application/json" http://<marathon_url>:8080/v2/apps -d @f5-marathon-lb.json

.. todo::

  Link to the BIG-IP f5-marathon-lb README

For advanced configuration and configuring Marathon applications for edge load balancing, see the BIG-IP f5-marathon-lb README.
