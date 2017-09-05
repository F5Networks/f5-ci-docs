.. index::
   :pair: Kubernetes, BIG-IP
   :single: concept
   :triple: Kubernetes, networking, BIG-IP

.. _k8s-bigip-networks:

The F5 Integration and Kubernetes cluster networks
==================================================

There are a number of options when it comes to connecting a BIG-IP device (platform or Virtual Edition) to a Kubernetes cluster network.
When choosing how to integrate a BIG-IP device into your cluster network, bear in mind that it impacts:

- how you'll expose Services to internal traffic;
- what BIG-IP system features you can use;
- how the |kctlr| handles network configurations on the BIG-IP system.

The |kctlr| supports the :ref:`clusterIP` and :ref:`nodeport` Service types.
It handles network setup differently depending on the selected type.

.. important::

   F5 recommends using the default ``clusterIP`` Service type, as it enables the greater set of BIG-IP ADC services.

.. _clusterIP:

ClusterIP
---------

The ``clusterIP`` type exposes Services to internal traffic via IP addresses allocated from the underlying L2/L3 cluster network.
The BIG-IP device can find any pod in the cluster via its assigned ``InternalIP`` address.
The |kctlr| and BIG-IP can monitor node health and log statistics for individual pods.

.. figure:: /_static/media/k8s_cluster_l2-l3.png
   :scale: 60%

\

For Services with type ``clusterIP``, the |kctlr| manages some networking tasks on the BIG-IP device automatically.
You'll have to manage other tasks either manually or with another automated system.
For example, if you provision and configure new nodes using Ansible, it makes sense to automate the BIG-IP system configurations with Ansible as well. [#ansible]_

In general, the manual operations required occur far less frequently than those the |kctlr| manages automatically.
The list below shows common operations for a typical Kubernetes cluster, from most-frequent to least-frequent.

- Add or remove Pods from an existing Service, or exposing a Service with Pods.
- Add capacity to your Kubernetes cluster by adding new Nodes, or remove a Node.
- Create a new Kubernetes cluster from scratch.

The |kctlr| **manages BIG-IP system configurations for Pods automatically.**
The manual system configurations shown in the table below may be required when creating/removing nodes and clusters, depending on your cluster network type.
Take these requirements into consideration if you're deciding how to set up your cluster network, or deciding how to integrate the |kctlr| and BIG-IP device into an existing cluster.

.. tip::

   BIG-IP platforms support several overlay networks, like VXLAN and NVGRE.
   The manual steps noted in the table apply when integrating the BIG-IP device into any overlay network.


.. table::

   +-----------------------+--------------------------------------------------------------------+--------------------------------------------------------------------------+
   | Network Type          | Add Cluster                                                        | Add Node(s)                                                              |
   +=======================+====================================================================+==========================================================================+
   | Layer 2 networks                                                                                                                                                      |
   +-----------------------+--------------------------------------------------------------------+--------------------------------------------------------------------------+
   | Openshift SDN         | Add a new subnet to OpenShift for the BIG-IP device.               | None. The |kctlr| automatically detects OpenShift routes and makes the   |
   |                       |                                                                    | necessary BIG-IP system configurations.                                  |
   |                       | Add a new VXLAN network to the BIG-IP system that corresponds to   |                                                                          |
   |                       | the subnet. [#encap]_                                              |                                                                          |
   +-----------------------+--------------------------------------------------------------------+--------------------------------------------------------------------------+
   | Flannel VXLAN         | Allocate an IP address from Flannel for the BIG-IP device.         | Add an FDB entry and ARP record for each node.                           |
   |                       |                                                                    |                                                                          |
   |                       | Add a VXLAN network to the BIG-IP system;                          |                                                                          |
   |                       | use the IP address allocated from Flannel as the VTEP.             |                                                                          |
   +-----------------------+--------------------------------------------------------------------+--------------------------------------------------------------------------+
   | Layer 3 networks                                                                                                                                                      |
   +-----------------------+--------------------------------------------------------------------+--------------------------------------------------------------------------+
   | Calico                | Set up BGP peering between the BIG-IP device and Calico.           | None. Managed by BGP.                                                    |
   |                       |                                                                    |                                                                          |
   |                       |                                                                    | **NOTE:** Depending on the BGP configuration, you may need to update the |
   |                       |                                                                    | BGP neighbor table.                                                      |
   +-----------------------+--------------------------------------------------------------------+--------------------------------------------------------------------------+
   | Flannel host-gw       | Configure routes in Flannel and on the BIG-IP device for per-node  | Add/update per-node subnet routes on the BIG-IP device.                  |
   |                       | subnet(s).                                                         |                                                                          |
   +-----------------------+--------------------------------------------------------------------+--------------------------------------------------------------------------+

\

.. seealso::

   - The Kubernetes `Cluster Networking`_ Administration Guide provides information about Kubernetes Cluster Network types.
   - The `BIG-IP TMOS: ​Tunneling and IPsec <https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/bigip-tmos-tunnels-ipsec-13-0-0/2.html>`_ guide provides instructions for setting up tunnels on your BIG-IP device.

.. _nodeport:

NodePort
--------

The NodePort type exposes Services via the ``kube-proxy`` process that runs on each node.
Each node's ``kube-proxy`` can communicate with all pods in the cluster.

.. figure:: /_static/media/k8s_nodeport.png
   :scale: 60%

\

While this mode is maximally compatible with the Kubernetes cluster, it limits the BIG-IP system's applicable functionality.
Using NodePort equates to two-tier load balancing: all requests go to any node in the cluster; the ``kube-proxy`` on the node that handles the request chooses which Pod to send the request to.
This means the |kctlr| and BIG-IP system can't provide some L7 services, like persistence, and that the |kctlr| doesn't have any insight into the health of nodes and/or pods.

What's Next
-----------

- :ref:`Install the BIG-IP Controller in standard Kubernetes <install-kctlr>`
- :ref:`Add your BIG-IP device to an OpenShift Cluster <bigip-openshift-setup>`
- :ref:`Install the BIG-IP Controller in OpenShift <install-kctlr-openshift>`
- :ref:`Configure the BIG-IP Controller for Kubernetes <kctlr-configuration>`

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
