.. index::
   :pair: BIG-IP Controller, Kubernetes
   :pair: BIG-IP Controller, OpenShift
   :pair: BIG-IP Controller, setup
   :pair: BIG-IP Controller, mode
   :single: concept

Nodeport mode vs Cluster mode
=============================

If you're setting up a Kubernetes cluster and/or the |kctlr-long| for the first time, you may be asking yourself *"What is the pool-member-type setting and which mode should I choose?"*.
This document clarifies the available options and provides vital information to take into account when making this decision.

In brief: The :code:`pool-member-type` setting determines what mode the Controller runs in -- :code:`nodeport` or :code:`cluster`.

.. _nodeport mode:

Nodeport mode
-------------

:code:`Nodeport` mode is the default mode of operation for the |kctlr|.
From a configuration standpoint, it's easier to set up and more compatible with the `Kubernetes Cluster`_, as it doesn't require you to add your BIG-IP system to the Kubernetes `Cluster Network`_.

As shown in the diagram below, :code:`nodeport` mode uses 2-tier load balancing: the |kctlr| load balances requests to Nodes, which in turn load balance requests to Pods.

.. figure:: /_static/media/k8s_nodeport.png


**Important limitations to consider:**

- The `Kubernetes Services`_ you want to manage must use :code:`type: NodePort`.
- You can't use the full BIG-IP feature set (L7 services like persistence are not available).
- Introduces extra latency.
- BIG-IP system can't load balance directly to Pods.
- |kctlr| has limited visibility into Pod health.

If you want to use NodePort mode, continue on to :ref:`Install the BIG-IP Controller in Kubernetes <install-kctlr>`.

.. _cluster mode:

Cluster mode
------------

