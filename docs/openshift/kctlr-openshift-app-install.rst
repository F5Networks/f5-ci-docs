:product: BIG-IP Controller for Kubernetes
:type: task

.. _install-kctlr-openshift:

Install the BIG-IP Controller: OpenShift
========================================

Use a `Deployment`_ to install the |octlr-long|.

If you use `helm`_, you can use the `f5-bigip-ctlr chart`_ to create and manage the resources below.

.. attention::

   These instructions are for the `Openshift`_ Kubernetes distribution.
   **If you are using standard Kubernetes**, see :ref:`Install the BIG-IP Controller in Kubernetes <install-kctlr>`.

.. table:: Task Summary

   =======  ===================================================================
   Step     Task
   =======  ===================================================================
   1.       :ref:`openshift initial setup`
   2.       :ref:`openshift-bigip-ctlr-deployment`

            - :ref:`kctlr-openshift basic deploy`
            - :ref:`kctlr-openshift routes deploy`
            - :ref:`kctlr-openshift ha deploy`
            - :ref:`kctlr-openshift snat deploy`

   3.       :ref:`upload openshift deployment`
   4.       :ref:`kctlr openshift verify pods`
   =======  ===================================================================


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
.. _create-openshift-deployment:

Create a Kubernetes Deployment
------------------------------

.. include:: /_static/reuse/kctlr-openshift-deployment-note.rst

.. _kctlr-configure-openshift:

Define a Kubernetes Deployment using valid YAML or JSON.
The |kctlr| has `configuration parameters specific to OpenShift`_ that you can define as best suits your needs.

At a minimum, all |kctlr| Deployments should include the following:

- :code:`--openshift-sdn-name=/path/to/bigip_openshift_vxlan`
- :code:`--pool-member-type=cluster`

.. danger::

   Do not increase the :code:`replica` count in the Deployment. Running duplicate Controller instances may cause errors and/or service interruptions.

.. include:: docs/_static/reuse/bigip-permissions-ctlr.rst

.. _kctlr-openshift basic deploy:

Basic Deployment
````````````````

The example below shows a Deployment with the basic config parameters required to run the |kctlr| in OpenShift.
With this configuration, you can :ref:`Create BIG-IP virtual servers for Services <kctlr-create-vs>` and :ref:`Deploy Application Services (iApps) <kctlr-deploy-iapps>`.

.. literalinclude:: /openshift/config_examples/f5-k8s-bigip-ctlr_openshift_basic.yaml
   :caption: Example OpenShift Deployment

:fonticon:`fa fa-download` :download:`f5-k8s-bigip-ctlr_openshift_basic.yaml </openshift/config_examples/f5-k8s-bigip-ctlr_openshift_basic.yaml>`

.. _kctlr-openshift snat deploy:

Use BIG-IP SNAT Pools and SNAT automap
``````````````````````````````````````

.. include:: /_static/reuse/k8s-version-added-1_5.rst

.. include:: /_static/reuse/kctlr-snat-note.rst

See :ref:`bigip snats` for more information.

To use a specific SNAT pool, add the following to the :code:`args` section of any :code:`k8s-bigip-ctlr` Deployment:

.. code-block:: YAML

   "--vs-snat-pool-name=<snat-pool>"

Replace :code:`<snat-pool>` with the name of any SNAT pool that already exists in the :code:`/Common` partition on the BIG-IP device. The |kctlr| cannot define a new SNAT pool for you.

:fonticon:`fa fa-download` :download:`f5-k8s-bigip-ctlr_openshift_snat.yaml </openshift/config_examples/f5-k8s-bigip-ctlr_openshift_snat.yaml>`

.. _kctlr-openshift routes deploy:

Deployments for Managing Routes
```````````````````````````````

The |kctlr| has a set of `Route configuration parameters`_ that you can add to any :code:`k8s-bigip-ctlr` Deployment if you want to manage Routes.

See :ref:`Manage Routes with the BIG-IP Controller <kctlr-openshift-routes>` for instructions and examples.

.. _kctlr-openshift ha deploy:

Deployments for BIG-IP HA pairs/groups
``````````````````````````````````````

If you want to manage a BIG-IP HA pair or group, you'll need to deploy one |kctlr| instance per BIG-IP device.

See :ref:`BIG-IP High Availability in OpenShift <openshift deploy kctlr ha>` for instructions and examples.

.. _upload openshift deployment:

Upload the Deployment to the OpenShift API Server
-------------------------------------------------

.. tip::
   :class: sidebar

   If you're deploying multiple Controller instances in the same Project/namespace, you can pass each Deployment's filename in a single :command:`oc create` command.

   Be sure to create all of the resources in the Project (namespace) that best suits your needs.

   For example, if your Controller will manage multiple Projects, deploy the Controller and its supporting resources to :code:`-n kube-system`. This is the namespace in which all of the Kubernetes system controllers run.

   If you intend to manage a single Project **and you are currently working in that Project**, you do not need to provide the :code:`-n` flag.

Use the :command:`oc create` command to upload the Deployment to the OpenShift API server.

.. parsed-literal::

   oc create -f **f5-k8s-bigip-ctlr_openshift-sdn.yaml** **[-n kube-system]**
   deployment "k8s-bigip-ctlr" created

.. _kctlr openshift verify pods:

Verify Pod(s)
-------------

You can verify that the Controller(s) created successfully using the :command:`oc get` command.

You should see one :code:`k8s-bigip-ctlr` `Pod`_ for each Node in the Cluster. The example below shows one :code:`k8s-bigip-ctlr` Pod running in a test cluster that has one worker node.

.. code-block:: console

   oc get pods
   NAME                              READY     STATUS    RESTARTS   AGE
   k8s-bigip-ctlr-1962020886-s31l4   1/1       Running   0          1m

.. note::

   Once the Controller is running, you should be able to successfully send traffic through the BIG-IP system to and from endpoints within your OpenShift Cluster.

.. _OpenShift: https://www.openshift.org/
.. _ReplicaSet: https://kubernetes.io/docs/user-guide/replicasets/
.. _ServiceAccount: https://kubernetes.io/docs/admin/service-accounts-admin/
