.. index::
   single: Kubernetes; Ingress
   single: OpenShift; Ingress
   single: BIG-IP Controller; Ingress

.. _kctlr-ingress-config:

Expose Services to External Traffic using Ingresses
===================================================

.. include:: /_static/reuse/k8s-version-added-1_1.rst

.. change title to "Use BIG-IP as an Edge Load Balancer "??

You can use the |kctlr-long| and OpenShift to expose Services to external traffic on BIG-IP virtual servers. The |kctlr| has a set of `supported Ingress annotations`_ that allow you to define the objects to create on the BIG-IP system.

The |kctlr| supports four (4) types of Kubernetes `Ingress Resource`_:

- :ref:`single service`,
- :ref:`simple fanout`,
- :ref:`name-based virtual hosting`, --OR--
- :ref:`ingress-TLS`.


.. attention::

   The |kctlr| creates one (1) BIG-IP virtual server per Ingress resource. If the Ingress resource incorporates multiple Services, the |kctlr| creates a pool for each Service.

   If you set setting :code:`allowHttp` or :code:`sslRedirect` to "True", the Controller creates two (2) virtual servers.

\

.. table:: Tasks

   =======  ===================================================================
   Step     Description
   =======  ===================================================================
   1.       :ref:`Create a BIG-IP Self IP address <ingress self IP>` for the
            virtual server.
   2.       :ref:`create k8s ingress`.
   3.       :ref:`add health monitor to ingress`.
   4.       :ref:`deploy ingress resource`.
   5.       :ref:`verify-ingress-vs-created`.
   =======  ===================================================================


.. _ingress self IP:

Initial Setup
-------------

#. Create a BIG-IP Self IP address.

   Allocate a `Self IP address`_ from the external network on the BIG-IP system. This is the IP address you should assign to the Ingress' virtual server.

.. todo:: add instructions for creating Self IP on BIG-IP; reuse? or link to in VE public cloud docs?


.. _ingress-quick-start:

Quick Start
-----------

You can add the `supported Ingress annotations`_ to any existing Ingress resource using :command:`kubectl annotate` or :command:`oc annotate`.
At minimum, define the following properties:

- :code:`virtual-server.f5.com/ip`
- :code:`virtual-server.f5.com/partition`

.. hint::

   In Kubernetes/OpenShift, the default for the :code:`ingress.class` property is unset. The |kctlr| automatically manages any Ingress resources for which this property is unset.

   To avoid conflicts with other Ingress controllers, set the :code:`ingress.class` property to "f5", as shown below:

   :code:`kubernetes.io/ingress.class="f5"`

   Specify a different value for Ingress resources that other controllers should manage. The |kctlr| ignores Ingress resources with any :code:`ingress.class` other than "f5".


Kubernetes
``````````

.. code-block:: console

   kubectl annotate ingress myIngress virtual-server.f5.com/ip="1.2.3.4"
   kubectl annotate ingress myIngress virtual-server.f5.com/partition="k8s"
                                      virtual-server.f5.com/balance="round-robin"
                                      virtual-server.f5.com/http-port="80"
                                      virtual-server.f5.com/health='[{"path": "svc1.bar.com/foo", "send": "HTTP GET /health/foo", "interval": 5, "timeout": 10}]'
                                      ingress.kubernetes.io/ssl-redirect="true"
                                      ingress.kubernetes.io/allow-http="false"
                                      kubernetes.io/ingress.class="f5"
   // Also valid
   kubectl annotate ingress myIngress virtual-server.f5.com/ip="controller-default"


