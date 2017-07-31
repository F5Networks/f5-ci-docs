.. _asp_how_it_gets_traffic:

How the |asp| Handles Traffic
=============================

Summary
-------

The |asp|, or ASP, runs on each node in a Kubernetes `Cluster`_.  When
Kubernetes `Pods`_ send network traffic, that traffic goes through several layers
and one of those layers may be an ASP.  This page describes how that traffic
flows.  To use the ASP day-to-day, you should not need to understand this in
detail because the f5-kube-proxy and ASP take care of this automatically.

You deploy the ASP as a **client-side proxy** in Kubernetes:

- **Proxy**: deployed in between the client and server to inspect and modify all
  the data exchanged between the client and server.

- **Client-Side**: intercepts the traffic as it leaves the client:  The ASP
  running on the same Kubernetes node as the client is the one that handles the
  network data, even though it is applying policy on behalf of the server.

The ASP controls Pod-to-Pod traffic so this document will describe in detail
the traffic for clients that are in the Kubernetes cluster.

Kubernetes Pods shouldn't worry about any of this.  If they need to become
clients and make connections to other Kubernetes `Services`_, they should just
make the connections as normal and expect that the network takes care of
proxying the traffic through ASP if necessary.  This happens because
f5-kube-proxy, ASP, and Linux iptables collaborate to make it happen.

We made the examples below with Kubernetes 1.6.4, using Calico 1.1.0,
f5-kube-proxy 1.0.0 and ASP 1.0.0.  The specific iptables rules created are an
implementation detail that may change with different versions, so treat the
examples as illustrative.  You deploy ASP differently in Mesos/Marathon, so
this example does not apply to that environment.

How Services in Kubernetes Work
-------------------------------

Kubernetes Services are resources that select a bunch of network endpoints
that implement that Service.  The endpoints are commonly Kubernetes Pods (but
can be external endpoints as well).  When the client resolves the service by
name using DNS, it gets the service IP as an answer.  When it sends packets to
the service IP, then that traffic gets routed to one of the endpoints that
implements that service.

To understand how it works in a plain Kubernetes cluster, we'll start without
ASP or f5-kube-proxy installed.  When using the kube-proxy in its default
iptables mode, iptables rules implement the service IP.  Let's try an
example (you can try the commands yourself or just read the output here).
We'll deploy *my-nginx* pods and a service for them much like the `Running Your
First Containers
<https://github.com/kubernetes/kubernetes/blob/master/examples/simple-nginx.md>`_
example from Kubernetes:

    .. code-block:: none

        user@k8s-master:~$ kubectl run my-nginx --image=nginx --replicas=2
        user@k8s-master:~$ kubectl get deployment -o wide
        NAME       DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE       CONTAINER(S)   IMAGE(S)   SELECTOR
        my-nginx   2         2         2            2           15m       my-nginx       nginx      run=my-nginx
        user@k8s-master:~$ kubectl get pods -o wide
        NAME                       READY     STATUS    RESTARTS   AGE       IP                NODE
        my-nginx-858393261-gngw8   1/1       Running   0          12m       192.168.36.129    kubeadm-worker-0
        my-nginx-858393261-sl5kh   1/1       Running   0          12m       192.168.155.193   kubeadm-worker-2

I can now talk directly to a particular pod (for example, ``curl
192.168.36.129`` returns the nginx Welcome page).  Next, I will make a Service
that references the *my-nginx* Pods so that I can scale the *my-nginx*
Deployment up or down and have traffic to that service be automatically
distributed:

    .. code-block:: none
    
        user@k8s-master:~$ kubectl expose deployment my-nginx --port=80
        user@k8s-master:~$ kubectl get service -o wide
        NAME         CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE       SELECTOR
        my-nginx     10.111.94.71   <none>        80/TCP    19m       run=my-nginx
        user@k8s-master:~$ kubectl get endpoints -o wide
        NAME         ENDPOINTS                              AGE
        my-nginx     192.168.155.193:80,192.168.36.129:80   20m

