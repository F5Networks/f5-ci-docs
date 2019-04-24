:product: BIG-IP Controller for Kubernetes
:type: task

.. _use-bigip-k8s-flannel:

Add BIG-IP device to flannel VXLAN
==================================

This document provides step-by-step instructions for adding a BIG-IP device to a Kubernetes Cluster using flannel VXLAN. For more information about this integration, see :ref:`flannel-bigip-info`.

Complete the following tasks to add a BIG-IP device to a `Kubernetes`_ `Cluster Network`_ using `flannel`_.

.. table:: Task Summary

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

.. important::

   The steps in this section require Administrator or Resource Administrator access to the TMOS shell (tmsh).

.. _k8s-flannel create bigip vxlan:

Create a VXLAN tunnel
`````````````````````

#. Log in to the TMOS shell (tmsh).

   .. parsed-literal::

      tmsh

#. Create a VXLAN profile with :code:`flooding-type none`.

   .. parsed-literal::

      create /net tunnels vxlan **fl-vxlan** port **8472** flooding-type **none**

#. Create a VXLAN tunnel.

   - Set the :code:`local-address` to an IP address from the network that will support the VXLAN overlay.
   - Set the :code:`key` to :code:`1` to grant the BIG-IP device access to all Cluster resources.

   .. parsed-literal::

      create /net tunnels tunnel **flannel_vxlan** key **1** profile **fl-vxlan** local-address **172.16.1.28**

.. _k8s-flannel create bigip self IP:

Create a self IP in the VXLAN
`````````````````````````````

#. Identify the flannel subnet you want to assign to the BIG-IP system. Make sure it doesn't overlap with a subnet that's already in use by existing Nodes in the Kubernetes Cluster. You will assign this subnet to a "dummy" Node for the BIG-IP device later.

#. Create a self IP using an address from the subnet you want to assign to the BIG-IP device.

.. important::

   - The self IP range must fall within the cluster subnet mask. The flannel network's default subnet mask is :code:`/16`.
   - If you use the BIG-IP configuration utility to create a self IP, you may need to provide the full netmask instead of the CIDR notation.

.. parsed-literal::

   create /net self **10.129.2.3/16** allow-service **none** vlan **flannel_vxlan**

.. _k8s-flannel create floating IP:

Create a floating self IP in the VXLAN
``````````````````````````````````````

Create a floating IP address in the flannel subnet you assigned to the BIG-IP device.

.. parsed-literal::

   create /net self **10.129.2.4/16** allow-service **none** traffic-group **traffic-group-1** vlan **flannel_vxlan**

.. include:: /_static/reuse/kctlr-snat-note.rst

.. _k8s-flannel verify objects:

Verify creation of the BIG-IP objects
`````````````````````````````````````

You can use a TMOS shell or the BIG-IP configuration utility to verify object creation.

.. parsed-literal::

   show /net tunnels tunnel **flannel_vxlan**
   show /net running-config self **10.129.2.3/16**
   show /net running-config self **10.129.2.4/16**

.. _add bigip to flannel overlay:
.. _k8s-bigip-node:

Add the BIG-IP device to the flannel overlay network
----------------------------------------------------

Flannel uses a set of custom Annotations to identify Nodes as part of the Cluster network.
When you create a dummy Node resource for the BIG-IP that contains these Annotations, flannel can discover the BIG-IP device and monitor it as part of the VXLAN.

.. _find vtepMAC:

Find the VTEP MAC address
`````````````````````````

You can find the MAC address of your BIG-IP VXLAN tunnel using a TMOS shell.

.. parsed-literal::

   show /net tunnels tunnel **flannel_vxlan all-properties**
   -------------------------------------------------
   Net::Tunnel: flannel_vxlan
   -------------------------------------------------
   MAC Address                   **ab:12:cd:34:ef:56**
   ...

.. _find flannel annotations:

Find the flannel Annotations
````````````````````````````

Run :command:`kubectl describe` for any Node in the Cluster and make note of the flannel Annotations included in the Node description.

.. code-block:: console

   kubectl describe nodes
   ...
   flannel.alpha.coreos.com/backend-data:'{"VtepMAC":"<mac-address>"}'
   flannel.alpha.coreos.com/backend-type: 'vxlan'
   flannel.alpha.coreos.com/kube-subnet-manager: 'true'
   flannel.alpha.coreos.com/public-ip: <node-ip-address>
   ...


.. _add flannel annotations:

Create a Kubernetes Node for the BIG-IP device
``````````````````````````````````````````````

.. important::
   :class: sidebar

   The BIG-IP dummy Node's status will always be **"NotReady"** because it is not a fully-participating Kubernetes Node (in other words, it's not a Node on which Kubernetes can schedule resources).
   This status does not affect the BIG-IP device's ability to communicate in the overlay network.

#. Create a "dummy" Kubernetes Node resource.

   Include all of the flannel Annotations. Define the :code:`backend-data` and :code:`public-ip` Annotations with data from the BIG-IP VXLAN:

   :code:`flannel.alpha.coreos.com/backend-data:'{"VtepMAC":"<BIG-IP_mac-address>"}'`

   :code:`flannel.alpha.coreos.com/public-ip: <BIG-IP_vtep-address>`

   (This is the :ref:`IP address you assigned to the VXLAN tunnel <k8s-flannel create bigip vxlan>`).

   - Set the :code:`podCIDR` to the subnet you used to :ref:`create the self IP <k8s-flannel create bigip self IP>` and floating IP.

   .. literalinclude:: /kubernetes/config_examples/f5-kctlr-bigip-node.yaml

   :fonticon:`fa fa-download` :download:`f5-kctlr-bigip-node.yaml </kubernetes/config_examples/f5-kctlr-bigip-node.yaml>`

#. Upload the Node resource to the Kubernetes API server.

   .. parsed-literal::

      kubectl create -f **f5-kctlr-bigip-node.yaml**

#. Verify creation of the Node.

   .. code-block:: console
      :emphasize-lines: 3

      kubectl get nodes
      NAME           STATUS    AGE       VERSION
      bigip          NotReady  5m        v1.7.5
      k8s-master-0   Ready     2d        v1.7.5
      k8s-worker-0   Ready     2d        v1.7.5
      k8s-worker-1   Ready     2d        v1.7.5


What's Next
-----------

Now that your BIG-IP device is part of the Cluster network, you'll need to :ref:`Deploy the BIG-IP Controller <install-kctlr>`.

.. seealso::

   - If you're having trouble with your network setup, see :ref:`networking troubleshoot openshift`.
     (This troubleshooting issue references the OpenShift Cluster Network, but the concepts are the same.)
   - If you get a traffic group configuration error when trying to create a virtual server with an iApp, see :ref:`Troubleshoot Your Kubernetes Deployment <iapp traffic group>`.


.. _Deploy flannel: https://coreos.com/flannel/docs/latest/kubernetes.html
.. _kube-flannel: https://github.com/coreos/flannel/blob/master/Documentation/kube-flannel.yml
.. _network addon: https://kubernetes.io/docs/concepts/cluster-administration/addons/
