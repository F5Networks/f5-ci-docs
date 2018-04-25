.. STAGED IN K8S_BIGIP_CTLR REPO
.. todo:: remove from this repo and add redirect in AWS

.. index::
   single: BIG-IP Controller; Kubernetes

.. sidebar:: Docs test matrix

   Documentation manually tested with:

   - kubernetes-v1.6.4 on Ubuntu-16.4.2
   - kubernetes-v1.4.8 on CoreOS 1409.6.0
   - ``k8s-bigip-ctlr`` v1.0.0-v1.4.0

.. _install-kctlr:

Install the BIG-IP Controller in Kubernetes
===========================================

Use a `Deployment`_ to install the |kctlr-long|.

If you use `helm`_ you can use the `f5-bigip-ctlr chart`_ to create and manage the resources below.

.. attention::

   These instructions are for a standard Kubernetes environment.
   **If you are using OpenShift**, see :ref:`Install the BIG-IP Controller for Kubernetes in OpenShift Origin <install-kctlr-openshift>`.

.. table:: Task Summary

   =======  ===================================================================
   Step     Task
   =======  ===================================================================
   1.       :ref:`kctlr initial setup bigip`
   2.       :ref:`k8s-rbac`
   3.       :ref:`k8s-bigip-ctlr-deployment`

            - :ref:`kctlr basic deploy`
            - :ref:`kctlr snat deploy`
            - :ref:`kctlr flannel deploy`

   4.       :ref:`upload to k8s api`
   5.       :ref:`kctlr verify pods`
   =======  ===================================================================

.. _kctlr initial setup bigip:

Initial Setup
-------------

.. include:: /_static/reuse/bigip-admin-permissions-reqd.rst

.. include:: /_static/reuse/kctlr-initial-setup.rst

.. _k8s-rbac:

Set up RBAC Authentication
--------------------------

#. Create a Service Account for the |kctlr|.

   .. code-block:: console

      kubectl create serviceaccount bigip-ctlr -n kube-system
      serviceaccount "bigip-ctlr" created

#. Create a `Cluster Role`_ and `Cluster Role Binding`_.

   .. important::

      You can substitute a Role and RoleBinding if your Controller doesn't need access to the entire Cluster.

      The example below shows the broadest supported permission set.
      You can narrow the permissions down to specific resources, namespaces, etc. to suit your needs.
      See the `Kubernetes RBAC documentation`_ for more information.

.. literalinclude:: /kubernetes/config_examples/f5-k8s-sample-rbac.yaml
   :linenos:

:fonticon:`fa fa-download` :download:`f5-k8s-sample-rbac.yaml </kubernetes/config_examples/f5-k8s-sample-rbac.yaml>`

.. _k8s-bigip-ctlr-deployment:

Create a Deployment
-------------------

Define a Kubernetes Deployment using valid YAML or JSON. See the `k8s-bigip-ctlr configuration parameters`_ reference for all supported configuration options.

.. danger::

   Do not increase the :code:`replica` count in the Deployment. Running duplicate Controller instances may cause errors and/or service interruptions.

.. include:: /_static/reuse/bigip-permissions-ctlr.rst

.. _kctlr basic deploy:

Basic Deployment
````````````````

The example below shows a Deployment with the basic config parameters required to run the |kctlr| in Kubernetes.

.. literalinclude:: /kubernetes/config_examples/f5-k8s-bigip-ctlr_basic.yaml
   :linenos:

:fonticon:`fa fa-download` :download:`f5-k8s-bigip-ctlr_basic.yaml </kubernetes/config_examples/f5-k8s-bigip-ctlr_basic.yaml>`

.. _kctlr flannel deploy:

Deployments for flannel BIG-IP Integrations
```````````````````````````````````````````

If :ref:`your BIG-IP device connects to the Cluster network via flannel VXLAN <use-bigip-k8s-flannel>`, you must include the following in your Deployment:

- :code:`--pool-member-type=cluster` (See :ref:`cluster mode` for more information.)
- :code:`--flannel-name=/Common/tunnel_name`

:fonticon:`fa fa-download` :download:`Download example Deployment with flannel-name defined </kubernetes/config_examples/f5-k8s-bigip-ctlr_flannel.yaml>`


.. _kctlr snat deploy:

Use BIG-IP SNAT Pools and SNAT automap
``````````````````````````````````````

.. include:: /_static/reuse/k8s-version-added-1_5.rst

.. include:: /_static/reuse/kctlr-snat-note.rst

See :ref:`bigip snats` for more information.

To use a specific SNAT pool, add the following to the :code:`args` section of any :code:`k8s-bigip-ctlr` Deployment:

.. code-block:: YAML

   "--vs-snat-pool-name=<snat-pool>"

Replace :code:`<snat-pool>` with the name of any SNAT pool that already exists in the :code:`/Common` partition on the BIG-IP device. The |kctlr| cannot define a new SNAT pool for you.

:fonticon:`fa fa-download` :download:`Download example Deployment with vs-snat-pool-name defined </kubernetes/config_examples/f5-k8s-bigip-ctlr_snat.yaml>`


.. literalinclude:: /kubernetes/config_examples/f5-k8s-bigip-ctlr_image-secret.yaml
   :linenos:

:fonticon:`fa fa-download` :download:`f5-k8s-bigip-ctlr_image-secret.yaml </kubernetes/config_examples/f5-k8s-bigip-ctlr_image-secret.yaml>`

Upload the resources to the Kubernetes API server
-------------------------------------------------

Upload the Deployment, Cluster Role, and Cluster Role Binding to the Kubernetes API server using ``kubectl apply``.

.. tip::
   :class: sidebar

   Be sure to create all of the resources in the namespace that best suits your needs.

   For example, if you intend to manage multiple namespaces, deploy the Controller and its supporting resources to :code:`kube-system` (which is where all of the Kubernetes system controllers run).
   If you intend to manage a single namespace, you can deploy the Controller and its supporting resources to that namespace.

.. parsed-literal::

   kubectl apply -f **f5-k8s-bigip-ctlr_basic.yaml** -f **f5-k8s-sample-rbac.yaml** **[-n kube-system]**
   deployment "k8s-bigip-ctlr" created
   cluster role "bigip-ctlr-clusterrole" created
   cluster role binding "bigip-ctlr-clusterrole-binding" created

.. _kctlr verify pods:

Verify Pod creation
-------------------

Use the :command:`kubectl get` command to verify that the :code:`k8s-bigip-ctlr` Pod launched successfully.

.. code-block:: console

   kubectl get deployments --namespace=kube-system
   NAME             DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
   k8s-bigip-ctlr   1         1         1            1           1h

   kubectl get pods -n kube-system
   NAME                                  READY     STATUS    RESTARTS   AGE
   k8s-bigip-ctlr-331478340-ke0h9        1/1       Running   0          1h

.. note::

   If you use flannel and :ref:`added your BIG-IP device to the Cluster network <use-bigip-k8s-flannel>`, you should now be able to send traffic through the BIG-IP system to and from endpoints within your Cluster.

What's Next
-----------

- Check out the `k8s-bigip-ctlr reference documentation`_.
- :ref:`Create a BIG-IP Virtual Server for a Service <kctlr-create-vs>`.
- :ref:`Create a BIG-IP Virtual Server for an Ingress Resource <kctlr-ingress-config>`.
