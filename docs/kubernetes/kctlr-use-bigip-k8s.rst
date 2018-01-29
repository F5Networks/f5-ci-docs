.. index::
   single: BIG-IP; Kubernetes; flannel; Network set-up; VXLAN

.. sidebar:: Docs test matrix

   Documentation manually tested with:

   - BIG-IP v12.1.1
   - Kubernetes v1.7.5
   - flannel v0.9.0

.. _use-bigip-k8s-flannel:

Add BIG-IP device to flannel VXLAN
==================================

This document provides step-by-step instructions for adding a BIG-IP device to a Kubernetes Cluster using flannel VXLAN. For more information about this integration, see :ref:`flannel-bigip-info`.

Complete the following tasks to add a BIG-IP device to a `Kubernetes`_ `Cluster Network`_ using `flannel`_.

.. table:: Task table

   ===== ==================================================================================
   Step  Task
   ===== ==================================================================================
   1.    :ref:`k8s-flannel-setup`.
   ----- ----------------------------------------------------------------------------------
   2.    :ref:`k8s-vxlan-setup`:

         - :ref:`k8s-flannel create bigip vxlan`
         - :ref:`k8s-flannel create bigip self IP`
         - :ref:`k8s-flannel verify objects`

   ----- ----------------------------------------------------------------------------------
   3.    :ref:`add bigip to flannel overlay`

         - :ref:`find vtepMAC`
         - :ref:`add flannel annotations`

   ===== ==================================================================================


.. _k8s-flannel-setup:

Deploy flannel for Kubernetes
-----------------------------

Take step 1 if you **haven't already deployed flannel** in your Kubernetes Cluster.

#. `Deploy flannel`_ :fonticon:`fa fa-external` using a `kube-flannel`_ manifest file.

   The manifest files defines all of the resources required to deploy flannel in Kubernetes.
   In the :code:`netconf.json` section of the ConfigMap:

   - Set :code:`Backend.Type` to :code:`vxlan`. The |kctlr| doesn't support other backend modes.
   - Set :code:`Network` to the desired network range, in CIDR format (for example, ``10.244.30.15/16``).

#. Run :command:`kubectl describe` and make note of the flannel Annotations included in the Node description.

   .. code-block:: console

      kubectl describe nodes flannel
      ...
      flannel.alpha.coreos.com/backend-data:'{"VtepMAC":"<mac-address>"}'
      flannel.alpha.coreos.com/backend-type: 'vxlan'
      flannel.alpha.coreos.com/kube-subnet-manager: 'true'
      flannel.alpha.coreos.com/public-ip: 172.16.1.3
      ...

.. _k8s-vxlan-setup:

Set up the BIG-IP system
------------------------

.. _k8s-flannel create bigip vxlan:

Create a VXLAN tunnel
`````````````````````

#. Create a VXLAN profile with :code:`flooding-type none`.

   .. code-block:: console
      :caption: ``admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$``

      create /net tunnels vxlan fl-vxlan port 8472 flooding-type none

#. Create a VXLAN tunnel.

   - Set the :code:`local-address` to the :code:`public-ip` address returned by :command:`kubectl describe` (in this example, ``172.16.1.3``).
   - Set the ``key`` to ``1`` to grant the BIG-IP device access to all Cluster resources.

   .. code-block:: console
      :caption: ``admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$``

      create/net tunnels tunnel flannel_vxlan key 1 profile fl-vxlan local-address 172.16.1.3

.. _k8s-flannel create bigip self IP:

Create a self IP in the VXLAN
`````````````````````````````

.. important::

   - The self IP's subnet mask must match that of the flannel network. The default is ``/16``.
   - If you are managing a BIG-IP device cluster, *you must assign a floating traffic group to the self IP* to ensure proper routing. See :ref:`bigip snats` for more information.
   - If you do not select a specific traffic group, the self IP will use the BIG-IP system's default traffic group.
   - If you create a self IP using the BIG-IP configuration utility, you may need to provide the full netmask instead of CIDR format (for example, :code:`255.255.0.0`).

.. code-block:: console
   :caption: ``admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$``

   create /net self flannel 10.244.30.15/16 allow-service all traffic-group 1 vlan flannel_vxlan

.. _k8s-flannel verify objects:

Verify creation of the BIG-IP objects
`````````````````````````````````````

You can use a TMOS shell or the BIG-IP configuration utility to verify object creation.

.. code-block:: console
   :caption: ``admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$``

   show /net tunnels tunnel flannel_vxlan
   show /net running-config self flannel


.. _add bigip to flannel overlay:
.. _k8s-bigip-node:

Add the BIG-IP device to the flannel overlay network
----------------------------------------------------

Flannel uses a set of custom Annotations to identify Nodes as part of the Cluster network. When you create a dummy Node resource for the BIG-IP that contains these Annotations, flannel can discover the BIG-IP device and monitor it as part of the VXLAN.

.. _find vtepMAC:

Find the VTEP MAC address
`````````````````````````

You can find the MAC address of your BIG-IP VXLAN tunnel using a TMOS shell.

.. code-block:: console
   :caption: ``admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$``

   show /net tunnels tunnel flannel_vxlan all-properties

   -------------------------------------------------
   Net::Tunnel: flannel_vxlan
   -------------------------------------------------
   MAC Address                     ab:12:cd:34:ef:56
   ...


.. _add flannel annotations:

Create a Kubernetes Node for the BIG-IP device
``````````````````````````````````````````````

#. Create a Kubernetes Node resource containing the flannel Annotations.

   Provide the MAC address of the BIG-IP VTEP as the ``VtepMAC`` address in the flannel ``backend-data`` Annotation.

   .. literalinclude:: /kubernetes/config_examples/f5-kctlr-bigip-node.yaml
      :linenos:
      :emphasize-lines: 8-12, 17

   :fonticon:`fa fa-download` :download:`f5-kctlr-bigip-node.yaml </kubernetes/config_examples/f5-kctlr-bigip-node.yaml>`

#. Upload the Node resource to the Kubernetes API server.

   .. code-block:: console

      kubectl create -f f5-kctlr-bigip-node.yaml

#. Verify creation of the BIG-IP Node.

   .. code-block:: console
      :emphasize-lines: 3

      kubectl get nodes
      NAME           STATUS    AGE       VERSION
      bigip          Ready     5m        v1.7.5
      k8s-master-0   Ready     2d        v1.7.5
      k8s-worker-0   Ready     2d        v1.7.5
      k8s-worker-1   Ready     2d        v1.7.5


You should now be able to successfully send traffic through the BIG-IP system to and from endpoints within your Kubernetes Cluster.

What's Next
-----------

- :ref:`Install the F5 BIG-IP Controller in Kubernetes <install-kctlr>`
- :ref:`Configure the F5 BIG-IP Controller for use in Kubernetes <kctlr-configuration>`

.. seealso:: See :ref:`iapp traffic group` if you get a configuration error when trying to create a virtual server using an iApp.


.. _Deploy flannel: https://coreos.com/flannel/docs/latest/kubernetes.html
.. _kube-flannel: https://github.com/coreos/flannel/blob/master/Documentation/kube-flannel.yml
.. _network addon: https://kubernetes.io/docs/concepts/cluster-administration/addons/
