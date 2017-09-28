.. index::
   single: BIG-IP Controller for Kubernetes; OpenShift
   single: OpenShift
   pair: BIG-IP Controller for Kubernetes; OpenShift
   triple: BIG-IP Controller for Kubernetes; OpenShift; F5 Router
   triple: OpenShift; F5 Router; replace
   triple: OpenShift; F5 Router; upgrade

.. _upgrade f5 router:

Replace the OpenShift F5 Router with the BIG-IP Controller
==========================================================

.. include:: /_static/reuse/k8s-version-added-1_2.rst

Take the steps below to replace the `OpenShift F5 Router`_ with the |kctlr-long| in OpenShift deployments.

===== ==================================================================================
Step  Task
===== ==================================================================================
1.    Remove the existing OpenShift F5 Router.
----- ----------------------------------------------------------------------------------
2.    Install the |kctlr| in OpenShift.
----- ----------------------------------------------------------------------------------
3.    Configure the |kctlr| to use OpenShift routes.
----- ----------------------------------------------------------------------------------
4.    Create OpenShift routes.
----- ----------------------------------------------------------------------------------
5.    Verify route creation on the BIG-IP system.
===== ==================================================================================

Remove the OpenShift F5 Router
------------------------------

.. todo:: **NEEDS VERIFICATION FROM RED HAT**

Use the OpenShift CLI to remove the pod(s) associated with the F5 Router.

.. note::

   The |kctlr| will remove/replace any objects on the BIG-IP system when it launches, **if** you set it to manage the same BIG-IP partition.
   If you want to manage a different partition with the |kctlr|, you should delete the objects from the F5 Router's partition manually.

.. code-block:: console

   $ oc delete pod <pod>

Install the |kctlr|
-------------------

#. Complete the :ref:`initial setup <openshift initial setup>`.
#. :ref:`Set up RBAC Authentication <openshift-rbac>`.
#. :ref:`Create a Deployment <create-openshift-deployment>` for the |kctlr|.

   Define the parameters highlighted below in your Deployment to set up route handling.

   .. literalinclude:: /_static/config_examples/f5-kctlr-openshift-routes.yaml
      :linenos:
      :emphasize-lines: 38-45

#. :ref:`Upload the Deployment <upload openshift deployment>` to the OpenShift API server.

Create OpenShift Routes
-----------------------

.. important::

   When you upload the Deployment to your OpenShift API server, the |kctlr| automatically detects existing OpenShift Routes and creates corresponding routes on the BIG-IP system.

   If you used the same BIG-IP partition for the F5 Router, the |kctlr| will replace any remaining F5 Router artifacts with new objects.

OpenShift supports 4 (4) types of routes: edge, passthrough, re-encrypt, and unsecure.
The |kctlr| supports all four types.

You can download sample Route definitions for each type below.
See `Supported Route Configurations </products/connectors/k8s-bigip-ctlr/#Supported-route-configurations>`_ for more information.

:fonticon:`fa fa-download` `sample-unsecured-route.yaml </products/connectors/k8s-bigip-ctlr/v1.2/_downloads/sample-unsecured-route.yaml>`_

:fonticon:`fa fa-download` `sample-edge-route.yaml </products/connectors/k8s-bigip-ctlr/v1.2/_downloads/sample-edge-route.yaml>`_

:fonticon:`fa fa-download` `sample-passthrough-route.yaml </products/connectors/k8s-bigip-ctlr/v1.2/_downloads/sample-passthrough-route.yaml>`_

:fonticon:`fa fa-download` `sample-reencrypt-route.yaml </products/connectors/k8s-bigip-ctlr/v1.2/_downloads/sample-reencrypt-route.yaml>`_

.. _OpenShift F5 Router: https://docs.openshift.org/1.4/install_config/router/f5_router.html
