|lwp| Configuration Example
```````````````````````````

An example Marathon configuration containing two virtual server sections:

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

