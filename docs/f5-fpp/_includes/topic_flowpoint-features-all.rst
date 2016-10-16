Features
--------

Builtin Middleware
``````````````````

Header Manipulation Module (HTTP only)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module provides functionality to manipulate HTTP headers (add,
remove, or modify) using the underlying Node.js header manipulation API
(``setHeader``, ``getHeader``, ``removeHeader``) on the http.ClientRequest and
http.serverResponse objects. LWP has the same semantics for adding
headers as the Node.js ``setHeader`` method, namely:

* Sets a single header value for implicit headers.
* If header already exists, its value will be replaced.
* Use an array of values if you need to send header with multiple values.

Load Balancer Module
~~~~~~~~~~~~~~~~~~~~

This module queries the marathon-dns module for the current list of
servers and implements a load balancing algorithm to choose a back-end
server.

Features:

* Round-robin load balancing
* Collection of load balancing related statistics

Connection Manager
~~~~~~~~~~~~~~~~~~

This module is responsible for managing server connections which involves the following:

* Maintain a mapping of client to server connection
* Given a client connection, check if corresponding server connection exists; reuse connection if it already exists, else create a new one.
* Implement similar lookup in reverse direction (i.e., lookup client connection given server connection).
* Manage lifetime of server connection. Server connection is closed when:

    - client connection closes;
    - inactivity timeout fires.

Forwarder
~~~~~~~~~

This module is responsible for forwarding data back and forth between client and server connections. The initial implementation will support the following modes:

* HTTP Forwarding

    - Provide HTTP proxy functionality between client and server.
    - Collect HTTP statistics:

        - across transactions: request / response counts, status code counts, method counts, error counts, etc.
        - per transaction: client and server address, url, method, status code, server RTT, latency at various stages, etc.

* TCP Forwarding

    - Provide TCP proxy functionality between client and application.
    - Collect TCP statistics:

        - across connections: total connections, current connections, total closed, error counts, etc.
        - per connection: client and server address, bytes read, bytes written, server RTT, latency at various stages, etc.

    - Other TCP configuration options: max connection limit

Express Middleware Support
~~~~~~~~~~~~~~~~~~~~~~~~~~

LWP provides helpers which makes it easy to run express middleware within the LWP middleware framework.

.. topic:: Example

    .. code-block:: javascript

        // Add cookie-parser express middleware
        const cookieParser = require('cookie-parser');
        proxyServer.useExpress(cookieParser(secret, options));


