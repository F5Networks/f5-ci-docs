F5 Lightweight Proxy and LWP-Controller Setup
=============================================

The instructions provided here demonstrate how to install the lwp-controller and lightweight-proxy, and provide a basic configuration example.

.. important::

    Normally, the lwp-controller is deployed from within Marathon. It dynamically deploys the lightweight-proxy as needed. The examples and instructions here are provided for informational and/or development purposes. We recommend following the :ref:`Usage Guide <usage-guide>` to test deployment of these tools in Marathon.


#. Pull the lightweight-proxy and lwp-controller from Docker Hub:

    .. code-block:: bash

        docker pull f5networks/f5-ci-beta:light-weight-proxy-v0.1.0
        docker pull f5networks/f5-ci-beta:lwp-controller-v0.1.0

#. Push the images to your own Docker repository for easy access (optional):

    .. todo:: add instructions here

Deploy lwp-controller
---------------------

#. Deploy the lwp-controller in your Docker container:

.. code-block:: shell

        docker run -it -d -e MARATHON_URL="http://api.mesos.example.com:8080" -e LWP_ENABLE_LABEL lwp-myapp -e LWP_DEFAULT_CONTAINER f5networks/lwp f5velcro/lwp-controller

#. Create your application in the Marathon instance running in Marathon and label it with the label ``lwp-myapp:enable``. The lwp-controller will create a new application in your Marathon cluster to be the LWP for your application.


.. note:: Advanced configuration options are provided in the :ref:`lwp-controller README <Lightweight Proxy Controller>`.


Deploy lightweight-proxy
------------------------

#. Set up your preferred configuration options. [#]_

    Example: A JSON configuration file with two virtual server sections.

    .. code-block:: json
        :linenos:
        :emphasize-lines: 3, 7, 8

        {
          "global": {
            "marathon-uri": "http://api.mesos.example.com",
            "console-log-level": "debug"
          },
          "stats": {
            "url": "http://localhost:8088",
            "token": "this-is-the-token",
            "flushInterval": 10000,
            "backend": "splunk"
          },
          "virtual-servers": [
            {
              "destination": 8080,
              "service-name": "web-server",
              "ip-protocol": "http",
              "load-balancing-mode": "round-robin",
              "flags" : {
                "x-forwarded-for": false,
                "x-served-by": true
              }
            },
            {
              "destination": 9090,
              "service-name": "identity",
              "ip-protocol": "http",
              "load-balancing-mode": "round-robin",
              "keep-alive-msecs": 2000
            }
          ]
        }

.. important::

    * You must provide the appropriate information for your environment in the highlighted lines.
    * In this example, Splunk is being used as the stats collector. [#]_


#. Deploy the lightweight proxy in your docker container:

    .. code-block:: bash

        $ lwp_proxy --config-file=/home/proxy/config.json



.. [#] See the :ref:`Lightweight Proxy Controller README <Lightweight Proxy Controller>` for more information.
.. [#] See the :ref:`Usage Guide <usage-guide>` for more information.
