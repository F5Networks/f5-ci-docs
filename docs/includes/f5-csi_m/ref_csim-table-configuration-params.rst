.. list-table:: F5 CSI Configuration Parameters
    :header-rows: 1

    * - Field
      - Type
      - Required
      - Default
      - Description
      - Allowed Values
    * - ``MARATHON_URL``
      - string
      - Yes
      - None
      - The Marathon URL
      - N/A
    * - ``F5_CSI_LISTENING_ADDR``
      - string
      - No
      - None
      - The IP address on which the CSI listens for Marathon events
      - N/A
    * - ``F5_CSI_CALLBACK_URL``
      - string
      - No
      - None
      - The HTTP address at which Marathon can call the CSI back
      - N/A
    * - ``F5_CSI_BIGIP_HOSTNAME``
      - string
      - Yes
      - None
      - The BIG-IP hostname / IP address
      - N/A
    * - ``F5_CSI_BIGIP_USERNAME``
      - string
      - Yes
      - None
      - Your BIG-IP username; provides the CSI access to the BIG-IP
      - N/A
    * - ``F5_CSI_BIGIP_PASSWORD``
      - string
      - Yes
      - None
      - Your BIG-IP password; provides the CSI access to the BIG-IP
      - N/A
    * - ``F5_CSI_PARTITIONS``
      - string
      - Yes
      - None
      - The partition(s) on the BIG-IP that the CSI will manage
      - N/A
    * - ``F5_CSI_USE_HEALTHCHECK``
      - boolean
      - No
      - False
      - If set, respect Marathon's health check statuses before adding the app instance into the backend pool.
      - True, False
    * - ``F5_CSI_SSE_TIMEOUT``
      - integer
      - No
      - 30
      - Marathon event stream timeout
      - N/A
    * - ``F5_CSI_LOG_FORMAT``
      - string
      - No
      - ``%(asctime)s %(name)s: %(levelname) -8s: %(message)s``
      - The log message format
      - N/A
    * - ``F5_CSI_MARATHON_AUTH``
      - string
      - No
      - None
      - Path to file containing a user/pass for the Marathon HTTP API in the format of 'user:pass'.
      - N/A

