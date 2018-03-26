.. _k8s-ingress-controller:

Using the BIG-IP Controller as an Ingress Controller
====================================================

This document provides an overview of what the |kctlr-long| can do when used as an Ingress Controller in Kubernetes.
See :ref:`kctlr-ingress-config` for step-by-step instructions.

Overview
--------

You can use the |kctlr| as an `Ingress Controller`_ in Kubernetes. The Controller creates one virtual server for each unique IP address listed in the Ingress resource(s).

For Ingress resources that share IP addresses -- like those that use the :ref:`default IP address <ingress default IP>` -- the |kctlr| creates one pool for each Ingress resource on the shared virtual server.

The |kctlr| supports the following Kubernetes `Ingress resource`_ types:

- :ref:`single service`,
- :ref:`simple fanout`,
- :ref:`name-based virtual hosting`, and
- :ref:`TLS <ingress-TLS>`.


Deployments using multiple Ingress Controllers
----------------------------------------------

.. important::

   In Kubernetes, the Ingress resource's :code:`ingress.class` property is empty by default.
   The |kctlr| **automatically manages all Ingress resources that don't have an** :code:`ingress.class` **defined**.

If you're using more than one Ingress Controller to manage your Ingress resources:

- Set the :code:`ingress.class` property to "f5" for all Ingress resources you want the |kctlr| to manage. ::

   kubernetes.io/ingress.class="f5"

- Define the :code:`ingress.class` as appropriate for the Ingress resources managed by other Ingress Controllers. The |kctlr| ignores Ingress resources that have any :code:`ingress.class` other than "f5".

IP address assignment
`````````````````````

The |kctlr| supports the following options for IP address assignment. See the `k8s-bigip-ctlr configuration parameters`_ table for more information about these settings.

.. _ingress default IP:

Default IP address
~~~~~~~~~~~~~~~~~~

.. include:: /_static/reuse/k8s-version-added-1_4.rst

You can set a default IP address for Ingress resources. To do so:

#. Add the :code:`default-ingress-ip` config parameter to the :ref:`k8s-bigip-ctlr Deployment <k8s-bigip-ctlr-deployment>`.
#. Add the annotation :code:`virtual-server.f5.com/ip="controller-default"` to your Ingress resource.

The |kctlr| replaces "controller-default" with the IP address provided as the :code:`default-ingress-ip`.

Each Ingress resource set to use the "controller-default" IP shares the same BIG-IP virtual server. The |kctlr| attaches a unique local traffic policy to the virtual server for each Ingress resource to ensure correct traffic routing.

.. important::

   You can only define one :code:`default-ingress-ip` per |kctlr| instance.

If you're using multiple Controllers to monitor separate namespaces, you can define a default IP address for each Controller. This type of deployment allows you to isolate the VIPs in each namespace from each other.

.. _dns lookup ingress:

DNS lookup
~~~~~~~~~~

The |kctlr| uses DNS lookup to resolve hostnames by default (as of v1.3.0). The |kctlr| attempts to resolve the first hostname provided in the :code:`spec.rules.host` section of the Ingress resource. It then assigns the resolved host's IP address to the Ingress' virtual server.

IPAM/Unattached pools
~~~~~~~~~~~~~~~~~~~~~

You can create :ref:`unattached pools <kctlr-pool-only>` for the Services defined in the Ingress resource. To do so, just omit the ``virtual-server.f5.com/ip=`` annotation from your Ingress resource.

You can then :ref:`use an IPAM system <kctlr-ipam>` to assign an IP address and attach a virtual server to the pools, or use another means to manually route traffic to the pools on the BIG-IP system.