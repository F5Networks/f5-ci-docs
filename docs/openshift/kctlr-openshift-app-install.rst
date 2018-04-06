:product: BIG-IP Controller for Kubernetes
:type: task

.. _install-kctlr-openshift:

Install the BIG-IP Controller: OpenShift
========================================

Use a `Deployment`_ to install the |octlr-long|.

If you use `helm`_ you can use the `f5-bigip-ctlr chart`_ to create the and manage the resources below.

.. attention::

   These instructions are for the `Openshift`_ Kubernetes distribution.
   **If you are using standard Kubernetes**, see :ref:`Install the BIG-IP Controller in Kubernetes <install-kctlr>`.

.. table:: Task Summary

   =======  ===================================================================
   Step     Task
   =======  ===================================================================
   1.       :ref:`openshift initial setup`
   2.       :ref:`openshift-bigip-ctlr-deployment`

            - :ref:`create-openshift-deployment`
            - :ref:`upload openshift deployment`
            - :ref:`kctlr verify pods`
   =======  ===================================================================

.. attention::

   These instructions are for the `OpenShift`_ Kubernetes distribution.
   **If you are using standard Kubernetes**, see :ref:`Install the BIG-IP Controller in Kubernetes <install-kctlr>`.

.. _openshift initial setup:

Initial Set-up
--------------

Follow the steps in the guides linked to below to set up your BIG-IP device(s) and OpenShift cluster for use with the |kctlr|.

.. include:: /_static/reuse/bigip-admin-permissions-reqd.rst

.. include:: /_static/reuse/kctlr-initial-setup.rst

.. _k8s-openshift-serviceaccount:
.. _openshift-rbac:

Set up RBAC Authentication
--------------------------

.. include:: /_static/reuse/kctlr-openshift-set-up-rbac.rst

.. _openshift-bigip-ctlr-deployment:

Deploy the |kctlr|
------------------

.. _kctlr-configure-openshift:


The |kctlr| has a subset of `configuration parameters specific to OpenShift`_.
Include the following required config parameters in all OpenShift Deployments:

- :code:`--openshift-sdn-name=/path/to/bigip_openshift_vxlan`
- :code:`--pool-member-type=cluster`


Define an OpenShift Deployment config using valid YAML or JSON.

.. _create-openshift-deployment:

Create a Deployment
```````````````````

Basic Deployment
~~~~~~~~~~~~~~~~

The example below shows a Deployment with the basic config parameters required to run the |kctlr| in OpenShift.
With this configuration, you can :ref:`Create BIG-IP virtual servers for Services <kctlr-create-vs>` and :ref:`Deploy Application Services (iApps) <kctlr-deploy-iapps>`.

.. literalinclude:: /openshift/config_examples/f5-k8s-bigip-ctlr_openshift-sdn.yaml
   :caption: Example OpenShift Deployment


:fonticon:`fa fa-download` :download:`f5-k8s-bigip-ctlr_openshift-sdn.yaml </openshift/config_examples/f5-k8s-bigip-ctlr_openshift-sdn.yaml>`

Deployments for Managing Routes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The |kctlr| has a set of `Route configuration parameters`_. See :ref:`Manage Routes with the BIG-IP Controller <kctlr-openshift-routes>` for examples and set-up instructions.

Deployments for BIG-IP HA
~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to manage a BIG-IP HA pair or group, you'll need to deploy a |kctlr| instance for each device.
See :ref:`BIG-IP High Availability in OpenShift <openshift deploy kctlr ha>` for more information.

.. _upload openshift deployment:

Upload the Deployment
`````````````````````
.. tip::
   :class: sidebar

   For HA deployments, you can pass in each Deployment's filename in a single :command:`oc create` command.

Use the :command:`oc create` command to upload the Deployment to the OpenShift API server.

.. code-block:: console

   oc create -f f5-k8s-bigip-ctlr_openshift-sdn.yaml
   deployment "k8s-bigip-ctlr" created

.. _kctlr verify pods:

Verify Pod(s)
`````````````

You can verify that the Controller(s) created successfully using the :command:`oc get` command.

You should see one :code:`k8s-bigip-ctlr` `Pod`_ for each Node in the Cluster. The example below shows one :code:`k8s-bigip-ctlr` Pod running in a test cluster with one worker node.

.. code-block:: console

   oc get pods
   NAME                              READY     STATUS    RESTARTS   AGE
   k8s-bigip-ctlr-1962020886-s31l4   1/1       Running   0          1m



.. _OpenShift: https://www.openshift.org/
.. _ReplicaSet: https://kubernetes.io/docs/user-guide/replicasets/
.. _ServiceAccount: https://kubernetes.io/docs/admin/service-accounts-admin/
