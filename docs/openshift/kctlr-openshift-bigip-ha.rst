.. index::
    single: OpenShift; BIG-IP Controller

.. _bigip ha openshift:

Managing BIG-IP HA Clusters in OpenShift
========================================

.. raw:: html

   <div class="alert alert-danger alert-dismissible">
      <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>
      <strong>Warning!</strong> This solution applies to BIG-IP devices v13.x and later only.
   </div>

You can use the |octlr-long| to manage a BIG-IP High Availability (HA) active-standby pair or device group [#f1]_. You will need to deploy one |kctlr| instance for each BIG-IP device. Each device will connect to a shared subnet that passes client traffic and to a management subnet.

.. figure:: /_static/media/kctlr-openshift-ha.png
   :width: 75%
   :alt: A diagram showing the BIG-IP High Availability solution in an OpenShift cluster. The solution features 2 BIG-IP devices, each of which has its own BIG-IP Controller. Both BIG-IPs have 2 interfaces; one connects to the floating subnet used for client traffic, and the other connects to a subnet used for health monitoring.

Complete the steps below to set up the solution shown in the diagram. Be sure to use the correct IP addresses and subnet masks for your OpenShift Cluster.

.. table:: Tasks

   ===== ==================================================================================
   Step  Task
   ===== ==================================================================================
   1.    :ref:`openshift initial bigip setup ha`

   2.    :ref:`add bigip devices openshift ha`

         - :ref:`openshift create hostsubnets ha`
         - :ref:`openshift upload hostsubnets ha`
         - :ref:`openshift verify hostsubnets ha`

   3.    :ref:`openshift vxlan setup ha`

         - :ref:`openshift create vxlan profile ha`
         - :ref:`openshift create vxlan tunnel ha`
         - :ref:`openshift vxlan selfIP ha`
         - :ref:`openshift vxlan floatingip ha`

   4.    :ref:`openshift deploy kctlr ha`

         - :ref:`openshift rbac ha`
         - :ref:`openshift create deployment ha`
         - :ref:`openshift upload deployment ha`

   ===== ==================================================================================

.. _openshift initial bigip setup ha:

Initial BIG-IP Device Setup
---------------------------

.. include:: /_static/reuse/bigip-admin-permissions-reqd.rst

.. include:: /_static/reuse/kctlr-initial-setup.rst

.. _add bigip devices openshift ha:

Add BIG-IP devices to OpenShift
-------------------------------

.. important::

   The examples below add two BIG-IP devices to the OpenShift cluster. If you have more than two BIG-IPs, be sure to repeat the steps here for each additional device.

.. _openshift create hostsubnets ha:

Define HostSubnets
``````````````````

.. tip:: HostSubnets must use valid YAML or JSON. Using a linter prior to deploying your HostSubnet can cut down on troubleshooting later!

#. Create one HostSubnet for each BIG-IP device. These will handle health monitor traffic.

   .. literalinclude:: /openshift/config_examples/f5-kctlr-openshift-hostsubnet-node01.yaml
      :caption: HostSubnet for BIG-IP 1

   :fonticon:`fa fa-download` :download:`f5-kctlr-openshift-hostsubnet-node01.yaml </openshift/config_examples/f5-kctlr-openshift-hostsubnet-node01.yaml>`

   .. literalinclude:: /openshift/config_examples/f5-kctlr-openshift-hostsubnet-node02.yaml
      :caption: HostSubnet for BIG-IP 2

   :fonticon:`fa fa-download` :download:`f5-kctlr-openshift-hostsubnet-node02.yaml </openshift/config_examples/f5-kctlr-openshift-hostsubnet-node02.yaml>`

#. Create one HostSubnet to pass client traffic. You will create the floating IP address for the active device in this subnet.

   \

   .. literalinclude:: /openshift/config_examples/f5-kctlr-openshift-hostsubnet-float.yaml
      :caption: HostSubnet for client traffic

   :fonticon:`fa fa-download` :download:`f5-kctlr-openshift-hostsubnet-float.yaml </openshift/config_examples/f5-kctlr-openshift-hostsubnet-float.yaml>`

.. _openshift upload hostsubnets ha:

Upload the HostSubnet files to the OpenShift API server
```````````````````````````````````````````````````````

You can upload the files individually using separate :command:`oc create` commands or upload them all at once, as shown below.

.. parsed-literal::

   oc create -f **f5-kctlr-openshift-hostsubnet-node01.yaml** -f **f5-kctlr-openshift-hostsubnet-node02.yaml** -f **f5-kctlr-openshift-hostsubnet-float.yaml**
   hostsubnet **f5-bigip-node01** created
   hostsubnet **f5-bigip-node02** created
   hostsubnet **f5-bigip-float** created

.. _openshift verify hostsubnets ha:

Verify creation of the HostSubnets
``````````````````````````````````

Use :command:`oc get` to retrieve information about your newly-created HostSubnets. Record the :code:`hostIP` and :code:`subnet` values for each; you will use these when setting up the VXLAN on your BIG-IP devices.

.. parsed-literal::

   oc get hostsubnet
   NAME	               HOST	               HOST IP	     SUBNET

   f5-bigip-float       f5-bigip-float       **172.16.1.30**   **10.129.6.0/23**
   f5-bigip-node01      f5-bigip-node01      **172.16.1.28**   **10.129.2.0/23**
   f5-bigip-node02      f5-bigip-node02      **172.16.1.29**   **10.129.4.0/23**
   ...

.. _openshift vxlan setup ha:

Set up the VXLAN on the BIG-IP devices
--------------------------------------

.. include:: /_static/reuse/bigip-admin-permissions-reqd.rst

Take the steps below on each BIG-IP device in the pair or cluster.

.. _openshift create vxlan profile ha:

Create a VXLAN profile
``````````````````````

In a TMOS shell, create a VXLAN profile that uses multi-cast flooding.

.. code-block:: bash

   create /net tunnels vxlan ose-vxlan flooding-type multipoint

.. _openshift create vxlan tunnel ha:

Create a VXLAN tunnel
`````````````````````

- Use the :code:`hostIP` IP address provided for the "float" HostSubnet as the VXLAN's :code:`local-address`.
- Use the :code:`hostIP` IP address provided for the BIG-IP node's HostSubnet as the VXLAN’s :code:`secondary-address`.
- Set the :code:`key` to :code:`0` to grant the BIG-IP device access to all OpenShift projects and subnets.

.. rubric:: BIG-IP Node 01

.. parsed-literal::

   create /net tunnels tunnel **openshift_vxlan** key **0** profile **ose-vxlan** local-address **172.16.1.30** secondary-address **172.16.1.28** traffic-group **traffic-group-1**

.. rubric:: BIG-IP Node 02

.. parsed-literal::

   create /net tunnels tunnel **openshift_vxlan** key **0** profile **ose-vxlan** local-address **172.16.1.30** secondary-address **172.16.1.29** traffic-group **traffic-group-1**

.. _openshift vxlan selfIP ha:

Create a self IP in the VXLAN
`````````````````````````````

Create a self IP address in the VXLAN on each device.

- The self IP range must fall within the cluster subnet mask. Use the command :command:`oc get clusternetwork` to find the correct subnet mask for your cluster.
- If you use the BIG-IP configuration utility to create a self IP, you may need to provide the full netmask instead of the CIDR notation.
- Be sure to specify a floating traffic group (for example, :code:`traffic-group-1`). Otherwise, the self IP will use the BIG-IP system's default.

.. rubric:: BIG-IP Node 01

.. parsed-literal::

   create /net self **10.129.2.3/14** allow-service **none** vlan **openshift_vxlan**

.. rubric:: BIG-IP Node 02

.. parsed-literal::

   create /net self **10.129.4.3/14** allow-service **none** vlan **openshift_vxlan**

.. seealso::
   :class: sidebar

   See :ref:`networking troubleshoot openshift` if you're having trouble with your network setup.

.. _openshift vxlan floatingip ha:

Create a floating IP in the VXLAN
`````````````````````````````````

#. On the active device, create a floating IP address in the subnet assigned by the OpenShift SDN.

   .. parsed-literal::

      create /net self **10.129.6.4/14** allow-service **none** traffic-group **traffic-group-1** vlan **openshift_vxlan**

#. In a TMOS shell, run the :command:`config-sync` command to sync your changes to the device group.

   .. parsed-literal::

      run /cm config-sync to-group **<sync_group>**


.. _openshift deploy kctlr ha:

Deploy the BIG-IP Controller
----------------------------

Take the steps below to deploy a |kctlr| for each BIG-IP device in the cluster.

.. _openshift rbac ha:

Set up RBAC
```````````

.. include:: /_static/reuse/kctlr-openshift-set-up-rbac.rst

.. _openshift create deployment ha:

Create Deployments
``````````````````

Create an OpenShift Deployment for each Controller (one per BIG-IP device):

- Provide a unique :code:`metadata.name` for each Controller.
- Provide a unique :code:`--bigip-url` in each Deployment (each Controller manages a separate BIG-IP device).
- Use the same :code:`--bigip-partition` in all Deployments.

.. important::

   Do not define multiple Deployment configs in a single manifest.

   If you launch multiple |kctlr| instances using a single manifest, they will run on the same Pod. This means that if the Pod goes down, you lose all of your Controllers.

   The example Deployments below include the settings that the |kctlr| needs to manage OpenShift Routes.
   If you don't need/want to manage Routes, exclude the following settings:

   - :code:`"--manage-routes=true"`
   - :code:`"--route-vserver-addr=1.2.3.4"`
   - :code:`"--route-label=App1"`

   See :ref:`kctlr-openshift-routes` for additional information.

.. literalinclude:: /openshift/config_examples/f5-k8s-bigip-ctlr_openshift-node01-route.yaml
   :caption: BIG-IP Controller 1
   :linenos:

:fonticon:`fa fa-download` :download:`Download f5-k8s-bigip-ctlr_openshift-node01-route.yaml </openshift/config_examples/f5-k8s-bigip-ctlr_openshift-node01-route.yaml>`

.. literalinclude:: /openshift/config_examples/f5-k8s-bigip-ctlr_openshift-node02-route.yaml
   :caption: BIG-IP Controller 2
   :linenos:

:fonticon:`fa fa-download` :download:`Download f5-k8s-bigip-ctlr_openshift-node02-route.yaml </openshift/config_examples/f5-k8s-bigip-ctlr_openshift-node02-route.yaml>`


.. _openshift upload deployment ha:

Upload the Deployments
``````````````````````

#. Upload the Deployments to the OpenShift API server.

   .. parsed-literal::

      oc create -f **f5-k8s-bigip-ctlr_openshift-node01-routes.yaml** -f **f5-k8s-bigip-ctlr_openshift-node02-routes.yaml**
      deployment "f5-bigip-ctlr-01" created
      deployment "f5-bigip-ctlr-02" created

#. Verify Pod creation.

   .. code-block:: console

      oc get pods
      NAME                                    READY     STATUS    RESTARTS   AGE
      f5-bigip-ctlr-01-1530682540-7rs5s         1         1         1         5m
      f5-bigip-ctlr-02-5973567192-trh2W         1         1         1         5m

.. rubric:: **Footnotes**
.. [#f1] Does not apply to BIG-IP devices v12.x and earlier.
