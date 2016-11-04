.. list-table:: f5-marathon-lb Application Labels
    :header-rows: 1

    * - Label
      - Definition
      - Default
      - Additional Information
    * - ``F5_PARTITION``
      - The BIG-IP partition in which the CSI should create objects
      - N/A
      - The partition must only be managed by the CSI and cannot be "Common".
    * - ``F5_{n}_BIND_ADDR``
      - The IP address of the App service
      - N/A
      - Used to communicate with the BIG-IP. Example: ``"F5_0_BIND_ADDR": "10.0.0.42"``
    * - ``F5_{n}_PORT``
      - The service port to use to communicate with the BIG-IP
      - N/A
      - Overrides the ``servicePort`` setting in the CSI configurations. Example: ``"F5_0_PORT": "80"``
    * - ``F5_{n}_MODE``
      - Connection mode (HTTP or TCP)
      - TCP
      - Example: ``"F5_0_MODE": "http"``
    * - ``F5_{n}_BALANCE``
      - The load balancing algorithm
      - roundrobin
      - Example: ``"F5_0_BALANCE": "leastconn"``
    * - ``\F5_{n}_SSL_PROFILE``
      - The SSL profile for the HTTPS virtual server
      - N/A
      - Must already be configured on the BIG-IP.  Example: ``"F5_0_SSL_PROFILE": "Common/clientssl"``