Configuration
`````````````

Configuration is expected to be valid JSON containing a global section, a stats section, and a virtual servers list.


-  Global section: configuration from the controller to control the
   process.
-  Stats section: configuration specific to statistics gathering and
   reporting.
-  Virtual servers section: list of virtual server objects representing
   service endpoints.

Configuration can be passed in one of two methods. The LWP can be run with a ``--config-file`` option which accepts a file name containing the JSON config. The LWP will also look for the ``LWP_CONFIG`` environment variable.

An LWP may be invoked simply via the command line as shown below:

.. code-block:: bash

    $ lwp_proxy --config-file=/home/proxy/config.json

\
or

.. code-block:: bash

    $ LWP_CONFIG='{ "virtual-servers": { ... } }' lwp_proxy


The latter method eases LWP startup in a containerized environment. As an example, the following command starts a LWP via docker :

.. code-block:: bash

    $ docker run -e LWP_CONFIG='{ "virtual-servers": { ... } }' -p 8080:8080 -d f5/lwp-proxy


Configuration Parameters
~~~~~~~~~~~~~~~~~~~~~~~~

Global section
^^^^^^^^^^^^^^

+---------------------+----------+------------+-----------+--------------------------------+---------------------------------------------------------------------------+
| Field               | Type     | Required   | Default   | Description                    | Allowed Values                                                            |
+=====================+==========+============+===========+================================+===========================================================================+
| console-log-level   | string   | No         | info      | Logging level                  | 'critical', 'error', 'warning', 'info', 'debug'                           |
+---------------------+----------+------------+-----------+--------------------------------+---------------------------------------------------------------------------+

Orchestration section
^^^^^^^^^^^^^^^^^^^^^

+----------------+---------------+------------+-----------+--------------------------------+--------------------+
| Field          | Type          | Required   | Default   | Description                    | Allowed Values     |
+================+===============+============+===========+================================+====================+
| marathon       | JSON object   | No         |           | Marathon specific config.      |                    |
+----------------+---------------+------------+-----------+--------------------------------+--------------------+
| kubernetes     | JSON object   | No         |           | Kubernetes specific config.    |                    |
+----------------+---------------+------------+-----------+--------------------------------+--------------------+

Orchestration \ marathon
************************

+-------------------------+-----------+------------+-----------+--------------------------------+--------------------+
| Field                   | Type      | Required   | Default   | Description                    | Allowed Values     |
+=========================+===========+============+===========+================================+====================+
| uri                     | string    | Yes        |           | URL of the marathon service.   |                    |
+-------------------------+-----------+------------+-----------+--------------------------------+--------------------+
| poll-interval           | number    | No         | 1000      | Polling time in milliseconds.  |                    |
+-------------------------+-----------+------------+-----------+--------------------------------+--------------------+

Orchestration \ kubernetes
**************************

+------------------------+------------+------------+-----------+--------------------------------+--------------------+
| Field                  | Type       | Required   | Default   | Description                    | Allowed Values     |
+========================+============+============+===========+================================+====================+
| config-file            | string     | Yes        |           | Service config file to watch.  |                    |
+------------------------+------------+------------+-----------+--------------------------------+--------------------+
| poll-interval          | number     | No         | 1000      | Polling time in milliseconds.  |                    |
+------------------------+------------+------------+-----------+--------------------------------+--------------------+

Stats section
^^^^^^^^^^^^^

+-----------------+----------+------------+-----------+----------------------------------------------------------+-------------------+
| Field           | Type     | Required   | Default   | Description                                              | Allowed Values    |
+=================+==========+============+===========+==========================================================+===================+
| url             | string   | Yes        |           | URL of the stats service.                                |                   |
+-----------------+----------+------------+-----------+----------------------------------------------------------+-------------------+
| token           | string   | Yes        |           | Authentication token for the stats server.               |                   |
+-----------------+----------+------------+-----------+----------------------------------------------------------+-------------------+
| flushInterval   | number   | No         | 10000     | Frequency in milliseconds of flushing stats to server.   |                   |
+-----------------+----------+------------+-----------+----------------------------------------------------------+-------------------+
| backend         | string   | Yes        |           | Type of backend stats service.                           | 'leo', 'splunk'   |
+-----------------+----------+------------+-----------+----------------------------------------------------------+-------------------+

Virtual server section
^^^^^^^^^^^^^^^^^^^^^^

+-----------------------+---------------+------------+-----------------+-----------------------------------------------------------------------------------------+------------------+
| Field                 | Type          | Required   | Default         | Description                                                                             | Allowed Values   |
+=======================+===============+============+=================+=========================================================================================+==================+
| destination           | number        | Yes        |                 | Service port this virtual server accepts cxns.                                          |                  |
+-----------------------+---------------+------------+-----------------+-----------------------------------------------------------------------------------------+------------------+
| service-name          | string        | Yes        |                 | Application tag this virtual server proxies for, services are discovered dynamically.   |                  |
+-----------------------+---------------+------------+-----------------+-----------------------------------------------------------------------------------------+------------------+
| ip-protocol           | string        | No         | 'http'          | Service type of this virtual server.                                                    | 'http', 'tcp'    |
+-----------------------+---------------+------------+-----------------+-----------------------------------------------------------------------------------------+------------------+
| load-balancing-mode   | string        | No         | 'round-robin'   | Load balancing algorithm for this virtual server.                                       | 'round-robin'    |
+-----------------------+---------------+------------+-----------------+-----------------------------------------------------------------------------------------+------------------+
| keep-alive-msecs      | number        | No         | 1000            | Time (in milliseconds) between TCP keep-alive packets on socket to back-end server.     |                  |
+-----------------------+---------------+------------+-----------------+-----------------------------------------------------------------------------------------+------------------+
| flags                 | JSON Object   | No         |                 | Flags specific to virtual server                                                        |                  |
+-----------------------+---------------+------------+-----------------+-----------------------------------------------------------------------------------------+------------------+

Virtual server \ Flags
**********************

+-------------------+-----------+------------+-----------+--------------------------------------------------------------------+------------------+
| Field             | Type      | Required   | Default   | Description                                                        | Allowed Values   |
+===================+===========+============+===========+====================================================================+==================+
| x-forwarded-for   | boolean   | No         | false     | Flag to set x-forwarded-for header in request to backend server.   |                  |
+-------------------+-----------+------------+-----------+--------------------------------------------------------------------+------------------+
| x-served-by       | boolean   | No         | false     | Flag to set x-served-by header in response to client.              |                  |
+-------------------+-----------+------------+-----------+--------------------------------------------------------------------+------------------+

Configuration Example
~~~~~~~~~~~~~~~~~~~~~

An example marathon configuration containing two virtual server sections:

.. code-block:: javascript

    {
      "global": {
        "console-log-level": "debug"
      },
      "orchestration": {
        "marathon": {
          "uri": "http://api.mesos.example.com",
          "poll-interval": 5000
        }
      },
      "stats": {
        "url": "http://localhost:8088",
        "token": "this-is-the-token",
        "flushInterval": 10000,
        "backend": "splunk"
      },
      "virtual-servers": [
        {
          "destination": 8080,
          "service-name": "web-server",
          "ip-protocol": "http",
          "load-balancing-mode": "round-robin",
          "flags" : {
            "x-forwarded-for": false,
            "x-served-by": true
          }
        },
        {
          "destination": 9090,
          "service-name": "identity",
          "ip-protocol": "http",
          "load-balancing-mode": "round-robin",
          "keep-alive-msecs": 2000
        }
      ]
    }


Statistics
``````````

The LWP can provide statistics to a configured Splunk server or to an F5 statistics gatherer and visualizer.

Global Stats
~~~~~~~~~~~~

-  splunk source: lwp.transaction
-  splunk sourcetype: f5:lwp.stats:json
-  Frequency: periodic (controlled by ``LWP_CONFIG`` environment variable)

+--------------------------+----------------------------------------------------------------------------------+
| Name                     | Description                                                                      |
+==========================+==================================================================================+
| tot_requests             | Number of HTTP requests received from the clients                                |
+--------------------------+----------------------------------------------------------------------------------+
| clientside_tot_conns     | Number of TCP connections received from the clients                              |
+--------------------------+----------------------------------------------------------------------------------+
| clientside_cur_conns     | Current number of active TCP connections to the clients                          |
+--------------------------+----------------------------------------------------------------------------------+
| clientside_max_conns     | Maximum number of active TCP connections to the clients since the start of LWP   |
+--------------------------+----------------------------------------------------------------------------------+
| clientside_bytes_in      | Number of bytes read from the clients                                            |
+--------------------------+----------------------------------------------------------------------------------+
| clientside_bytes_out     | Number of bytes written to the clients                                           |
+--------------------------+----------------------------------------------------------------------------------+
| serverside_tot_conns     | Number of TCP connections opened to the servers                                  |
+--------------------------+----------------------------------------------------------------------------------+
| serverside_cur_conns     | Current number of active TCP connections to the servers                          |
+--------------------------+----------------------------------------------------------------------------------+
| serverside_max_conns     | Maximum number of active TCP connections to the servers since the start of LWP   |
+--------------------------+----------------------------------------------------------------------------------+
| server_latency           | Average time (in milliseconds) to connection to a server                         |
+--------------------------+----------------------------------------------------------------------------------+
| max_server_latency       | Maximum time (in milliseconds) to connection to a server                         |
+--------------------------+----------------------------------------------------------------------------------+
| failed_tcp_conns         | Number of TCP connections that have failed                                       |
+--------------------------+----------------------------------------------------------------------------------+

TCP Transaction Stats
~~~~~~~~~~~~~~~~~~~~~

-  splunk source: lwp.transaction
-  splunk sourcetype: f5:lwp.stats:json
-  Frequency: per connection

+----------------------+--------------------------------------------------------------------+
| Name                 | Description                                                        |
+======================+====================================================================+
| client_ip            | IP Address of the connection                                       |
+----------------------+--------------------------------------------------------------------+
| client_port          | TCP Port of the connection                                         |
+----------------------+--------------------------------------------------------------------+
| pool_member_name     | ID of the particular server pool member (embeds the server name)   |
+----------------------+--------------------------------------------------------------------+
| pool_member_ip       | IP address for the particular server pool member                   |
+----------------------+--------------------------------------------------------------------+
| pool_member_port     | TCP port of the particular server pool member                      |
+----------------------+--------------------------------------------------------------------+

HTTP Transaction Stats
~~~~~~~~~~~~~~~~~~~~~~

-  splunk source: lwp.transaction
-  splunk sourcetype: f5:lwp.stats:json
-  Frequency: per request

+---------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
| Name                      | Description                                                                                                                           |
+===========================+=======================================================================================================================================+
| client_ip                 | IP address of the connection associated with this request                                                                             |
+---------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
| client_port               | TCP port of the connect associated with this request                                                                                  |
+---------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
| client_user               | HTTP basic authentication user                                                                                                        |
+---------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
| ttfb                      | time-to-first-byte: Time (in milliseconds) between when the request was received and starting to write out the response headers       |
+---------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
| ttlb                      | time-to-first-byte: Time (in milliseconds) between when the request was received and writing out the last byte of the response body   |
+---------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
| response_status_code      | HTTP response code (e.g. 200)                                                                                                         |
+---------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
| http_version              | HTTP protocol version being used by the client (e.g. "1.1")                                                                           |
+---------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
| method_name               | HTTP method for this request (e.g. "POST")                                                                                            |
+---------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
| request_date              | Time (in milliseconds) when this request was received                                                                                 |
+---------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
| pool_member_name          | ID of the particular server pool member (embeds the server name)                                                                      |
+---------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
| pool_member_ip            | IP address for the particular server pool member                                                                                      |
+---------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
| pool_member_port          | TCP port of the particular server pool member                                                                                         |
+---------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
| url                       | URL for the HTTP request                                                                                                              |
+---------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
| user_agent                | HTTP user agent of the client                                                                                                         |
+---------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
| referrer                  | HTTP referer which indicates the originating URI                                                                                      |
+---------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
| request_headers_size      | Size (in bytes) of the request headers                                                                                                |
+---------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
| request_body_size         | Size (in bytes) of the request body                                                                                                   |
+---------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
| response_headers_size     | Size (in bytes) of the response headers                                                                                               |
+---------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
| response_body_size        | Size (in bytes) of the response body                                                                                                  |
+---------------------------+---------------------------------------------------------------------------------------------------------------------------------------+
