Troubleshoot Your Kubernetes Deployment
=======================================

Application Services Proxy
--------------------------

.. _k8s-asp-verify:

Verify the ASP handles traffic for a Service
````````````````````````````````````````````

#. Add the ``x-served-by`` flag to the `asp.config` annotation in the Service definition:

    .. literalinclude:: /_static/config_examples/f5-asp-k8s-example-service.yaml
        :emphasize-lines: 10

#. Send a ``curl -v`` request to the Service and view the headers to verify the ASP handled the request. The ``X-Served-By`` line should match the IP address of an ASP pod.

    .. code-block:: bash
        :emphasize-lines: 15

        k8s-worker-0 core:~$ curl -v http://172.16.1.19:30597
        * Rebuilt URL to: http://172.16.1.19:30597/
        *   Trying 172.16.1.19...
        * TCP_NODELAY set
        * Connected to 172.16.1.19 (172.16.1.19) port 30597 (#0)
        > GET / HTTP/1.1
        > Host: 172.16.1.19:30597
        > User-Agent: curl/7.50.2
        > Accept: */*
        >
        < HTTP/1.1 200 OK
        < Date: Fri, 17 Feb 2017 23:14:32 GMT
        < Connection: keep-alive
        < Transfer-Encoding: chunked
        < X-Served-By: 10.2.0.123
        <
        * Curl_http_done: called premature == 0
        * Connection #0 to host 172.16.1.19 left intact
        Hello Kubernetes!


|aspk-long|
-----------

Coming soon!

|kctlr-long|
------------

Coming soon!


|kctlr-long| running in OpenShift Origin
----------------------------------------

Coming soon!

