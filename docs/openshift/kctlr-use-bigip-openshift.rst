.. _bigip-openshift-setup:

How to add your BIG-IP device to an OpenShift Cluster
=====================================================

.. sidebar:: Docs test matrix

   We tested this documentation with:

   - BIG-IP v12.1.1
   - OpenShift Origin v1.5

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
----- ----------------------------------------------------------------------------------
4.    :ref:`Create an OpenShift service account <k8s-openshift-serviceaccount>` for the
      |kctlr-long|.
===== ==================================================================================

\

.. tip::

   The examples provided here deploy the |kctlr| to the 'default' namespace and assign it a Service Account named 'bigip-ctlr'.


.. _k8s-openshift-hostsubnet:

Create a new OpenShift HostSubnet
---------------------------------

#. Define a HostSubnet using valid JSON or YAML.

   .. important::

      You must include the "annotation" section shown in the example below.
      The VNID ``0`` grants the BIG-IP device access to all OpenShift projects.

   .. literalinclude:: /_static/config_examples/f5-kctlr-openshift-hostsubnet.yaml
      :linenos:
      :emphasize-lines: 5-7, 9, 13

   :fonticon:`fa fa-download` :download:`f5-kctlr-openshift-hostsubnet.yaml </_static/config_examples/f5-kctlr-openshift-hostsubnet.yaml>`

   .. code-block:: console

      user@openshift:~$ oc create -f f5-kctlr-openshift-hostsubnet.yaml

#. Verify creation of the HostSubnet.

   .. code-block:: console
      :emphasize-lines: 3

      $ oc get hostsubnet
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


   .. tip::

      You can use the command below to verify creation of the profile before moving on to the next task.

      :command:`admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$ list net tunnels vxlan vxlan-mp`

#. Create a new BIG-IP VXLAN tunnel.

   - Use the OpenShift HostSubnet's ``hostIP`` address as the VXLAN ``local-address`` (the BIG-IP VTEP).
   - Set the ``key`` to ``0`` to grant the BIG-IP device access to all OpenShift projects and subnets.

   .. code-block:: console

      admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$ create net tunnels tunnel openshift_vxlan key 0 profile vxlan-mp local-address 172.16.1.28

#. Verify creation of the VXLAN tunnel.

   .. code-block:: console

      admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$ list net tunnels tunnel openshift_vxlan


.. _k8s-openshift-assign-ip:

Assign a self IP address from the cluster overlay to the BIG-IP device
----------------------------------------------------------------------

#. Create a new self IP address on the BIG-IP system.

   - Use an address in the range defined in the :ref:`HostSubnet <k8s-openshift-hostsubnet>` with a subnet mask of ``/14``.
     **This ensures that all VXLAN traffic is correctly routed via the ``openshift_vxlan`` tunnel.** [#ossdn]_
   - The self IP uses the BIG-IP ``default`` traffic group unless you specify a different one.

   .. code-block:: console

      admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$ create net self 10.129.2.10/14 allow-service all vlan openshift_vxlan

#. Verify creation of the self IP.

   .. code-block:: console

      admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$ list net self 10.129.2.10/14

Next Steps
----------

- :ref:`Install the F5 BIG-IP Controller in Openshift <install-kctlr-openshift>`
- :ref:`Configure the F5 BIG-IP Controller for use in OpenShift <kctlr-configure-openshift>`

.. rubric:: Footnotes
.. [#ossdn] See the `OpenShift SDN documentation <https://docs.openshift.org/latest/architecture/additional_concepts/sdn.html#sdn-design-on-masters>`_.

.. _OpenShift: https://www.openshift.org/
.. _Create an OpenShift service account: https://docs.openshift.org/latest/admin_guide/service_accounts.html
.. _VXLAN profile:
.. _Self IP address: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/tmos-routing-administration-12-1-1/5.html
.. _cluster role binding:
.. _cluster role: https://docs.openshift.org/latest/architecture/additional_concepts/authorization.html
.. _service account: