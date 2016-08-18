f5-marathon-lb
==============

.. toctree::
    :hidden:
    :glob:

    self


Part of the F5® Container Services Integration suite, f5-marathon-lb allows users to manage BIG-IP® devices in a  `Mesos <https://mesos.apache.org/>`_ / `Marathon <https://github.com/mesosphere/marathon>`_ environment.

Architecture
------------

F5's f5-marathon-lb is a service discovery and load balancing tool for Marathon used to configure an F5 BIG-IP device by consuming the app state. It reads the Marathon task information and dynamically generates BIG-IP configuration details.

f5-marathon-lb listens to the Marathon event stream and automatically updates the configuration of the BIG-IP as follows:

-  Matches Marathon apps by the specified BIG-IP partition.
-  Creates a Virtual Server and pool for each app type in Marathon that matches the BIG-IP partition.
-  For each task, creates a pool member and adds the member to the server pool.
-  If the app has a Marathon Health Monitor configured, creates a corresponding health monitor for each BIG-IP pool member.

To gather the task information, f5-marathon-lb needs to know where to find Marathon. The service :ref:`configuration` details are stored in Marathon :ref:`application labels`.

Partitions and Resources
------------------------

f5-marathon-lb allows you to manage resources in specific partitions on a BIG-IP device. The partitions you want to manage with f5-marathon-lb must already exist on the BIG-IP before you configure anything in Marathon.

.. warning::

    * f5-marathon-lb can not manage the "Common" partition.


The BIG-IP object types listed below are managed by the f5-marathon-lb application; these should not be manually added, changed, or deleted, as this may result in unexpected behavior.

-  Virtual Servers
-  Virtual Addresses
-  Pools
-  Pool Members
-  Nodes
-  Health Monitors
-  Application Services


Configuration
-------------

First, f5-marathon-lb needs to know how to connect to Marathon and the BIG-IP. This is done via the command-line arguments:

.. code-block:: console

    usage: f5_marathon_lb.py [-h] [--longhelp]
                             [--marathon MARATHON [MARATHON ...]]
                             [--listening LISTENING] [--callback-url CALLBACK_URL]
                             [--hostname HOSTNAME] [--username USERNAME]
                             [--password PASSWORD] [--partition PARTITION] [--sse]
                             [--health-check] [--syslog-socket SYSLOG_SOCKET]
                             [--log-format LOG_FORMAT]
                             [--marathon-auth-credential-file MARATHON_AUTH_CREDENTIAL_FILE]

    If an arg is specified in more than one place, then commandline values override environment variables, which override defaults.

    optional arguments:
      -h, --help            show this help message and exit
      --longhelp            Print out configuration details (default: False)
      --marathon MARATHON [MARATHON ...], -m MARATHON [MARATHON ...]
                            [required] Marathon endpoint, eg. -m
                            http://marathon1:8080 http://marathon2:8080 [env var:
                            MARATHON_URL] (default: None)
      --listening LISTENING, -l LISTENING
                            The address this script listens on for marathon events
                            [env var: F5_CSI_LISTENING_ADDR] (default: None)
      --callback-url CALLBACK_URL, -u CALLBACK_URL
                            The HTTP address that Marathon can call this script
                            back at (http://lb1:8080) [env var:
                            F5_CSI_CALLBACK_URL] (default: None)
      --hostname HOSTNAME   F5 BIG-IP hostname [env var: F5_CSI_BIGIP_HOSTNAME]
                            (default: None)
      --username USERNAME   F5 BIG-IP username [env var: F5_CSI_BIGIP_USERNAME]
                            (default: None)
      --password PASSWORD   F5 BIG-IP password [env var: F5_CSI_BIGIP_PASSWORD]
                            (default: None)
      --partition PARTITION
                            [required] Only generate config for apps which match
                            the specified partition. Use '*' to match all
                            partitions. Can use this arg multiple times to specify
                            multiple partitions [env var: F5_CSI_PARTITIONS]
                            (default: [])
      --sse, -s             Use Server Sent Events instead of HTTP Callbacks [env
                            var: F5_CSI_USE_SSE] (default: False)
      --health-check, -H    If set, respect Marathon's health check statuses
                            before adding the app instance into the backend pool.
                            [env var: F5_CSI_USE_HEALTHCHECK] (default: False)
      --sse-timeout SSE_TIMEOUT, -t SSE_TIMEOUT
                            Marathon event stream timeout [env var:
                            F5_CSI_SSE_TIMEOUT] (default: 30)
      --syslog-socket SYSLOG_SOCKET
                            Socket to write syslog messages to. Use '/dev/null' to
                            disable logging to syslog [env var:
                            F5_CSI_SYSLOG_SOCKET] (default: /var/run/syslog)
      --log-format LOG_FORMAT
                            Set log message format [env var: F5_CSI_LOG_FORMAT]
                            (default: %(asctime)s %(name)s: %(levelname) -8s:
                            %(message)s)
      --marathon-auth-credential-file MARATHON_AUTH_CREDENTIAL_FILE
                            Path to file containing a user/pass for the Marathon
                            HTTP API in the format of 'user:pass'. [env var:
                            F5_CSI_MARATHON_AUTH] (default: None)

.. important:: The **marathon**, **hostname**, **username**, **password**, and **partition** arguments are mandatory.

Use the ``--partition`` argument multiple times to specify multiple BIG-IP partitions (e.g. ``--partition tenant_a --partition tenant_b``).

.. topic:: Example

    .. code-block:: console

         f5-marathon-lb.py --marathon http://marathon1:8080 http://marathon2:8080 --hostname https://10.190.4.187 --username admin --password admin --partition tenant_a



Application Labels
------------------

Applications managed by f5-marathon-lb are identified and configured via their *Marathon Labels*. Some labels are specified *per service port*. These are denoted with the ``{n}`` parameter in the label key; ``{n}`` corresponds to the service port index, beginning at ``0``.

The list of labels which can be specified are:

==================== ================================================ =========== ===================================================================================================
Field                Definition                                       Default     Additional Information
==================== ================================================ =========== ===================================================================================================
F5_PARTITION         The BIG-IP partition to be configured                        | * Resources like virtual servers and pool members are configured in this partition on BIG-IP.
                                                                                  | * The partition must be owned by f5-marathon-lb  (configured via the ``--partition`` argument).
-------------------- ------------------------------------------------ ----------- ---------------------------------------------------------------------------------------------------
\F5_{n}_BIND_ADDR    Bind to the specific address for the service                 | Example: ``"F5_0_BIND_ADDR": "10.0.0.42"``
-------------------- ------------------------------------------------ ----------- ---------------------------------------------------------------------------------------------------
\F5_{n}_PORT         Bind to the specific port for the service                    | This setting overrides ``servicePort``, which must be unique.
                                                                                  | Example: ``"F5_0_PORT": "80"``
-------------------- ------------------------------------------------ ----------- ---------------------------------------------------------------------------------------------------
\F5_{n}_MODE         Set the connection mode (TCP or HTTP)            TCP         | Example: ``"F5_0_MODE": "http"``
-------------------- ------------------------------------------------ ----------- ---------------------------------------------------------------------------------------------------
\F5_{n}_BALANCE      Set the load balancing algorithm                 roundrobin  | Example: ``"F5_0_BALANCE": "leastconn"``
-------------------- ------------------------------------------------ ----------- ---------------------------------------------------------------------------------------------------
\F5_{n}_SSL_PROFILE  Set the SSL profile for the HTTPS Virtual Server             | Example: ``"F5_0_SSL_PROFILE": "Common/clentssl"``
==================== ================================================ =========== ===================================================================================================


iApps
-----

