Troubleshoot Your Kubernetes Deployment
=======================================

How to get help
---------------

If the issue you're experiencing isn't covered here, try one of the following options:

- `Contact F5 Support`_ (valid support contract required).
- `Report a bug <https://github.com/F5Networks/k8s-bigip-ctlr/issues>`_ in the k8s-bigip-ctlr GitHub repo.
- `Ask a question <https://f5cloudsolutions.slack.com>`_ in the #cc-kubernetes channel in the F5 Cloud Solutions Slack team.


General Kubernetes and OpenShift troubleshooting
------------------------------------------------

The following troubleshooting docs may help with Kubernetes- or OpenShift-specific issues.

- `Kubernetes: Troubleshoot Applications <https://kubernetes.io/docs/tasks/debug-application-cluster/debug-application/>`_
- `Kubernetes: Troubleshoot Clusters <https://kubernetes.io/docs/tasks/debug-application-cluster/debug-cluster/>`_
- `OpenShift: Troubleshooting OpenShift SDN <https://docs.openshift.org/1.5/admin_guide/sdn_troubleshooting.html>`_

.. _k8s-bigip-ctlr troubleshoot:

BIG-IP Controller for Kubernetes/OpenShift
------------------------------------------

Logging
```````

Set the log level
~~~~~~~~~~~~~~~~~

To change the log level for the |kctlr|:

#. Edit the :ref:`Deployment <k8s-bigip-ctlr-deployment>` for each k8s-bigip-ctlr instance. Be sure to specify the correct namespace for the instance.

   .. code-block:: bash

      kubectl edit my-bigip-ctlr.yaml [--namespace kube-system]
      oc edit my-bigip-ctlr.yaml [--namespace kube-system]

#. Add the desired log-level to the :code:`args` section. For example:

   .. code-block:: yaml

      - --log-level
      - debug

#. Verify the Deployment updated successfully.

   .. code-block:: bash

      kubectl describe deployment my-bigip-ctlr -o wide [--namespace kube-system]
      oc describe deployment my-bigip-ctlr -o wide [--namespace kube-system]


View the logs
~~~~~~~~~~~~~

- To view the logs:

  .. code-block:: bash

     kubectl logs my-bigip-ctlr-pod
     oc logs my-bigip-ctlr-pod

- To follow the logs:

  .. code-block:: bash

     kubectl logs -f my-bigip-ctlr-pod
     oc logs -f my-bigip-ctlr-pod

- To view logs for a container that isn't responding:

  .. code-block:: bash

     kubectl logs --previous my-bigip-ctlr-pod
     oc logs --previous my-bigip-ctlr-pod


How do I check the settings of my |kctlr| using the command line?
`````````````````````````````````````````````````````````````````

You can use `kubectl`_ or `oc`_ commands to check the |kctlr| configurations using the command line.

.. code-block:: console

   kubectl [|oc] get pod -o yaml [--namespace=kube-system]          \\ Returns the Pod's YAML settings
   kubectl [|oc] describe pod myBigIpCtlr [--namespace=kube-system] \\ Returns an information dump about the Pod you can use to troubleshoot specific issues


What happened to my BIG-IP configuration changes?
`````````````````````````````````````````````````

If you make changes to objects in the partition managed by the |kctlr| -- whether via configuration sync or manually -- **the Controller will overwrite them**. By design, the |kctlr| keeps the BIG-IP system  in sync with what it knows to be the desired configuration. For this reason, F5 does not recommend making any manual changes to objects in the partition(s) managed by the |kctlr|.


Why don't the |kctlr| pod(s) show up when I run ``kubectl get pods``?
`````````````````````````````````````````````````````````````````````

If you launched the |kctlr| in the ``--kube-system`` namespace, you should add the ``--namespace`` flag to your :command:`kubectl get` command.

.. code-block:: console

   kubectl [|oc] get pods --namespace=kube-system
   kubectl [|oc] get pod myBigIpCtlr --namespace=kube-system


Why do the BIG-IP pool members use the Kubernetes node IPs instead of the pod IPs?
``````````````````````````````````````````````````````````````````````````````````

The |kctlr| uses node IPs when running in its default mode, ``nodeport``. See :ref:`Nodeport mode vs Cluster mode <kctlr modes>` for more information.