OpenShift
`````````

.. code-block:: console

   oc annotate ingress myIngress virtual-server.f5.com/ip="1.2.3.4"
   oc annotate ingress myIngress virtual-server.f5.com/partition="openshift"
                                 virtual-server.f5.com/balance="round-robin"
                                 virtual-server.f5.com/http-port="80"
                                 virtual-server.f5.com/health='[{"path": "svc1.bar.com/foo", "send": "HTTP GET /health/foo", "interval": 5, "timeout": 10}]'
                                 ingress.kubernetes.io/ssl-redirect="true"
                                 ingress.kubernetes.io/allow-http="false"
                                 kubernetes.io/ingress.class="f5"

.. tip::

   There are multiple ways to configure the Virtual IP address for Ingress resources:
     #. Do not specify it at all, and the controller creates only pools.
     #. Have an external controller (or manually) set the ``virtual-server.f5.com/ip`` annotation with the desired address.
     #. Use the DNS lookup option (``resolve-ingress-names``) in the `k8s-bigip-ctlr configuration parameters`_.

        - Controller sets the IP address to the resolved host's IP Address

     #. Set the ``default-ingress-ip`` in the `k8s-bigip-ctlr configuration parameters`_.

        - The controller configures Ingresses with the annotation ``virtual-server.f5.com/ip="controller-default"`` with the IP address specified in the ``default-ingress-ip`` parameter.
        - Note that there is only one of these ``default-ingress-ip`` parameters per controller. If you want multiple IP addresses, then you can
          run multiple controllers that each monitor different namespaces. This also enables access control if you don't want certain namespaces
          to be able to attach to certain VIPs.


.. _create k8s ingress:

Create an Ingress Resource with the F5 virtual-server annotation
----------------------------------------------------------------

Define the `supported Ingress annotations`_ in a Kubernetes `Ingress Resource`_ using valid JSON.


.. _single service:

Single Service
``````````````

A :dfn:`Single Service` Ingress creates a BIG-IP virtual server and server pool for a single Kubernetes Service.

.. literalinclude:: /kubernetes/config_examples/f5-k8s-single-ingress.yaml
   :linenos:
   :emphasize-lines: 6-10

:fonticon:`fa fa-download` :download:`f5-k8s-single-ingress.yaml </kubernetes/config_examples/f5-k8s-single-ingress.yaml>`

.. _simple fanout:

Simple Fanout
`````````````

A :dfn:`Simple Fanout` Ingress creates a BIG-IP virtual server and pools for a group of Kubernetes Services (one pool per Service).

.. literalinclude:: /kubernetes/config_examples/f5-k8s-ingress-fanout.yaml
   :linenos:
   :emphasize-lines: 7-12

:fonticon:`fa fa-download` :download:`f5-k8s-ingress-fanout.yaml </kubernetes/config_examples/f5-k8s-ingress-fanout.yaml>`

.. _name-based virtual hosting:

Name-based virtual hosting
``````````````````````````

A :dfn:`Name-based virtual hosting` ingress creates the following BIG-IP objects:

- One (1) virtual server with one (1) pool for each Service.
- Local traffic policies that route requests to specific pools based on host name and path.

.. tip::

   If you don't specify any hosts or paths, the BIG-IP device will proxy traffic for all hosts/paths for the Service specified in the :code:`backend` section of the virtual-server annotation.

\

.. literalinclude:: /kubernetes/config_examples/f5-k8s-ingress-virtual-hosting.yaml
   :linenos:
   :caption: Specific hosts
   :emphasize-lines: 6-14, 18, 27

:fonticon:`fa fa-download` :download:`f5-k8s-ingress-virtual-hosting.yaml </kubernetes/config_examples/f5-k8s-ingress-virtual-hosting.yaml>`

.. literalinclude:: /kubernetes/config_examples/f5-k8s-ingress-virtual-hosting_all.yaml
   :linenos:
   :caption: All hosts
   :emphasize-lines: 6-14, 17

:fonticon:`fa fa-download` :download:`f5-k8s-ingress-virtual-hosting_all.yaml </kubernetes/config_examples/f5-k8s-ingress-virtual-hosting_all.yaml>`

.. _ingress-TLS:

