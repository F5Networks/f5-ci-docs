.. todo: MOVE TO ASP REPO

.. _asp_how_it_gets_traffic:

How the ASP Handles Traffic in Kubernetes
=========================================

Summary
-------

This document uses practical examples to demonstrate how the |asp| (ASP) and `f5-kube-proxy`_ fit into Kubernetes' network traffic flow.
While not essential for ASP use, an understanding of how ASP instances and f5-kube-proxy interact with each other and the Kubernetes network framework can be beneficial.

An ASP runs on each node in a Kubernetes `Cluster`_.
Within a Cluster, `Pods`_ send network traffic through several layers; one of those layers may be an ASP.
That ASP acts as a **client-side proxy**, controlling Pod-to-Pod traffic for clients in the Cluster.

.. important::

   An ASP instance sitting in between the client and server inspects and modifies all of the data exchanged between the two.

   - The ASP intercepts traffic as it leaves the client;
   - The ASP running on *the same Kubernetes node as the client* handles the network data, even though it applies policy on behalf of the server.

   The Kubernetes Pods themselves don't really have to worry about any of this.
   If Pods need to become clients and make connections to other Kubernetes `Services`_, they just make the connection.

   The f5-kube-proxy, ASP, and Linux iptables work together to handle traffic and data for Services, including proxying traffic through an ASP.

Working Environment
```````````````````
- Kubernetes 1.6.4
- `Calico`_ 1.1.0
- `f5-kube-proxy 1.0.0`_
- `ASP 1.0.0`_.

Caveats
```````
- The iptables rules created are an implementation detail that may change with different versions, so treat the examples as illustrative.
- :ref:`ASP deploys differently in Mesos/Marathon <aspm-overview>`, so this example doesn't apply to that environment.

How Kubernetes Services Work
----------------------------

