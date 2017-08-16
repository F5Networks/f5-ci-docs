.. _bigip-openshift-setup:

Add your BIG-IP device to an OpenShift Cluster
==============================================

.. sidebar:: Docs test matrix

   We tested this documentation with:

   - BIG-IP v12.1.1
   - OpenShift Origin v1.5

Tasks
-----

Complete the following tasks to set up a BIG-IP device and |kctlr| for use in an `OpenShift`_ cluster:

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
      |kctlr| with the necessary permissions
===== ==================================================================================


.. tip::

   The examples provided here deploy the |kctlr| to the 'default' namespace and assign it a Service Account named 'bigip-ctlr'.


.. _k8s-openshift-hostsubnet:

Create a new OpenShift HostSubnet
---------------------------------

#. Define a HostSubnet using valid JSON or YAML.

   .. important::

      You must include the "annotation" section shown in the example below.


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

Create a BIG-IP VXLAN
---------------------

#. Create a new VXLAN profile with multi-point flooding on the BIG-IP device.

   .. admonition:: TMSH

      admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$ create net tunnels vxlan vxlan-mp flooding-type multipoint


   .. tip::

      You can use the command below to verify creation of the profile before moving on to the next task.

      :command:`admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$ list net tunnels vxlan vxlan-mp`

#. Create a BIG-IP VXLAN using your new VXLAN profile.

   - Use the OpenShift HostSubnet's ``hostIP`` address as the VXLAN ``local-address`` (the VTEP).
   - The ``key`` must be ``0`` if you want to give the BIG-IP access to all OpenShift subnets.


   .. admonition:: TMSH

      admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$ create net tunnels tunnel openshift_vxlan key 0 profile vxlan-mp local-address 172.16.1.28


#. Verify creation of the VXLAN tunnel.

   .. admonition:: TMSH

      admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$ list net tunnels tunnel openshift_vxlan


.. _k8s-openshift-assign-ip:

Add the BIG-IP device to the OpenShift overlay network
------------------------------------------------------

#. Create a BIG-IP self IP address.

   - Use an address in the range you defined in the :ref:`HostSubnet <k8s-openshift-hostsubnet>` ``subnet`` field with a subnet mask of ``/14``.
     **This ensures that all VXLAN traffic is correctly routed via the ``openshift_vxlan`` tunnel.** [#ossdn]_
   - The self IP uses the default traffic group unless you specify a different one.

   .. admonition:: TMSH

      admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$ create net self 10.129.2.10/14 allow-service all vlan openshift_vxlan

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
