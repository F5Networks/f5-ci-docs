:product: BIG-IP Controller for Kubernetes
:type: tutorial

.. _kctlr-ingress-config:

Attach a Virtual Server to a Kubernetes Ingress
===============================================

.. include:: /_static/reuse/k8s-version-added-1_1.rst

Overview
--------

You can use the |kctlr-long| as an `Ingress Controller`_ in Kubernetes. To do so, add the |kctlr| `Ingress annotations`_ to a Kubernetes Ingress Resource. The annotations define the objects you want to create on the BIG-IP system.

If you use `helm`_ you can use the `f5-bigip-ingress chart`_ to create and manage the resources below. You may also use the `f5-bigip-ctlr chart`_ to create and manage the resources for the |kctlr| itself, though the charts are independent and may be used separately.

.. note::

   This document provides set-up instructions for using the |kctlr| as a Kubernetes Ingress Controller. For a functionality overview, see :ref:`k8s-ingress-controller`.

.. table:: Task summary

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

.. _initial-setup-kctlr-ingress:

Initial Setup
-------------

**Skip this step if:**

- You have already assigned a :ref:`default IP address <ingress default IP>` to the Controller **--OR--**
- You are using :ref:`DNS lookup <dns lookup ingress>` to resolve host IP addresses.

.. _ingress self IP:

Allocate a `Self IP address`_ from the external network on the BIG-IP system. You will assign this IP address to the Ingress resource.
If you're running the |kctlr| in :ref:`cluster mode <cluster mode>`, the IP address must be within the :ref:`subnet assigned to the BIG-IP VXLAN tunnel <k8s-vxlan-setup>`.

