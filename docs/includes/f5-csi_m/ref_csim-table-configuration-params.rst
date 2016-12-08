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
      - Required
      - None
      - The Marathon URL
      - N/A
    * - ``F5_CSI_BIGIP_HOSTNAME``
      - string
      - Required
      - None
      - The BIG-IP hostname / IP address
      - N/A
    * - ``F5_CSI_BIGIP_USERNAME``
      - string
      - Required
      - None
      - Your BIG-IP username; provides the CSI access to the BIG-IP
      - N/A
    * - ``F5_CSI_BIGIP_PASSWORD``
      - string
      - Required
      - None
      - Your BIG-IP password; provides the CSI access to the BIG-IP
      - N/A
    * - ``F5_CSI_PARTITIONS``
      - string
      - Required
      - None
      - The partition(s) on the BIG-IP that the CSI will manage
      - N/A
    * - ``F5_CSI_USE_HEALTHCHECK``
      - boolean
      - Optional
      - False
      - If set, respect Marathon's health check statuses before adding the app instance into the backend pool.
      - True, False
    * - ``F5_CSI_SSE_TIMEOUT``
      - integer
      - Optional
      - 30
      - Marathon event stream timeout
      - N/A
    * - ``F5_CSI_MARATHON_CA_CERT``
      - integer
      - Optional
      - None
      - CA certificate for Marathon HTTPS connections
      - N/A
    * - ``F5_CSI_VERIFY_INTERVAL``
      - integer
      - Optional
      - 30
      - Interval at which to verify the BIG-IP configuration
      - N/A
    * - ``F5_CSI_LOG_FORMAT``
      - string
      - Optional
      - ``%(asctime)s %(name)s: %(levelname) -8s: %(message)s``
      - The log message format
      - N/A
    * - ``F5_CSI_LOG_LEVEL``
      - string
      - Optional
      - INFO
      - The log message format
      - N/A
    * - ``F5_CSI_MARATHON_AUTH``
      - string
      - Optional
      - None
      - Path to file containing a user/pass for the Marathon HTTP API in the format of 'user:pass'.
      - N/A
    * - ``F5_CSI_DCOS_AUTH_CREDENTIALS``
      - string
      - Optional
      - None
      - ``DC/OS service account credentials``
      - N/A
    * - ``F5_CSI_DCOS_AUTH_TOKEN``
      - string
      - Optional
      - None
      - ``DC/OS ACS Token``
      - N/A
