.. _bigip-openshift-setup:

Add BIG-IP device to an OpenShift Cluster
=========================================

.. sidebar:: Docs test matrix

   We tested this documentation with:

   - BIG-IP v12.1.1
   - OpenShift Origin v1.5

Summary
-------

Complete the following tasks to set up a BIG-IP device and |kctlr| for use in an `OpenShift`_ cluster:

#. :ref:`Create a host subnet <k8s-openshift-hostsubnet>` in your OpenShift cluster.
#. :ref:`Create a VXLAN tunnel <k8s-openshift-vxlan-setup>` on the BIG-IP device.
#. :ref:`Assign an overlay address <k8s-openshift-assign-ip>` from the subnet to a BIG-IP `Self IP address`_.
#. :ref:`Create an OpenShift service account <k8s-openshift-serviceaccount>` for the |kctlr| with permission to manage the following:

   - nodes
   - endpoints
   - services
   - configmaps
   - namespaces
   - ingresses
   - ingresses/status
   - events

.. tip::

   The examples deploy the |kctlr| to the namespace 'default' and the create the ``serviceAccountName`` named 'bigip-ctlr'.


.. _k8s-openshift-hostsubnet:

Create a new OpenShift HostSubnet
---------------------------------

#. Define a HostSubnet using valid JSON or YAML.

   .. code-block:: console

      user@openshift:~$ oc create -f f5-kctlr-openshift-hostsubnet.yaml

   .. important::

      - You must include the "annotation" section shown in the example below.

   .. literalinclude:: /_static/config_examples/f5-kctlr-openshift-hostsubnet.yaml
      :linenos:
      :emphasize-lines: 5-7, 9, 13

   :fonticon:`fa fa-download` :download:`f5-kctlr-openshift-hostsubnet.yaml </_static/config_examples/f5-kctlr-openshift-hostsubnet.yaml>`


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

#. Create a new VXLAN profile on the BIG-IP device using multi-point flooding.

   .. admonition:: TMSH

      admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$ create net \\
      tunnels vxlan vxlan-mp flooding-type multipoint

#. Verify creation of the profile.

   .. admonition:: TMSH

      admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$ list net \\
      tunnels vxlan vxlan-mp

#. Create a BIG-IP VXLAN using the new ``vxlan-mp`` profile.

   .. admonition:: TMSH

      admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$ create net \\
      tunnels tunnel openshift_vxlan key 0 profile vxlan-mp local-address 172.16.1.28

   - The ``hostIP`` address defined in the OpenShift HostSubnet is the ``local-address`` (the VTEP).
   - The ``key`` must be ``0`` if you want to give the BIG-IP access to all OpenShift subnets.

#. Verify creation of the VXLAN tunnel.

   .. admonition:: TMSH

      admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$ list net \\
      tunnels tunnel openshift_vxlan

.. _k8s-openshift-assign-ip:

Assign an OpenShift overlay address to the BIG-IP device
--------------------------------------------------------

#. Create a `Self IP address`_ on the BIG-IP device.
   Use an address in the range you defined in the :ref:`HostSubnet <k8s-openshift-hostsubnet>` ``subnet`` field.

   .. admonition:: TMSH

      admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$ create net self \\
      10.129.2.10/14 allow-service all vlan openshift_vxlan

   .. note::

      - Specify a subnet mask of ``/14`` when creating the Self IP; this is the subnet range of the default OpenShift cluster network. [#ossdn]_
        This ensures that all VXLAN traffic is correctly routed via the ``openshift_vxlan`` tunnel.
      - If you don't specify a traffic group when creating the Self IP, it will use the default traffic group.

#. Verify creation of the Self IP.

   .. admonition:: TMSH

       admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$ list net self 10.129.2.10/14

.. [#ossdn] https://docs.openshift.org/latest/architecture/additional_concepts/sdn.html#sdn-design-on-masters

.. _k8s-openshift-serviceaccount:

Create an OpenShift service account and policy
-----------------------------------------------

#. Create a serviceaccount for the |kctlr|.

   .. code-block:: console

      user@openshift:~$ oc create serviceaccount bigip-ctlr -n default
      serviceaccount "bigip-ctlr" created

#. Create a valid clusterrole.

   .. code-block:: console

      user@openshift:~$ oc create -f f5-kctlr-openshift-clusterrole.yaml
      clusterrole "system:bigip-ctlr" created

   .. literalinclude:: /_static/config_examples/f5-kctlr-openshift-clusterrole.yaml
      :linenos:

   :fonticon:`fa fa-download` :download:`f5-kctlr-openshift-clusterrole.yaml </_static/config_examples/f5-kctlr-openshift-clusterrole.yaml>`

#. Create a valid clusterrole.

   .. code-block:: console

      user@openshift:~$ oc create -f f5-kctlr-openshift-clusterrole-binding.yaml
      clusterrolebinding "bigip-ctlr-role" created

   .. literalinclude:: /_static/config_examples/f5-kctlr-openshift-clusterrole-binding.yaml
       :linenos:

   :fonticon:`fa fa-download` :download:`f5-kctlr-openshift-clusterrole-binding.yaml </_static/config_examples/f5-kctlr-openshift-clusterrole-binding.yaml>`

Next Steps
----------

- :ref:`Install the F5 Kubernetes BIG-IP Controller <install-kctlr-openshift>`.
- :ref:`Configure the F5 Kubernetes BIG-IP Controller for OpenShift <kctlr-configure-openshift>`.

.. _OpenShift: https://www.openshift.org/
.. _Create an OpenShift service account: https://docs.openshift.org/latest/admin_guide/service_accounts.html
.. _VXLAN profile:
.. _Self IP address: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/tmos-routing-administration-12-1-1/5.html