TLS
```

You can secure an Ingress using :ref:`Secrets <k8s-ingress-secrets>` or :ref:`BIG-IP SSL profiles <k8s-ingress-bigip-ssl>`.

#. Specify the SSL profile(s) or the Secret containing the cert and key in the :code:`spec.tls` section of the Ingress resource.
#. Add the :code:`ingress.kubernetes.io/ssl-redirect` annotation (**OPTIONAL**; defaults to :code:`"true"`).
#. Add the :code:`ingress.kubernetes.io/allow-http` annotation (**OPTIONAL**; defaults to :code:`"false"`).

.. note::

   - You can specify one (1) or more SSL profiles in your Ingress resource.
   - If you specify a :code:`spec.tls` section without providing the TLS Ingress properties,the BIG-IP device uses local traffic policies to redirect HTTP requests to HTTPS.

\

.. seealso::

   Refer to the `Kubernetes TLS Ingress documentation <https://kubernetes.io/docs/concepts/services-networking/ingress/#tls>`_ for details regarding supported port(s) and termination.


.. _k8s-ingress-bigip-ssl:

BIG-IP SSL profiles
~~~~~~~~~~~~~~~~~~~

.. literalinclude:: /kubernetes/config_examples/f5-k8s-ingress-tls.yaml
   :caption: TLS Example
   :linenos:
   :emphasize-lines: 11-14, 16-19

:fonticon:`fa fa-download` :download:`f5-k8s-ingress-tls.yaml </kubernetes/config_examples/f5-k8s-ingress-tls.yaml>`

.. _k8s-ingress-secrets:

Kubernetes Secrets
~~~~~~~~~~~~~~~~~~

.. literalinclude:: /kubernetes/config_examples/f5-k8s-ingress-tls-secret.yaml
      :caption: TLS Example
      :linenos:
      :emphasize-lines: 16-18

:fonticon:`fa fa-download` :download:`f5-k8s-ingress-tls-secret.yaml </kubernetes/config_examples/f5-k8s-ingress-tls-secret.yaml>`

.. _add health monitor to ingress:

Create a BIG-IP Health Monitor for an Ingress
---------------------------------------------

#. Add the :code:`virtual-server.f5.com/health` annotation to your Ingress resource.

   .. literalinclude:: /kubernetes/config_examples/f5-k8s-ingress-health-monitor.yaml
      :caption: Health Monitor Example
      :linenos:
      :emphasize-lines: 9-22


.. _deploy ingress resource:

Upload the Ingress to the API server
------------------------------------

Use :command:`kubectl create` to upload the Ingress Resource to the Kubernetes API server.

.. code-block:: console

   kubectl create ingress -f <filename>.yaml
   Ingress "myIngress" created

.. _verify-ingress-vs-created:

Verify creation of BIG-IP objects
---------------------------------

You can use TMOS or the BIG-IP configuration utility to verify that the |kctlr| created the requested BIG-IP objects for your Ingress.

To verify using the BIG-IP configuration utility:

#. Log in to the configuration utility at the management IP address (for example: :code:`https://10.190.25.225/tmui/login.jsp?`).
#. Select the correct partition from the :guilabel:`Partition` drop-down menu.
#. Go to :menuselection:`Local Traffic --> Virtual Servers` to view all virtual servers, pools, and pool members.
#. Go to :menuselection:`Local Traffic --> Policies` to view any new policies.

See the `TMSH Reference Guide`_ (PDF) for the relevant :command:`tmsh ltm` commands.


.. What's Next
   ------------
   -- add links
   -- to new Ingress use-case
   -- solution docs here

.. _TMSH Reference Guide: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/bigip-tmsh-reference-12-0-0.html
.. _BIG-IP server pool: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/ltm-basics-13-0-0/4.html
.. _Host header: https://tools.ietf.org/html/rfc7230#section-5.4
.. _Kubernetes documentation: https://kubernetes.io/docs/concepts/services-networking/ingress/#name-based-virtual-hosting
.. _TLS ingress: https://kubernetes.io/docs/concepts/services-networking/ingress/#tls
