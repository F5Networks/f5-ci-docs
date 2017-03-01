Proxy Kubernetes Services with the |asp|
========================================

.. table:: Docs test matrix

    +-----------------------------------------------------------+
    | kubernetes v1.3.7                                         |
    +-----------------------------------------------------------+
    | coreos-stable-1185.3.0                                    |
    +-----------------------------------------------------------+
    | asp v1.0.0                                                |
    +-----------------------------------------------------------+
    | f5-kube-proxy f5-v1.3.7                                   |
    +-----------------------------------------------------------+
    | `kubernetes hello-world`_ service with ASP annotation     |
    +-----------------------------------------------------------+


Summary
-------

The |asp| watches Kubernetes `Service`_ definitions for a set of annotations defining virtual server objects. The annotation consists of the ``asp: enable`` label and a set of ASP `configuration parameters </products/asp/latest/index.html#configuration-parameters>`_. When you annotate an existing Kubernetes `Service`_, the ASP creates a virtual server for that Service.

Annotate a Kubernetes Service
-----------------------------

#. Annotate the Service definition.

    .. code-block:: bash

        user@k8s-master:~$ kubectl annotate service example-service asp.f5.com/config="{\"ip-protocol\":\"http\",\"load-balancing-mode\":\"round-robin\"}"
        service "example-service" annotated

    :download:`Download an example Service definition with the ASP annotation </_static/config_examples/f5-asp-k8s-example-service.yaml>`

#. View the "proxy-plugin" :file:`service-ports.json` file to verify the ASP picked up the annotation.

    .. code-block:: bash

        master core:~$ less /var/run/kubernetes/proxy-plugin/service-ports.json
        [{"name":"default/example-service:","port":8080,"port-name":"","protocol":"tcp","bind-port":10000,"config":"{\"ip-protocol\":\"http\",\"load-balancing-mode\":\"round-robin\"}","endpoints":["10.2.5.4:8080","10.2.5.7:8080"]}]
        /var/run/kubernetes/proxy-plugin/service-ports.json (END)


#. Send a request to the `Service`_ to verify the ASP handles the traffic.

    .. code-block:: bash

        k8s-worker-0 core:~$ curl -v http://172.16.1.19:30597 \\ node IP and NodePort
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
        <
        * Curl_http_done: called premature == 0
        * Connection #0 to host 172.16.1.19 left intact
        Hello Kubernetes!



.. _kubernetes hello-world: https://kubernetes.io/docs/tutorials/stateless-application/expose-external-ip-address-service/
.. _Service: https://kubernetes.io/docs/user-guide/services/
