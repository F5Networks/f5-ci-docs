.. todo:: add index entries

.. _openshift:

F5 BIG-IP Controller for OpenShift
==================================

.. see https://docs.openshift.org/1.4/architecture/additional_concepts/f5_big_ip.html
.. see https://docs.openshift.org/1.4/install_config/routing_from_edge_lb.html


The |kctlr-long| also functions as a BIG-IP Controller in Red Hat OpenShift.
The |kctlr| not only provides feature parity with OpenShift's F5 Router, but offers expanded BIG-IP services as well.


F5 BIG-IP Controller features
`````````````````````````````

- container runs as non-root unique user
- ctlr listens for HTTP route events in OpenShift and can create/delete/expire routes on BIG-IP devices
   (including L7 config policies such as wildcard routes, prefixes, etc.).
- ctlr can apply client SSL certificates from k8s secrets to BIG-IP LTM objects
- ctlr can apply existing BIG-IP SSL certificates to BIG-IP LTM objects
- ctlr functions as an ingress controller for external traffic (as introduced in v1.1)
- SSL termination: edge, passthrough, and re-encryption (passthrough and re-encryption added for parity with existing F5 Router)
- ctlr can deploy iApps
- no special OpenShift configurations required for passthrough routes

Questions
---------
- what are the image CPU and memory requirements??

How do I migrate from the OpenShift F5 Router?
----------------------------------------------
TBD


|kctlr| and OpenShift Routes
----------------------------

The |kctlr| can create/delete/expire BIG-IP objects for OpenShift routes, in addition to the standard Kubernetes functionality (virtual servers for Services).

- user creates a route
- |kctlr| creates a corresponding virtual server, pool, and pool member on BIG-IP with policies defined for OpenShift "vserver"
- |kctlr| adds/removes pool members to the pool for the route as endpoints are added/removed in OpenShift
- if/when user deletes all routes (and associated endpoints), the |kctlr| deletes the virtual server, pool, and pool members.


This solution uses the "F5 Native Integration" with OpenShift, as described in :ref:`Add your BIG-IP device to an OpenShift Cluster <bigip-openshift-setup>`.

-------------------------------------------------------------------------------
FROM OPENSHIFT DOCS:

Features

- create and delete pools,
- add endpoints to and delete them from those pools, and
- configure policy rules to route to pools based on vhost.
- use scp and ssh commands to upload custom TLS/SSL certificates to F5 BIG-IP®


The F5 router configures pools and policy rules on virtual servers as follows:

When a user creates or deletes a route on OpenShift Origin, the router creates a pool to F5 BIG-IP® for the route (if no pool already exists) and adds a rule to, or deletes a rule from, the policy of the appropriate vserver: the HTTP vserver for non-TLS routes, or the HTTPS vserver for edge or re-encrypt routes. In the case of edge and re-encrypt routes, the router also uploads and configures the TLS certificate and key. The router supports host- and path-based routes.

Passthrough routes are a special case: to support those, it is necessary to write an iRule that parses the SNI ClientHello handshake record and looks up the servername in an F5 data-group. The router creates this iRule, associates the iRule with the vserver, and updates the F5 data-group as passthrough routes are created and deleted. Other than this implementation detail, passthrough routes work the same way as other routes.
When a user creates a service on OpenShift Origin, the router adds a pool to F5 BIG-IP® (if no pool already exists). As endpoints on that service are created and deleted, the router adds and removes corresponding pool members.

When a user deletes the route and all endpoints associated with a particular pool, the router deletes that pool."

Overview - F5 Native Integration
````````````````````````````````
With native integration of F5 with OpenShift Origin, you do not need to configure a ramp node for F5 to be able to reach the pods on the overlay network as created by OpenShift SDN.

   CONNECTION

   The F5 appliance can connect to the OpenShift Origin cluster via an L3 connection. An L2 switch connectivity is not required between OpenShift Origin nodes. On the appliance, you can use multiple interfaces to manage the integration:

   Management interface - Reaches the web console of the F5 appliance.

   External interface - Configures the virtual servers for inbound web traffic.

   Internal interface - Programs the appliance and reaches out to the pods.

   F5 and OpenShift Connection Diagram
   An F5 controller pod has admin access to the appliance. The F5 image is launched within the OpenShift Origin cluster (scheduled on any node) that uses iControl REST APIs to program the virtual servers with policies, and configure the VXLAN device.

DATA FLOW: PACKETS TO PODS

This section explains how the packets reach the pods, and vice versa. These actions are performed by the F5 controller pod and the F5 appliance, not the user.
When natively integrated, The F5 appliance reaches out to the pods directly using VXLAN encapsulation. This integration works only when OpenShift Origin is using openshift-sdn as the network plug-in. The openshift-sdn plug-in employs VXLAN encapsulation for the overlay network that it creates.

To make a successful data path between a pod and the F5 appliance:

F5 needs to encapsulate the VXLAN packet meant for the pods. This requires the sdn-services license add-on. A VXLAN device needs to be created and the pod overlay network needs to be routed through this device.

F5 needs to know the VTEP IP address of the pod, which is the IP address of the node where the pod is located.

F5 needs to know which source-ip to use for the overlay network when encapsulating the packets meant for the pods. This is known as the gateway address.

OpenShift Origin nodes need to know where the F5 gateway address is (the VTEP address for the return traffic). This needs to be the internal interface’s address. All nodes of the cluster must learn this automatically.

Since the overlay network is multi-tenant aware, F5 must use a VXLAN ID that is representative of an admin domain, ensuring that all tenants are reachable by the F5. Ensure that F5 encapsulates all packets with a vnid of 0 (the default vnid for the admin namespace in OpenShift Origin) by putting an annotation on the manually created hostsubnet - pod.network.openshift.io/fixed-vnid-host: 0.

A ghost hostsubnet is manually created as part of the setup, which fulfills the third and forth listed requirements. When the F5 controller pod is launched, this new ghost hostsubnet is provided so that the F5 appliance can be programmed suitably.

The term ghost hostsubnet is used because it suggests that a subnet has been given to a node of the cluster. However, in reality, it is not a real node of the cluster. It is hijacked by an external appliance.
The first requirement is fulfilled by the F5 controller pod once it is launched. The second requirement is also fulfilled by the F5 controller pod, but it is an ongoing process. For each new node that is added to the cluster, the controller pod creates an entry in the VXLAN device’s VTEP FDB. The controller pod needs access to the nodes resource in the cluster, which you can accomplish by giving the service account appropriate privileges. Use the following command:

$ oadm policy add-cluster-role-to-user system:sdn-reader system:serviceaccount:default:router
DATA FLOW FROM THE F5 HOST

These actions are performed by the F5 controller pod and the F5 appliance, not the user.
The destination pod is identified by the F5 virtual server for a packet.

VXLAN dynamic FDB is looked up with pod’s IP address. If a MAC address is found, go to step 5.

Flood all entries in the VTEP FDB with ARP requests seeking the pod’s MAC address.

One of the nodes (VTEP) will respond, confirming that it is the one where the pod is located. An entry is made into the VXLAN dynamic FDB with the pod’s MAC address and the VTEP to be used as the value.

Encap an IP packet with VXLAN headers, where the MAC of the pod and the VTEP of the node is given as values from the VXLAN dynamic FDB.

Calculate the VTEP’s MAC address by sending out an ARP or checking the host’s neighbor cache.

Deliver the packet through the F5 host’s internal address.

DATA FLOW: RETURN TRAFFIC TO THE F5 HOST

These actions are performed by the F5 controller pod and the F5 appliance, not the user.
The pod sends back a packet with the destination as the F5 host’s VXLAN gateway address.

The openvswitch at the node determines that the VTEP for this packet is the F5 host’s internal interface address. This is learned from the ghost hostsubnet creation.

A VXLAN packet is sent out to the internal interface of the F5 host.

During the entire data flow, the VNID is pre-fixed to be 0 to bypass multi-tenancy.


-------------------------------------------------------------------------------

