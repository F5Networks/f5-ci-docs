.. _mesos-integration:

F5 Container Services Mesos Integration
=======================================

Overview
--------

The F5® Container Services Integration beta release provides the means to do the following in Mesos:

    - use BIG-IP® as an edge load balancer for North-South traffic;
    - use the F5 Lightweight Proxy to load balance East-West traffic within Marathon.


Prerequisites
-------------

- A Mesos/Marathon environment with containerization enabled. See `Running Docker Containers on Marathon <https://mesosphere.github.io/marathon/docs/native-docker.html>`_ for configuration instructions.
- Access to the F5 Integration for Mesos Environments beta site. This is where all components are available for download.
- An Amazon AWS account that can incur small charges, -OR-
- An existing Mesos+Marathon environment.
- A BIG-IP with active license (Good, Better, or Best); a VE lab license that can be used in AWS can be provided by your F5 sales rep.
- Internet access (required for AWS and to pull images from Docker).
- `Docker <https://docs.docker.com/engine/getstarted/>`_ installed and at least one running container.

Set up Docker authorization
```````````````````````````

Both the f5-marathon-lb and lightweight-proxy-controller run as dockerized container applications inside of Marathon.

In order to retrieve the corresponding images during the F5 Integration for Mesos Environments beta, you will need to the proper authorization to access the private docker images in the F5 Networks repository.

From the command line on your system, add the following to your local docker configuration file, $HOME/.docker/config.json with the following:

.. code:: javascript

  {
    "auths": {
      "https://index.docker.io/v1/": {
        "auth": "ZjViZXRhdXNlcjpjOURUS3RBVnQyZHc="
      }
    }
  }%

For Windows users, the file is located at *%HOME%\.docker\config.json*

Caveats
-------
None


Configuration
-------------

.. include:: includes/topic_f5-mesos-csi-install.rst

.. include:: includes/topic_f5-mesos-lwp-install.rst


Further Reading
---------------

For advanced configuration options and additional information regarding configuring Marathon applications for edge load balancing, see the project READMEs and the Usage Guide.

    - :ref:`f5-marathon-lb`
    - :ref:`lightweight-proxy <Lightweight Proxy>`
    - :ref:`lwp-controller <Lightweight Proxy Controller>`
    - :ref:`Usage Guide: F5 Container Integration in a Mesos/Marathon Environment`
