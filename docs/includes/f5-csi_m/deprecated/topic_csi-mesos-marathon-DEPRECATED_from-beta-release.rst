Features
--------

Overview
````````

The |csi_m| listens to the Marathon event stream and automatically configures the BIG-IP as follows:

-  matches a Marathon app to an existing BIG-IP partition;
-  creates a virtual server and pool for the Marathon app in the matching BIG-IP partition;
-  creates a pool member for each Marathon application task;
-  adds the new pool member to the virtual server pool for the app;
-  creates a health monitor for the pool member on the BIG-IP if the app has a Marathon Health Monitor configured.

BIG-IP Partitions and Resources
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

|csi_m-short| allows you to manage resources in specific partitions on a BIG-IP device.

.. important:: The partitions you want to manage with |csi_m-short| must exist on the BIG-IP before you configure anything in Marathon.

The f5-marathon-lb application manages the BIG-IP object types listed below. These should not be manually added, changed, or deleted in the partition managed by f5-marathon-lb, as this may result in unexpected behavior.

-  Virtual Servers
-  Virtual Addresses
-  Pools
-  Pool Members
-  Nodes
-  Health Monitors
-  Application Services


Prerequisites
`````````````

- Licensed, operational BIG-IP :term:`device`.
- An existing, functional `Mesos`_ `Marathon`_ deployment.
- Administrator access to both the BIG-IP and Marathon.
- Partitions corresponding to the Marathon apps.

Caveats
```````

- |csi_m-short| can not manage the "Common" partition.



Usage
`````

First, |csi_m-short| needs to know where to find Marathon, the BIG-IP, and how to connect to both. The service configuration details are stored in Marathon `application labels <#manage_applications>`_.

You can launch |csi_m-short| in Marathan via the `REST API <#rest_api>`_ or the `command line <#command_line>`_. Both use the same set of arguments.

Configuration
~~~~~~~~~~~~~

Parameters
^^^^^^^^^^

.. code-block:: console

    sse                 Use Server Sent Events instead of HTTP Callbacks [env
                        var: F5_CSI_USE_SSE] (default: False)
    -h, --help          show this help message and exit
    --longhelp          Print out configuration details (default: False)
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
    --hostname HOSTNAME F5 BIG-IP hostname [env var: F5_CSI_BIGIP_HOSTNAME]
                        (default: None)
    --username USERNAME F5 BIG-IP username [env var: F5_CSI_BIGIP_USERNAME]
                        (default: None)
    --password PASSWORD F5 BIG-IP password [env var: F5_CSI_BIGIP_PASSWORD]
                        (default: None)
    --partition PARTITION
                        [required] Only generate config for apps which match
                        the specified partition. Use '*' to match all
                        partitions. Can use this arg multiple times to specify
                        multiple partitions [env var: F5_CSI_PARTITIONS]
                        (default: [])
    --health-check, -H  If set, respect Marathon's health check statuses
                        before adding the app instance into the backend pool.
                        [env var: F5_CSI_USE_HEALTHCHECK] (default: False)
    --sse-timeout SSE_TIMEOUT, -t SSE_TIMEOUT
                        Marathon event stream timeout [env var:
                        F5_CSI_SSE_TIMEOUT] (default: 30)
    --log-format LOG_FORMAT
                        Set log message format [env var: F5_CSI_LOG_FORMAT]
                        (default: %(asctime)s %(name)s: %(levelname) -8s:
                        %(message)s)
    --marathon-auth-credential-file MARATHON_AUTH_CREDENTIAL_FILE
                        Path to file containing a user/pass for the Marathon
                        HTTP API in the format of 'user:pass'. [env var:
                        F5_CSI_MARATHON_AUTH] (default: None)


.. important::

    - The following arguments are mandatory:

        * ``--marathon``
        * ``--hostname``
        * ``--username``
        * ``--password``
        * ``partition``

    - The ``--partition`` argument can be used multiple times to specify multiple BIG-IP partitions (for example, ``--partition tenant_a --partition tenant_b``).


REST API
^^^^^^^^

