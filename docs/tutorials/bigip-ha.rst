.. index::
   single: BIG-IP Controller
   single: BIG-IP high availability
   single: Cloud Foundry
   single: Kubernetes
   single: OpenShift
   single: Marathon

.. _manage BIG-IP HA:

Manage BIG-IP HA pairs with the F5 Container Connectors
=======================================================

The F5 Container Connectors provide platform-native integrations for BIG-IP devices from PaaS providers like Cloud Foundry, Kubernetes, Mesos, & OpenShift. The BIG-IP Controllers for these platforms translate native commands to F5 Python SDK/iControl REST calls. [#cccl]_

You can use any BIG-IP Controller to manage a BIG-IP HA active-standby pair or device group. While the platform details vary, all of the Controllers operate on the same basic principle: To provide redundancy, run one Controller instance for each BIG-IP device.

**For example**:

You have one active and one standby BIG-IP device. You want to manage a Kubernetes Cluster in a single partition on the BIG-IP system. For your HA setup, you'd deploy two |kctlr| instances - one for each BIG-IP device. To ensure Controller HA, deploy each Controller instance on a separate node in the cluster.

.. figure:: /_static/media/bigip-ha.png
   :alt: A diagram showing a BIG-IP active-standby device pair and 2 BIG-IP Controllers, running on separate nodes in a Kubernetes Cluster.

.. [#cccl] See `Introduction to F5 Common Controller Core Library <https://devcentral.f5.com/articles/introduction-to-f5-common-controller-core-library-cccl-28355>`_ on DevCentral for more information.

BIG-IP config sync
------------------

.. warning::

   Each |kctlr| monitors the BIG-IP partition it manages for configuration changes. If it discovers changes, the Controller reapplies its own configuration to the BIG-IP system.

   F5 does not recommend making configuration changes to objects in any partition managed by the |kctlr| via any other means (for example, the configuration utility, TMOS, or by syncing configuration with another device or service group). Doing so may result in disruption of service or unexpected behavior.

If you use automatic config sync, you should deploy one |kctlr| instance to manage the active device.

If you sync device group configurations manually, you can use the two-instance deployment. If you choose to deploy one |kctlr| instance and manually sync configurations to the standby device, be sure to always sync *from* the BIG-IP device managed by the |kctlr| *to* the other device(s) in the group.

.. important::

   If you use tunnels to connect your BIG-IP device(s) to the Cluster network, you should disable config sync for tunnels. See "About configuring VXLAN tunnels on high availability BIG-IP device pairs" in the `BIG-IP TMOS Tunneling and IPsec Guide <https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/bigip-tmos-tunnels-ipsec-13-0-0/2.html>`_ for more information.

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

   F5 does not recommend creating two Deployments in a single manifest file. If you launch two |kctlr| instances using a single manifest, both will run on the same Pod. This means that if the Pod goes down, you lose both Controllers.

   .. tip::

      You can :k8sdocs:`Assign Pods to Nodes </concepts/configuration/assign-pod-node/>` in Kubernetes using Node labels and ``nodeSelector``.
      The examples provided below use Node labels to assign each Pod to a different Node.

#. Provide the IP address/hostname for the active device in the first Deployment. Provide the IP address/hostname for the standby device in the second Deployment.

   .. literalinclude:: /kubernetes/config_examples/f5-k8s-bigip-ctlr_ha-active.yaml
      :emphasize-lines: 31
      :caption: Deployment with the IP address for the active BIG-IP device

   :fonticon:`fa fa-download` :download:`Download the ha-active Deployment </kubernetes/config_examples/f5-k8s-bigip-ctlr_ha-active.yaml>`
   :fonticon:`fa fa-download` :download:`Download the ha-standby Deployment </kubernetes/config_examples/f5-k8s-bigip-ctlr_ha-active.yaml>`

#. Upload the Deployments to the Kubernetes/OpenShift API server.

   .. code-block:: console

      kubectl apply -f f5-k8s-bigip-ctlr_ha-active.yaml --namespace=kube-system
      deployment "k8s-bigip-ctlr-deployment" created

   .. code-block:: console

      kubectl apply -f f5-k8s-bigip-ctlr_ha-standby.yaml --namespace=kube-system
      deployment "k8s-bigip-ctlr-deployment" created

.. seealso::

   `Learn how to deploy Pods to specific Nodes in Kubernetes <https://kubernetes.io/docs/concepts/configuration/assign-pod-node/>`_.

.. todo:: add information about using namespace-labels

.. note::

   Using one Controller and autosync means that at failover there is a window where the FDB entries won’t be populated on the new active device (config sync does not populate FDB entries). This window will be, at minumum, the length of the poll-interval setting - the interval at which the Controller polls for Kubernetes nodes. The window can be reduced with shorter polling to the API server by reducing the poll-interval config value (5-10 seconds instead of hte default 30).

   Using two Controllers creates FDB entries on both the active and stand-by devices. This option involves a shorter delay at failover, since the standby device doesn't have to wait for the FDB updates.

 
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



