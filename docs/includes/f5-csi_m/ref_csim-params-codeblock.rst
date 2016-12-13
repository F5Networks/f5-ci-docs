.. code-block:: console

    -h, --help          show this help message and exit
    --longhelp          Print out configuration details (default: False)
    --marathon MARATHON [MARATHON ...], -m MARATHON [MARATHON ...]
                        [required] Marathon endpoint, eg. -m
                        http://marathon1:8080 http://marathon2:8080 [env var:
                        MARATHON_URL] (default: None)
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
    --marathon-ca-cert MARATHON_CA_CERT
                        CA certificate for Marathon HTTPS connections [env
                        var: F5_CSI_MARATHON_CA_CERT] (default: None)
    --sse-timeout SSE_TIMEOUT, -t SSE_TIMEOUT
                        Marathon event stream timeout [env var:
                        F5_CSI_SSE_TIMEOUT] (default: 30)
    --verify-interval VERIFY_INTERVAL, -v VERIFY_INTERVAL
                        Interval at which to verify the BIG-IP configuration.
                        [env var: F5_CSI_VERIFY_INTERVAL] (default: 30)
    --log-format LOG_FORMAT
                        Set log message format [env var: F5_CSI_LOG_FORMAT]
                        (default: %(asctime)s %(name)s: %(levelname) -8s:
                        %(message)s)
    --log-level LOG_LEVEL
                        Set logging level. Valid log levels are: DEBUG, INFO,
                        WARNING, ERROR, and CRITICAL [env var:
                        F5_CSI_LOG_LEVEL] (default: INFO)
    --marathon-auth-credential-file MARATHON_AUTH_CREDENTIAL_FILE
                        Path to file containing a user/pass for the Marathon
                        HTTP API in the format of 'user:pass'. [env var:
                        F5_CSI_MARATHON_AUTH] (default: None)
    --dcos-auth-credentials DCOS_AUTH_CREDENTIALS
                        DC/OS service account credentials [env var:
                        F5_CSI_DCOS_AUTH_CREDENTIALS] (default: None)
    --dcos-auth-token DCOS_AUTH_TOKEN
                        DC/OS ACS Token [env var: F5_CSI_DCOS_AUTH_TOKEN]
                        (default: None)
