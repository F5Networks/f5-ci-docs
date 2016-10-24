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

