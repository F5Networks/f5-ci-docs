.. index::
   :pair: Kubernetes, BIG-IP
   :single: concept
   :triple: Kubernetes, networking, BIG-IP

.. _k8s-bigip-networks:

OVERALL QUESTIONS:
------------------
- WHAT DO WE MANAGE AUTOMATICALLY?
- WHAT DOES THE USER HAVE TO MANAGE?
- WHAT IS THE DIFFERENCE BETWEEN L2 & L3 AUTOMATION IN THESE USE CASES? (THE ROUTING TABLE UPDATES)

.. todo:: Ask Brian M for his table on what the user has to manage manually vs what's automatic / what's just done for initial setup vs what requires ongoing management

How the F5 Integration fits in to Kubernetes Cluster Networks
=============================================================

The |kctlr-long| controller configures services on the BIG-IP device to expose applications inside your Kubernetes cluster to external users.
In some deployments, the |kctlr| also makes network configurations on the BIG-IP system.

There are a number of options when it comes to connecting a BIG-IP device (platform or Virtual Edition) to a Kubernetes cluster network.
In some configurations, the |kctlr| may automate more tasks than in other configurations.
While generally more automation is better, some of these tasks may be better left to other automation systems, or may be rarely done.

For instance, in some configurations the |kctlr| will not automatically configure networking on BIG-IP for a new node that you add to your Kubernetes cluster.
But you may already be using another automation system like Ansible to provision and configure that node, so it makes sense to also have Ansible configure BIG-IP.
Also consider that some operations may occur less frequently than others.
For instance, creating new pods may happen every few seconds, creating new services several times a day, and adding nodes to the cluster only once or twice a month or less.
Even if the |kctlr| does not help automate cluster node addition, its handling of changes to pods and deployments is still helpful.
Finally, we are continuing to add cluster network automation to the |kctlr| so if we do not handle an important case for you, let us know with an issue.

These are the categories of operations that you should consider, listed from most-frequent to least-frequent (for a typical Kubernetes cluster):

- New Pod: Adding or removing Pods from an existing Service.
- New Service: Exposing applications via Services, Ingresses or similar.
- New Node: Adding capacity to your Kubernetes cluster by adding new Nodes (or removing).
- New Cluster: Creating a new Kubernetes cluster from scratch.

.. todo:: Brian's table here?  With the headings of the columns matching the bullets ("New Pod", "New Service", ...)


- :ref:`Cluster overlay networks`
- :ref:`Cluster routed networks`
- :ref:`Kubernetes NodePort`

.. seealso::

   See the Kubernetes `Cluster Networking`_ Administration Guide for more information about setting up a Kubernetes cluster network.

.. _cluster overlay networks:

Cluster Overlay Networks
------------------------

In a Cluster Overlay Network, the BIG-IP system connects to an L2 overlay (a VLAN).
The nodes in a Kubernetes cluster connect to the overlay by means of VXLANs.

.. figure:: /_static/media/k8s-sdn-vxlan_copy.png
   :scale: 60%

In this deployment, you'll need to make some initial configurations on the BIG-IP system.

#. Create a new VLAN and self IP address.

   - The VLAN corresponds to the L2 overlay providing connectivity to the nodes in your cluster.
   - The VLAN connects to an untaffed interface on the BIG-IP platform (in this example, ``1.1``).
   - The self IP address will serve as the VXLAN tunnel endpoint; set it to an IP address available in the overlay VLAN.

   .. code-block:: console

      tmsh create net vlan k8s_vlan interfaces add { 1.1 }
      tmsh create net self 1.2.3.4 vlan k8s_vlan

#. Create a new ``vxlan`` tunnel profile and a VXLAN tunnel.

   - Set the ``flooding-type`` to ``multi-point``.
   - Use the self IP address as the tunnel's ``local-address``.

   .. code-block:: console

      tmsh create net tunnels vxlan vxlan-mp flooding-type multipoint
      tmsh create net tunnels tunnel k8s_vxlan profile vxlan-mp local-address 1.2.3.4

   .. important::

      Be sure to use the correct encapsulation format for your network.

#. Create **FDB entries** and **ARP records** for the cluster endpoints.
   For instructions, see **Examples for manually populating L2 location records** in the `BIG-IP TMOS: ​Tunneling and IPsec <https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/bigip-tmos-tunnels-ipsec-13-0-0/2.html>`_ guide.

OpenShift SDN
`````````````

The OpenShift SDN cluster overlay setup is similar to the standard Kubernetes setup, but it has a few key differences.

- Instead of setting up a VLAN and self IP on the BIG-IP system, you'll :ref:`create a host subnet <k8s-openshift-hostsubnet>` in your OpenShift cluster.
- The ``hostIP`` address assigned to the BIG-IP device from the host subnet provides the means of connecting the BIG-IP to the L2 overlay.
- If using the ``ovs-multitenant`` plugin, assign the BIG-IP device the OpenShift ``VNID 0`` to grant it access to all projects. [#originsdn]_
- In OpenShift, the |kctlr-long| is route-aware; it automatically discovers FDB entries and updates the BIG-IP system accordingly.

See :ref:`How to add your BIG-IP device to an OpenShift Cluster <bigip-openshift-setup>` for complete setup instructions.

.. seealso::

   <Link to OpenShift feature parity page>

.. _cluster routed networks:

Cluster Routed Networks
-----------------------

In a cluster routed network, the BIG-IP device connects to a flat IP network.

.. figure:: /_static/media/k8s-direct_2_copy.png
   :scale: 60%

In this model, the Kubernetes master assigns IP addresses to all Pods.
You'll need to manually configure routes on the BIG-IP system so it can discover all Pod IP addresses on the cluster network.

See the `BIG-IP TMOS Routing Administration`_ guide for more information about managing routes on your BIG-IP device.

ClusterIP/iptables

Project Calico
``````````````

You can use `Calico for Kubernetes`_ as part of a cluster routed network.


Calico BGP https://docs.projectcalico.org/v2.4/usage/configuration/bgp

Questions:

- How does this work?
- What BIG-IP pre-configs are required?
- Do we have to set up VLANs on BIG-IP

We understand the control plane and there's no encapsulation required.


.. _Kubernetes NodePort:

Kubernetes NodePort
-------------------

.. figure:: /_static/media/k8s_nodeport_copy.png
   :scale: 60%

type:NodePort


https://kubernetes.io/docs/concepts/architecture/nodes/

DON'T USE IT UNLESS YOU NEED TO



.. rubric:: Footnotes
.. [#originsdn] See the `OpenShift Origin SDN`_ documentation for more information.



.. _Cluster Networking: https://kubernetes.io/docs/concepts/cluster-administration/networking/
.. _OpenShift Origin SDN: https://docs.openshift.org/latest/architecture/additional_concepts/sdn.html
.. _Flannel: https://docs.openshift.org/latest/architecture/additional_concepts/flannel.html
.. _Open vSwitch VXLAN network: https://kubernetes.io/docs/admin/ovs-networking/
.. _Calico for Kubernetes: https://docs.projectcalico.org/latest/getting-started/kubernetes/
.. _Calico BGP: https://docs.projectcalico.org/v2.4/usage/configuration/bgp
.. _Create a network virtualization tunnel: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/bigip-tmos-tunnels-ipsec-13-0-0/2.html
.. _BIG-IP TMOS Routing Administration: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/tmos-routing-administration-13-0-0.html
