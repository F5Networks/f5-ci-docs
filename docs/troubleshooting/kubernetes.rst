Troubleshoot Your Kubernetes Deployment
=======================================

Application Services Proxy
--------------------------

.. _k8s-asp-verify:

Verify the ASP handles traffic for a Service
````````````````````````````````````````````

#. Add the ``x-served-by`` flag to the `asp.config` annotation in the Service definition:

   .. literalinclude:: /_static/config_examples/f5-asp-k8s-example-service.yaml
      :linenos:
      :lines: 1-9,21-
      :emphasize-lines: 12

#. Send a ``curl -v`` request to the Service and view the headers to verify the ASP handled the request.
   The ``X-Served-By`` line should match the IP address of an ASP pod.

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

.. _k8s-asp-event-handlers-verify:

Verify the execution of Event Handlers
``````````````````````````````````````

#. Add the event handlers to the `asp.config` annotation in the Service definition:

   .. literalinclude:: /_static/config_examples/f5-asp-k8s-example-service.yaml
      :linenos:
      :emphasize-lines: 10-20

#. Send a ``curl -X POST -v`` to the service to verify the ``http-request`` event handler. 
   The response status code should be ``503`` and the response message should be ``POST Method not supported``.

   .. code-block:: bash
     :emphasize-lines: 10,17

     core@asp-ctlr-master-k8s-functest-master-0 ~ $ curl -X POST -v http://10.3.0.155:80/
     *   Trying 10.3.0.155...
     * TCP_NODELAY set
     * Connected to 10.3.0.155 (10.3.0.155) port 80 (#0)
     > POST / HTTP/1.1
     > Host: 10.3.0.155
     > User-Agent: curl/7.50.2
     > Accept: */*
     >
     < HTTP/1.1 503 Service Unavailable
     < Date: Wed, 13 Sep 2017 22:16:27 GMT
     < Connection: keep-alive
     < Content-Length: 25
     <
     * Curl_http_done: called premature == 0
     * Connection #0 to host 10.3.0.155 left intact
     POST Method not supported

#. Send a ``curl -v`` to the service to verify the ``http-response`` event handler. The response should contain the header ``x-my-bar`` with value ``foo``.

   .. code-block:: bash
     :emphasize-lines: 20

     core@asp-ctlr-master-k8s-functest-master-0 ~ $ curl -v http://10.3.0.155:80/
     *   Trying 10.3.0.155...
     * TCP_NODELAY set
     * Connected to 10.3.0.155 (10.3.0.155) port 80 (#0)
     > GET / HTTP/1.1
     > Host: 10.3.0.155
     > User-Agent: curl/7.50.2
     > Accept: */*
     >
     < HTTP/1.1 200 OK
     < Server: nginx/1.10.3
     < Date: Wed, 13 Sep 2017 22:25:18 GMT
     < Content-Type: text/html
     < Content-Length: 52
     < Last-Modified: Wed, 13 Sep 2017 20:54:08 GMT
     < Connection: keep-alive
     < ETag: "59b99af0-34"
     < Accept-Ranges: bytes
     < X-Served-By: 10.2.97.5
     < x-my-bar: foo
     <
     Hello from cf8b4295-ac03-49fe-bc21-5d2aa05f48f8 :0)
     * Curl_http_done: called premature == 0
     * Connection #0 to host 10.3.0.155 left intact

  







