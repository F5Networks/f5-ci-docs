.. STAGED IN K8S_BIGIP_CTLR REPO
.. todo:: remove from this repo and add redirect in AWS

.. _install-kctlr:

Install the BIG-IP Controller in Kubernetes
===========================================

.. sidebar:: Docs test matrix

   Documentation manually tested with:

   - ``kubernetes-v1.6.4 on Ubuntu-16.4.2``
   - ``kubernetes-v1.4.8 on CoreOS 1409.6.0``
   - ``k8s-bigip-ctlr v1.1.0``
   - ``k8s-bigip-ctlr v1.0.0``


The |kctlr-long| installs via a `Kubernetes Deployment`_.
The Deployment creates a `ReplicaSet`_ that, in turn, launches a `Pod`_ running the |kctlr| app.

.. attention::

   These instructions are for a standard Kubernetes environment.
   **If you are using OpenShift**, see :ref:`Install the BIG-IP Controller for Kubernetes in OpenShift Origin <install-kctlr-openshift>`.

Initial Setup
-------------

.. include:: /_static/reuse/kctlr-initial-setup.rst
   :end-line: 4

.. include:: /_static/reuse/kctlr-initial-setup.rst
   :start-line: 6

.. _k8s-rbac:

Set up RBAC Authentication
--------------------------

.. note::

   If your cluster doesn't use `Role Based Access Control <https://kubernetes.io/docs/admin/authorization/rbac/>`_ , you can skip this step.

#. Create a Service Account for the |kctlr|.

   .. code-block:: console

      $ kubectl create serviceaccount bigip-ctlr -n kube-system
      serviceaccount "bigip-ctlr" created

#. Create a `Cluster Role`_ and `Cluster Role Binding`_.

   You can restrict the permissions granted in the cluster role as needed for your deployment.
   The supported permission set is shown in the table and Cluster Role example below.

   +--------------+-------------------+---------------------------------------------+
   | API groups   | Resources         | Actions                                     |
   +==============+===================+=============================================+
   | ""           | endpoints         | get, list, watch                            |
   |              +-------------------+                                             |
   |              | namespaces        |                                             |
   |              +-------------------+                                             |
   |              | nodes             |                                             |
   |              +-------------------+                                             |
   |              | services          |                                             |
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

   .. literalinclude:: /kubernetes/config_examples/f5-k8s-sample-rbac.yaml
      :linenos:

   :fonticon:`fa fa-download` :download:`f5-k8s-sample-rbac.yaml </kubernetes/config_examples/f5-k8s-sample-rbac.yaml>`


.. _k8s-bigip-ctlr-deployment:

Create a Deployment
-------------------

#. Define the |kctlr| configurations in a `Kubernetes Deployment`_ using valid JSON or YAML.

   .. literalinclude:: /kubernetes/config_examples/f5-k8s-bigip-ctlr_image-secret.yaml
      :linenos:

   :fonticon:`fa fa-download` :download:`f5-k8s-bigip-ctlr_image-secret.yaml </kubernetes/config_examples/f5-k8s-bigip-ctlr_image-secret.yaml>`

Upload the resources to the Kubernetes API server
-------------------------------------------------

Upload the Deployment, Cluster Role, and Cluster Role Binding to the Kubernetes API server using ``kubectl apply``.
Be sure to create all resources in the ``kube-system`` namespace.

.. code-block:: console

   kubectl apply -f f5-k8s-bigip-ctlr_image-secret.yaml --namespace=kube-system
   kubectl apply -f f5-k8s-sample-rbac.yaml --namespace=kube-system
   deployment "k8s-bigip-ctlr-deployment" created
   cluster role "bigip-ctlr-clusterrole" created
   cluster role binding "bigip-ctlr-clusterrole-binding" created


Verify creation
---------------

Use :command:`kubectl get` to verify all of the objects launched successfully.

You should see one (1) `ReplicaSet`_, as well as one (1) k8s-bigip-ctlr `Pod`_ for each node in the cluster. The example below shows one (1) Pod running the k8s-bigip-ctlr in a test cluster with one worker node.

.. code-block:: console
   :emphasize-lines: 3, 7, 11, 13

   kubectl get deployments --namespace=kube-system
   NAME             DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
   k8s-bigip-ctlr   1         1         1            1           1h

   kubectl get replicasets --namespace=kube-system
   NAME                       DESIRED   CURRENT   AGE
   k8s-bigip-ctlr-331478340   1         1         1h

   kubectl get pods --namespace=kube-system
   NAME                                  READY     STATUS    RESTARTS   AGE
   k8s-bigip-ctlr-331478340-ke0h9        1/1       Running   0          1h
   kube-apiserver-172.16.1.19            1/1       Running   0          2d
   kube-controller-manager-172.16.1.19   1/1       Running   0          2d
   kube-dns-v11-2a66j                    4/4       Running   0          2d
   kube-proxy-172.16.1.19                1/1       Running   0          2d
   kube-proxy-172.16.1.21                1/1       Running   0          2d
   kube-scheduler-172.16.1.19            1/1       Running   0          2d
   kubernetes-dashboard-172.16.1.19      1/1       Running   0          2d

What's Next
-----------

- Check out the `k8s-bigip-ctlr reference documentation`_.
- Learn how to :ref:`expose Services to external traffic using an Ingress <kctlr-ingress-config>`.
