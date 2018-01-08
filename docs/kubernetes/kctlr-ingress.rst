.. index::
   single: Kubernetes; Ingress
   single: OpenShift; Ingress
   single: BIG-IP Controller; Ingress

.. _kctlr-ingress-config:

Use Ingress Resources to Expose Services to External Traffic
============================================================

.. include:: /_static/reuse/k8s-version-added-1_1.rst

You can use the |kctlr-long| as an Ingress Controller in Kubernetes.

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


Overview
--------

The |kctlr| uses the Kubernetes `Ingress resource`_ to expose Services to external traffic as follows:

- creates a BIG-IP virtual server for the Ingress Resource,
- creates a pool on the virtual server for each Service in the Ingress' path.

The |kctlr| supports the following Ingress resource types:

- :ref:`single service`,
- :ref:`simple fanout`,
- :ref:`name-based virtual hosting`, and
- :ref:`ingress-TLS`.


The |kctlr| has a set of `supported Ingress annotations`_ that let you define the objects you want to create on the BIG-IP system.

.. attention::

   The |kctlr| creates one BIG-IP virtual server for each Ingress resource. If the Ingress resource incorporates multiple Services, the |kctlr| creates one pool for each Service.

   If you set :code:`allowHttp` or :code:`sslRedirect` to "True", the Controller creates two virtual servers -- one for HTTP and one for HTTPS.

IP address assignment
`````````````````````

The |kctlr| supports the following options for IP address assignment. See the `k8s-bigip-ctlr configuration parameters`_ table for more information about these settings.

.. _ingress default IP:

Default IP address
~~~~~~~~~~~~~~~~~~

.. include:: /_static/reuse/k8s-version-added-1_4.rst

You can set a default IP address for Ingress resources. To do so:

#. Add the ``--default-ingress-ip`` config parameter to the :ref:`k8s-bigip-ctlr Deployment <k8s-bigip-ctlr-deployment>`.
#. Add the annotation ``virtual-server.f5.com/ip="controller-default"`` to your Ingress resource.

The |kctlr| will replace "controller-default" with the IP address provided for the ``default-ingress-ip`` parameter.

.. important::

   You can only define ``--default-ingress-ip`` once for a single |kctlr| instance.

   If you're running multiple Controllers to monitor separate namespaces, you can define a default IP address for each Controller. This type of deployment allows you to isolate the VIPs in each namespace from each other.

DNS lookup
~~~~~~~~~~

The |kctlr| uses DNS lookup to resolve hostnames by default (as of v1.3.0). Provide the hostname in the ``virtual-server.f5.com/ip=`` annotation. The Controller will attempt to resolve the hostname and assign the resolved host's IP address to the Ingress' virtual server.

Unattached pools
~~~~~~~~~~~~~~~~

You can create :ref:`unattached pools <kctlr-pool-only>` for the Services defined in the Ingress resource. To do so, just omit the ``virtual-server.f5.com/ip=`` annotation from your Ingress resource.

You can then :ref:`use an IPAM system <kctlr-ipam>` to assign an IP address and attach a virtual server to the pools, or use another means to manually route traffic to the pools on the BIG-IP system.

Deployments using multiple Ingress Controllers
``````````````````````````````````````````````

.. note::

   In Kubernetes, the Ingress resource's :code:`ingress.class` property is unset by default. The |kctlr| automatically manages all Ingress resources that don't have an :code:`ingress.class`` defined.

If you're using more than one Ingress Controller to manage your Ingress resources:

- Set the :code:`ingress.class` property to "f5" for all Ingress resources you want the |kctlr| to manage. ::

   kubernetes.io/ingress.class="f5"

- Define the :code:`ingress.class` as appropriate for the Ingress resources managed by other Ingress Controllers. The |kctlr| ignores Ingress resources that have any :code:`ingress.class` other than "f5".


.. _ingress self IP:

Initial Setup
-------------

