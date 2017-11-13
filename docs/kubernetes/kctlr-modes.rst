.. index::
   single: BIG-IP Controller; Kubernetes
   single: BIG-IP Controller; OpenShift
   single: BIG-IP Controller; setup
   single: BIG-IP Controller; mode

.. _kctlr modes:

Nodeport mode vs Cluster mode
=============================

If you're setting up a Kubernetes or OpenShift cluster with the |kctlr| for the first time, you may be asking yourself,

*"What is the pool-member-type setting and which mode should I choose?"*.

This document clarifies the available options and provides vital information to take into account when making this decision.

In brief: The :code:`pool-member-type` setting determines what mode the Controller runs in -- :code:`nodeport` or :code:`cluster`.

.. _nodeport mode:

Nodeport mode
-------------

Nodeport mode is the default mode of operation for the |kctlr| in Kubernetes.
From a configuration standpoint, it's easier to set up since it doesn't matter what Kubernetes `Cluster Network`_ you use.
In addition, NodePort mode doesn't have any specific BIG-IP licensing requirements.

As shown in the diagram below, :code:`nodeport` mode uses 2-tier load balancing:

#. The |kctlr| load balances requests to Nodes.
#. Nodes load balance requests to Pods.

.. figure:: /_static/media/k8s_nodeport.png


**Important limitations to consider:**

- The Kubernetes Services you want to manage must use :code:`type: NodePort`. [#servicetype]_
- The BIG-IP system can't load balance directly to Pods, which means:

  - some BIG-IP services, like L7 persistence, won't behave as expected;
  - there's extra latency; and
  - |kctlr| has limited visibility into Pod health.

If you want to use NodePort mode, continue on to :ref:`Install the BIG-IP Controller in Kubernetes <install-kctlr>`.

.. _cluster mode:

Cluster mode
------------

You should use :code:`cluster` mode if you intend to integrate your BIG-IP device into the Kubernetes cluster network.

.. important::

   OpenShift users must run the |kctlr| in cluster mode.

Cluster mode requires a `Better or Best license`_ that includes SDN services and advanced routing.
While there are additional networking configurations to make, cluster mode has distinct benefits over nodeport mode:

- You can use any type you like for your Kubernetes Services.
- BIG-IP system can load balance directly to any Pod in the Cluster, which means:

  - BIG-IP services - including L7 persistence - function as expected, and
  - the |kctlr| has full visibility into Pod health via the Kubernetes API.

.. figure:: /_static/media/k8s_cluster.png

.. _k8s-cluster-networks:

If you want to run |kctlr| in cluster mode, continue on to :ref:`Network considerations`.

.. seealso::

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

.. important::

   BIG-IP platforms `support several overlay networks`_, like VXLAN, NVGRE, and IPIP.
   The manual steps noted in the table apply when integrating a BIG-IP device into any overlay network, not just the examples shown here.

   **The examples below are for instructional purposes only.**


.. table::

   +-----------------------+-----------------------------------------------------------------------------------------+-----------------------------------------------------+
   | Network Type          | Add Cluster                                                                             | Add Node(s)                                         |
   +=======================+====================================================================+====================+=====================================================+
   | **Layer 2 networks**                                                                                                                                                  |
   +-----------------------+-----------------------------------------------------------------------------------------+-----------------------------------------------------+
   | Openshift SDN         | :ref:`Create a new OpenShift HostSubnet <k8s-openshift-hostsubnet>` for the BIG-IP      | None. The |kctlr| automatically detects OpenShift   |
   |                       | self IP.                                                                                | routes and makes the necessary BIG-IP system        |
   |                       |                                                                                         | configurations.                                     |
   |                       | :ref:`Add a new VXLAN network to the BIG-IP system <k8s-openshift-vxlan-setup>`         |                                                     |
   |                       | that corresponds to the subnet. [#encap]_                                               |                                                     |
   +-----------------------+-----------------------------------------------------------------------------------------+-----------------------------------------------------+
   | flannel VXLAN         | :ref:`Create a VXLAN tunnel on the BIG-IP system <k8s-vxlan-setup>`.                    | None. The |kctlr| automatically detects Kubernetes  |
   |                       |                                                                                         | Nodes and makes the necessary BIG-IP system         |
   |                       | :ref:`Create a fake BIG-IP Node in Kubernetes <k8s-bigip-node>`.                        | configurations.                                     |
   |                       |                                                                                         |                                                     |
   |                       | :ref:`Add the BIG-IP to the flannel overlay network <k8s-assign-ip>`.                   |                                                     |
   +-----------------------+-----------------------------------------------------------------------------------------+-----------------------------------------------------+
   | **Layer 3 networks**                                                                                                                                                  |
   +-----------------------+-----------------------------------------------------------------------------------------+-----------------------------------------------------+
   | Calico                | Set up BGP peering between the BIG-IP device and Calico.                                | None. Managed by BGP.                               |
   |                       |                                                                                         |                                                     |
   |                       |                                                                                         | **NOTE:** Depending on the BGP configuration, you   |
   |                       |                                                                                         | may need to update the BGP neighbor table.          |
   +-----------------------+-----------------------------------------------------------------------------------------+-----------------------------------------------------+
   | flannel host-gw       | Configure routes in flannel and on the BIG-IP device for per-node                       | Add/update per-node subnet routes on the BIG-IP     |
   |                       | subnet(s).                                                                              | device.                                             |
   +-----------------------+-----------------------------------------------------------------------------------------+-----------------------------------------------------+


What's Next
-----------

Review the `k8s-bigip-ctlr configuration parameters`_.

Kubernetes
``````````

- :ref:`bigip-k8s-setup`
- :ref:`Install the BIG-IP Controller in standard Kubernetes <install-kctlr>`

OpenShift
`````````

- :ref:`Add your BIG-IP device to an OpenShift Cluster <bigip-openshift-setup>`
- :ref:`Install the BIG-IP Controller in OpenShift <install-kctlr-openshift>`


.. rubric:: Footnotes
.. [#servicetype] See `Publishing Services - Service Types <https://kubernetes.io/docs/concepts/services-networking/service>`_ in the Kubernetes documentation.
.. [#ansible] See the `f5-ansible repo on GitHub <https://github.com/F5Networks/f5-ansible>`_ for Ansible modules that can manipulate F5 products.
.. [#encap] Be sure to use the correct encapsulation format for your network.

.. _Cluster Networking: https://kubernetes.io/docs/concepts/cluster-administration/networking/
.. _OpenShift Origin SDN: https://docs.openshift.org/latest/architecture/additional_concepts/sdn.html
.. _Open vSwitch VXLAN network: https://kubernetes.io/docs/admin/ovs-networking/
.. _Calico for Kubernetes: https://docs.projectcalico.org/latest/getting-started/kubernetes/
.. _Calico BGP: https://docs.projectcalico.org/v2.4/usage/configuration/bgp
.. _Create a network virtualization tunnel: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/bigip-tmos-tunnels-ipsec-13-0-0/2.html
.. _BIG-IP TMOS Routing Administration: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/tmos-routing-administration-13-0-0.html
.. _support several overlay networks: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/bigip-tmos-tunnels-ipsec-13-0-0/1.html
.. _Add an FDB entry and ARP record: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/tmos-routing-administration-13-0-0/11.html
