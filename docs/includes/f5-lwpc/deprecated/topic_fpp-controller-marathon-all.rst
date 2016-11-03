Configure the |lwpc|
--------------------

Configure the |lwpc| using the environment variables shown in the table.

+-----------------------------------+---------------------------------------------------+-----------------------+---------------+
| Name                              | Description                                       | Default               | Is Required   |
+===================================+===================================================+=======================+===============+
| MARATHON_URL                      | URL of the Marathon API                           | http://127.0.0.1:8080 | Required      |
+-----------------------------------+---------------------------------------------------+-----------------------+---------------+
| LWP_ENABLE_LABEL                  | label used to determine LWP requirements          | f5-lwp                | Optional      |
+-----------------------------------+---------------------------------------------------+-----------------------+---------------+
| LWP_DEFAULT_CPU                   | amount of CPU for LWP tasks                       | 1.0                   | Optional      |
+-----------------------------------+---------------------------------------------------+-----------------------+---------------+
| LWP_DEFAULT_MEM                   | amount of memory for LWP tasks                    | 256.0                 | Optional      |
+-----------------------------------+---------------------------------------------------+-----------------------+---------------+
| LWP_DEFAULT_STORAGE               | amount of memory for LWP tasks                    | 0                     | Optional      |
+-----------------------------------+---------------------------------------------------+-----------------------+---------------+
| LWP_DEFAULT_COUNT_PER_APP         | number of LWP tasks per application               | 1                     | Optional      |
+-----------------------------------+---------------------------------------------------+-----------------------+---------------+
| LWP_DEFAULT_CONTAINER             | location of docker image to pull                  | f5networks/lwp        | Optional      |
+-----------------------------------+---------------------------------------------------+-----------------------+---------------+
| LWP_DEFAULT_CONTAINER_PORT        | container port to expose                          | 8000                  | Optional      |
+-----------------------------------+---------------------------------------------------+-----------------------+---------------+
| LWP_DEFAULT_URIS                  | comma separated list of URIs to pass to Marathon  | EMPTY                 | Optional      |
+-----------------------------------+---------------------------------------------------+-----------------------+---------------+
| LWP_DEFAULT_VS_KEEP_ALIVE         | Virtual server keep alive, in msecs               | 1000                  | Optional      |
+-----------------------------------+---------------------------------------------------+-----------------------+---------------+
| LWP_DEFAULT_VS_PROTOCOL           | protocol for virtual server (http or tcp)         | http                  | Optional      |
+-----------------------------------+---------------------------------------------------+-----------------------+---------------+
| LWP_DEFAULT_STATS_URL             | Url for sending stats                             | None                  | Optional      |
+-----------------------------------+---------------------------------------------------+-----------------------+---------------+
| LWP_DEFAULT_STATS_TOKEN           | Stats authentication token                        | None                  | Optional [#]_ |
+-----------------------------------+---------------------------------------------------+-----------------------+---------------+
| LWP_DEFAULT_STATS_FLUSH_INTERVAL  | Stats flush interval, in msecs                    | 10000                 | Optional      |
+-----------------------------------+---------------------------------------------------+-----------------------+---------------+
| LWP_DEFAULT_STATS_BACKEND         | Stats backend type, (for example, splunk)         | None                  | Optional      |
+-----------------------------------+---------------------------------------------------+-----------------------+---------------+
| LWP_DEFAULT_FORCE_PULL            | Sets Marathon to force pull at LWP start-up       | true                  | Optional      |
+-----------------------------------+---------------------------------------------------+-----------------------+---------------+
| LWP_ENV_PREFIX                    | prefix for env variables to pass to the LWP       | \LWP_ENV_             | Optional      |
+-----------------------------------+---------------------------------------------------+-----------------------+---------------+
| LWP_DEFAULT_LOG_LEVEL             | logging level                                     | INFO                  | Optional      |
+-----------------------------------+---------------------------------------------------+-----------------------+---------------+
| LWP_DEFAULT_VS_FLAGS              | flags for configuring LWP behavior [#]_           |  {}                   | Optional      |
+-----------------------------------+---------------------------------------------------+-----------------------+---------------+
| LWP_VIP_PREFIX                    | prefix for port labels to pass to LWP             | \LWP_                 | Optional      |
+-----------------------------------+---------------------------------------------------+-----------------------+---------------+

.. [#] If LWP_DEFAULT_STATS_URL is configured then LWP_DEFAULT_STATS_TOKEN and LWP_DEFAULT_STATS_BACKEND become required parameters.
.. [#] Only bools (true or false) are permitted.

Marathon Example
~~~~~~~~~~~~~~~~

The following example demonstrates an application deployment in Marathon with an example configuration using various LWP_DEFAULT_* overrides. Note, the only required environment parameter is MARATHON_URL. The |lwpc| will run successfully with its defaults but with certain functionality disabled (e.g. without providing LWP_DEFAULT_STATS_* parameters this feature is disabled while the |lwpc| remains operational).

.. topic:: Deploy to Marathon Example

    .. code-block:: shell

        curl -X POST -H "Content-Type: application/json" http://marathon.mesos.example.com:8080/v2/apps -d @f5-fpp-controller.json

The f5-fpp-controller.json is a file containing a Marathon application description structured as JSON.

.. topic:: F5 |lwpc| Example Configuration

    .. code-block:: javascript

        {
          "id": "/example/fpp-controller",
          "cpus": 1,
          "mem": 128,
          "instances": 1,
          "container": {
            "type": "DOCKER",
            "docker": {
              "image": "[f5-docker-user]/lwp-controller[-version-tag]",
              "network": "BRIDGE",
              "forcePullImage": true,
              "privileged": false,
              "portMappings": []
            },
            "volumes": []
          },
          "env": {
            "MARATHON_URL": "http://marathon.mesos.example.com:8080",
            "LWP_DEFAULT_CONTAINER": "[f5-docker-user]/light-weight-proxy[-version-tag]",
            "LWP_DEFAULT_STATS_URL": "http://splunk.example.com:8088",
            "LWP_DEFAULT_STATS_TOKEN": "example-stats-token",
            "LWP_DEFAULT_STATS_BACKEND": "splunk",
            "LWP_DEFAULT_STATS_FLUSH_INTERVAL": "10000",
            "LWP_ENABLE_LABEL": "lwp",
            "LWP_DEFAULT_CPU": "1",
            "LWP_DEFAULT_MEM": "256",
            "LWP_DEFAULT_LOG_LEVEL": "info",
            "LWP_DEFAULT_FORCE_PULL": true,
          }
        }

Manually Deploy in Docker
~~~~~~~~~~~~~~~~~~~~~~~~~

Usually, the |lwpc| is deployed by Marathon (as with the previous example). The example below shows how it can be run from the command-line. **This example is provided for enhanced understanding, not as a recommendation.**

.. topic:: Example

    .. code-block:: shell

        docker run -it -d -e MARATHON_URL="http://172.28.128.3:8080" -e LWP_ENABLE_LABEL lwp-myapp -e LWP_DEFAULT_CONTAINER f5networks/lwp [f5-docker-user]/lwp-controller

    Then, create your application in the Marathon instance running at 172.28.128.3 and label it with the label ``lwp-myapp:enable``.

    The |lwpc| will create a new application in your Marathon cluster to be the LWP for your application.

    This example illustrates the |lwpc| interaction with Marathon and deployed applications. The |lwpc| was configured with the Marathon URL to receive event notifications. When the application was configured and labelled as ``lwp-myapp:enable`` |lwpc| received an application create event. When the |lwpc| matched its LWP_ENABLE_LABEL (``lwp-myapp``) an LWP was started to proxy and load balance for the newly deployed application.

Override Controller Configuration
---------------------------------

Default values configured for the LWP Controller can be modified on a per-app basis. The following labels, which can be applied to the application being controlled, override the corresponding LWP Controller default value.

+-----------------------------------+---------------------------------------------------+
| Name                              | Description                                       |
+===================================+===================================================+
| LWP_VS_KEEP_ALIVE                 | | overrides LWP_DEFAULT_VS_KEEP_ALIVE             |
+-----------------------------------+---------------------------------------------------+
| LWP_VS_PROTOCOL                   | | overrides LWP_DEFAULT_VS_PROTOCOL               |
+-----------------------------------+---------------------------------------------------+
| LWP_LOG_LEVEL                     | | overrides LWP_DEFAULT_LOG_LEVEL                 |
+-----------------------------------+---------------------------------------------------+
| LWP_STATS_URL                     | | overrides LWP_DEFAULT_STATS_URL                 |
+-----------------------------------+---------------------------------------------------+
| LWP_STATS_TOKEN                   | | overrides LWP_DEFAULT_STATS_TOKEN               |
+-----------------------------------+---------------------------------------------------+
| LWP_STATS_FLUSH_INTERVAL          | | overrides LWP_DEFAULT_STATS_FLUSH_INTERVAL      |
+-----------------------------------+---------------------------------------------------+
| LWP_STATS_BACKEND                 | | overrides LWP_DEFAULT_STATS_BACKEND             |
+-----------------------------------+---------------------------------------------------+
| LWP_FORCE_PULL                    | | overrides LWP_DEFAULT_FORCE_PULL                |
+-----------------------------------+---------------------------------------------------+
| LWP_CPU                           | | overrides LWP_DEFAULT_CPU                       |
+-----------------------------------+---------------------------------------------------+
| LWP_MEM                           | | overrides LWP_DEFAULT_MEM                       |
+-----------------------------------+---------------------------------------------------+
| LWP_STORAGE                       | | overrides LWP_DEFAULT_STORAGE                   |
+-----------------------------------+---------------------------------------------------+
| LWP_COUNT_PER_APP                 | | overrides LWP_DEFAULT_COUNT_PER_APP             |
+-----------------------------------+---------------------------------------------------+
| LWP_CONTAINER                     | | overrides LWP_DEFAULT_CONTAINER                 |
+-----------------------------------+---------------------------------------------------+
| LWP_URIS                          | | overrides LWP_DEFAULT_URIS                      |
+-----------------------------------+---------------------------------------------------+
| LWP_VS_FLAGS                      | | merges with and overrides collisions on         |
|                                   | | LWP_DEFAULT_VS_FLAGS                            |
+-----------------------------------+---------------------------------------------------+