Allocate a `Self IP address`_ from the external network on the BIG-IP system. You'll assign this IP address to the Ingress resource's BIG-IP virtual server.

.. note::

   - If you intend to create :ref:`unattached pools <kctlr-pool-only>` (pools without a virtual server), you will need to set up another way to route traffic to the pools on the BIG-IP system.

   - If you have already assigned a :ref:`default IP address <ingress default IP>` to the Controller, you may skip this step.


.. _ingress-quick-start:

Set Virtual Server Ingress Annotations using kubectl
----------------------------------------------------

Add the `supported Ingress annotations`_ to any existing Ingress resource using :command:`kubectl annotate`. The examples below demonstrate correct usage on the command line.

- Assign an IP address to the Ingress: ::

   kubectl annotate ingress myIngress virtual-server.f5.com/ip="1.2.3.4"

- Use the default IP address assigned in the :ref:`k8s-bigip-ctlr Deployment <k8s-bigip-ctlr-deployment>`: ::

   kubectl annotate ingress myIngress virtual-server.f5.com/ip="controller-default"

- Set the desired port: ::

   kubectl annotate ingress myIngress virtual-server.f5.com/http-port="80"

- Set the BIG-IP partition: ::

   kubectl annotate ingress myIngress virtual-server.f5.com/partition="k8s"

- Set the load balancing method: ::

   kubectl annotate ingress myIngress virtual-server.f5.com/balance="round-robin"

- Define a BIG-IP health monitor: ::

   kubectl annotate ingress myIngress virtual-server.f5.com/health='[{"path": "svc1.example.com/app1", "send": "HTTP GET /health/svc1", "interval": 5, "timeout": 10}]'

- Redirect HTTP requests to HTTPS: ::

   kubectl annotate ingress myIngress ingress.kubernetes.io/ssl-redirect="true"

- Deny HTTP requests: ::

   kubectl annotate ingress myIngress ingress.kubernetes.io/allow-http="false"

- Assign the F5 Ingress class to avoid conflicts with other Ingress Controllers: ::

   kubectl annotate ingress myIngress kubernetes.io/ingress.class="f5"

.. _create k8s ingress:

Define Virtual Server Ingress Annotations in an Ingress Resource
----------------------------------------------------------------

When creating a new Ingress Resource, include the `supported Ingress annotations`_ as needed. The annotations must be valid JSON.

.. _add health monitor to ingress:

Add a BIG-IP Health Monitor to the virtual server for an Ingress
````````````````````````````````````````````````````````````````

Add the :code:`virtual-server.f5.com/health` annotation to your Ingress resource. The example below shows the correct usage.

.. literalinclude:: /kubernetes/config_examples/f5-k8s-ingress-health-monitor.yaml
   :caption: Health Monitor Example
   :linenos:
   :emphasize-lines: 9-22


.. _ingress-TLS:

Secure an Ingress using TLS
```````````````````````````

You can secure an Ingress using :ref:`Secrets <k8s-ingress-secrets>` or :ref:`BIG-IP SSL profiles <k8s-ingress-bigip-ssl>`.

#. Specify the SSL profile(s) or the Secret containing the cert and key in the :code:`spec.tls` section of the Ingress resource.
#. Add the :code:`ingress.kubernetes.io/ssl-redirect` annotation (**OPTIONAL**; defaults to :code:`"true"`).
#. Add the :code:`ingress.kubernetes.io/allow-http` annotation (**OPTIONAL**; defaults to :code:`"false"`).

.. note::

   - You can specify one or more SSL profiles in your Ingress resource.
   - If you specify a :code:`spec.tls` section without providing the TLS Ingress properties, the BIG-IP device uses its local traffic policies to redirect HTTP requests to HTTPS.

\

.. seealso::

   Refer to the `Kubernetes TLS Ingress documentation <https://kubernetes.io/docs/concepts/services-networking/ingress/#tls>`_ for details regarding supported port(s) and termination.