#. Create a .json file with the correct arguments for your BIG-IP device and Marathon (for example, "f5-marathon-lb.json").

    .. code-block:: json

        {
          "id": "f5-marathon-lb",
          "cpus": 0.5,
          "mem": 64.0,
          "instances": 1,
          "container": {
            "type": "DOCKER",
            "docker": {
              "image": "<f5-marathon-lb-container>",
              "network": "BRIDGE"
            }
          },
          "args": [
            "sse",
            "--marathon", "<Marathon-REST-API-URL>",
            "--partition", "<BigIP-Partition>",
            "--hostname", "<BigIP-Admin-IP>",
            "--username", "admin",
            "--password", "<BigIP-Admin-Password>"
          ]
        }


#. Use ``curl`` to launch |csi_m-short| using the .json file:

    .. code-block:: bash

        curl -X POST -H "Content-Type: application/json" http://<marathon_url>:8080/v2/apps -d @f5-marathon-lb.json


Command Line
^^^^^^^^^^^^

Run ``f5-marathon-lb.py`` with the arguments appropriate for your environment:

    .. code-block:: console

        $ f5-marathon-lb.py --marathon http://<marathonURL>:8080 --hostname https://<big-ip_ip-address> --username <username> --password <password> --partition <partition_name>



Manage Applications with |csi_m-short|
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


|csi_m-short| identifies and configures applications via Marathon *Application Labels*. These can be used in .json blobs to issue commands to |csi_m-short| via the Marathon REST API.

.. tip::

    Some labels are specified *per service port*. These are denoted with the ``{n}`` parameter in the label key; ``{n}`` corresponds to the service port index, beginning at ``0``.


.. table:: f5-marathon-lb Application Labels

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

|csi_m-short| and iApps
```````````````````````

`iApps® <https://devcentral.f5.com/iapps>`_ is a user-customizable framework for deploying applications that enables you to templatize sets of functionality on your BIG-IP. You can use |csi_m-short| to instantiate and manage an iApp Application Service. The iApp template and variables are specified via Marathon application labels specific to the iApp you are deploying.

.. important::

    The iApp template you wish to deploy **must** already be installed on the BIG-IP. Variable names and values are template-specific.

.. table:: iApp Application Labels

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


Deployment Examples
~~~~~~~~~~~~~~~~~~~

Marathon Application
^^^^^^^^^^^^^^^^^^^^

In the following example, we deploy an application in Marathon with the appropriate |csi_m-short| labels configured.

- The app (``server-app4``) has three service ports configured; only the first two are exposed via the BIG-IP (port indices 0 and 1 are configured in the ``labels`` section).
- Marathon health monitors are configured for all three service ports.

.. note:: All IP addresses shown are for demonstration purposes only.

#. Deploy the application in Marathon via the REST API.

    .. code-block:: shell

        curl -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' \
        http://<marathon_url>:8080/v2/apps -d '
        {
          "id": "server-app4",
          "cpus": 0.1,
          "mem": 16.0,
          "instances": 2,
          "container": {
            "type": "DOCKER",
            "docker": {
              "image": "f5_demo/node-web-app",
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
        }'


#. For our Marathon application, |csi_m-short| configures virtual servers, pools, and health monitors on the BIG-IP as shown below.

    .. note::

        - If a Marathon health monitor exists for a service port, |csi_m-short| creates a corresponding health monitor for it on the BIG-IP.
        - If the ``--health-check`` option is set, |csi_m-short| checks the Marathon health status for the service port before adding it to the backend pool.

    .. code-block:: shell

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
`````````````````

The following example uses the "f5.http" iApp template to define an HTTP service.[#]_

.. note::

    Only the the ``IAPP`` labels and the ``F5_PARTITION`` label are needed to deploy using an iApp template. For example, the ``F5_0_BIND_ADDR`` and ``F5_0_PORT`` parameters are accounted for by iApp variables (``pool__addr`` and ``pool__port``, respectively).

#. Deploy the iApp in Marathon via the REST API.

    .. code-block:: shell

        curl -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' \
        http://<marathon_url>:8080/v2/apps -d '
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
        }'

#. You can then log in to your BIG-IP to verify creation of the iApp. (Be sure to look in the correct partition!)

    * Go to :menuselection:`iApps --> Application Services` to view the list of Application Services.
    * Click on ``f5.http`` to view all of the objects configured as part of the iApp deployment.


.. [#] available for download from https://downloads.f5.com/

.. _Mesos: https://mesos.apache.org/
.. _Marathon: https://mesosphere.github.io/marathon/