.. index::
   single: OpenShift; BIG-IP; setup

.. sidebar:: Docs test matrix

   Documentation manually tested with:

   - BIG-IP v12.1.1
   - OpenShift Origin v1.4

.. _bigip-openshift-setup:

Add BIG-IP device to OpenShift Cluster Network
==============================================

This document provides step-by-step instructions for integrating a BIG-IP device into an OpenShift Cluster Network. If you are already using the `OpenShift F5 Router`_, see :ref:`upgrade f5 router`.

Complete the following tasks to add a BIG-IP device to an `OpenShift`_ cluster network.

.. table:: Task Table

   ===== ==================================================================================
   Step  Task
   ===== ==================================================================================
   1.    :ref:`k8s-openshift-hostsubnet`
   ----- ----------------------------------------------------------------------------------
   2.    :ref:`openshift-bigip-setup`:

         - :ref:`k8s-openshift-vxlan-setup`
         - :ref:`k8s-openshift create bigip self IP`
         - :ref:`k8s-openshift create bigip floating IP`
         - :ref:`os-sdn verify bigip`
   ===== ==================================================================================

.. _k8s-openshift-hostsubnet:

Add the BIG-IP Device to OpenShift SDN
--------------------------------------

OpenShift SDN uses custom Annotations to identify Nodes as part of the Cluster network. Include the Annotations shown below in a HostSubnet manifest to allocate a subnet for the BIG-IP device.

:code:`pod.network.openshift.io/fixed-vnid-host: "0"`

:code:`pod.network.openshift.io/assign-subnet: "true"`

#. Create a HostSubnet manifest.

   Define the :code:`hostIP` with an IP address from the BIG-IP external VLAN. You will use this address later to to :ref:`create the BIG-IP VXLAN tunnel <k8s-openshift-vxlan-setup>`.

   .. literalinclude:: /openshift/config_examples/f5-kctlr-openshift-hostsubnet.yaml

   :fonticon:`fa fa-download` :download:`f5-kctlr-openshift-hostsubnet.yaml </openshift/config_examples/f5-kctlr-openshift-hostsubnet.yaml>`

#. Upload the Host Subnet to the OpenShift API server.

   .. code-block:: console

      oc create -f f5-kctlr-openshift-hostsubnet.yaml

#. Verify creation of the HostSubnet and note the assigned subnet.

   .. code-block:: console
      :emphasize-lines: 3

      oc get hostsubnet
      NAME                  HOST                  HOST IP         SUBNET
      big-ip                f5-server             172.16.1.28     10.129.2.0/23
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

   .. code-block:: console

      admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$ create /net tunnels vxlan vxlan-mp flooding-type multipoint

#. Create a BIG-IP VXLAN tunnel.

   - Use the IP address you provided for the OpenShift HostSubnet :code:`hostIP` as the VXLAN's :code:`local-address`.
   - Set the :code:`key` to :code:`0` to grant the BIG-IP device access to all OpenShift projects and subnets.

   \

   .. code-block:: console

      admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$ create /net tunnels tunnel openshift_vxlan key 0 profile vxlan-mp local-address 172.16.1.28


.. _k8s-openshift create bigip self IP:
.. _k8s-openshift-assign-ip:

Create a self IP in the VXLAN
`````````````````````````````

Create a self IP address in the VXLAN tunnel. Use an address from the subnet allocated by the OpenShift SDN.

.. code-block:: console

   admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$ create /net self 10.129.2.3/23 allow-service none vlan openshift_vxlan

.. important::

   - The subnet mask you assign to the self IP must match that of the subnet assigned by the OpenShift SDN (in this example, :code:`/23`).
   - When creating a self IP using the BIG-IP configuration utility instead of TMSH, you may need to provide the full netmask (for example, :code:`255.255.254.0` instead of :code:`/23`).
   - If you do not specify a traffic group, the self IP will use the BIG-IP system's default.

.. _k8s-openshift create bigip floating IP:

Create a floating self IP in the VXLAN
``````````````````````````````````````

Create a floating IP address in the subnet assigned by the OpenShift SDN.

.. code-block:: console

   admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$ create /net self 10.129.2.4/23 allow-service none traffic-group traffic-group-1 vlan openshift_vxlan

.. note::

   All virtual servers created by the |kctlr| use the `BIG-IP SNAT`_ automap feature, which prefers floating IP addresses over static IPs.
   See :ref:`bigip snats` for more information.


.. _os-sdn verify bigip:

Verify creation of the BIG-IP objects
`````````````````````````````````````

You can use a TMOS shell or the BIG-IP configuration utility to verify object creation.

.. code-block:: console

   admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$ show /net tunnels tunnel openshift_vxlan
   admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$ show /net running-config self 10.129.2.3/23
   admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$ show /net running-config self 10.129.2.4/23


You should now be able to successfully send traffic through the BIG-IP system to and from endpoints within your OpenShift Cluster.

What's Next
-----------

- :ref:`Deploy the BIG-IP Controller for Openshift <install-kctlr-openshift>`

.. seealso::

   If you're having trouble with your network setup, see :ref:`networking troubleshoot openshift`.


.. _OpenShift: https://www.openshift.org/
.. _Create an OpenShift service account: https://docs.openshift.org/latest/admin_guide/service_accounts.html
