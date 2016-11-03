.. list-table:: F5 Lightweight Proxy Controller Configuration Parameters
    :header-rows: 1

    * - Name
      - Description
      - Default
      - Required
      - Overrride Label
    * - ``MARATHON_URL``
      - URL of the Marathon API
      - http://127.0.0.1:8080
      - Required
      - None
    * - ``LWP_ENABLE_LABEL``
      - label used to determine LWP requirements
      - f5-lwp
      - Optional
      - None
    * - ``LWP_DEFAULT_CPU``
      - amount of CPU for LWP tasks
      - 1.0
      - Optional
      - ``LWP_CPU``
    * - ``LWP_DEFAULT_MEM``
      - amount of memory for LWP tasks
      - 256.0
      - Optional
      - ``LWP_MEM``
    * - ``LWP_DEFAULT_STORAGE``
      - amount of memory for LWP tasks
      - 0
      - Optional
      - ``LWP_STORAGE``
    * - ``LWP_DEFAULT_COUNT_PER_APP``
      - number of LWP tasks per application
      - 1
      - Optional
      - ``LWP_COUNT_PER_APP``
    * - ``LWP_DEFAULT_CONTAINER``
      - location of docker image to pull
      - f5networks/lwp
      - Optional
      - ``LWP_CONTAINER``
    * - ``LWP_DEFAULT_CONTAINER_PORT``
      - container port to expose
      - 8000
      - Optional
      - None [#]_
    * - ``LWP_DEFAULT_URIS``
      - comma separated list of URIs to pass to Marathon
      - EMPTY
      - Optional
      - ``LWP_URIS``
    * - ``LWP_DEFAULT_VS_KEEP_ALIVE``
      - Virtual server keep alive, in msecs
      - 1000
      - Optional
      - ``LWP_VS_KEEP_ALIVE``
    * - ``LWP_DEFAULT_VS_PROTOCOL``
      - protocol for virtual server (http or tcp)
      - http
      - Optional
      - ``LWP_VS_PROTOCOL``
    * - ``LWP_DEFAULT_STATS_URL``
      - URL of analytics provider
      - None
      - Optional
      - ``LWP_STATS_URL``
    * - ``LWP_DEFAULT_STATS_TOKEN``
      - Authentication token for analytics provider
      - None
      - Optional [#]_
      - ``LWP_STATS_TOKEN``
    * - ``LWP_DEFAULT_STATS_FLUSH_INTERVAL``
      - Stats flush interval, in msecs
      - 10000
      - Optional
      - ``LWP_STATS_FLUSH_INTERVAL``
    * - ``LWP_DEFAULT_STATS_BACKEND``
      - Stats backend type, (e.g., Splunk)
      - None
      - Optional
      - ``LWP_STATS_BACKEND``
    * - ``LWP_DEFAULT_FORCE_PULL``
      - Sets Marathon to force pull image from Docker container at LWP start-up
      - true
      - Optional
      - ``LWP_FORCE_PULL``
    * - ``LWP_DEFAULT_LOG_LEVEL``
      - logging level
      - INFO
      - Optional
      - ``LWP_LOG_LEVEL``
    * - ``LWP_DEFAULT_VS_FLAGS``
      - flags for configuring LWP behavior [#]_
      - {}
      - Optional
      - ``LWP_VS_FLAGS``
    * - ``LWP_VIP_PREFIX``
      - prefix for port labels to pass to LWP
      - \LWP_
      - Optional
      - None
    * - ``LWP_ENV_PREFIX``
      - prefix for env variables to pass to the LWP
      - \LWP_ENV_
      - Optional
      - None


.. [#] If you wish to override the default container port setting, you can do so by editing the applications' configs in the Marathon UI.
.. [#] If ``LWP_DEFAULT_STATS_URL`` is configured, then ``LWP_DEFAULT_STATS_TOKEN`` and ``LWP_DEFAULT_STATS_BACKEND`` are required.
.. [#] Only bools (true or false) are permitted.
