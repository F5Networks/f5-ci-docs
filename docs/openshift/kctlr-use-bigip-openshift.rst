.. index::
   single: OpenShift; BIG-IP; setup

.. sidebar:: Docs test matrix

   Documentation manually tested with:

   - BIG-IP v12.1.1
   - OpenShift Origin v1.4

.. _bigip-openshift-setup:

Add your BIG-IP device to an OpenShift Cluster
==============================================

Tasks
-----

Complete the following tasks to add a BIG-IP device to an `OpenShift`_ cluster network.

===== ==================================================================================
Step  Task
===== ==================================================================================
1.    :ref:`Create a host subnet <k8s-openshift-hostsubnet>` in your OpenShift cluster.
----- ----------------------------------------------------------------------------------
2.    :ref:`Create a VXLAN tunnel <k8s-openshift-vxlan-setup>` on the BIG-IP device.
----- ----------------------------------------------------------------------------------
3.    :ref:`Assign an overlay address <k8s-openshift-assign-ip>` from the subnet to a
      BIG-IP `Self IP address`_.
===== ==================================================================================

.. _k8s-openshift-hostsubnet:

Create a new OpenShift HostSubnet
---------------------------------

#. Define a HostSubnet using valid JSON or YAML.

   .. important::

      Include the "annotation" section shown in the example below with VNID ``0``. This grants the BIG-IP device access to all OpenShift projects.

   \

   .. literalinclude:: /openshift/config_examples/f5-kctlr-openshift-hostsubnet.yaml
      :linenos:
      :emphasize-lines: 5-7, 9, 13

   :fonticon:`fa fa-download` :download:`f5-kctlr-openshift-hostsubnet.yaml </openshift/config_examples/f5-kctlr-openshift-hostsubnet.yaml>`

#. Upload the Host Subnet to the OpenShift API server.

   .. code-block:: console

      oc create -f f5-kctlr-openshift-hostsubnet.yaml

#. Verify creation of the HostSubnet.

   .. code-block:: console
      :emphasize-lines: 3

      oc get hostsubnet
      NAME                  HOST                  HOST IP         SUBNET
      f5-server             f5-server             172.16.1.28     10.129.2.0/23
      master.internal.net   master.internal.net   172.16.1.10     10.129.0.0/23
      node1.internal.net    node1.internal.net    172.16.1.24     10.130.0.0/23
      node2.internal.net    node2.internal.net    172.16.1.25     10.128.0.0/23

.. _k8s-openshift-vxlan-setup:

Create a BIG-IP VXLAN tunnel
----------------------------

#. Create a new BIG-IP VXLAN profile using multi-point flooding.

   .. code-block:: console

      create /net tunnels vxlan vxlan-mp flooding-type multipoint

#. Create a new BIG-IP VXLAN tunnel.

   - Use the OpenShift HostSubnet's ``hostIP`` address as the VXLAN ``local-address`` (the BIG-IP VTEP).
   - Set the ``key`` to ``0`` to grant the BIG-IP device access to all OpenShift projects and subnets.

   .. code-block:: console

      create /net tunnels tunnel openshift_vxlan key 0 profile vxlan-mp local-address 172.16.1.28

#. Verify creation of the BIG-IP objects in a TMOS shell.

   .. code-block:: console

      list net tunnels vxlan vxlan-mp
      list net tunnels tunnel openshift_vxlan


.. tip:: You can also use the BIG-IP configuration utility to verify object creation.


.. _k8s-openshift-assign-ip:

Add the BIG-IP device to the OpenShift overlay network
------------------------------------------------------

.. important::

   If you are managing a BIG-IP pair or device cluster, you must create a floating self IP to ensure correct routing between BIG-IP nodes and OpenShift endpoints. See the :ref:`bigip snats` section of the BIG-IP/flannel VXLAN Integration document for more information.

To add the BIG-IP device to the OpenShift network, assign it a floating self IP address from the range defined in the :ref:`OpenShift HostSubnet <k8s-openshift-hostsubnet>`.
This ensures that the BIG-IP routes traffic to OpenShift Pod endpoints correctly via the :code:`openshift_vxlan` tunnel.

Assign a subnet mask to the self IP that matches that of the OpenShift SDN cluster network. In Red Hat OpenShift Container Platform v3.7, for example, the default cluster network CIDR is ``10.128.0.0/14``. [#ossdn]_

.. tip::

   When creating a self IP using the BIG-IP configuration utility, you may need to specify the full netmask instead of using CIDR format (for example, :code:`255.252.0.0`).

.. rubric:: Create a floating self IP using a TMOS shell:

.. code-block:: console
   :caption: ``admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$``

   create /net self 10.129.2.0/16 allow-service all traffic-group traffic-group-1 vlan openshift_vxlan

If you don't specify a traffic group when you create the self IP, it will use the default, non-floating traffic group:

.. code-block:: console
   :caption: ``admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$``

   create /net self 10.129.2.10/14 allow-service all vlan openshift_vxlan

.. seealso:: See :ref:`networking troubleshoot openshift` if you're having trouble with your network setup.

What's Next
-----------

- :ref:`Deploy the BIG-IP Controller for Openshift <install-kctlr-openshift>`

.. rubric:: Footnotes
.. [#ossdn] See the `OpenShift SDN documentation <https://docs.openshift.org/1.4/architecture/additional_concepts/sdn.html#sdn-design-on-masters>`_.

.. _OpenShift: https://www.openshift.org/
.. _Create an OpenShift service account: https://docs.openshift.org/latest/admin_guide/service_accounts.html
