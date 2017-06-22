.. _install-kctlr:

Install the |kctlr-long|
========================

.. sidebar:: Docs test matrix

   We tested this documentation with:

   - ``kubernetes-v1.4.8_coreos.0``
   - |kctlr| ``v1.0.0``

The |kctlr-long| installs via a `Kubernetes Deployment`_.
The Deployment creates a `ReplicaSet`_ that, in turn, launches a `Pod`_ running the |kctlr| app.

Before you begin
----------------

* :ref:`Add a Kubernetes Secret <k8s-add-secret>` containing your BIG-IP user credentials to your Kubernetes master.
* `Create a new partition`_ for Kubernetes on your BIG-IP.
  The |kctlr| can not manage objects in the ``/Common`` partition.
* *OPTIONAL*: Create a Kubernetes :ref:`docker-registry secret <k8s-secret-docker-config>` if you intend to pull the container image from a private Docker registry.
* **If you're using OpenShift**, complete the steps in :ref:`Use BIG-IP in an OpenShift Cluster <bigip-openshift-setup>` before proceeding.

.. _create-k8s-deployment:

.. important::

   You should create all |kctlr| objects in the ``kube-system`` `namespace`_, unless otherwise specified in the deployment instructions.

.. _k8s-bigip-ctlr-deployment:

Create a Deployment
-------------------

Kubernetes
``````````

Define a `Kubernetes Deployment`_ using valid JSON or YAML.

.. literalinclude:: /_static/config_examples/f5-k8s-bigip-ctlr_image-secret.yaml
   :linenos:


:fonticon:`fa fa-download` :download:`f5-k8s-bigip-ctlr_image-secret.yaml </_static/config_examples/f5-k8s-bigip-ctlr_image-secret.yaml>`


OpenShift Origin
````````````````

Define an OpenShift Deployment using valid JSON or YAML.

.. important::

    OpenShift deployments must use the following required configuration parameters:

    - ``pool-member-type=cluster``
    - ``openshift-sdn-name=</BIG-IP-partition/BIG-IP-vxlan-tunnel>``

.. literalinclude:: /_static/config_examples/f5-k8s-bigip-ctlr_openshift-sdn.yaml
    :linenos:

:fonticon:`fa fa-download` :download:`f5-k8s-bigip-ctlr_openshift-sdn.yaml </_static/config_examples/f5-k8s-bigip-ctlr_openshift-sdn.yaml>`


Upload the Deployment
---------------------

Upload the Deployment to the Kubernetes or OpenShift API server with the ``kubectl create`` command.

.. code-block:: bash

   user@k8s-master:~$ kubectl create -f k8s-bigip-ctlr_image-secret.yaml --namespace=kube-system
   deployment "k8s-bigip-ctlr" created


Verify creation
---------------

When you create a Deployment, a `ReplicaSet`_ and `Pod`_ (s) launch automatically.
Use ``kubectl`` to verify all of the objects launched successfully.

.. code-block:: bash
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
.. _Create a new partition: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/tmos-implementations-12-1-0/29.html
