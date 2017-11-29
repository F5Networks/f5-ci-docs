.. index::
   single: OpenShift; BIG-IP Controller
   single: OpenShift; BIG-IP Controller; install
   single: OpenShift; RBAC; BIG-IP Controller

.. sidebar:: Docs test matrix

   Documentation manually tested with:

   - OpenShift v1.4.1 on CentOS 7.2.1511
   - k8s-bigip-ctlr v1.1.0-1.3.0

.. _install-kctlr-openshift:

Install the BIG-IP Controller in OpenShift
==========================================

Use a `Deployment`_ to install the |kctlr-long| in `OpenShift`_.
The Deployment creates a `ReplicaSet`_ that, in turn, launches the |kctlr| app in `Pods`_.

.. attention::

   These instructions are for the `Openshift`_ Kubernetes distribution.
   **If you are using standard Kubernetes**, see :ref:`Install the BIG-IP Controller in Kubernetes <install-kctlr>`.


.. table:: Task table

   =======  ===================================================================
   Step     Task
   =======  ===================================================================
   1.       Complete :ref:`openshift initial setup`.

   2.       :ref:`openshift-rbac`

   3.       :ref:`kctlr-configure-openshift`

   4.       :ref:`upload openshift deployment` to OpenShift
   =======  ===================================================================

.. _openshift initial setup:

Initial Setup
-------------

.. include:: /_static/reuse/kctlr-initial-setup.rst

.. _k8s-openshift-serviceaccount:
.. _openshift-rbac:

Set up RBAC Authentication
--------------------------

#. Create a Service Account for the |kctlr|.

   .. code-block:: console

      oc create serviceaccount bigip-ctlr -n kube-system
      serviceaccount "bigip-ctlr" created

#. Create a `Cluster Role`_ and `Cluster Role Binding`_. The |kctlr| for OpenShift requires the permissions shown in the table below.

   +--------------+-------------------+---------------------------------------------+
   | API groups   | Resources         | Actions                                     |
   +==============+===================+=============================================+
   | ""           | endpoints         | get, list, watch                            |
   |              +-------------------+                                             |
   |              | namespaces        |                                             |
   |              +-------------------+                                             |
   |              | nodes             |                                             |
   |              +-------------------+                                             |
   |              | routes            |                                             |
   |              +-------------------+                                             |
   |              | services          |                                             |
   |              +-------------------+                                             |
   |              | secrets           |                                             |
   +--------------+-------------------+---------------------------------------------+
   | "extensions" | ingresses         | get, list, watch                            |
   +--------------+-------------------+---------------------------------------------+
   | ""           | configmaps        | get, list, watch, update, create, patch     |
   +--------------+-------------------+                                             |
   |              | events            |                                             |
   +--------------+-------------------+---------------------------------------------+
   | "extensions" | ingresses/status  | get, list, watch, update, create, patch     |
   +--------------+-------------------+---------------------------------------------+

   \

   .. literalinclude:: /openshift/config_examples/f5-kctlr-openshift-clusterrole.yaml
      :linenos:

   :fonticon:`fa fa-download` :download:`f5-kctlr-openshift-clusterrole.yaml </openshift/config_examples/f5-kctlr-openshift-clusterrole.yaml>`

#. Upload the Cluster Role and Cluster Role Binding to the API server.

   .. code-block:: console

      oc create -f f5-kctlr-openshift-clusterrole.yaml
      clusterrole "system:bigip-ctlr" created
      clusterrolebinding "bigip-ctlr-role" created


.. _create-openshift-deployment:

.. _openshift-bigip-ctlr-deployment:

Deploy the k8s-bigip-ctlr
-------------------------

.. _kctlr-configure-openshift:

Define the k8s-bigip-ctlr configuration in an OpenShift Deployment
``````````````````````````````````````````````````````````````````

The |kctlr| has a subset of `configuration parameters specific to OpenShift`_. At minimum, you must include the following configuration parameters in your Deployment:

- :code:`--openshift-sdn-name=/path/to/bigip_openshift_vxlan`
- :code:`--pool-member-type=cluster`

If using the |kctlr| to manage OpenShift Routes, include the desired `Route configuration parameters`_.

The Deployment must consist of valid JSON or YAML.

Ingress Deployment
~~~~~~~~~~~~~~~~~~

The example below shows the |kctlr| configurations required if you want to :ref:`expose OpenShift Services to external traffic using an Ingress <kctlr-ingress-config>`.

.. literalinclude:: /openshift/config_examples/f5-k8s-bigip-ctlr_openshift-sdn.yaml
   :caption: Example k8s-bigip-ctlr OpenShift Deployment
   :linenos:

:fonticon:`fa fa-download` :download:`f5-k8s-bigip-ctlr_openshift-sdn.yaml </openshift/config_examples/f5-k8s-bigip-ctlr_openshift-sdn.yaml>`

Routes Deployment
~~~~~~~~~~~~~~~~~

The example below shows the |kctlr| configurations required if you want to :ref:`expose OpenShift Services to external traffic using Routes <kctlr-openshift-routes>`.

.. literalinclude:: /openshift/config_examples/f5-k8s-bigip-ctlr_openshift-sdn.yaml
   :caption: Example k8s-bigip-ctlr OpenShift Deployment
   :linenos:

.. _upload openshift deployment:

Upload the Deployment
`````````````````````

#. Upload the Deployment to the OpenShift API server using :command:`oc create`.

   .. code-block:: console

      oc create -f f5-k8s-bigip-ctlr_openshift-sdn.yaml --namespace=kube-system
      deployment "k8s-bigip-ctlr" created

#. Verify creation using :command:`oc get`.

   You should see one (1) `ReplicaSet`_, as well as one (1) k8s-bigip-ctlr `Pod`_ for each Node in the Cluster. The example below shows one (1) Pod running the k8s-bigip-ctlr in a test cluster with one worker node.

   .. code-block:: console

      oc get deployments --namespace=kube-system
      NAME             DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
      k8s-bigip-ctlr   1         1         1            1           1h

      oc get replicasets --namespace=kube-system
      NAME                       DESIRED   CURRENT   AGE
      k8s-bigip-ctlr-331478340   1         1         1h

      oc get pods --namespace=kube-system
      user@k8s-master:~oc get pods --namespace=kube-system
      NAME                              READY     STATUS    RESTARTS   AGE
      k8s-bigip-ctlr-1962020886-s31l4   1/1       Running   0          1m

What's Next
-----------

- Check out the `k8s-bigip-ctlr reference documentation`_.
- Learn how to :ref:`Expose Services to external traffic using an Ingress <kctlr-ingress-config>` or `Manage OpenShift Routes <kctlr-openshift-routes>`.

What's next
-----------

Now that you have the |kctlr| up and running, here are a few things you can do with it:

- :ref:`kctlr-create-vs`
- :ref:`kctlr-deploy-iapps`
- :ref:`kctlr-ingress-config`
- :ref:`kctlr-openshift-routes`

.. _OpenShift: https://www.openshift.org/
.. _ReplicaSet: https://kubernetes.io/docs/user-guide/replicasets/
.. _ServiceAccount: https://kubernetes.io/docs/admin/service-accounts-admin/