iApps® is the BIG-IP system framework for deploying services-based, template-driven configurations on BIG-IP systems running TMOS 11.0.0 and later. It consists of three components: Templates, Application Services, and Analytics. An iApps Template is where the application is described and the objects (required and optional) are defined through presentation and implementation language. An iApps Application Service is the deployment process of an iApps Template which bundles all of the configuration options for a particular application together.

iApp Application Labels
~~~~~~~~~~~~~~~~~~~~~~~

You can use f5-marathon-lb to instantiate and manage an iApp Application Service. The iApp template and variables are specified via the Marathon application labels.

.. important::

    In all cases, the iApp template must already be installed on the BIG-IP. The variable names and values are specific to the template being used.

====================================    =================================================================   =======================================================================
Field                                   Definition                                                          Additional Information
====================================    =================================================================   =======================================================================
\F5_{n}_IAPP_TEMPLATE                   The iApp template to create the Application Service                 | Example: ``"F5_0_IAPP_TEMPLATE": "/Common/f5.http"``
------------------------------------    -----------------------------------------------------------------   -----------------------------------------------------------------------
\F5_{n}_IAPP_OPTION_*                   Defines configuration options for the service                       | Example: ``"F5_0_IAPP_OPTION_description": "This is a test iApp"``
------------------------------------    -----------------------------------------------------------------   -----------------------------------------------------------------------
\F5_{n}_IAPP_VARIABLE_*                 Defines the variables needed by the iApp to create the service      | * Use an existing resource, or
                                                                                                            | * tell the service to create a new one using ``#create_new#``.
                                                                                                            | Example: ``"F5_0_IAPP_VARIABLE_pool__addr": "10.128.10.240"``
                                                                                                            | Example: ``"F5_0_IAPP_VARIABLE_pool__pool_to_use": "#create_new#"``
------------------------------------    -----------------------------------------------------------------   -----------------------------------------------------------------------
\F5_{n}_IAPP_POOL_MEMBER_TABLE_NAME     The name of the iApp table entry that specifies the pool members    | * Can be different for each iApp template.
                                                                                                            | Example: ``"F5_0_IAPP_POOL_MEMBER_TABLE_NAME": "pool__members"``
====================================    =================================================================   =======================================================================



Build and Launch via Docker
---------------------------

Follow the steps below to build and launch f5-marathon-lb as a Docker container.

.. topic:: 1. Build a Docker container:

    .. code-block:: shell

        docker build -t docker-registry.pdbld.f5net.com/darzins/f5-marathon-lb:latest .


.. topic:: 2. Push to a Docker registry:

    .. code-block:: shell

        docker push docker-registry.pdbld.f5net.com/darzins/f5-marathon-lb:latest

.. topic:: 3. Launch in Marathon:

    .. code-block:: shell

        curl -X POST -H "Content-Type: application/json" http://10.141.141.10:8080/v2/apps -d @f5-marathon-lb.json


Define Marathon Application Labels via JSON
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In step 3, above, we use the command ``curl -X POST -H "Content-Type: application/json" http://10.141.141.10:8080/v2/apps -d @f5-marathon-lb.json``. In this command, "f5-marathon-lb.json" is the file that contains the details needed to deploy the container in Marathon. You can use either **args** or **env** variables in your json file to define the Marathon application labels.

For example:

.. topic:: args

    .. code-block:: javascript

        {
          "id": "f5-marathon-lb",
          "cpus": 0.5,
          "mem": 128.0,
          "instances": 1,
          "container": {
            "type": "DOCKER",
            "forcePullImage": true,
            "docker": {
              "image": "docker-registry.pdbld.f5net.com/darzins/f5-marathon-lb:latest",
              "network": "BRIDGE"
            }
          },
          "args": [
            "sse",
            "--marathon", "http://10.141.141.10:8080",
            "--partition", "mesos_1",
            "--hostname", "10.128.1.145",
            "--username", "admin",
            "--password", "default"
          ]
        }

\

