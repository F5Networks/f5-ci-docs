F5 Container Service Integrator Installation
````````````````````````````````````````````

To install the f5-marathon-lb service to configure your BIG-IP for edge load balancing with Mesos and Marathon, you must first pull the proper docker image:

.. code:: bash

  docker pull f5networks/f5-ci-beta/f5-marathon-lb:v0.1.0

.. todo::
  insure that the pull command is correct



If needed, you can then push the image to your own docker repository:

.. code:: bash

    docker push <your_repository>/f5-marathon-lb:beta

To deploy the f5-marathon-lb application to Marathon, you can deploy via:

- Marathon GUI
- Marathon API

**Marathon Installation**

.. todo::

  Explain Marathon GUI with example screenshots

**Marathon API Installation**

Advanced configurations can use a JSON configuration file and the Marathon API to launch the f5-marathon-lb container integrator.

The following can be added to a file named *f5-marathon-lb.json*

.. code::

  {
    "id": "f5-marathon-lb",
    "cpus": 0.5,
    "mem": 128.0,
    "instances": 1,
    "container": {
      "type": "DOCKER",
      "forcePullImage": true,
      "docker": {
        "image": "<your_repository>/f5-marathon-lb:beta",
        "network": "BRIDGE"
      }
    },
    "args": [
      "sse",
      "--marathon", "<marathon_ip_addr>:<port>",
      "--partition", "<big_ip_parition>",
      "--hostname", "<big_ip_addr>",
      "--username", "<big_ip_username>",
      "--password", "<bip_ip_passwd>"
    ]
  }

For advanced configuration, see the BIG-IP f5-marathon-lb usage guide.
