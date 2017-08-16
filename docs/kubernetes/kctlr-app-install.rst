.. STAGED IN K8S_BIGIP_CTLR REPO
.. todo:: remove from this repo and add redirect in AWS

.. _install-kctlr:

Install the |kctlr-long|
========================

.. sidebar:: Docs test matrix

   We tested this documentation with:

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

#. `Create a new partition`_ for Kubernetes on your BIG-IP system.
   The |kctlr| can not manage objects in the ``/Common`` partition.

#. :ref:`Add a Kubernetes Secret <k8s-add-secret>` containing your BIG-IP login credentials to your Kubernetes master node.

#. `Create a Kubernetes Secret containing your Docker login credentials`_ (required if you need to pull the container image from a private Docker registry).

.. _create-k8s-deployment:

.. important::

   You should create all |kctlr| objects in the ``kube-system`` `namespace`_, unless otherwise specified in the deployment instructions.

.. _k8s-bigip-ctlr-deployment:

Create a Deployment
-------------------

#. Define a `Kubernetes Deployment`_ using valid JSON or YAML.

   The deployment example below also creates a `ServiceAccount`_ for the controller to use.

   .. literalinclude:: /_static/config_examples/f5-k8s-bigip-ctlr_image-secret.yaml
      :linenos:
      :caption: Example Kubernetes Manifest
      :emphasize-lines: 2,50

   :fonticon:`fa fa-download` :download:`f5-k8s-bigip-ctlr_image-secret.yaml </_static/config_examples/f5-k8s-bigip-ctlr_image-secret.yaml>`

Set up RBAC Authentication
``````````````````````````

.. note::

   - If your cluster is not using `Role Based Access Control <https://kubernetes.io/docs/admin/authorization/rbac/>`_ , you can skip this step.

Create a `cluster role <https://kubernetes.io/docs/admin/authorization/rbac/#role-and-clusterrole>`_ and `cluster role binding <https://kubernetes.io/docs/admin/authorization/rbac/#rolebinding-and-clusterrolebinding>`_.
These resources allow the |kctlr| to monitor and update the resources it manages.

You can restrict the permissions granted in the cluster role as needed for your deployment.
Those shown below are the supported permission set.


.. literalinclude:: /_static/config_examples/f5-k8s-sample-rbac.yaml
   :linenos:
   :caption: Example ``ClusterRole`` and ``ClusterRoleBinding``

:fonticon:`fa fa-download` :download:`f5-k8s-sample-rbac.yaml </_static/config_examples/f5-k8s-sample-rbac.yaml>`

Upload the Deployment
---------------------

Upload the Deployment, Cluster Role, and Cluster Role Binding to the Kubernetes API server using ``kubectl apply``.
Be sure to create all resources in the ``kube-system`` namespace.

.. code-block:: console

   user@k8s-master:~$ kubectl apply -f f5-k8s-bigip-ctlr_image-secret.yaml --namespace=kube-system
   user@k8s-master:~$ kubectl apply -f f5-k8s-sample-rbac.yaml --namespace=kube-system


Verify creation
---------------

When you create a Deployment, a `ReplicaSet`_ and `Pod`_ (s) launch automatically.
Use ``kubectl`` to verify all of the objects launched successfully.

.. code-block:: console
   :emphasize-lines: 3, 7, 11

   user@k8s-master:~$ kubectl get deployments --namespace=kube-system
   NAME             DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
   k8s-bigip-ctlr   1         1         1            1           1h

   user@k8s-master:~$ kubectl get replicasets --namespace=kube-system
   NAME                       DESIRED   CURRENT   AGE
   k8s-bigip-ctlr-331478340   1         1         1h

   user@k8s-master:~$ kubectl get pods --namespace=kube-system
   NAME                                  READY     STATUS    RESTARTS   AGE
   k8s-bigip-ctlr-331478340-ke0h9        1/1       Running   0          1h
   kube-apiserver-172.16.1.19            1/1       Running   0          2d
   kube-controller-manager-172.16.1.19   1/1       Running   0          2d
   kube-dns-v11-2a66j                    4/4       Running   0          2d
   kube-proxy-172.16.1.19                1/1       Running   0          2d
   kube-proxy-172.16.1.21                1/1       Running   0          2d
   kube-scheduler-172.16.1.19            1/1       Running   0          2d
   kubernetes-dashboard-172.16.1.19      1/1       Running   0          2d

.. _ReplicaSet: https://kubernetes.io/docs/user-guide/replicasets/
.. _Pod: https://kubernetes.io/docs/user-guide/pods/
.. _ServiceAccount: https://kubernetes.io/docs/admin/service-accounts-admin/
.. _Create a new partition: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/tmos-implementations-12-1-0/29.html
.. _Create a Kubernetes Secret containing your Docker login credentials: https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/
