:product: BIG-IP Controller for Kubernetes
:type: concept

.. _flannel-bigip-info:

BIG-IP and flannel VXLAN Integration
====================================

This document provides a general overview of the BIG-IP device integration with flannel VXLAN in Kubernetes. For set-up instructions, see :ref:`use-bigip-k8s-flannel`.

Overview of Cluster Networking with flannel in Kubernetes
---------------------------------------------------------

.. sidebar:: :fonticon:`fa fa-info-circle` Related:

   Read about the Kubernetes `Cluster Network`_ and `Using flannel with Kubernetes`_.

`Flannel`_ is a layer 3 network fabric (or, in their words, "a virtual network that attaches IP addresses to containers"). In Kubernetes, the flannel runs as a Pod on each Node in the Cluster. The Pod contains the flannel daemon -- :code:`flanneld` -- that provides network information to Nodes and reads information about Nodes from the Kubernetes API server.

Flannel assigns a subnet to each Kubernetes Node. It allocates an IP address within that subnet to each Pod running on the Node. Because the flannel daemon (:code:`flanneld`) runs on every Node, all of the Pods across the Cluster can talk to each other directly.

.. note::

   In older versions of Kubernetes (pre-1.6), flannel used an ``etcd`` key-value store to read and write information about Kubernetes Nodes. Though ``etcd`` is still viable in later versions, it's not commonly used.

.. _k8s-to-bigip:

BIG-IP Devices and the Kubernetes Cluster Network
-------------------------------------------------

.. sidebar:: :fonticon:`fa fa-exclamation-circle` Important:

   See :ref:`use-bigip-k8s-flannel` for step-by-step set-up instructions.

As discussed in :ref:`kctlr modes`, when a BIG-IP device is part of the Kubernetes Cluster Network, it can load balance directly to any Pod in the Cluster. This is the case because, via flannel and the |kctlr|, the BIG-IP can find each Pod's :code:`public-IP` address. Read on for an overview of how this works.

The BIG-IP device connects to the flannel network via a VXLAN tunnel. The |kctlr| populates this tunnel with the following information about the flannel network:

- forwarding database (FDB) records that map the MAC address of each Kubernetes Node's flannel VXLAN interface to the Node IP address;
- static ARP entries that map the flannel VXLAN interface's MAC address to the Pod's flannel :code:`public-IP`.

The |kctlr| also assigns each Pod's flannel :code:`public-ip` address to a node on the BIG-IP.

.. rubric:: **Example:**

Node1 has the NodeIP address, MAC address, and Pod :code:`public-ip` address shown in the table below.

+-------------------------------------------------------------------+
| Kubernetes Node1                                                  |
+===============================================+===================+
| Node IP address                               | 172.16.2.10       |
+-----------------------------------------------+-------------------+
| MAC address of Node's flannel VXLAN interface | 98:ba:76:dc:54:fe |
+-----------------------------------------------+-------------------+
| Pod public-ip address assigned by flannel     | 10.244.1.2        |
+-----------------------------------------------+-------------------+

The |kctlr| uses this information to create an FDB record for the Node on the BIG-IP system: ::

   flannel_vxlan {
    records [
       98:ba:76:dc:54:fe {
         endpoint: 172.16.2.10
       }
    ]
   }

The |kctlr| also creates a static ARP entry for the Node: ::

   {
      name: k8s-10.244.1.2
      ipaddress: 10.244.1.2
      macaddress: 98:ba:76:dc:54:fe
   }

Together, these records tell the BIG-IP device that a Pod on Node1 should receive traffic from the BIG-IP node with the IP address "10.244.1.2".

BIG-IP SNAT Pools and SNAT automap
``````````````````````````````````

.. include:: /_static/reuse/k8s-version-added-1_5.rst

You can set the |kctlr| to create virtual servers from SNAT pools or to use `BIG-IP SNAT`_ automap. Prior to v1.5.0, the |kctlr| used BIG-IP SNAT automap automatically for all virtual servers. From v1.5.0 forward, use of SNAT automap is the default behavior.

When you use SNAT automap, the self IP address that serves as the VTEP for the VXLAN tunnel also functions as a SNAT pool. The subnet mask you provide when creating the self IP will define the addresses available in the SNAT pool. The self IP subnet mask must match the flannel podCIDR.

See :ref:`bigip snats` for more information.

How flannel knows about the BIG-IP device
-----------------------------------------

At this point, your BIG-IP device knows how to route to the Kubernetes network, but flannel doesn't know about the BIG-IP device. Flannel's :code:`kube-subnet-manager` uses the Kubernetes API to discover information about Kubernetes Nodes. This means that, to add the BIG-IP device to the flannel network, we need to add the BIG-IP device as a Node in Kubernetes.

When you add a new Node to Kubernetes to represent the BIG-IP device, :ref:`add the flannel Annotations <add flannel annotations>` and podCIDR to the Node resource. Once the Node is up and running, flannel will discover its Annotations and add the BIG-IP device to the VXLAN.
 
With all of these pieces in place, you can successfully send traffic from (or through) a BIG-IP virtual server to a specific Kubernetes Pod!

What's Next
-----------

- :ref:`Add your BIG-IP device to the Kubernetes Cluster <use-bigip-k8s-flannel>`.
- :ref:`Install the F5 BIG-IP Controller in Kubernetes <install-kctlr>`