.. note::

   If you intend to create :ref:`unattached pools <kctlr-pool-only>` (pools that aren't attached to a virtual server), you will need to set up another way to route traffic to the pools on the BIG-IP system *before* proceeding with the steps below.

.. _ingress-quick-start:
.. _ingress annotate kubectl:

Annotate Ingress Resources using kubectl
----------------------------------------

Use :command:`kubectl annotate` to add the supported `Ingress annotations`_ to any existing Ingress resource.
It's good practice to include all of your key-value pairs in a single :command:`kubectl annotate` command, to avoid piecemeal updates to the BIG-IP system.

The example below creates a virtual server on the BIG-IP with the following settings:

- set the Ingress class to "f5" to avoid conflicts with other Ingress Controllers;
- use the default IP address assigned in the :ref:`k8s-bigip-ctlr Deployment <k8s-bigip-ctlr-deployment>`;
- listen on port 443;
- create the virtual server in the "k8s" partition;
- use the BIG-IP "round-robin" load balancing algorithm;
- create a BIG-IP health monitor;
- redirect HTTP requests to HTTPS; and
- deny HTTP requests.

.. code-block:: console

   kubectl annotate ingress myIngress kubernetes.io/ingress.class="f5" \
                                      myIngress virtual-server.f5.com/ip="controller-default" \
                                      virtual-server.f5.com/http-port="443" \
                                      virtual-server.f5.com/partition="k8s" \
                                      virtual-server.f5.com/balance="round-robin" \
                                      virtual-server.f5.com/health='[{"path": "svc1.example.com/app1", "send": "HTTP GET /health/svc1", "interval": 5, "timeout": 10}]' \
                                      ingress.kubernetes.io/ssl-redirect="true" \
                                      ingress.kubernetes.io/allow-http="false"

.. _create k8s ingress:

Define Virtual Server Ingress Annotations in an Ingress Resource
----------------------------------------------------------------

You can also define the virtual server settings when creating a new Ingress resource.
Define the desired `Ingress annotations`_ using valid JSON.

.. _add health monitor to ingress:

Health Monitors
```````````````

Use the :code:`virtual-server.f5.com/health` annotation to add (or update) health monitors to the virtual server for a Kubernetes Ingress resource. You can include it in the resource definition, as shown below, or use the command line (shown in the previous example).

.. literalinclude:: /kubernetes/config_examples/f5-k8s-ingress-health-monitor.yaml
   :caption: Health Monitor Example
   :lines: 1-6, 10-41
   :emphasize-lines: 9-22

.. _ingress-TLS:

Use a BIG-IP SSL profile or Secret
``````````````````````````````````

You can secure an Ingress using :ref:`BIG-IP SSL profiles <k8s-ingress-bigip-ssl>` or Kubernetes :ref:`Secrets <k8s-ingress-secrets>`.

#. Specify the SSL profile(s) or the Secret containing the cert and key in the :code:`spec.tls` section of the Ingress resource.
#. Add the :code:`ingress.kubernetes.io/ssl-redirect` annotation (**OPTIONAL**; defaults to :code:`"true"`).
#. Add the :code:`ingress.kubernetes.io/allow-http` annotation (**OPTIONAL**; defaults to :code:`"false"`).

.. note::

   - You can specify one or more SSL profiles in your Ingress resource.
   - If you specify a :code:`spec.tls` section without providing the TLS Ingress properties, the BIG-IP device uses its local traffic policies to redirect HTTP requests to HTTPS.

The table below shows how the Controller behaves for different combinations of the :code:`ingress.kubernetes.io/ssl-redirect` and :code:`ingress.kubernetes.io/allow-http` settings.

+-------+-------------+-----------+-----------------------------+
| State | sslRedirect | allowHttp | Description                 |
+=======+=============+===========+=============================+
|   1   |     F       |    F      | Just HTTPS, nothing on HTTP |
+-------+-------------+-----------+-----------------------------+
|   2   |     T       |    F      | HTTP redirects to HTTPS     |
+-------+-------------+-----------+-----------------------------+
|   2   |     T       |    T      | Honor sslRedirect == true   |
+-------+-------------+-----------+-----------------------------+
|   3   |     F       |    T      | Both HTTP and HTTPS         |
+-------+-------------+-----------+-----------------------------+


.. _k8s-ingress-bigip-ssl:

.. literalinclude:: /kubernetes/config_examples/f5-k8s-ingress-tls.yaml
   :caption: TLS Ingress example using a BIG-IP SSL profile

:fonticon:`fa fa-download` :download:`f5-k8s-ingress-tls.yaml </kubernetes/config_examples/f5-k8s-ingress-tls.yaml>`

.. _k8s-ingress-secrets:

.. literalinclude:: /kubernetes/config_examples/f5-k8s-ingress-tls-secret.yaml
   :caption: TLS Ingress example using a Secret

:fonticon:`fa fa-download` :download:`f5-k8s-ingress-tls-secret.yaml </kubernetes/config_examples/f5-k8s-ingress-tls-secret.yaml>`

.. seealso::

   Refer to the `Kubernetes TLS Ingress documentation <https://kubernetes.io/docs/concepts/services-networking/ingress/#tls>`_ for details regarding supported port(s) and termination.

.. _deploy ingress resource:

Upload the Ingress to the API server
````````````````````````````````````

Use the :command:`kubectl apply` command to upload your new or edited Ingress resource to the Kubernetes API server.

.. include:: /_static/reuse/kubectl-apply.rst

.. _verify-ingress-vs-created:

Verify object creation on the BIG-IP system
-------------------------------------------

.. include:: /_static/reuse/verify-bigip-objects.rst

.. _delete vs ingress:

Delete the virtual server
-------------------------

If you want to remove the virtual server associated with an Ingress from the BIG-IP system, but **keep the Ingress**:

#. Remove the |kctlr| Annotations from the Ingress definition.
#. Update the Kubernetes API server.

   .. include:: /_static/reuse/kubectl-apply.rst

.. seealso:: See :ref:`kctlr-manage-bigip-objects` for more information.

Example Ingress Resources
-------------------------

.. _single service:

Single Service
``````````````

A :dfn:`Single Service` Ingress creates a BIG-IP virtual server and server pool for a single Kubernetes Service.

.. literalinclude:: /kubernetes/config_examples/f5-k8s-single-ingress.yaml

:fonticon:`fa fa-download` :download:`f5-k8s-single-ingress.yaml </kubernetes/config_examples/f5-k8s-single-ingress.yaml>`

.. _simple fanout:

Simple Fanout
`````````````

A :dfn:`Simple Fanout` Ingress creates a BIG-IP virtual server and pools for a group of Kubernetes Services (one pool per Service).

.. literalinclude:: /kubernetes/config_examples/f5-k8s-ingress-fanout.yaml

:fonticon:`fa fa-download` :download:`f5-k8s-ingress-fanout.yaml </kubernetes/config_examples/f5-k8s-ingress-fanout.yaml>`

.. _name-based virtual hosting:

Name-based virtual hosting
``````````````````````````

A :dfn:`Name-based virtual hosting` ingress creates the following BIG-IP objects:

- One virtual server
- One pool per Service
- `Local traffic policies`_ to route requests to specific pools based on host name and path.

.. tip::

   If you don't specify any hosts or paths for the Service named in the :code:`backend` section of the Ingress resource, the BIG-IP device will proxy traffic for all hosts/paths.

.. literalinclude:: /kubernetes/config_examples/f5-k8s-ingress-virtual-hosting.yaml
   :caption: Specific hosts

:fonticon:`fa fa-download` :download:`f5-k8s-ingress-virtual-hosting.yaml </kubernetes/config_examples/f5-k8s-ingress-virtual-hosting.yaml>`

.. literalinclude:: /kubernetes/config_examples/f5-k8s-ingress-virtual-hosting_all.yaml
   :caption: All hosts

:fonticon:`fa fa-download` :download:`f5-k8s-ingress-virtual-hosting_all.yaml </kubernetes/config_examples/f5-k8s-ingress-virtual-hosting_all.yaml>`



.. _TMSH Reference Guide: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/bigip-tmsh-reference-12-0-0.html
.. _BIG-IP server pool: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/ltm-basics-13-0-0/4.html
.. _Host header: https://tools.ietf.org/html/rfc7230#section-5.4
.. _Kubernetes documentation: https://kubernetes.io/docs/concepts/services-networking/ingress/#name-based-virtual-hosting
.. _TLS ingress: https://kubernetes.io/docs/concepts/services-networking/ingress/#tls
