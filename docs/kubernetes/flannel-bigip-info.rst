.. index::
   single: BIG-IP; flannel; VXLAN; BIG-IP Controller; Kubernetes; Cluster Network

.. _flannel-bigip-info:

BIG-IP device integration with flannel VXLAN in Kubernetes
==========================================================

Overview of Cluster Networking with flannel in Kubernetes
---------------------------------------------------------

.. sidebar:: :fonticon:`fa fa-info-circle` Related

   Read about the Kubernetes `Cluster Network`_ and `Using flannel with Kubernetes`_.

`Flannel`_ is a layer 3 network fabric (or, in their words, "a virtual network that attaches IP addresses to containers"). Flannel assigns a subnet to each Node and allocates an IP address within the Node's subnet to each of the Node's Pods.

For Kubernetes v1.6 and later, flannel provides a ``kubeadm`` network add-on. When you apply the `flannel manifest`_ in Kubernetes, the flannel Pod deploys on each Node in the Cluster. The Pod consists of two containers:

- ``install-cni``: Deploys the configurations needed for the `flannel-cni network plugin`_.
- ``flanneld``: Runs the flannel daemon.

These containers allow flannel to provide network information to Nodes and to read information about Nodes from the Kubernetes API server.

.. note::

   In older versions of Kubernetes (pre-1.6), flannel used an ``etcd`` key-value store to read and write information about Kubernetes Nodes. This information included the VTEP (VXLAN tunnel endpoint) of each Node and a subnet within the defined flannel network range. Though ``etcd`` is still viable in later versions, it's not as common.

Once you have the flannel daemon running on each Node, all of the Pods across the Cluster can talk to each other.

Now that we have flannel set up, let's focus on your BIG-IP.

BIG-IP devices and the Kubernetes Cluster network
-------------------------------------------------

As discussed in :ref:`kctlr modes`, when you integrate your BIG-IP device into the Kubernetes Cluster Network, it can load balance directly to any Pod in the Cluster. Read on for a high-level view of how the integration works.

.. tip::

   See :ref:`bigip-k8s-setup` for step-by-step instructions.

Tell the BIG-IP about Kubernetes
````````````````````````````````

First, you'll connect the BIG-IP device to the Kubernetes Cluster Network using a VXLAN tunnel. When you launch the |kctlr|, it will populate the tunnel with forwarding database (FDB) records. The FDB records map each Kubernetes Node's [cluster] IP address to the MAC address of its flannel VXLAN interface. The |kctlr| will also create static ARP entries. The ARP entries map the flannel VXLAN interface's MAC address to the public IP address assigned to the Pod by flannel; this public IP address is also assigned to the node on the BIG-IP.

.. todo:: Verify if the above statement re cluster IP is correct.

**For example:**

Node1 has the IP address, MAC address, and Pod IP address shown in the table below.

+-------------------------------------------------------------------+
| Kubernetes Node1                                                  |
+===============================================+===================+
| Node IP address                               | 172.16.2.10       |
+-----------------------------------------------+-------------------+
| MAC address of Node's flannel VXLAN interface | 98:ba:76:dc:54:fe |
+-----------------------------------------------+-------------------+
| Pod public_ip address assigned by flannel     | 10.244.1.2        |
+-----------------------------------------------+-------------------+

The BIG-IP FDB record created for this Node would look like this ::

   flannel_vxlan {
    records [
       98:ba:76:dc:54:fe {
         endpoint: 172.16.2.10
       }
    ]
   }

and the static ARP entry would look like this: ::

   {
      name: k8s-10.244.1.2
      ipaddress: 10.244.1.2
      macaddress: 98:ba:76:dc:54:fe
   }

Together, these records tell the BIG-IP device what Kubernetes resource(s) should receive traffic from the node whose IP address is "10.244.1.2".

Tell flannel about the BIG-IP
`````````````````````````````

At this point, your BIG-IP device knows how to route to the Kubernetes network, but it isn't a part of the network yet. You'll need to set up flannel to be aware of the BIG-IP device. To do so, you'll create an additional flannel subnet and allocate a self IP address from this subnet as the BIG-IP's VTEP.

When setting up a new subnet to use for the BIG-IP, make sure that it doesn't collide with any of the Node subnets.

**For example:**
First, define a subnet to allocate BIG-IP self IP addresses from: ``10.244.30.0/24``.

Then, create a self IP to use as the VTEP for the VXLAN tunnel: ``10.244.30.15/16``. The subnet mask -- ``/16`` -- matches the flannel network range's default subnet mask.

As mentioned earlier, flannel knows about Kubernetes Nodes via the Kubernetes API. This means that, in order for flannel to add the BIG-IP device to the Kubernetes network,
the Kubernetes API has to know about the BIG-IP device. How can we possibly do that?

Add the BIG-IP device as a Node in Kubernetes, of course!

This may seem complicated at first, but it's actually fairly simple. When you create a new Node resource for the BIG-IP device, add the flannel Annotations and podCIDR.

Here is what the BIG-IP Node resource looks like:

.. literalinclude:: /kubernetes/config_examples/f5-kctlr-bigip-node.yaml
   :linenos:

Flannel sees its Annotations on the Node and adds the BIG-IP device to the VXLAN.
 
With all of these pieces in place, we can successfully send traffic from (or through) a BIG-IP virtual server to a specific Kubernetes Pod!

What's Next
-----------

:ref:`Add your BIG-IP device to the Kubernetes Cluster <bigip-k8s-setup>`.

.. _flannel-cni network plugin: https://github.com/containernetworking/plugins/tree/master/plugins/meta/flannel
