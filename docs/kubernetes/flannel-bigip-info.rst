.. _flannel-bigip-info:

Flannel VXLAN, Kubernetes, and BIG-IP
=====================================

Cluster Networking in Kubernetes with Flannel
---------------------------------------------

Be sure to read about Kubernetes `Cluster Networking`_ to understand the theory behind this strategy.

The basic gist of this approach is that we have a Kubernetes cluster with multiple Nodes, Kubernetes creates Pods across the Nodes, 
and we want these Pods to be able to communicate with each other without NAT.
In this article, we will implement this using Flannel's VXLAN configuration.

`Flannel`_ is a way to configure a layer 3 network fabric. In older versions of Kubernetes (pre-1.6),
Flannel solely used an etcd key-value store to read and write information about Kubernetes Nodes.
This information included the VTEP (VXLAN tunnel endpoint) of each Node, as well as a subnet within the defined Flannel network range.
Flannel assigns a different subnet to each Node, and allocates all Pod IP's within these subnets (on their respective Nodes).
In more recent versions of Kubernetes, Flannel's preferred mode of operation is via the Kubernetes API.
Etcd is still viable, but is not as common. Flannel provides a `kube-flannel.yml`_ file for use
as a network addon to kubeadm. This creates a Flannel Pod on each Kubernetes node that runs two containers: install-cni and flanneld.
Each instance of flanneld now monitors the Kubernetes API for the Nodes that live in the cluster.
The Nodes will have flannel-specific annotations attached to them, containing similar information to what etcd stores.

Here are the supported annotations:

.. code-block:: console

  flannel.alpha.coreos.com/backend-data:'{"VtepMAC":"<mac-address>"}'
  flannel.alpha.coreos.com/backend-type: 'vxlan'
  flannel.alpha.coreos.com/kube-subnet-manager: 'true'
  flannel.alpha.coreos.com/public-ip: <vtep-ip-address>

The kube-subnet-manager annotation tells Flannel to use the Kubernetes API instead of etcd to find the information it cares about.

Node resource's configuration defines the Pod subnet in the "podCIDR" field.

With this approach, Flannel will create the VXLAN with each Node that contains the appropriate annotations.
On each Node, FLannel creates a file, ``/run/flannel/subnet.env``, that contains information about the Flannel
network range, as well as the subnet range for the Pods on that Node. Each Node will also now have a Flannel VXLAN interface.

Now all the Pods across these Nodes can talk to each other!
 
This is a good first step in getting cluster networking functioning within Kubernetes.
Now what if we want to get the BIG-IP device involved?

Adding the BIG-IP device to the Kubernetes network
--------------------------------------------------

.. note::

  For specific information on the user steps to accomplish this, see :ref:`this page <bigip-k8s-setup>`.

Why would we want to include the BIG-IP device in the Kubernetes network?
Simply put, in combining this approach with the functionality of the F5 BIG-IP Controller,
we are able to have direct communication from the BIG-IP device to Pods in our Kubernetes cluster!
What do we need to do to accomplish this?
 
The first step is to configure a VXLAN profile and tunnel on the BIG-IP device.
This is what connects the BIG-IP device to the Kubernetes cluster.
This VXLAN tunnel will contain FDB (forwarding database) records that map the VTEP's (Nodes) IP addresses
in Kubernetes to the MAC addresses of their respective Flannel VXLAN interfaces.
Once active, the F5 BIG-IP Controller will populate these records in the tunnel.
The F5 BIG-IP Controller also configures static ARP entries.
These ARP entries tie directly to the tunnel's FDB records by mapping the VTEP MAC addresses to the
IP addresses of the nodes created on the BIG-IP device.

Here is an example of what this looks like:

  .. code-block:: console

    Node in Kubernetes with IP address 172.16.2.10
    MAC address of this Node's Flannel VXLAN interface is 98:ba:76:dc:54:fe
    Pod running on this Node with IP address 10.244.1.2

    F5 BIG-IP Controller creates a node on the BIG-IP device
      with IP address 10.244.1.2 (this is our Kubernetes Pod).
    Controller creates FDB record in the BIG-IP device's VXLAN tunnel
      that looks like this:
       flannel_vxlan {
          records [
             98:ba:76:dc:54:fe {
               endpoint: 172.16.2.10
             }
          ]
       }
    Controller creates a static ARP entry that looks like this:
       {
         name: k8s-10.244.1.2
         ipaddress: 10.244.1.2
         macaddress: 98:ba:76:dc:54:fe
       }

These configurations performed by the F5 BIG-IP Controller informs the BIG-IP device about where
and how to forward traffic to the node "10.244.1.2".
 
The next step is to define a tunnel self-ip on the BIG-IP device that will live in a Flannel subnet.
At this point there should be Flannel subnets (podCIDR) defined for each Node in Kubernetes.
We need to decide on a similar subnet that will not collide with any other Node's subnet.
We'll say this subnet is 10.244.30.0/24. Our BIG-IP device's self-ip will live within this subnet;
we will create one for our VXLAN tunnel at 10.244.30.15/16. The subnet mask /16 matches
the default subnet mask of the Flannel network range.
 
At this point, our BIG-IP device knows how to route to the Kubernetes network,
but is not yet a part of it. That's Flannel's job. We need to tell Flannel about the BIG-IP device.
 
Earlier we mentioned that Flannel knows about the Kubernetes Nodes via the Kubernetes API.
This means that in order for Flannel to add the BIG-IP device to the Kubernetes network,
the Kubernetse API must know about the BIG-IP device. How can we possibly do that?
By adding the BIG-IP device as a Node in Kubernetes, of course!
This may seem complicated, but is actually quite simple. Flannel simply needs to see the
BIG-IP device's information in the supported Flannel annotations, and a defined subnet (podCIDR)
on the Node, and "voila!", the BIG-IP device will be able to participate in the VXLAN.

Here is what the BIG-IP device Node looks like:

  .. literalinclude:: /kubernetes/config_examples/f5-kctlr-bigip-node.yaml
     :linenos:

Flannel sees the required annotations on this Node, and adds the BIG-IP device to the VXLAN.
 
With all of these pieces in place, traffic sent from (or through) the BIG-IP device,
directed at the Kubernetes Pod, will successfully reach its destination!

The F5 BIG-IP Controller does most of the heavy lifting in this process, so the user steps are much easier.
A user simply has to:

.. table:: Steps

   =======  ===========================================================================================================
   Step     Description
   =======  ===========================================================================================================
   1.       Ensure Flannel is correctly installed in Kubernetes, via the kube-flannel.yml file provided.
   2.       Create the VXLAN profile/tunnel on the BIG-IP device.
   3.       Create a self-ip address for the tunnel that lives within a defined Flannel subnet.
   4.       Create the BIG-IP Node in Kubernetes.
   5.       Enable the F5 BIG-IP Controller in cluster mode to configure your Kubernetes Services on the BIG-IP device.
   =======  ===========================================================================================================


.. _Cluster networking: https://kubernetes.io/docs/concepts/cluster-administration/networking/
.. _Flannel: https://github.com/coreos/flannel
.. _kube-flannel.yml: https://github.com/coreos/flannel/blob/master/Documentation/kube-flannel.yml