You should use :code:`Cluster` mode if you intend to integrate your BIG-IP device into the Kubernetes cluster network. [#clusternet]_
While there are additional networking configurations to make, there are distinct benefits:

- You can use any type you like for your Kubernetes Services.
- You get the full BIG-IP ADC functionality, including L7 persistence.
- BIG-IP system can load balance directly to any Pod in the Cluster.
- |kctlr| has full visibility into Pod health, via the Kubernetes API.


.. figure:: /_static/media/k8s_cluster.png

.. _k8s-cluster-networks:

If you want to run |kctlr| in cluster mode, continue on to :ref:`Network considerations`.
The following guides provide relevant information and instructions:

- The Kubernetes `Cluster Networking`_ Administration Guide -- provides information about Kubernetes Cluster Network types.
- The `BIG-IP TMOS: ​Tunneling and IPsec <https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/bigip-tmos-tunnels-ipsec-13-0-0/2.html>`_ Guide -- provides instructions for setting up tunnels on your BIG-IP device.

.. _network considerations:

Network considerations
``````````````````````

When thinking about how to integrate your BIG-IP device into the cluster network, you'll probably want to take into account what you have to do manually vs what the |kctlr| takes care of automatically.
In general, the manual operations required occur far less frequently than those that are automatic.
The list below shows common operations for a typical Kubernetes cluster, from most-frequent to least-frequent.

- Add or remove Pods from an existing Service, or expose a Service with Pods.
- Add or remove a Node from the Cluster.
- Create a new Kubernetes Cluster from scratch.

The |kctlr| **always manages BIG-IP system configurations for Pods automatically.**
For Nodes and Clusters, you may have to perform some actions manually (or automate them using a different system, like Ansible). [#ansible]_
Take these into consideration if you're deciding how to set up your cluster network, or deciding how to integrate the |kctlr| and a BIG-IP device into an existing cluster.

.. tip::

   BIG-IP platforms `support several overlay networks`_, like VXLAN, NVGRE, and IPIP.
   The manual steps noted in the table apply when integrating a BIG-IP device into any overlay network, not just the examples shown here.


.. table::

   +-----------------------+-----------------------------------------------------------------------------------------+-----------------------------------------------------+
   | Network Type          | Add Cluster                                                                             | Add Node(s)                                         |
   +=======================+====================================================================+====================+=====================================================+
   | **Layer 2 networks**                                                                                                                                                  |
   +-----------------------+-----------------------------------------------------------------------------------------+-----------------------------------------------------+
   | Openshift SDN         | :ref:`Add a new subnet to OpenShift <k8s-openshift-hostsubnet>` for the BIG-IP device.  | None. The |kctlr| automatically detects OpenShift   |
   |                       |                                                                                         | routes and makes the necessary BIG-IP system        |
   |                       | :ref:`Add a new VXLAN network to the BIG-IP system <k8s-openshift-vxlan-setup>`         | configurations.                                     |
   |                       | that corresponds to the subnet. [#encap]_                                               |                                                     |
   +-----------------------+-----------------------------------------------------------------------------------------+-----------------------------------------------------+
   | Flannel VXLAN         | Allocate an IP address from Flannel for the BIG-IP device.                              | `Add an FDB entry and ARP record`_ for each node.   |
   |                       |                                                                                         |                                                     |
   |                       | Add a VXLAN network to the BIG-IP system;                                               |                                                     |
   |                       | use the IP address allocated from Flannel as the VTEP.                                  |                                                     |
   +-----------------------+-----------------------------------------------------------------------------------------+-----------------------------------------------------+
   | **Layer 3 networks**                                                                                                                                                  |
   +-----------------------+-----------------------------------------------------------------------------------------+-----------------------------------------------------+
   | Calico                | Set up BGP peering between the BIG-IP device and Calico.                                | None. Managed by BGP.                               |
   |                       |                                                                                         |                                                     |
   |                       |                                                                                         | **NOTE:** Depending on the BGP configuration, you   |
   |                       |                                                                                         | may need to update the BGP neighbor table.          |
   +-----------------------+-----------------------------------------------------------------------------------------+-----------------------------------------------------+
   | Flannel host-gw       | Configure routes in Flannel and on the BIG-IP device for per-node                       | Add/update per-node subnet routes on the BIG-IP     |
   |                       | subnet(s).                                                                              | device.                                             |
   +-----------------------+-----------------------------------------------------------------------------------------+-----------------------------------------------------+


What's Next
-----------

- :ref:`Install the BIG-IP Controller in standard Kubernetes <install-kctlr>`
- :ref:`Add your BIG-IP device to an OpenShift Cluster <bigip-openshift-setup>`
- :ref:`Install the BIG-IP Controller in OpenShift <install-kctlr-openshift>`
- `Configuration options for the BIG-IP Controller </products/connectors/k8s-bigip-ctlr/latest/#controller-configuration-parameters>`_

.. rubric:: Footnotes
.. [#servicetype] See `Publishing Services - Service Types <https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services---service-types>`_ in the Kubernetes documentation.
.. [#originsdn] See the `OpenShift Origin SDN`_ documentation for more information.
.. [#ansible] See the `f5-ansible repo on GitHub <https://github.com/F5Networks/f5-ansible>`_ for Ansible modules that can manipulate F5 products.
.. [#encap] Be sure to use the correct encapsulation format for your network.

.. _Cluster Networking: https://kubernetes.io/docs/concepts/cluster-administration/networking/
.. _OpenShift Origin SDN: https://docs.openshift.org/latest/architecture/additional_concepts/sdn.html
.. _Flannel: https://docs.openshift.org/latest/architecture/additional_concepts/flannel.html
.. _Open vSwitch VXLAN network: https://kubernetes.io/docs/admin/ovs-networking/
.. _Calico for Kubernetes: https://docs.projectcalico.org/latest/getting-started/kubernetes/
.. _Calico BGP: https://docs.projectcalico.org/v2.4/usage/configuration/bgp
.. _Create a network virtualization tunnel: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/bigip-tmos-tunnels-ipsec-13-0-0/2.html
.. _BIG-IP TMOS Routing Administration: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/tmos-routing-administration-13-0-0.html
.. _support several overlay networks: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/bigip-tmos-tunnels-ipsec-13-0-0/1.html
.. _Add an FDB entry and ARP record: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/tmos-routing-administration-13-0-0/11.html

.. [#clusternet] OpenShift users must run the |kctlr| in cluster mode.