.. topic:: env variables

    .. code-block:: javascript

        {
          "id": "f5-mlb",
          "cpus": 0.5,
          "mem": 128.0,
          "instances": 1,
          "container": {
            "type": "DOCKER",
            "forcePullImage": true,
            "docker": {
              "image": "docker-registry.pdbld.f5net.com/velcro/f5-marathon-lb:latest",
              "network": "BRIDGE"
            }
          },
          "env": {
            "F5_CSI_USE_SSE": "True",
            "MARATHON_URL": "http://10.141.141.10:8080",
            "F5_CSI_PARTITIONS": "[mesos_1, mesos_test]",
            "F5_CSI_BIGIP_HOSTNAME": "10.128.1.145",
            "F5_CSI_BIGIP_USERNAME": "admin",
            "F5_CSI_BIGIP_PASSWORD": "default"
          }
        }


Deployment Examples
-------------------

Marathon Application
~~~~~~~~~~~~~~~~~~~~

The following example demonstrates an application deployment in Marathon with the appropriate f5-marathon-lb labels configured.

- The app (``server-app4``) has three service ports configured; only the first two are exposed via the BIG-IP (in other words, only port indices 0 and 1 are configured in the *labels* section).
- Marathon health monitors are configured for all three service ports.

.. code-block:: json
    :linenos:
    :emphasize-lines: 29, 32

    {
      "id": "server-app4",
      "cpus": 0.1,
      "mem": 16.0,
      "instances": 2,
      "container": {
        "type": "DOCKER",
        "docker": {
          "image": "edarzins/node-web-app",
          "network": "BRIDGE",
          "forcePullImage": false,
          "portMappings": [
            { "containerPort": 8088,
              "hostPort": 0,
              "protocol": "tcp" },
            { "containerPort": 8188,
              "hostPort": 0,
              "protocol": "tcp" },
            { "containerPort": 8288,
              "hostPort": 0,
              "protocol": "tcp" }
          ]
        }
      },
      "labels": {
        "F5_PARTITION": "mesos",
        "F5_0_BIND_ADDR": "10.128.10.240",
        "F5_0_MODE": "http",
        "F5_0_PORT": "8080",
        "F5_1_BIND_ADDR": "10.128.10.242",
        "F5_1_MODE": "http",
        "F5_1_PORT": "8090"
      },
      "healthChecks": [
        {
          "protocol": "HTTP",
          "portIndex": 0,
          "path": "/",
          "gracePeriodSeconds": 5,
          "intervalSeconds": 20,
          "maxConsecutiveFailures": 3
        },
        {
          "protocol": "HTTP",
          "portIndex": 1,
          "path": "/",
          "gracePeriodSeconds": 5,
          "intervalSeconds": 20,
          "maxConsecutiveFailures": 3
        },
        {
          "protocol": "HTTP",
          "portIndex": 2,
          "path": "/",
          "gracePeriodSeconds": 5,
          "intervalSeconds": 20,
          "maxConsecutiveFailures": 3
        }
      ]
    }

For our Marathon application, f5-marathon-lb configures the BIG-IP as demonstrated below, showing virtual servers, pools, and health monitors.

.. note::

    If a Marathon health monitor exists for a service port, f5-marathon-lb will create a corresponding health monitor for it on the BIG-IP.

    If the ``--health-check`` option is set, f5-marathon-lb will respect the Marathon health status for the service port before adding it to the backend pool.

