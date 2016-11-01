.. table:: Forwarder Stats Collection

    ===============     ===========================     =============================
    Connection Type     Per Transaction/Connection      Across Transaction/Connection
    ---------------     ---------------------------     -----------------------------
    HTTP                client address                  request counts
                        server address                  response counts
                        method                          method counts
                        status code                     status code counts
                        URL                             error counts
                        server RTT                      total connections
                        latency                         current connections
                        bytes read                      total closed
                        bytes written
    ---------------     ---------------------------     -----------------------------
    TCP                 client address                  total connections
                        server address                  current connections
                        bytes read                      total closed
                        bytes written                   error counts
                        server RTT
                        latency
    ===============     ===========================     =============================

.. todo:: This tables doesn't render correctly
