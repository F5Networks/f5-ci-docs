:product: BIG-IP Controller for Kubernetes
:type: concept

.. _k8s-ingress-controller:

Use the BIG-IP Controller as a Kubernetes Ingress Controller
============================================================

This document provides an overview of how you can use the |kctlr-long| as an `Ingress Controller`_ in Kubernetes.
For set-up instructions, see :ref:`kctlr-ingress-config`.

Overview
--------

You can use the |kctlr| as a Kubernetes `Ingress Controller`_. The |kctlr| supports the following Kubernetes `Ingress resource`_ types:

- :ref:`single service`
- :ref:`simple fanout`
- :ref:`name-based virtual hosting`
- :ref:`TLS <ingress-TLS>`

.. _k8s-multiple-ingress-controllers:

Using Multiple Ingress Controllers
``````````````````````````````````

.. important::

   The |kctlr| automatically manages all Ingress resources that don't have an :code:`ingress.class` defined.

Because the Ingress resource's :code:`ingress.class` property is empty by default, the |kctlr| will automatically try to manage all Ingress resources residing in the namespace(s) it watches. The |kctlr| ignores Ingress resources that have any :code:`ingress.class` other than "f5".

If you're using another Ingress Controller to manage Kubernetes Ingress resources:

#. Set :code:`ingress.class` to "f5" in all Ingress resources you want the |kctlr| to manage.

   :code:`kubernetes.io/ingress.class="f5"`

#. Define the :code:`ingress.class` as appropriate in Ingress resources managed by other Ingress Controllers.

.. _k8s-ip-addresses:

IP address assignment
---------------------

The Controller creates one virtual server for each unique IP address listed in an Ingress resource. You can manage IP address assignment using the options below.

See the `k8s-bigip-ctlr configuration parameters`_ table for more information about the required settings.

Use BIG-IP SNAT Pools and SNAT automap
``````````````````````````````````````

.. include:: /_static/reuse/k8s-version-added-1_5.rst

.. include:: /_static/reuse/kctlr-snat-note.rst

See :ref:`bigip snats` for more information.

.. _ingress default IP:

Set a Default, Shared IP address
````````````````````````````````

.. include:: /_static/reuse/k8s-version-added-1_4.rst

When you set the |kctlr| to use a default IP address, you can share that IP address across Ingress resources. When you share the default IP address across Ingress resources, the |kctlr|

- creates a shared virtual server with one pool for each Ingress resource, and
- attaches a unique local traffic policy for each Ingress resource to the virtual server to ensure correct traffic routing.

.. important::

   You can only define one :code:`default-ingress-ip` per |kctlr| instance.

   If you're using multiple Controllers to monitor separate namespaces, you can define a default IP address for each Controller. This type of deployment allows you to isolate the VIPs in each namespace from each other.

To share the default IP address across Ingress resources:

#. Define the :code:`default-ingress-ip` setting in your :ref:`k8s-bigip-ctlr Deployment <k8s-bigip-ctlr-deployment>` using the desired IP address.
#. Add the :code:`virtual-server.f5.com/ip="controller-default"` annotation to each Ingress resource for which you want to share the IP address.

When the |kctlr| creates the virtual server on the BIG-IP system, it replaces "controller-default" with the default IP address.

.. warning::

   Use caution when setting the :code:`--default-ingress-ip` and :ref:`specifying a BIG-IP SNAT pool <kctlr snat deploy>`.

   If you choose to set both options, make sure the IP address defined for the virtual server falls within the range of the selected SNAT pool.

.. _dns lookup ingress:

Use DNS lookup
``````````````

.. include:: /_static/reuse/k8s-version-added-1_3.rst

The |kctlr| uses DNS lookup to resolve hostnames by default. The |kctlr| attempts to resolve the first hostname provided in the :code:`spec.rules.host` section of the Ingress resource. It then assigns the resolved host's IP address to the Ingress' virtual server.

.. _kctlr-assign-ip-ipam:

Use an IPAM system
``````````````````

.. include:: /_static/reuse/k8s-version-added-1_1.rst

If you want to assign IP addresses using an IPAM system, use the |kctlr| to :ref:`create unattached pools <kctlr-pool-only>`. To do so, just omit the :code:`virtual-server.f5.com/ip=` annotation from your Ingress resource.

You can then add the virtual-server annotation to the Ingress using the IP address selected by the IPAM system. The |kctlr| will create a new virtual server with the selected IP address and attach the previously-created pool(s) to it.

The `F5 IPAM Controller`_ can write the :code:`virtual-server.f5.com/ip` annotation for you. See the `f5-ipam-ctlr docs`_ for more information.

.. _k8s ingress-ctlr url rewrite:

URL Rewrite
-----------

.. include:: /_static/reuse/k8s-version-added-1_5.rst

The |kctlr| has Annotations that provide `Rewrite`_ functionality for Ingress resources. See :ref:`k8s url rewrite` for more information.

What's Next
-----------

- :ref:`kctlr-ingress-config`
- :ref:`kctlr-manage-bigip-objects`
- :ref:`kctlr-per-svc-vs` for L4 ingress and L7 ingress on non-standard ports


.. _Rewrite: https://github.com/kubernetes/ingress-nginx/blob/master/docs/user-guide/annotations.md#rewrite
