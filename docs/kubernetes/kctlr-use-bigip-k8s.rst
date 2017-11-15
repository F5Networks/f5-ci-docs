.. _bigip-k8s-setup:

How to add your BIG-IP device to a Kubernetes Cluster
=====================================================

.. sidebar:: Docs test matrix

   We tested this documentation with:

   - BIG-IP v12.1.1
   - Kubernetes v1.7.5
   - Flannel v0.9.0

Tasks
-----

Complete the following tasks to add a BIG-IP device to a `Kubernetes`_ cluster network.

===== ==================================================================================
Step  Task
===== ==================================================================================
1.    :ref:`Create a VXLAN tunnel <k8s-vxlan-setup>` on the BIG-IP device.
----- ----------------------------------------------------------------------------------
2.    :ref:`Configure Flannel for Kubernetes <k8s-flannel-setup>`.
----- ----------------------------------------------------------------------------------
3.    :ref:`Create a fake 'bigip' node <k8s-bigip-node>` in your Kubernetes cluster.
----- ----------------------------------------------------------------------------------
4.    :ref:`Assign an overlay address <k8s-assign-ip>` from the Flannel subnet to a
      BIG-IP `Self IP address`_.
===== ==================================================================================

\

.. _k8s-vxlan-setup:

Create a BIG-IP VXLAN tunnel
----------------------------

#. Create a new BIG-IP VXLAN profile.

   .. code-block:: console

      admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$ create net tunnels vxlan fl-vxlan port 8472 flooding-type none

#. Verify creation of the VXLAN profile.

   .. code-block:: console

      admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$ list net tunnels vxlan fl-vxlan


#. Create a new BIG-IP VXLAN tunnel.

   - Use the BIG-IP VTEP (internal) address as the VXLAN ``local-address``.
   - Set the ``key`` to ``1`` to grant the BIG-IP device access to all Kubernetes/Flannel projects and subnets.

   .. code-block:: console

      admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$ create net tunnels tunnel flannel_vxlan key 1 profile fl-vxlan local-address 172.16.1.3

#. Verify creation of the VXLAN tunnel.

   .. code-block:: console

      admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$ list net tunnels tunnel flannel_vxlan


.. _k8s-flannel-setup:

Configure Flannel for Kubernetes
--------------------------------
In order to deploy Flannel in your Kubernetes cluster, use the `kube-flannel.yml`_ file provided by Flannel.
You can manually create this or use it as a `network addon`_ during kubeadm's setup. This file deploys Flannel
on each Kubernetes Node, configuring the VXLAN network.

For further information on running Flannel in Kubernetes, see the `Flannel Kubernetes documentation`_.


.. _k8s-bigip-node:

Create a new Kubernetes BIG-IP Node
-----------------------------------

Flannel needs to know the BIG-IP device's configuration in order to add the device to the VXLAN network.
Flannel monitors `Kubernetes Node`_ annotations to do this. We must define the BIG-IP device as a Node
in Kubernetes with the proper annotations so Flannel can monitor it.

#. Define a Node using valid JSON or YAML.

   .. important::

      You must include the "annotation" section shown in the example below.


   .. literalinclude:: /kubernetes/config_examples/f5-kctlr-bigip-node.yaml
      :linenos:
      :emphasize-lines: 8-10, 12, 17

   :fonticon:`fa fa-download` :download:`f5-kctlr-bigip-node.yaml </kubernetes/config_examples/f5-kctlr-bigip-node.yaml>`

   .. code-block:: console

      kubectl create -f f5-kctlr-bigip-node.yaml

#. Verify creation of the Node.

   .. code-block:: console
      :emphasize-lines: 3

      kubectl get nodes
      NAME           STATUS    AGE       VERSION
      bigip          Unknown   30s
      k8s-master-0   Ready     2d        v1.7.5
      k8s-worker-0   Ready     2d        v1.7.5
      k8s-worker-1   Ready     2d        v1.7.5


.. _k8s-assign-ip:

Add the BIG-IP device to the Flannel overlay network
------------------------------------------------------

#. Create a BIG-IP self IP address.

   - Use an address in the range allocated for the :ref:`Node <k8s-bigip-node>` created earlier.
     **This ensures that all VXLAN traffic is correctly routed via the** :code:`flannel_vxlan` **tunnel.** [#flannel]_
   - Assign a subnet mask that matches that of the Flannel cluster network. The default is ``/16``.

     .. tip::

        When creating a self IP using the BIG-IP configuration utility, specify the full netmask (for example, :code:`255.255.0.0`).

   - If you don't specify a traffic group, the self IP uses the BIG-IP system's default.

   .. code-block:: console

      admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$ create net self 10.244.30.15/16 allow-service all vlan flannel_vxlan

.. note::

    Be sure to set the |kctlr|'s pool-member-type to `cluster` mode, rather than the default `nodeport` mode,
    in order to take advantage of the direct-to-pod networking that you have now enabled.


Next Steps
----------

- :ref:`Install the F5 BIG-IP Controller in Kubernetes <install-kctlr>`
- :ref:`Configure the F5 BIG-IP Controller for use in Kubernetes <kctlr-configuration>`

.. rubric:: Footnotes
.. [#flannel] See the `Flannel documentation <https://github.com/coreos/flannel#flannel>`_.

.. _kube-flannel.yml: https://github.com/coreos/flannel/blob/master/Documentation/kube-flannel.yml
.. _network addon: https://kubernetes.io/docs/concepts/cluster-administration/addons/
.. _Flannel Kubernetes documentation: https://github.com/coreos/flannel/blob/master/Documentation/kubernetes.md
.. _Self IP address: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/tmos-routing-administration-12-1-1/5.html
