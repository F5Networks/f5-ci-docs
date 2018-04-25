:product: BIG-IP Controller for Kubernetes
:type: task

.. _upgrade f5 router:

Replace the F5 Router in OpenShift
==================================

Take the steps below to replace the `OpenShift F5 Router`_ with the |kctlr-long| in OpenShift deployments.

.. table:: Task Summary

   ===== =========================================
   Step  Task
   ===== =========================================
   1.    :ref:`remove f5 router`.
   ----- -----------------------------------------
   2.    :ref:`oc install kctlr`.
   ----- -----------------------------------------
   3.    :ref:`set up kctlr routes`.
   ----- -----------------------------------------
   4.    :ref:`deploy route resource`.
   ----- -----------------------------------------
   5.    :ref:`verify BIG-IP route objects`.
   ===== =========================================

.. _remove f5 router:

Remove the OpenShift F5 Router
------------------------------

.. todo:: **NEEDS VERIFICATION FROM RED HAT**

Use the OpenShift CLI to remove the Pod(s) associated with the F5 Router.

.. note::

   The |kctlr| will remove/replace any objects on the BIG-IP system when it launches, **if** you set it to manage the same BIG-IP partition.
   If you want to manage a different partition with the |kctlr|, you should delete the objects from the F5 Router's partition manually.

.. code-block:: console

   oc delete pod <pod-name>

.. _oc install kctlr:

Install the |kctlr|
-------------------

#. Complete the :ref:`initial setup <openshift initial setup>`.
#. :ref:`Set up RBAC Authentication <openshift-rbac>`.
#. :ref:`Create a Deployment <create-openshift-deployment>` for the |kctlr|.

   .. literalinclude:: /openshift/config_examples/f5-k8s-bigip-ctlr_openshift_routes.yaml
      :linenos:

#. :ref:`Upload the Deployment <upload openshift deployment>` to the OpenShift API server.

When you upload the Deployment to your OpenShift API server, the |kctlr| will automatically detect any existing OpenShift Routes and create corresponding routes on the BIG-IP system.

If you set up the |kctlr| to manage the same BIG-IP partition you used with the OpenShift F5 Router, the |kctlr| automatically replaces any remaining F5 Router artifacts in the partition with new objects.

What's Next
-----------

- :ref:`kctlr-openshift-routes`
- Discover the |kctlr| supported `route configuration parameters`_.