.. code-block:: bash
    :linenos:

    ltm monitor http server-app4_10.128.10.240_8080 {
        adaptive disabled
        defaults-from /Common/http
        destination *:*
        interval 20
        ip-dscp 0
        partition mesos
        send "GET /\r\n"
        time-until-up 0
        timeout 61
    }
    ltm monitor http server-app4_10.128.10.242_8090 {
        adaptive disabled
        defaults-from /Common/http
        destination *:*
        interval 20
        ip-dscp 0
        partition mesos
        send "GET /\r\n"
        time-until-up 0
        timeout 61
    }
    ltm node 10.141.141.10 {
        address 10.141.141.10
        partition mesos
        session monitor-enabled
        state up
    }
    ltm persistence global-settings { }
    ltm pool server-app4_10.128.10.240_8080 {
        members {
            10.141.141.10:31383 {
                address 10.141.141.10
                session monitor-enabled
                state up
            }
            10.141.141.10:31775 {
                address 10.141.141.10
                session monitor-enabled
                state up
            }
        }
        monitor server-app4_10.128.10.240_8080
        partition mesos
    }
    ltm pool server-app4_10.128.10.242_8090 {
        members {
            10.141.141.10:31384 {
                address 10.141.141.10
                session monitor-enabled
                state up
            }
            10.141.141.10:31776 {
                address 10.141.141.10
                session monitor-enabled
                state up
            }
        }
        monitor server-app4_10.128.10.242_8090
        partition mesos
    }
    ltm virtual server-app4_10.128.10.240_8080 {
        destination 10.128.10.240:webcache
        ip-protocol tcp
        mask 255.255.255.255
        partition mesos
        pool server-app4_10.128.10.240_8080
        profiles {
            /Common/http { }
            /Common/tcp { }
        }
        source 0.0.0.0/0
        source-address-translation {
            type automap
        }
        vs-index 153
    }
    ltm virtual server-app4_10.128.10.242_8090 {
        destination 10.128.10.242:8090
        ip-protocol tcp
        mask 255.255.255.255
        partition mesos
        pool server-app4_10.128.10.242_8090
        profiles {
            /Common/http { }
            /Common/tcp { }
        }
        source 0.0.0.0/0
        source-address-translation {
            type automap
        }
        vs-index 154
    }


iApps Application
~~~~~~~~~~~~~~~~~

The following example uses the "f5.http" iApp template to define an HTTP service.

.. note::

    Only the the IAPP labels and the ``F5_PARTITION`` label are needed to deploy using an iApp template. For example, the ``F5_0_BIND_ADDR`` and ``F5_0_PORT`` parameters are accounted for by iApp variables (``pool__addr`` and ``pool__port``, respectively).


.. code-block:: json
    :linenos:

    {
      "id": "server-app2",
      "cpus": 0.1,
      "mem": 16.0,
      "instances": 4,
      "container": {
        "type": "DOCKER",
        "docker": {
          "image": "edarzins/node-web-app",
          "network": "BRIDGE",
          "forcePullImage": false,
          "portMappings": [
            { "containerPort": 8088,
              "hostPort": 0,
              "protocol": "tcp" }
          ]
        }
      },
      "labels": {
        "F5_PARTITION": "mesos",
        "F5_0_IAPP_TEMPLATE": "/Common/f5.http",
        "F5_0_IAPP_POOL_MEMBER_TABLE_NAME": "pool__members",
        "F5_0_IAPP_VARIABLE_net__server_mode": "lan",
        "F5_0_IAPP_VARIABLE_pool__addr": "10.128.10.240",
        "F5_0_IAPP_VARIABLE_pool__pool_to_use": "/#create_new#",
        "F5_0_IAPP_VARIABLE_monitor__monitor": "/#create_new#",
        "F5_0_IAPP_VARIABLE_monitor__uri": "/",
        "F5_0_IAPP_VARIABLE_monitor__response": "none",
        "F5_0_IAPP_VARIABLE_net__client_mode": "wan",
        "F5_0_IAPP_VARIABLE_pool__port": "8080",
        "F5_0_IAPP_OPTION_description": "This is a test iApp"
      },
      "healthChecks": [
        {
          "protocol": "TCP",
          "portIndex": 0,
          "path": "/",
          "gracePeriodSeconds": 5,
          "intervalSeconds": 20,
          "maxConsecutiveFailures": 3
        }
      ]
    }
