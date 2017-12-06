.. index::
   single: BIG-IP Controller
   single: BIG-IP high availability
   single: Cloud Foundry
   single: Kubernetes
   single: OpenShift
   single: Marathon

.. _manage BIG-IP HA:

How to manage BIG-IP HA pairs
=============================

The F5 Container Connectors provide platform-native integrations for BIG-IP devices from PaaS providers like Cloud Foundry, Kubernetes, Mesos, & OpenShift. The BIG-IP Controllers for these platforms translate native commands to F5 Python SDK/iControl REST calls. [#cccl]_

You can use any BIG-IP Controller to manage a BIG-IP HA active-standby pair or device group. While the platform details vary, all of the Controllers operate on the same basic principle: To provide redundancy, run one (1) Controller instance for each BIG-IP device.

**For example**:

You have one (1) active and one (1) standby BIG-IP device. You want to manage a Kubernetes Cluster in a single partition on the BIG-IP system. [#mtuc1]_. For your HA setup, you'd deploy two (2) |kctlr| instances - one for each BIG-IP device. To ensure Controller HA, deploy each Controller instance on a separate node in the cluster.

.. figure:: /_static/media/bigip-ha.png
   :alt: A diagram showing a BIG-IP active-standby device pair and 2 BIG-IP Controllers, running on separate nodes in a Kubernetes Cluster.

.. [#cccl] See `Introduction to F5 Common Controller Core Library <https://devcentral.f5.com/articles/introduction-to-f5-common-controller-core-library-cccl-28355>`_ on DevCentral for more information.

BIG-IP config sync
------------------

.. warning::

   F5 does not recommended using automatic configuration sync for BIG-IP devices managed by BIG-IP Controllers. The BIG-IP Controller automatically reconfigures its managed device if it discovers changes from what it knows to be the desired state.

   This means that the Controller overwrites *all manual changes*, whether made directly to the managed BIG-IP device or to a BIG-IP that automatically syncs its configuration to the managed BIG-IP device.

If you do use config sync, you should deploy one (1) |kctlr| instance to manage the active device. If you manually sync device group configurations, be sure to always sync configurations *from* the BIG-IP device managed by the |kctlr| *to* the other devices in the group. The Controller will overwrite any changes synced to its managed device from other devices in the group.

.. important::

   If you use tunnels to connect your BIG-IP HA pair to the Cluster network, you should disable config sync for tunnels. See "About configuring VXLAN tunnels on high availability BIG-IP device pairs in the `BIG-IP TMOS Tunneling and IPsec Guide <https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/bigip-tmos-tunnels-ipsec-13-0-0/2.html>`_ for more information.

Examples
--------

Cloud Foundry
`````````````

In Cloud Foundry, the |cf-long| creates a single HTTP BIG-IP virtual server by default [#cf]_. This virtual server is the entry point for all traffic coming into the cloud.

To deploy identical |cfctlr| instances for each BIG-IP device in an active-standby pair, take the steps below.

#. :ref:`Create an Application Manifest <create-application-manifest>` for each ``cf-bigip-ctlr`` instance.

#. Include the correct IP address or hostname for each BIG-IP device in each manifest.

   .. literalinclude:: /cloudfoundry/config_examples/manifest_ha-active.yaml
      :emphasize-lines: 8
      :caption: Deployment with IP address for active BIG-IP device

#. Deploy each App to the appropriate cloud.

   .. code-block:: console

      cf push -o f5networks/cf-bigip-ctlr -f manifest_ha-active.yaml

   .. code-block:: console

      cf push -o f5networks/cf-bigip-ctlr -f manifest_ha-standby.yaml


.. [#cf] See :ref:`BIG-IP Controller for Cloud Foundry <cf-home>` for more information.

Kubernetes/OpenShift
````````````````````

.. sidebar:: :fonticon:`fa fa-info-circle` Did you know?

   In most cases, OpenShift users can substitute :command:`oc` for :command:`kubectl`.

#. :ref:`Set up RBAC <k8s-rbac>` as needed.
#. :ref:`Create a Deployment <k8s-bigip-ctlr-deployment>` for each ``k8s-bigip-ctlr`` instance.
#. Provide the IP address/hostname for the active device in one Deployment, and the standby device in the other Deployment.

   .. literalinclude:: /kubernetes/config_examples/f5-k8s-bigip-ctlr_ha-active.yaml
      :emphasize-lines: 31
      :caption: Deployment with IP address for active BIG-IP device

#. Upload the Deployments to the Kubernetes/OpenShift API server.

   .. code-block:: console

      kubectl apply -f f5-k8s-bigip-ctlr_ha-active.yaml --namespace=kube-system
      deployment "k8s-bigip-ctlr-deployment" created

   .. code-block:: console

      kubectl apply -f f5-k8s-bigip-ctlr_ha-standby.yaml --namespace=kube-system
      deployment "k8s-bigip-ctlr-deployment" created

.. seealso::

   `Learn how to deploy Pods to specific Nodes in Kubernetes <https://kubernetes.io/docs/concepts/configuration/assign-pod-node/>`_.


Mesos
`````

#. :ref:`Set up RBAC <mesos-authentication>` as needed.
#. :ref:`Create a JSON Application file <mctlr-deploy>` for each marathon-bigip-ctlr instance.
#. Include the correct IP address or hostname for each BIG-IP device in each Deployment.

   .. literalinclude:: /marathon/config_examples/f5-marathon-bigip-ctlr_ha-active.json
      :emphasize-lines: 16

#. Deploy the Application using the `Marathon Web Interface`_ or the REST API.

   .. code-block:: console

      curl -X POST -H "Content-Type: application/json" http://<marathon_uri>/v2/apps -d @f5-marathon-bigip-ctlr_ha-active.json



