:product: BIG-IP Controller for Kubernetes
:type: task

.. _install-kctlr:

Install the BIG-IP Controller: Kubernetes
=========================================

The |kctlr-long| installs via a Kubernetes `Deployment`_.
The Deployment creates a `ReplicaSet`_ that, in turn, launches a `Pod`_ running the |kctlr| app.

If you use `helm`_ you can use the `f5-bigip-ctlr chart`_ to create and manage the resources below.

.. attention::

   These instructions are for a standard Kubernetes environment.
   **If you are using OpenShift**, see :ref:`Install the BIG-IP Controller for Kubernetes in OpenShift Origin <install-kctlr-openshift>`.


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

   You can restrict the permissions granted in the cluster role as needed for your deployment.
   The table below shows the supported permission set (these are also provided in the Cluster Role example below).

   +--------------+-------------------+---------------------------------------------+
   | API groups   | Resources         | Actions                                     |
   +==============+===================+=============================================+
   | ""           | endpoints         | get, list, watch                            |
   |              +-------------------+                                             |
   |              | namespaces        |                                             |
   |              +-------------------+                                             |
   |              | nodes             |                                             |
   |              +-------------------+                                             |
   |              | pods              |                                             |
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

   .. literalinclude:: /kubernetes/config_examples/f5-k8s-sample-rbac.yaml
      :linenos:

   :fonticon:`fa fa-download` :download:`f5-k8s-sample-rbac.yaml </kubernetes/config_examples/f5-k8s-sample-rbac.yaml>`


.. _k8s-bigip-ctlr-deployment:

Create a Deployment
-------------------

Define the |kctlr| configurations in a Kubernetes `Deployment`_ using valid JSON or YAML.

.. literalinclude:: /kubernetes/config_examples/f5-k8s-bigip-ctlr_image-secret.yaml
   :linenos:

:fonticon:`fa fa-download` :download:`f5-k8s-bigip-ctlr_image-secret.yaml </kubernetes/config_examples/f5-k8s-bigip-ctlr_image-secret.yaml>`

.. danger::

   Do not increase the :code:`replica` count in the Deployment. Running duplicate Controller instances may cause errors and/or service interruptions.

.. important::

   If :ref:`your BIG-IP device connects to the Cluster network via flannel VXLAN <use-bigip-k8s-flannel>`, be sure to define the following `k8s-bigip-ctlr configuration parameters`_ in your Deployment:

   - :code:`--pool-member-type=cluster` (See :ref:`cluster mode` for more information.)
   - :code:`--flannel-name=[bigip_tunnel_name]`

.. _upload to k8s api:

Upload the Resources to the Kubernetes API server
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

You should see one ``k8s-bigip-ctlr`` `Pod`_ for each node in the cluster. The example below shows one (1) Pod running the ``k8s-bigip-ctlr`` in a test cluster with one worker node.

.. code-block:: console
   :emphasize-lines: 3

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

- :ref:`Create a BIG-IP Virtual Server for a Service <kctlr-per-svc-vs>` (L4 ingress).
- :ref:`Create a BIG-IP Virtual Server for an Ingress resource <kctlr-ingress-config>` (L7 ingress).
- Check out the `k8s-bigip-ctlr reference documentation`_.
