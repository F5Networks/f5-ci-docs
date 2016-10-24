How to Run |lwp| Manually
`````````````````````````

* Start |lwp| from the command line using a config file:

    .. code-block:: bash

        $ lwp_proxy --config-file=/home/proxy/config.json

-- OR --

* Start |lwp| from the command line using an environment variable:

    .. code-block:: bash

        $ LWP_CONFIG='{ "virtual-servers": { ... } }' lwp_proxy


.. tip::

    Using the environment variable makes it easier to start |lwp| in a containerized environment.

    For example, the following command can be used to start |lwp| with Docker.

    .. code-block:: bash

        $ docker run -e LWP_CONFIG='{ "virtual-servers": { ... } }' -p 8080:8080 -d f5/lwp-proxy

