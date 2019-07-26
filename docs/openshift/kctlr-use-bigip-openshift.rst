:product: BIG-IP Controller for Kubernetes
:type: task

.. _bigip-openshift-setup:

Add BIG-IP device to OpenShift Cluster Network
==============================================

This document provides step-by-step instructions for integrating a **standalone** BIG-IP device into an OpenShift Cluster Network.

- If you are using the `OpenShift F5 Router`_, see :ref:`upgrade f5 router`.
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

OpenShift SDN uses custom Annotations to identify Nodes as part of the Cluster network.

- :code:`pod.network.openshift.io/fixed-vnid-host: "0"`
- :code:`pod.network.openshift.io/assign-subnet: "true"`

When you include these Annotations in a HostSubnet manifest, the SDN recognizes the new Node and allocates a subnet to it.

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

Use the :command:`oc create` command to upload the HostSubnet file(s) to the OpenShift API server.

.. parsed-literal::

   oc create -f **f5-kctlr-openshift-hostsubnet.yaml**
   hostsubnet "f5-bigip-node" created


.. _k8s-openshift hostsubnet verify:

Verify creation of the HostSubnet(s)
````````````````````````````````````

.. important:: Note the subnet that the OpenShift SDN assigned to the BIG-IP host Node.

.. code-block:: console

   oc get hostsubnet
   NAME                  HOST                  HOST IP         SUBNET
   f5-bigip-node         f5-bigip-node         172.16.1.28     10.129.2.0/14


.. _openshift-bigip-setup:

Set up the BIG-IP system
------------------------

.. important::

   The steps in this section require Administrator or Resource Administrator access to the BIG-IP system's TMOS shell (tmsh).


.. _k8s-openshift-vxlan-setup:

Create a VXLAN tunnel
`````````````````````

#. Log in to the TMOS shell (tmsh).

   .. parsed-literal::

      tmsh

#. Create a BIG-IP VXLAN profile with :code:`flooding-type multi-point`.

   .. parsed-literal::

      create net tunnels vxlan **ose-vxlan** flooding-type **multipoint**

#. Create a BIG-IP VXLAN tunnel.

   - Set the :code:`local-address` to the BIG-IP HostSubnet's :code:`hostIP` address.
   - Set the :code:`key` to :code:`0` to grant the BIG-IP device access to all OpenShift projects and subnets.

   .. parsed-literal::

      create net tunnels tunnel **openshift_vxlan** key **0** profile **ose-vxlan** local-address **172.16.1.28**

.. _k8s-openshift-self-vxlan:

Create a self IP in the VXLAN
`````````````````````````````

Create a self IP address in the VXLAN tunnel.

- The self IP range must fall within the cluster subnet mask. Use the command :command:`oc get clusternetwork` to find the correct subnet mask for your cluster.
- If you use the BIG-IP configuration utility to create a self IP, you may need to provide the full netmask instead of the CIDR notation.

.. parsed-literal::

   create net self **10.129.2.3/14** allow-service **none** vlan **openshift_vxlan**

.. _k8s-openshift-floating-self-vxlan:

Create a floating self IP in the VXLAN
``````````````````````````````````````

Create a floating IP address on the BIG-IP device. Use an IP address from the subnet that the OpenShift SDN allocated to the BIG-IP's HostSubnet.

.. parsed-literal::

   create net self **10.129.2.4/14** allow-service **none** traffic-group **traffic-group-1** vlan **openshift_vxlan**

.. include:: /_static/reuse/kctlr-snat-note.rst

.. _k8s-openshift-verify:

Verify creation of the BIG-IP objects
`````````````````````````````````````

You can use the TMOS shell (tmsh) to verify object creation.

   .. parsed-literal::

      tmsh show net tunnels tunnel **openshift_vxlan**
      tmsh show net self **10.129.2.3/14**
      tmsh show net self **10.129.2.4/14**

.. seealso:: If you're having trouble with your network setup, see :ref:`networking troubleshoot openshift`.

What's Next
-----------

- :ref:`Deploy the BIG-IP Controller <install-kctlr-openshift>`

.. _OpenShift: https://www.openshift.org/
.. _Create an OpenShift service account: https://docs.openshift.org/latest/admin_guide/service_accounts.html
