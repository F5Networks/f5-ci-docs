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
   1.    :ref:`k8s-flannel-setup`
   ----- ----------------------------------------------------------------------------------
   2.    :ref:`k8s-vxlan-setup`:

         - :ref:`k8s-flannel create bigip vxlan`
         - :ref:`k8s-flannel create bigip self IP`
         - :ref:`k8s-flannel create floating IP`
         - :ref:`k8s-flannel verify objects`

   ----- ----------------------------------------------------------------------------------
   3.    :ref:`add bigip to flannel overlay`

         - :ref:`find vtepMAC`
         - :ref:`find flannel annotations`
         - :ref:`add flannel annotations`
   ===== ==================================================================================


.. _k8s-flannel-setup:

Deploy flannel for Kubernetes
-----------------------------

If you **haven't already deployed flannel** in your Kubernetes Cluster, you can do so using a `kube-flannel`_ manifest file.
The manifest file defines all of the resources required to deploy flannel in Kubernetes.

.. important::

   In the :code:`netconf.json` section of the ConfigMap, the :code:`Backend.Type` must be :code:`vxlan`. The |kctlr| doesn't support other backend modes.

.. _k8s-vxlan-setup:

Set up the BIG-IP system
------------------------

.. include:: /_static/reuse/bigip-admin-permissions-reqd.rst

.. _k8s-flannel create bigip vxlan:

Create a VXLAN tunnel
`````````````````````

#. Create a VXLAN profile with :code:`flooding-type none`.

   .. code-block:: console

      create /net tunnels vxlan fl-vxlan port 8472 flooding-type none

#. Create a VXLAN tunnel.

   - Set the :code:`local-address` to an IP address from the network that will support the VXLAN overlay.
   - Set the :code:`key` to :code:`1` to grant the BIG-IP device access to all Cluster resources.

   \

   .. code-block:: console

      create /net tunnels tunnel flannel_vxlan key 1 profile fl-vxlan local-address 172.16.1.3

.. _k8s-flannel create bigip self IP:

Create a self IP in the VXLAN
`````````````````````````````

#. Identify the flannel subnet you want to assign to the BIG-IP system. Make sure it doesn't overlap with a subnet that's already in use by existing Nodes in the Kubernetes Cluster. You will assign this subnet to a "dummy" Node for the BIG-IP device later.

#. Create a self IP using an address from the subnet you want to assign to the BIG-IP device.

.. code-block:: console

   create /net self 10.244.30.3/16 allow-service none vlan flannel_vxlan

.. important::

   - The subnet mask you assign to the self IP must match that of the flannel network (the default is :code:`/16`).
   - When creating a self IP using the BIG-IP configuration utility instead of TMSH, you may need to provide the full netmask (for example, :code:`255.255.0.0` instead of :code:`/16`).
   - If you do not specify a traffic group, the self IP will use the BIG-IP system's default.

.. _k8s-flannel create floating IP:

Create a floating self IP in the VXLAN
``````````````````````````````````````

Create a floating IP address in the subnet you want to assign to the BIG-IP device. Use the same subnet mask as the flannel network.

.. code-block:: console

   create /net self 10.244.30.4/16 allow-service none traffic-group traffic-group-1 vlan flannel_vxlan

.. note::

   All virtual servers created by the |kctlr| use the `BIG-IP SNAT`_ automap feature, which prefers floating IP addresses over static IPs.
   See :ref:`bigip snats` for more information.

.. _k8s-flannel verify objects:

Verify creation of the BIG-IP objects
`````````````````````````````````````

You can use a TMOS shell or the BIG-IP configuration utility to verify object creation.

.. code-block:: console

   show /net tunnels tunnel flannel_vxlan
   show /net running-config self 10.244.30.3/16
   show /net running-config self 10.244.30.4/16


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

   show /net tunnels tunnel flannel_vxlan all-properties
   -------------------------------------------------
   Net::Tunnel: flannel_vxlan
   -------------------------------------------------
   MAC Address                     ab:12:cd:34:ef:56
   ...

.. _find flannel annotations:

Find the flannel Annotations
````````````````````````````

Run :command:`kubectl describe` for any Node in the Cluster and make note of the flannel Annotations included in the Node description.

.. code-block:: console

   kubectl describe nodes <node>
   ...
   flannel.alpha.coreos.com/backend-data:'{"VtepMAC":"<mac-address>"}'
   flannel.alpha.coreos.com/backend-type: 'vxlan'
   flannel.alpha.coreos.com/kube-subnet-manager: 'true'
   flannel.alpha.coreos.com/public-ip: <node-ip-address>
   ...


.. _add flannel annotations:

Create a Kubernetes Node for the BIG-IP device
``````````````````````````````````````````````

#. Create a Kubernetes Node resource.

   - Include all of the flannel Annotations. Define the :code:`backend-data` and :code:`public-ip` Annotations with data from the BIG-IP VXLAN:

     :code:`flannel.alpha.coreos.com/backend-data:'{"VtepMAC":"<BIG-IP_mac-address>"}'`

     :code:`flannel.alpha.coreos.com/public-ip: <BIG-IP_vtep-address>`

     (This is the :ref:`IP address you assigned to the VXLAN tunnel <k8s-flannel create bigip vxlan>`).

   - Set the :code:`podCIDR` to the subnet you used to :ref:`create the self IP <k8s-flannel create bigip self IP>` and floating IP.

   .. literalinclude:: /kubernetes/config_examples/f5-kctlr-bigip-node.yaml

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

.. seealso::

   If you get a configuration error when trying to create a virtual server using an iApp, see :ref:`Troubleshoot Your Kubernetes Deployment <iapp traffic group>`.


.. _Deploy flannel: https://coreos.com/flannel/docs/latest/kubernetes.html
.. _kube-flannel: https://github.com/coreos/flannel/blob/master/Documentation/kube-flannel.yml
.. _network addon: https://kubernetes.io/docs/concepts/cluster-administration/addons/
