:product: BIG-IP Controller for Kubernetes
:type: task

.. _bigip-openshift-setup:

Add BIG-IP device to OpenShift Cluster Network
==============================================

This document provides step-by-step instructions for integrating a **standalone** BIG-IP device into an OpenShift Cluster Network.

- If you are already using the `OpenShift F5 Router`_, see :ref:`upgrade f5 router`.
- If you are using a BIG-IP HA pair or cluster, see :ref:`bigip ha openshift`

Complete the following tasks to add a BIG-IP device to an `OpenShift`_ cluster network.

.. table:: Task Summary

   ===== ==================================================================================
   Step  Task
   ===== ==================================================================================
   1.    :ref:`k8s-openshift-node`:

         - :ref:`k8s-openshift-hostsubnet`
         - :ref:`k8s-openshift hostsubnet upload`
         - :ref:`k8s-openshift hostsubnet verify`
   ----- ----------------------------------------------------------------------------------
   2.    :ref:`openshift-bigip-setup`:

         - :ref:`k8s-openshift-vxlan-setup`
         - :ref:`k8s-openshift create bigip self IP`
         - :ref:`k8s-openshift create bigip floating IP`
         - :ref:`os-sdn verify bigip`
   ===== ==================================================================================

.. _k8s-openshift-node:

Create a Node for the BIG-IP device
-----------------------------------

OpenShift SDN uses custom Annotations to identify Nodes as part of the Cluster network. When you include these Annotations in a HostSubnet manifest, the SDN recognizes the new Node and allocates a subnet to it.

- :code:`pod.network.openshift.io/fixed-vnid-host: "0"`
- :code:`pod.network.openshift.io/assign-subnet: "true"`

.. _k8s-openshift-hostsubnet:

Create a HostSubnet
```````````````````

Define a HostSubnet manifest using valid YAML or JSON.

For the :code:`hostIP`, provide an IP address from the BIG-IP network that will support the VXLAN overlay.

.. literalinclude:: /openshift/config_examples/f5-kctlr-openshift-hostsubnet.yaml

:fonticon:`fa fa-download` :download:`HostSubnet - BIG-IP Standalone </openshift/config_examples/f5-kctlr-openshift-hostsubnet.yaml>`


.. _k8s-openshift hostsubnet upload:

Upload the Host Subnet to the OpenShift API server
``````````````````````````````````````````````````

Use the :command:`oc create <HostSubnet-filename.yaml>` command to upload the HostSubnet file(s) to the OpenShift API server.

.. code-block:: console

   oc create -f f5-kctlr-openshift-hostsubnet.yaml
   hostsubnet "f5-bigip-01" created


.. _k8s-openshift hostsubnet verify:

Verify creation of the HostSubnet(s)
````````````````````````````````````

.. important:: Note the subnet that the OpenShift SDN assigned to the BIG-IP host Node.

.. code-block:: console
   :emphasize-lines: 3

   oc get hostsubnet
   NAME                  HOST                  HOST IP         SUBNET
   f5-big-ip             f5-bigip-node         172.16.1.28     10.129.2.0/23
   master.internal.net   master.internal.net   172.16.1.10     10.129.0.0/23
   node1.internal.net    node1.internal.net    172.16.1.24     10.130.0.0/23
   node2.internal.net    node2.internal.net    172.16.1.25     10.128.0.0/23

.. _openshift-bigip-setup:

Set up the BIG-IP system
------------------------

.. include:: /_static/reuse/bigip-admin-permissions-reqd.rst

.. _k8s-openshift-vxlan-setup:

Create a VXLAN tunnel
`````````````````````

#. Create a BIG-IP VXLAN profile with :code:`flooding-type multi-point`.

   .. parsed-literal::

      create /net tunnels vxlan **ose-vxlan** flooding-type **multipoint**

#. Create a BIG-IP VXLAN tunnel.

   - Set the :code:`local-address` to the BIG-IP HostSubnet's :code:`hostIP` address.
   - Set the :code:`key` to :code:`0` to grant the BIG-IP device access to all OpenShift projects and subnets.

   .. parsed-literal::

      create /net tunnels tunnel **openshift_vxlan** key **0** profile **ose-vxlan** local-address **172.16.1.28**


.. _k8s-openshift create bigip self IP:
.. _k8s-openshift-assign-ip:

Create a self IP in the VXLAN
`````````````````````````````

Create a self IP address in the VXLAN tunnel. Use an IP address from the subnet that the OpenShift SDN allocated to the BIG-IP's HostSubnet.

- The subnet mask you assign to the self IP must match the one that the OpenShift SDN assigns to nodes (in this example, it's :code:`/23`).

  .. warning:: The default subnet mask varies depending on which OpenShift platform you're using (Origin/Online vs. Enterprise vs. OCP). Check the documentation for your platform before proceeding.

- If you use the BIG-IP configuration utility to create a self IP, you may need to provide the full netmask instead of the CIDR notation.
- If you don't specify a traffic group, the self IP will use the BIG-IP system's default (:code:`traffic-group-local-only`).

.. parsed-literal::

   create /net self **10.129.2.3/23** allow-service **none** vlan **openshift_vxlan**

.. _k8s-openshift create bigip floating IP:

Create a floating self IP in the VXLAN
``````````````````````````````````````

Create a floating IP address on the BIG-IP device. Use an IP address from the subnet that the OpenShift SDN allocated to the BIG-IP's HostSubnet.

.. parsed-literal::

   create /net self **10.129.2.4/23** allow-service **none** traffic-group **traffic-group-1** vlan **openshift_vxlan**

.. note::

   All virtual servers created by the |kctlr| use the `BIG-IP SNAT`_ automap feature, which prefers floating IP addresses over static IPs.
   See :ref:`bigip snats` for more information.

.. _os-sdn verify bigip:

Verify creation of the BIG-IP objects
`````````````````````````````````````

You can use a TMOS shell or the BIG-IP configuration utility to verify object creation.

.. code-block:: console

   show /net tunnels tunnel openshift_vxlan
   show /net running-config self 10.129.2.3/23
   show /net running-config self 10.129.2.4/23

You should now be able to successfully send traffic through the BIG-IP system to and from endpoints within your OpenShift Cluster.

.. seealso:: If you're having trouble with your network setup, see :ref:`networking troubleshoot openshift`.


.. _OpenShift: https://www.openshift.org/
.. _Create an OpenShift service account: https://docs.openshift.org/latest/admin_guide/service_accounts.html
