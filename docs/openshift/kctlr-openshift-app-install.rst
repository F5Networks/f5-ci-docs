.. _install-kctlr-openshift:

Install the |kctlr-long| in `OpenShift`_ Origin 
===============================================

.. sidebar:: Docs test matrix

   We tested this documentation with:

   - ``kubernetes-v1.4.0 on CentOS 7.2.1511``
   - ``OpenShift v1.4.1``
   - ``k8s-bigip-ctlr v1.1.0``
   - ``k8s-bigip-ctlr v1.0.0``


The |kctlr-long| installs via a `Kubernetes Deployment`_.
The Deployment creates a `ReplicaSet`_ that, in turn, launches a `Pod`_ running the |kctlr| app.

.. attention::

   These instructions are for the `Openshift`_ Origin Kubernetes distribution. **If you are using standard Kubernetes**: Complete the steps in :ref:`Install the BIG-IP Controller for Kubernetes <install-kctlr>`.


Initial Setup
-------------

#. Complete the steps to :ref:`Add BIG-IP device to an OpenShift Cluster <bigip-openshift-setup>`

.. _k8s-openshift-serviceaccount:

2. Create a serviceaccount for the |kctlr|.

   .. code-block:: console

      user@openshift:~$ oc create serviceaccount bigip-ctlr -n kube-system
      serviceaccount "bigip-ctlr" created

#. Create a valid clusterrole.

   .. code-block:: console

      user@openshift:~$ oc create -f f5-kctlr-openshift-clusterrole.yaml
      clusterrole "system:bigip-ctlr" created

   .. literalinclude:: /_static/config_examples/f5-kctlr-openshift-clusterrole.yaml
      :linenos:

   :fonticon:`fa fa-download` :download:`f5-kctlr-openshift-clusterrole.yaml </_static/config_examples/f5-kctlr-openshift-clusterrole.yaml>`

#. Create a valid clusterrole binding.

   .. code-block:: console

      user@openshift:~$ oc create -f f5-kctlr-openshift-clusterrole-binding.yaml
      clusterrolebinding "bigip-ctlr-role" created

   .. literalinclude:: /_static/config_examples/f5-kctlr-openshift-clusterrole-binding.yaml
       :linenos:

   :fonticon:`fa fa-download` :download:`f5-kctlr-openshift-clusterrole-binding.yaml </_static/config_examples/f5-kctlr-openshift-clusterrole-binding.yaml>`


#. :ref:`Add a Kubernetes Secret <k8s-add-secret>` containing your BIG-IP login credentials to your Kubernetes master node.

#. `Create a new partition`_ for Kubernetes on your BIG-IP.
   The |kctlr| can not manage objects in the ``/Common`` partition.

#. `Create a Kubernetes Secret containing your Docker login credentials`_ (required if you need to pull the container image from a private Docker registry).

.. _create-openshift-deployment:

.. important::

   You should create all |kctlr| objects in the ``kube-system`` `namespace`_, unless otherwise specified in the deployment instructions.

.. _openshift-bigip-ctlr-deployment:

Create a Deployment
-------------------

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

Upload the Deployment to the OpenShift API server with the ``oc apply`` command.

.. code-block:: bash

   user@openshift-master:~$ oc apply -f f5-k8s-bigip-ctlr_openshift-sdn.yaml --namespace=kube-system
   deployment "k8s-bigip-ctlr" created


Verify creation
---------------

When you create a Deployment, a `ReplicaSet`_ and `Pod`_ (s) launch automatically.
Use ``oc`` to verify all of the objects launched successfully.

.. code-block:: bash
   :emphasize-lines: 3, 7, 11

   user@k8s-master:~$ oc get deployments --namespace=kube-system
   NAME             DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
   k8s-bigip-ctlr   1         1         1            1           1h

   user@k8s-master:~$ oc get replicasets --namespace=kube-system
   NAME                       DESIRED   CURRENT   AGE
   k8s-bigip-ctlr-331478340   1         1         1h

   user@k8s-master:~$ oc get pods --namespace=kube-system
   NAME                                  READY     STATUS    RESTARTS   AGE
   k8s-bigip-ctlr-331478340-ke0h9        1/1       Running   0          1h
   kube-apiserver-172.16.1.19            1/1       Running   0          2d
   kube-controller-manager-172.16.1.19   1/1       Running   0          2d
   kube-dns-v11-2a66j                    4/4       Running   0          2d
   kube-proxy-172.16.1.19                1/1       Running   0          2d
   kube-proxy-172.16.1.21                1/1       Running   0          2d
   kube-scheduler-172.16.1.19            1/1       Running   0          2d
   kubernetes-dashboard-172.16.1.19      1/1       Running   0          2d

.. _OpenShift: https://www.openshift.org/
.. _ReplicaSet: https://kubernetes.io/docs/user-guide/replicasets/
.. _Pod: https://kubernetes.io/docs/user-guide/pods/
.. _ServiceAccount: https://kubernetes.io/docs/admin/service-accounts-admin/
.. _Create a new partition: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/tmos-implementations-12-1-0/29.html
.. _Create a Kubernetes Secret containing your Docker login credentials: https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/