.. _k8s-ingress-bigip-ssl:

BIG-IP SSL profiles
~~~~~~~~~~~~~~~~~~~

.. literalinclude:: /kubernetes/config_examples/f5-k8s-ingress-tls.yaml
   :caption: TLS Example
   :linenos:

:fonticon:`fa fa-download` :download:`f5-k8s-ingress-tls.yaml </kubernetes/config_examples/f5-k8s-ingress-tls.yaml>`

.. _k8s-ingress-secrets:

Kubernetes Secrets
~~~~~~~~~~~~~~~~~~

.. literalinclude:: /kubernetes/config_examples/f5-k8s-ingress-tls-secret.yaml
      :caption: TLS Example
      :linenos:

:fonticon:`fa fa-download` :download:`f5-k8s-ingress-tls-secret.yaml </kubernetes/config_examples/f5-k8s-ingress-tls-secret.yaml>`


See Example Ingress Resources
`````````````````````````````

.. _single service:

Single Service
~~~~~~~~~~~~~~

A :dfn:`Single Service` Ingress creates a BIG-IP virtual server and server pool for a single Kubernetes Service.

.. literalinclude:: /kubernetes/config_examples/f5-k8s-single-ingress.yaml
   :linenos:

:fonticon:`fa fa-download` :download:`f5-k8s-single-ingress.yaml </kubernetes/config_examples/f5-k8s-single-ingress.yaml>`

.. _simple fanout:

Simple Fanout
~~~~~~~~~~~~~

A :dfn:`Simple Fanout` Ingress creates a BIG-IP virtual server and pools for a group of Kubernetes Services (one pool per Service).

.. literalinclude:: /kubernetes/config_examples/f5-k8s-ingress-fanout.yaml
   :linenos:

:fonticon:`fa fa-download` :download:`f5-k8s-ingress-fanout.yaml </kubernetes/config_examples/f5-k8s-ingress-fanout.yaml>`

.. _name-based virtual hosting:

Name-based virtual hosting
~~~~~~~~~~~~~~~~~~~~~~~~~~

A :dfn:`Name-based virtual hosting` ingress creates the following BIG-IP objects:

- One (1) virtual server with one (1) pool for each Service.
- Local traffic policies that route requests to specific pools based on host name and path.

.. tip::

   If you don't specify any hosts or paths, the BIG-IP device will proxy traffic for all hosts/paths for the Service specified in the :code:`backend` section of the virtual-server annotation.

\

.. literalinclude:: /kubernetes/config_examples/f5-k8s-ingress-virtual-hosting.yaml
   :linenos:
   :caption: Specific hosts

:fonticon:`fa fa-download` :download:`f5-k8s-ingress-virtual-hosting.yaml </kubernetes/config_examples/f5-k8s-ingress-virtual-hosting.yaml>`

.. literalinclude:: /kubernetes/config_examples/f5-k8s-ingress-virtual-hosting_all.yaml
   :linenos:
   :caption: All hosts

:fonticon:`fa fa-download` :download:`f5-k8s-ingress-virtual-hosting_all.yaml </kubernetes/config_examples/f5-k8s-ingress-virtual-hosting_all.yaml>`

.. _deploy ingress resource:

Upload the Ingress to the API server
------------------------------------

If you have created a new Ingress resource, use the :command:`create` command to upload it to the API server.

.. code-block:: console

   kubectl create ingress -f myIngress.yaml

You can apply updates to an existing Ingress resource using the :command:`apply` command.

.. code-block:: console

   kubectl apply -f myIngress.yaml


.. _verify-ingress-vs-created:

Verify object creation on the BIG-IP system
-------------------------------------------

You can use TMOS or the BIG-IP configuration utility to verify that the |kctlr| created the requested BIG-IP objects for your Ingress.

To verify using the BIG-IP configuration utility:

#. Log in to the configuration utility at the management IP address (for example, :code:`https://10.190.25.225/tmui/login.jsp?`).
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
