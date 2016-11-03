.. list-table:: Global Stats
    :header-rows: 1

    * - Name
      - Description
    * - ``tot_requests``
      - Number of HTTP requests received from the clients
    * - ``clientside_tot_conns``
      - Number of TCP connections received from the clients
    * - ``clientside_cur_conns``
      - Current number of active TCP connections to the clients
    * - ``clientside_max_conns``
      - Maximum number of active TCP connections to the clients since the start of |lwp|
    * - ``clientside_bytes_in``
      - Number of bytes read from the clients
    * - ``clientside_bytes_out``
      - Number of bytes written to the clients
    * - ``serverside_tot_conns``
      - Number of TCP connections opened to the servers
    * - ``serverside_cur_conns``
      - Current number of active TCP connections to the servers
    * - ``serverside_max_conns``
      - Maximum number of active TCP connections to the servers since the start of |lwp|
    * - ``server_latency``
      - Average time (in milliseconds) to connection to a server
    * - ``max_server_latency``
      - Maximum time (in milliseconds) to connection to a server
    * - ``clientside_failed_conns``
      - Number of failed TCP connections from clients
    * - ``serverside_failed_conns``
      - Number of failed TCP connections to servers
    * - ``aggr_period``
      - Time interval for flushing aggregate statistics

