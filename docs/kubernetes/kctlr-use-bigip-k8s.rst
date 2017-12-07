.. index::
   single: BIG-IP; Kubernetes; flannel; Network set-up; VXLAN

.. sidebar:: Docs test matrix

   Documentation manually tested with:

   - BIG-IP v12.1.1
   - Kubernetes v1.7.5
   - flannel v0.9.0

.. _bigip-k8s-setup:

Add your BIG-IP device to a Kubernetes Cluster using flannel VXLAN
==================================================================

This document provides step-by-step instructions for adding a BIG-IP device to a Kubernetes Cluster using flannel VXLAN. For more information about this integration, see :ref:`flannel-bigip-info`.

.. important::

   When you add your BIG-IP device to the Cluster Network, you should run the |kctlr| in ``cluster`` mode (``--pool-member-type=cluster``). See :ref:`cluster mode` for more information.

Tasks
-----

Complete the following tasks to add a BIG-IP device to a `Kubernetes`_ `Cluster Network`_ using `flannel`_.

===== ==================================================================================
Step  Task
===== ==================================================================================
1.    :ref:`k8s-vxlan-setup`
----- ----------------------------------------------------------------------------------
2.    :ref:`k8s-flannel-setup`.
----- ----------------------------------------------------------------------------------
3.    :ref:`k8s-bigip-node`
----- ----------------------------------------------------------------------------------
4.    :ref:`k8s-assign-ip`
===== ==================================================================================

\

.. _k8s-vxlan-setup:

Create a VXLAN tunnel on the BIG-IP device
------------------------------------------

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

Deploy flannel for Kubernetes
-----------------------------

Most users deploy flannel as a `network addon`_ when setting up ``kubeadm``. See Kubernetes` :k8sdocs:`Installing a Pod network <setup/independent/create-cluster-kubeadm/#pod-network>` guide for instructions.

**If you want to install flannel manually**, take the steps below.

#. (Optional) Edit the flannel `kube-flannel manifest`_.

   - ``Backend``: Defaults to ``vxlan``; see `Backends <https://github.com/coreos/flannel/blob/master/Documentation/backends.md>`_ for additional information.
   - ``Network``: Should match the Pod network CIDR. Flannel will populate this information automatically.

#. Use :command:`kubectl apply` to deploy the flannel manifest.

   .. code-block:: console

      kubectl apply -f kube-flannel.yaml --namespace=kube-system

   \

.. seealso::

   For more information about flannel and Kubernetes, see `Using flannel with Kubernetes`_.

#. Verify flannel deployment.

   Check the Node resource(s) for the following Annotations: ::

      flannel.alpha.coreos.com/backend-data:'{"VtepMAC":"<mac-address>"}'
      flannel.alpha.coreos.com/backend-type: 'vxlan'
      flannel.alpha.coreos.com/kube-subnet-manager: 'true'
      flannel.alpha.coreos.com/public-ip: <vtep-ip-address>

   \

   - The ``kube-subnet-manager`` annotation tells flannel to use the Kubernetes API (instead of ``etcd``) to find the information it cares about.
   - The ``kube-subnet-manager`` allocates an IP address from the Node's subnet and populates the ``public-ip`` annotation.


.. _k8s-bigip-node:

Create a dummy Kubernetes Node for the BIG-IP device
----------------------------------------------------

.. note::

   Flannel uses a set of custom Annotations to discover information about all Nodes in the Kubernetes Cluster. When you add these Annotations to the BIG-IP Node resource, flannel can discover the BIG-IP device and monitor it as part of the VXLAN.

#. Create a Node resource using valid JSON or YAML.

   .. important::

      You must include the "annotation" section shown in the example below.

   .. literalinclude:: /kubernetes/config_examples/f5-kctlr-bigip-node.yaml
      :linenos:
      :emphasize-lines: 8-10, 12, 17

   :fonticon:`fa fa-download` :download:`f5-kctlr-bigip-node.yaml </kubernetes/config_examples/f5-kctlr-bigip-node.yaml>`

   .. code-block:: console

      kubectl create -f f5-kctlr-bigip-node.yaml

#. Verify creation of the BIG-IP Node.

   .. code-block:: console
      :emphasize-lines: 3

      kubectl get nodes
      NAME           STATUS    AGE       VERSION
      bigip          Unknown   30s
      k8s-master-0   Ready     2d        v1.7.5
      k8s-worker-0   Ready     2d        v1.7.5
      k8s-worker-1   Ready     2d        v1.7.5

.. _k8s-assign-ip:

Add the BIG-IP device to the flannel overlay network
----------------------------------------------------

#. Create a BIG-IP `self IP address`_.

   - Use an address in the range you allocated to the :ref:`BIG-IP Node <k8s-bigip-node>`.
     **This ensures that all VXLAN traffic is correctly routed via the** :code:`flannel_vxlan` **tunnel.** [#fdocs]_
   - Assign a subnet mask matching that of the flannel cluster network. The default is ``/16``.

     .. tip::

        When creating a self IP using the BIG-IP configuration utility, you may need to provide the full netmask (for example, :code:`255.255.0.0`).

   - If you don't specify a traffic group, the self IP will use the BIG-IP system's default.

   .. code-block:: console

      admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$ create net self 10.244.30.15/16 allow-service all vlan flannel_vxlan


.. seealso:: See :ref:`iapp traffic group` if you get a configuration error when trying to create a virtual server via an iApp.

What's Next
-----------

- :ref:`Install the F5 BIG-IP Controller in Kubernetes <install-kctlr>`
- :ref:`Configure the F5 BIG-IP Controller for use in Kubernetes <kctlr-configuration>`

.. rubric:: Footnotes
.. [#fdocs] See the `Flannel documentation <https://github.com/coreos/flannel#flannel>`_.

.. _kube-flannel manifest: https://github.com/coreos/flannel/blob/master/Documentation/kube-flannel.yml
.. _network addon: https://kubernetes.io/docs/concepts/cluster-administration/addons/