We can see that there is now a Service with an IP of 10.111.94.71.  The two
endpoints 192.168.155.193:80 and 192.168.36.129:80 *implement* that IP:  In the
end one of these two endpoints will handle all the traffic for the service IP.
These two endpoints are the IP addresses of the my-nginx pods.  Now we can
start a toolbox pod and test being a client of this service:

    .. code-block:: none

        user@k8s-master:~$ kubectl run -i --tty toolbox --image=sjourdan/toolbox --restart=Never -- sh
        If you don't see a command prompt, try pressing enter.
        / # curl -v my-nginx
        * Rebuilt URL to: my-nginx/
        *   Trying 10.111.94.71...
        * TCP_NODELAY set
        * Connected to my-nginx (10.111.94.71) port 80 (#0)
        > GET / HTTP/1.1
        ... (an HTTP GET request and the nginx welcome page appear here) ...


.. figure:: /_static/media/howkubeproxy.png

    **How kube-proxy receives traffic without ASP**

What happened here?  First, our pod's ``curl`` process tried to resolve the
name "my-nginx" via DNS.  It got 10.111.94.71, the service IP, back from
`kube-dns
<https://github.com/kubernetes/kubernetes/tree/master/cluster/addons/dns>`_.
Then it connected to this service IP and got a response from one of the pods.
If your Kubernetes cluster is running kube-proxy in iptables mode (the
default), then this is due to some iptables rules.  We can see these rules on
any of the nodes.  Below, we show only the relevant rules after reordering
sections and cleaning up whitespace.

    .. code-block:: none

	user@k8s-master:~$ sudo iptables -L -t nat
	Chain KUBE-SERVICES (2 references)
	target     prot opt source               destination
	KUBE-SVC-BEPXDJBUHFCSYIC3  tcp  --  anywhere             10.111.94.71         /* default/my-nginx: cluster IP */ tcp dpt:http
	KUBE-SVC-NPX46M4PTMTKRN6Y  tcp  --  anywhere             10.96.0.1            /* default/kubernetes:https cluster IP */ tcp dpt:https
	KUBE-SVC-TCOU7JCQXEZGVUNU  udp  --  anywhere             10.96.0.10           /* kube-system/kube-dns:dns cluster IP */ udp dpt:domain
	KUBE-SVC-ERIFXISQEP7F7OF4  tcp  --  anywhere             10.96.0.10           /* kube-system/kube-dns:dns-tcp cluster IP */ tcp dpt:domain
	KUBE-SVC-NTYB37XIWATNM25Y  tcp  --  anywhere             10.96.232.136        /* kube-system/calico-etcd: cluster IP */ tcp dpt:6666
	KUBE-SVC-XGLOHA7QRQ3V22RZ  tcp  --  anywhere             10.102.149.238       /* kube-system/kubernetes-dashboard: cluster IP */ tcp dpt:http
	KUBE-NODEPORTS  all  --  anywhere             anywhere             /* kubernetes service nodeports; NOTE: this must be the last rule in this chain */ ADDRTYPE match dst-type LOCAL

	Chain KUBE-SVC-BEPXDJBUHFCSYIC3 (1 references)
	target     prot opt source               destination
	KUBE-SEP-5QJQLOAYBTXEYYW5  all  --  anywhere             anywhere             /* default/my-nginx: */ statistic mode random probability 0.50000000000
	KUBE-SEP-OJZLCJUDW7QMREOS  all  --  anywhere             anywhere             /* default/my-nginx: */

	Chain KUBE-SEP-5QJQLOAYBTXEYYW5 (1 references)
	target     prot opt source               destination
	KUBE-MARK-MASQ  all  --  192.168.155.193      anywhere             /* default/my-nginx: */
	DNAT       tcp  --  anywhere             anywhere             /* default/my-nginx: */ tcp to:192.168.155.193:80

	Chain KUBE-SEP-OJZLCJUDW7QMREOS (1 references)
	target     prot opt source               destination
	KUBE-MARK-MASQ  all  --  192.168.36.129       anywhere             /* default/my-nginx: */
	DNAT       tcp  --  anywhere             anywhere             /* default/my-nginx: */ tcp to:192.168.36.129:80


This is example output from Kubernetes 1.6.4 with Calico.  Your particular
output may differ if you are in a different environment but we'll discuss the highlights.

When we asked our client pod to ``curl my-nginx``, it sent a TCP SYN packet to
10.111.94.71, the service IP.  Let's walk through the iptables rules for this packet.

First, it hit the PREROUTING table and jumped into KUBE-SERVICES.  (We'll skip
cali-PREROUTING because that's specific to Calico).  the KUBE-SERVICES chain
has one rule for each service (and finally a catch-all for nodeports that we'll
ignore).  We're looking for a rule that will match the destination IP
10.111.94.71; notice that the first rule KUBE-SVC-BEPXDJBUHFCSYIC3 matches (and
has a comment indicating it's for the "default/my-nginx" service).

So, jump to the KUBE-SVC-BEPXDJBUHFCSYIC3 chain and note that it has two rules:
it will apply KUBE-SEP-5QJQLOAYBTXEYYW5 with probability 0.5, and then if that
doesn't happen it will apply KUBE-SEP-OJZLCJUDW7QMREOS.  

Now look at KUBE-SEP-5QJQLOAYBTXEYYW5; it does two things:

- Mark that the kernel should enable masquerading for 192.168.155.193 for the packet.
- Apply DNAT (destination network address translation) to 192.168.155.193, port 80.

KUBE-SEP-OJZLCJUDW7QMREOS is the same for the other endpoint IP:

- Mark that the kernel should enable masquerading for 192.168.36.129 for the packet.
- Apply DNAT (destination network address translation) to 192.168.36.129, port 80.

The DNAT rule causes linux to rewrite the destination IP address and port in
the packet.  The masquerade mark causes linux's IP masquerading functionality
to be ready to un-NAT the packets that come back from the server pod.

The random rule application implements equal-weight random load-balancing; in a
Kubernetes Service with 2 endpoints you'll go to the first one half of the time
and the last one the other half.  With N=3 endpoints, you can see that the
first has probability 0.33 (1/N), the second probability 0.5 (1/N-1), and the
last probability 1. (You can try this yourself with ``kubectl edit deployment
my-nginx``)


How ASP provides Enhanced Services
----------------------------------

Now that we understand how Kubernetes' kube-proxy configures iptables rules by
default, we can learn how f5-kube-proxy configures different iptables rules to
direct some traffic to ASP.

First, I installed f5-kube-proxy following the instructions.  Now, when I run
``iptables -L -t nat``, the first thing I notice is... nothing changed.  By
default, f5-kube-proxy doesn't do anything different than kube-proxy.  Only
services that request ASP services get different rules.

Next, I modify the ``my-nginx`` service to use ASP by adding the "annotations"
section:

    .. code-block:: bash
       :emphasize-lines: 5-11

        user@k8s-master:~$ kubectl edit service my-nginx
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


.. figure:: /_static/media/howasp.png
    :align: center

    **How ASP receives traffic with f5-kube-proxy**

Now if I run ``iptables -L -t nat`` I see that most rules are the same, but the
implementation of the KUBE-SVC-BEPXDJBUHFCSYIC3 chain has changed.  Here's the
relevant part of my output for the top-level KUBE-SERVICES and the
implementation of the my-nginx service:

    .. code-block:: none

	Chain KUBE-SERVICES (2 references)
	target     prot opt source               destination
	KUBE-SVC-NPX46M4PTMTKRN6Y  tcp  --  anywhere             10.96.0.1            /* default/kubernetes:https cluster IP */ tcp dpt:https
	KUBE-SVC-NTYB37XIWATNM25Y  tcp  --  anywhere             10.96.232.136        /* kube-system/calico-etcd: cluster IP */ tcp dpt:6666
	KUBE-SVC-BEPXDJBUHFCSYIC3  tcp  --  anywhere             10.111.94.71         /* default/my-nginx: cluster IP */ tcp dpt:http
	KUBE-SVC-XGLOHA7QRQ3V22RZ  tcp  --  anywhere             10.102.149.238       /* kube-system/kubernetes-dashboard: cluster IP */ tcp dpt:http
	KUBE-SVC-TCOU7JCQXEZGVUNU  udp  --  anywhere             10.96.0.10           /* kube-system/kube-dns:dns cluster IP */ udp dpt:domain
	KUBE-SVC-ERIFXISQEP7F7OF4  tcp  --  anywhere             10.96.0.10           /* kube-system/kube-dns:dns-tcp cluster IP */ tcp dpt:domain
	KUBE-NODEPORTS  all  --  anywhere             anywhere             /* kubernetes service nodeports; NOTE: this must be the last rule in this chain */ ADDRTYPE match dst-type LOCAL


	Chain KUBE-SVC-BEPXDJBUHFCSYIC3 (1 references)
	target     prot opt source               destination
	KUBE-SEP-BEPXDJBUHFCSYIC3  all  --  anywhere             anywhere             /* default/my-nginx: via plugin */

	Chain KUBE-SEP-BEPXDJBUHFCSYIC3 (1 references)
	target     prot opt source               destination
	DNAT       tcp  --  anywhere             anywhere             /* default/my-nginx: via plugin */ tcp to:127.0.0.1:10000


Let's walkthrough the changes.  First, the KUBE-SERVICES table is the same -
the Service IP 10.111.94.71 is still associated with the my-nginx service, and
it's still a jump to the KUBE-SVC-BEPXDJBUHFCSYIC3 chain.  Now we get to the
interesting part - this SVC chain used to be where kube-proxy and iptables
implemented the random loadbalancing across two endpoints.  Instead, now the
rules just jump straight to one particular endpoint
(KUBE-SEP-BEPXDJBUHFCSYIC3).  That endpoint as well is interesting: it's not
one of the my-nginx pods any more.  It's actually a DNAT rule to
127.0.0.1:10000.

The ASP listens on 127.0.0.1:10000.  This is the ``--proxy-plugin-port``
option defined in the f5-kube-proxy configuration (which defaults to 10000) -
the f5-kube-proxy agrees to DNAT traffic for the ASP to this port, and the ASP
agrees to accept it on that port.

All traffic for the ASP goes through 127.0.0.1:10000 regardless of the
Kubernetes Service.  But the ASP needs to handle traffic differently for
different Services.  As soon as the traffic enters the ASP, the ASP uses the
SO_ORIGINAL_DST sockopt to get the original destination (before DNATting).  For
traffic that was originally sent to the my-nginx service, we'll get
10.111.94.71 back as the SO_ORIGINAL_DST and ASP internally sends it through
the traffic processing associated with the my-nginx service.

In this case, ASP knows about the endpoints for this service
(192.168.155.193:80,192.168.36.129:80), and chooses among them using its own
load-balancing algorithm (round-robin in this example).


Conclusion
----------

This example walked through how kube-proxy uses iptables by default to
implement the IPs for Kubernetes Services, and then showed how f5-kube-proxy
uses different iptables rules to direct traffic for Kubernetes Services to ASP.
This allows ASP to function as a full client-side proxy to provide advanced
traffic services.

.. _DaemonSet: https://kubernetes.io/docs/admin/daemons/
.. _Cluster: https://kubernetes.io/docs/admin/cluster-management/
.. _Pods: https://kubernetes.io/docs/concepts/workloads/pods/pod-overview/
