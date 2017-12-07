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

\

.. tip::

   The examples provided here deploy the |kctlr| to the 'default' namespace and assign it a Service Account named 'bigip-ctlr'.

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

      admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$ create net tunnels vxlan vxlan-mp flooding-type multipoint

#. Verify creation of the VXLAN profile.

   .. code-block:: console

      admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$ list net tunnels vxlan vxlan-mp


#. Create a new BIG-IP VXLAN tunnel.

   - Use the OpenShift HostSubnet's ``hostIP`` address as the VXLAN ``local-address`` (the BIG-IP VTEP).
   - Set the ``key`` to ``0`` to grant the BIG-IP device access to all OpenShift projects and subnets.

   .. code-block:: console

      admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$ create net tunnels tunnel openshift_vxlan key 0 profile vxlan-mp local-address 172.16.1.28

#. Verify creation of the VXLAN tunnel.

   .. code-block:: console

      admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$ list net tunnels tunnel openshift_vxlan


.. _k8s-openshift-assign-ip:

Add the BIG-IP device to the OpenShift overlay network
------------------------------------------------------

#. Create a BIG-IP self IP address.

   - Use an address in the range allocated for the :ref:`HostSubnet <k8s-openshift-hostsubnet>` created earlier.
     **This ensures that all VXLAN traffic is correctly routed via the** :code:`openshift_vxlan` **tunnel.** [#ossdn]_
   - Assign a subnet mask that matches that of the OpenShift SDN cluster network. In OpenShift Origin 1.4, for example, the default is ``/14``.

     .. tip::

        When creating a self IP using the BIG-IP configuration utility, specify the full netmask (for example, :code:`255.252.0.0`).

   - If you don't specify a traffic group, the self IP uses the BIG-IP system's default.

   .. code-block:: console

      admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$ create net self 10.129.2.10/14 allow-service all vlan openshift_vxlan


What's Next
-----------

- :ref:`Deploy the BIG-IP Controller for Openshift <install-kctlr-openshift>`

.. rubric:: Footnotes
.. [#ossdn] See the `OpenShift SDN documentation <https://docs.openshift.org/1.4/architecture/additional_concepts/sdn.html#sdn-design-on-masters>`_.

.. _OpenShift: https://www.openshift.org/
.. _Create an OpenShift service account: https://docs.openshift.org/latest/admin_guide/service_accounts.html
