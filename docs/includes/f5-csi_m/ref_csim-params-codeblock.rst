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