In Kubernetes, `Services`_ are resources that define a set of network endpoints and a policy via which network traffic can reach those endpoints.
The endpoints are typically Kubernetes Pods (in other words, they're within the Kubernetes Cluster), but they can also be external. [#k8sservice]_

When a client requests a specific Service by name using DNS, it receives the service IP address.
When the client sends packets to that service IP, the traffic gets routed to one of the endpoints defined in the Service, according to the specified policy.

Practice Exercise #1
````````````````````

To understand how this works, start with a plain Kubernetes cluster **without** ASP or f5-kube-proxy installed.

In this example, you'll use the `kube-proxy`_ in its default ``iptables`` mode, in which iptables rules implement the service IP.

#. Deploy "my-nginx" pods and a service for them (much like in the `Running Your First Containers <https://github.com/kubernetes/kubernetes/blob/master/examples/simple-nginx.md>`_ example from Kubernetes).

   .. code-block:: console

      kubectl run my-nginx --image=nginx --replicas=2
      kubectl get deployment -o wide
      NAME       DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE       CONTAINER(S)   IMAGE(S)   SELECTOR
      my-nginx   2         2         2            2           15m       my-nginx       nginx      run=my-nginx
      kubectl get pods -o wide
      NAME                       READY     STATUS    RESTARTS   AGE       IP                NODE
      my-nginx-858393261-gngw8   1/1       Running   0          12m       192.168.36.129    kubeadm-worker-0
      my-nginx-858393261-sl5kh   1/1       Running   0          12m       192.168.155.193   kubeadm-worker-2

   You can now talk directly to a particular pod (for example, ``curl 192.168.36.129`` returns the nginx Welcome page).

#. Next, make a Service that references the *my-nginx* Pods.
   This will allow you to scale the *my-nginx* Deployment up or down and automatically distribute traffic to that service.

   .. code-block:: console
    
      kubectl expose deployment my-nginx --port=80
      kubectl get service -o wide         NAME         CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE       SELECTOR
      my-nginx     10.111.94.71   <none>        80/TCP    19m       run=my-nginx
      kubectl get endpoints -o wide
      NAME         ENDPOINTS                              AGE
      my-nginx     192.168.155.193:80,192.168.36.129:80   20m

   As you can see, you now have a Service with an IP of 10.111.94.71.

   You have two endpoints -- 192.168.155.193:80 and 192.168.36.129:80 -- which *implement* that Service IP.
   (In other words, the traffic for the service IP gets directed to one or the other of these two endpoints.)

   These two endpoints are the IP addresses of the "my-nginx" pods.

#. Now, you can start a toolbox pod and test the service from the client side.

   .. code-block:: console

      kubectl run -i --tty toolbox --image=sjourdan/toolbox --restart=Never -- sh
      If you don't see a command prompt, try pressing enter.
      / #curl -v my-nginx
      * Rebuilt URL to: my-nginx/
      *   Trying 10.111.94.71...
      * TCP_NODELAY set
      * Connected to my-nginx (10.111.94.71) port 80 (#0)
      > GET / HTTP/1.1
      ... (an HTTP GET request and the nginx welcome page appear here) ...


What happened here?
~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/media/howkubeproxy.png
   :align: center
   :scale: 100%
   :alt: A diagram showing the traffic flow from a client to Pods via a Service IP. The kube-proxy uses iptables rules and a basic load balancer to route traffic to one of the Pods associated with an endpoint defined for the Service.

   **How kube-proxy receives traffic without ASP**


First, the pod's ``curl`` process tried to resolve the name "my-nginx" via DNS.
It received the service IP -- 10.111.94.71 -- from `kube-dns <https://github.com/kubernetes/kubernetes/tree/master/cluster/addons/dns>`_.
Then, it connected to the service IP and received a response from one of the Pods.

In a Kubernetes cluster with kube-proxy running in iptables mode (the default), the iptables rules determines the responses and how to handle the client traffic.
You can see these rules on any of the nodes in the Cluster.

.. note::

   - This example output is from Kubernetes 1.6.4 with Calico.
     Your particular output may differ depending on your environment.
   - The information displayed in the example is a reorganized version, edited for clarity.

.. code-block:: console

	sudo iptables -L -t nat
	Chain KUBE-SERVICES (2 references)
	target                     prot opt source               destination
	KUBE-SVC-BEPXDJBUHFCSYIC3  tcp  --  anywhere             10.111.94.71        /* default/my-nginx: cluster IP */ tcp dpt:http
	KUBE-SVC-NPX46M4PTMTKRN6Y  tcp  --  anywhere             10.96.0.1           /* default/kubernetes:https cluster IP */ tcp dpt:https
	KUBE-SVC-TCOU7JCQXEZGVUNU  udp  --  anywhere             10.96.0.10          /* kube-system/kube-dns:dns cluster IP */ udp dpt:domain
	KUBE-SVC-ERIFXISQEP7F7OF4  tcp  --  anywhere             10.96.0.10          /* kube-system/kube-dns:dns-tcp cluster IP */ tcp dpt:domain
	KUBE-SVC-NTYB37XIWATNM25Y  tcp  --  anywhere             10.96.232.136       /* kube-system/calico-etcd: cluster IP */ tcp dpt:6666
	KUBE-SVC-XGLOHA7QRQ3V22RZ  tcp  --  anywhere             10.102.149.238      /* kube-system/kubernetes-dashboard: cluster IP */ tcp dpt:http
	KUBE-NODEPORTS             all  --  anywhere             anywhere            /* kubernetes service nodeports; NOTE: this must be the last rule in this chain */ ADDRTYPE match dst-type LOCAL

	Chain KUBE-SVC-BEPXDJBUHFCSYIC3 (1 references)
	target                     prot opt source               destination
	KUBE-SEP-5QJQLOAYBTXEYYW5  all  --  anywhere             anywhere            /* default/my-nginx: */ statistic mode random probability 0.50000000000
	KUBE-SEP-OJZLCJUDW7QMREOS  all  --  anywhere             anywhere            /* default/my-nginx: */

	Chain KUBE-SEP-5QJQLOAYBTXEYYW5 (1 references)
	target                     prot opt source              destination
	KUBE-MARK-MASQ             all  --  192.168.155.193     anywhere             /* default/my-nginx: */
	DNAT                       tcp  --  anywhere            anywhere             /* default/my-nginx: */ tcp to:192.168.155.193:80

	Chain KUBE-SEP-OJZLCJUDW7QMREOS (1 references)
	target                     prot opt source              destination
	KUBE-MARK-MASQ             all  --  192.168.36.129      anywhere             /* default/my-nginx: */
	DNAT                       tcp  --  anywhere            anywhere             /* default/my-nginx: */ tcp to:192.168.36.129:80


When you asked the client Pod to ``curl my-nginx``, it sent a TCP SYN packet to the service IP (10.111.94.71).
Here's how the iptables rules applied to that packet:

.. sidebar:: Demystifying iprules:

   ``KUBE-SEP-5QJQLOAYBTXEYYW5`` and ``KUBE-SEP-OJZLCJUDW7QMREOS`` do the same thing.

   Each pertains to one of the two endpoints defined for the Service.
   If the packet fails to reach the first endpoint via the defined load balancing method (``statistic mode random probability 0.50000000000``), it gets directed to the other endpoint.

   The *masquerade mark* tells linux's IP masquerading functionality to be ready to un-NAT the packets that come back from the server pod.

   The *DNAT rule* tells linux to rewrite the destination IP address and port in the packet.

   The *random probability* rule application implements equal-weight random load-balancing.
   In a Kubernetes Service with 2 endpoints, this means that you'll go to the first one half of the time and the last one the other half.

- **The packet hit the PREROUTING table and jumped into KUBE-SERVICES.**

  - The KUBE-SERVICES chain has one rule for each service and a catch-all for nodeports.
    You can ignore the latter for the purposes of this example.
  - Look for a rule that will match the destination IP -- **10.111.94.71**.

- **The packet jumps to KUBE-SVC-BEPXDJBUHFCSYIC3, which matches the destination IP.**

In the KUBE-SVC-BEPXDJBUHFCSYIC3 chain:

- **The packet jumps to KUBE-SEP-5QJQLOAYBTXEYYW5 with probability 0.5.** --OR --
- If KUBE-SEP-5QJQLOAYBTXEYYW5 doesn't work, **the packet jumps to KUBE-SEP-OJZLCJUDW7QMREOS.**

  In either case, the following rules apply:

  - Mark that the kernel should enable masquerading for 192.168.155.193 for the packet.
  - Apply DNAT (destination network address translation) to 192.168.155.193, port 80.


How ASP Enhances Services
-------------------------

Now that you understand how Kubernetes' kube-proxy uses iptables rules to handle network traffic, you'll discover how f5-kube-proxy uses iptables rules to direct traffic to an ASP.

Practice Exercise #2
````````````````````

#. `Install ASP and f5-kube-proxy`_.

#. Run ``iptables -L -t nat``.

   .. hint::

      The first thing you should notice is that nothing changed. By default, f5-kube-proxy doesn't do anything any differently than kube-proxy does.

      *Only Services that have an ASP attached follow different rules.*

#. Attach an ASP to the "my-nginx" Service by adding the "annotations" section.

   .. code-block:: console
      :emphasize-lines: 5-11

      kubectl edit service my-nginx
      apiVersion: v1
      kind: Service
      metadata:
        annotations:
          asp.f5.com/config: |
            {
         "ip-protocol": "http",
         "load-balancing-mode": "round-robin",
         "flags": { "x-forwarded-for": true }
            }
        creationTimestamp: 2017-07-28T22:11:01Z
        labels:
          run: my-nginx
        name: my-nginx
        namespace: default
        resourceVersion: "467045"
        selfLink: /api/v1/namespaces/default/services/my-nginx
        uid: a43b2184-73e1-11e7-aa9b-fa163e4222e5
      spec:
        clusterIP: 10.111.94.71
        ports:
        - port: 80
          protocol: TCP
          targetPort: 80
        selector:
          run: my-nginx
        sessionAffinity: None
        type: ClusterIP
      status:
        loadBalancer: {}


#. Run ``iptables -L -t nat`` again.

   You'll see that most rules are the same, but the **implementation** of the KUBE-SVC-BEPXDJBUHFCSYIC3 chain has changed.


What happened here?
~~~~~~~~~~~~~~~~~~~

.. figure:: /_static/media/howasp.png
   :align: center
   :scale: 100%
   :alt: A diagram showing how the traffic flow from a client to Pods differs when using f5-kube-proxy. F5-kube-proxy routes traffic to a specific endpoint representing the ASP 'proxy-plugin-port'. This is where ASP listens for connections for the Service.

   **How ASP receives traffic with f5-kube-proxy**

Here's the relevant section of the output for the top-level KUBE-SERVICES and the implementation of the "my-nginx" Service:

.. code-block:: console

   Chain KUBE-SERVICES (2 references)
   target                     prot opt source               destination
   KUBE-SVC-NPX46M4PTMTKRN6Y  tcp  --  anywhere             10.96.0.1            /* default/kubernetes:https cluster IP */ tcp dpt:https
   KUBE-SVC-NTYB37XIWATNM25Y  tcp  --  anywhere             10.96.232.136        /* kube-system/calico-etcd: cluster IP */ tcp dpt:6666
   KUBE-SVC-BEPXDJBUHFCSYIC3  tcp  --  anywhere             10.111.94.71         /* default/my-nginx: cluster IP */ tcp dpt:http
   KUBE-SVC-XGLOHA7QRQ3V22RZ  tcp  --  anywhere             10.102.149.238       /* kube-system/kubernetes-dashboard: cluster IP */ tcp dpt:http
   KUBE-SVC-TCOU7JCQXEZGVUNU  udp  --  anywhere             10.96.0.10           /* kube-system/kube-dns:dns cluster IP */ udp dpt:domain
   KUBE-SVC-ERIFXISQEP7F7OF4  tcp  --  anywhere             10.96.0.10           /* kube-system/kube-dns:dns-tcp cluster IP */ tcp dpt:domain
   KUBE-NODEPORTS             all  --  anywhere             anywhere             /* kubernetes service nodeports; NOTE: this must be the last rule in this chain */ ADDRTYPE match dst-type LOCAL

   Chain KUBE-SVC-BEPXDJBUHFCSYIC3 (1 references)
   target                     prot opt source               destination
   KUBE-SEP-BEPXDJBUHFCSYIC3  all  --  anywhere             anywhere             /* default/my-nginx: via plugin */

   Chain KUBE-SEP-BEPXDJBUHFCSYIC3 (1 references)
   target                     prot opt source               destination
   DNAT                       tcp  --  anywhere             anywhere             /* default/my-nginx: via plugin */ tcp to:127.0.0.1:10000


**The KUBE-SERVICES chain is the same.**

- The Service IP 10.111.94.71 is still associated with the "my-nginx" service.
- The packet still jumps to the KUBE-SVC-BEPXDJBUHFCSYIC3 chain.

**And, finally, the interesting part:**

- Instead of implementing random loadbalancing across the two endpoints, **the f5-kube-proxy rules jump straight to one particular endpoint** (KUBE-SEP-BEPXDJBUHFCSYIC3).
- The endpoint is  no longer one of the "my-nginx" pods. Now, it's a DNAT rule to ``127.0.0.1:10000``.

  .. tip::

     - The ASP listens on ``127.0.0.1:10000``.
       This is the ``--proxy-plugin-port`` option defined in the `f5-kube-proxy configuration`_ (which defaults to 10000).
     - The f5-kube-proxy agrees to DNAT traffic for the ASP to this port, and the ASP agrees to accept it on that port.
     - All traffic for the ASP goes through 127.0.0.1:10000 regardless of the Kubernetes Service.

The ASP can handle traffic differently for different Services.

- When traffic enters the ASP, the ASP uses the ``SO_ORIGINAL_DST`` sockopt to get the original destination (before DNAT-ing).
- ASP internally uses the traffic-processing associated with the originating Service ("my-nginx").

In this case,

- For traffic that was originally sent to the "my-nginx" Service, the ASP gets 10.111.94.71 back as the ``SO_ORIGINAL_DST``.
- f5-kube-proxy directs traffic from the original destination to the ASP at 127.0.0.1:10000.
- The ASP **uses its own load balancing algorithm** (round-robin) to direct traffic to each of the Service endpoints (192.168.155.193:80,192.168.36.129:80).

Conclusion
----------

By way of the practical examples provided, this document demonstrated the differences between kube-proxy's default iptables routing and how f5-kube-proxy uses its own iptables to route traffic for Kubernetes Services through the ASP.
This allows the ASP to function as a full client-side proxy, thereby providing advanced traffic services beyond Kubernetes' native kube-proxy capabilities.

.. rubric:: **Footnotes**
.. [#k8sservice] See `Kubernetes Services without Selectors <https://kubernetes.io/docs/concepts/services-networking/service/#services-without-selectors>`_ :fonticon:`fa fa-external`.

.. _DaemonSet: https://kubernetes.io/docs/admin/daemons/
.. _Cluster: https://kubernetes.io/docs/admin/cluster-management/
.. _Calico: https://www.projectcalico.org/
.. _ASP 1.0.0: /products/asp/v1.0
.. _f5-kube-proxy 1.0.0: /products/connectors/f5-kube-proxy/v1.0
.. _install ASP and f5-kube-proxy: /containers/v1/kubernetes/asp-install-k8s.html
.. _f5-kube-proxy configuration: /products/connectors/f5-kube-proxy/v1.0/#configuration-parameters
