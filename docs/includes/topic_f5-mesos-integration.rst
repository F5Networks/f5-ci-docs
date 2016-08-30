.. _mesos-integration:

Mesos Integration
-----------------

The F5® Container Services Integration beta release provides the means to do the following in Mesos:

    - use BIG-IP® as an edge load balancer for North-South traffic;
    - use the F5 Lightweight Proxy to load balance East-West traffic within Marathon.


Prerequisites
`````````````

- Access to the F5 Integration for Mesos Environments beta site. This is where all components are available for download.
- An existing Mesos environment with Marathon configured.
- A BIG-IP with active license (Good, Better, or Best); a VE lab license that can be used in AWS can be provided by your F5 sales rep.
- Internet access (required to pull images from Docker).
- `Docker <https://docs.docker.com/engine/getstarted/>`_ installed and at least one running container.

Caveats
```````

Docker Authorization
~~~~~~~~~~~~~~~~~~~~

Both the f5-marathon-lb and lightweight-proxy-controller run as Dockerized container applications inside of Marathon. Because the F5 CSI beta Docker repository is private, you will need to add the Docker authorization to Marathon. [#]_

If you are running the F5 Integration for Mesos Environments beta in your own Marathon environment, take the following steps to add the Docker authorization to each Mesos node to make them accessible by the "URIs" property of the Marathon app.

     * Download :file:`dockercfg-beta.tgz` from the F5 Beta site.
     * Add :file:`dockercfg-beta.tgz` to the ``/etc/`` directory on each Mesos node as ``dockercfg.tgz``.

If you want to push the Docker image into your own registry, you can use a local Docker install to pull the private image, then push to your own repository. To authorize Docker, extract :file:`dockercfg-beta.tgz` into your home directory to create the file :file:`$HOME/.docker/config.json`. Check to see if an existing config.json file exists and create a backup of it before proceeding.

The command in the example below will extract the .tgz file from the Downloads directory; change the location of the .tgz as appropriate for your environment.

    .. code-block:: bash

        cd $HOME
        tar -xvf ~/Downloads/dockercfg-beta.tgz

.. [#] If you are running the beta from the AWS CloudFormation template, the authorization is set up automatically.


Further Reading
```````````````

For advanced configuration options and additional information regarding configuring Marathon applications for edge load balancing, see the project READMEs and the Usage Guide.

    - :ref:`f5-marathon-lb`
    - :ref:`Lightweight Proxy`
    - :ref:`Lightweight Proxy Controller`
    - :ref:`Usage Guide: F5 Container Integration in a Mesos/Marathon Environment`