Why didn't the |kctlr| create any objects on the BIG-IP system?
```````````````````````````````````````````````````````````````

Here are a few things to check:

#. **Does the namespace of the Kubernetes resource match the namespace(s) you set the Controller to watch?**

   .. code-block:: yaml
      :caption: Excerpt from a sample Deployment

      apiVersion: extensions/v1beta1
      kind: Deployment
      metadata:
        name: k8s-bigip-ctlr-deployment
        namespace: kube-system
      ...
                args: [
                  "--bigip-username=$(BIGIP_USERNAME)",
                  "--bigip-password=$(BIGIP_PASSWORD)",
                  "--bigip-url=10.190.24.171",
                  "--bigip-partition=kubernetes",
                  "--namespace=<my-namespace>",
                  ]
      ...


#. **Are the Service name and port provided in your virtual server ConfigMap correct?**

   .. code-block:: yaml
      :caption: Sample Kubernetes Service
      :emphasize-lines: 4, 11

      kind: Service
      apiVersion: v1
      metadata:
        name: hello
      spec:
        selector:
          app: hello
          tier: backend
        ports:
        - protocol: TCP
          port: 80
          targetPort: http

   *Source:* `Connect a Front End to a Back End Using a Service <https://kubernetes.io/docs/tasks/access-application-cluster/connecting-frontend-backend/#creating-the-backend-service-object>`_


   .. code-block:: yaml
      :caption: Excerpt from a sample virtual server ConfigMap
      :emphasize-lines: 10-11

      kind: ConfigMap
      apiVersion: v1
      ...
      data:
       schema: "f5schemadb://bigip-virtual-server_v0.1.4.json"
        data: |
          {
            "virtualServer": {
              "backend": {
                "servicePort": 80,
                "serviceName": "hello",
              },
         ...
          }

#. **Does the** `service type`_ **provided in the BIG-IP Controller Deployment match the service type defined for the Service?**

   - The default service type used by Kubernetes is ``clusterIP``.
   - The default service type used by the |kctlr| is ``nodeport``.

   **If you didn't specify a service type** in the Service definition or the |kctlr| Deployment, you probably have a service type mismatch. See :ref:`Nodeport mode vs Cluster mode <kctlr modes>` for more information about each service type and recommended use.


#. **Did you provide valid JSON?**

   The |kctlr| can only parse valid JSON. Run your desired configurations through a JSON linter before use to avoid potential object creation errors.


#. **Have you used the correct version of the** `F5 schema`_ **to support your version of the BIG-IP Controller?**

   Additions to the F5 schema made with each version release support the new features in that specific version. For example, if you use v1.3.0 of the Controller with v0.1.2 of the schema, the Controller's core functionality would be fine. You wouldn't, however, be able to use `v1.3 features`_ like DNS resolution or :ref:`adding health monitors for OpenShift Routes <add health monitor to route>`.

#. **Are you looking in the correct partition on the BIG-IP system?**

   **In the BIG-IP configuration utility** (aka, the GUI), check the partition drop-down menu.

   .. image:: /_static/media/bigip-partition_gui.png


   **In the BIG-IP Traffic Management shell** (TMSH), check the name of the partition shown in the prompt.

   .. image:: /_static/media/bigip-partition_tmsh.png

   \ If you're in the ``Common`` partition, switch to the partition managed by the |kctlr| to find the objects it deployed.


Why didn't the |kctlr| create the pools/rules for my Ingress on the BIG-IP system?
``````````````````````````````````````````````````````````````````````````````````

When you create multiple rules in an Ingress that overlap, Kubernetes silently drops all but one of them. If you don't see all of the pools and/or rules you expect to see on the BIG-IP system, double-check your Ingress resource for redundant or overlapping settings.

For example, say you want to create a pool for your website's frontend app, with one (1) pool member for each of the Services comprising the app.

.. code-block:: yaml
   :caption: Good: 1 rule that includes both Services comprising the frontend app

   host: mysite.example.com
      path: /frontend
      - service: svc1
      - service: svc2

.. code-block:: yaml
   :caption: Bad: 2 rules that both attempt to route traffic for the frontend app

   host: mysite.example.com
      path: /frontend
      - service: svc1

   host: mysite.example.com
      path: /frontend
      - service: svc2

In the latter case, Kubernetes would drop one of the overlapping rules and the |kctlr| would only create one (1) pool member on the BIG-IP system.

Why don't my Annotations work?
``````````````````````````````

- Are you using Annotations recommended for a different `Kubernetes Ingress Controller`_ ?

  Annotations aren't universally applicable. You should only use Annotations included in the list of `Ingress annotations`_ supported by the |kctlr|.


.. _asp k8s troubleshoot:

Application Services Proxy
--------------------------

.. _k8s-asp-verify:

Verify the ASP handles traffic for a Service
````````````````````````````````````````````

Send a ``curl -v`` request to the Service and view the headers to verify the ASP handled the request.
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




.. _service type: https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services---service-types
.. _v1.3 features: /products/connectors/k8s-bigip-ctlr/latest/RELEASE-NOTES.html#v1-3-0
