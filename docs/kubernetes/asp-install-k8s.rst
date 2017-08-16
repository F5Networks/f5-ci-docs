.. todo: MOVE TO ASP REPO

.. _install-asp-k8s:

Install the ASP in Kubernetes
=============================

.. sidebar:: Docs test matrix

   We tested this documentation with:

   - ``kubernetes-v1.4.8_coreos.0``
   - ``k8s-bigip-ctlr v1.0.0``
   - ``asp v1.0.0``

Summary
-------

The |asp|, or ASP, runs on each node in a Kubernetes `Cluster`_.
Create a `ConfigMap`_ to configure the ASP; then, create a `DaemonSet`_ to run the ASP in a pod on each node in your cluster.

Initial Setup
-------------

.. include:: /_static/reuse/asp-initial-setup.rst

#. Create a Kubernetes Secret containing your Docker login credentials (required to pull the ``asp`` image from Docker Store).
   The Kubernetes documentation provides instructions for creating the Secret:

   - `Pull an Image from a Private Registry <https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/>`_
   - `Kubernetes API docs <https://kubernetes.io/docs/user-guide/kubectl/v1.6/>`_ (see :code:`secret docker-registry`)

   .. important::

      You must create the Secret in the same namespace the ASP runs in: ``kube-system``.

.. _asp-configure-k8s:

Set up the ASP using a ConfigMap
--------------------------------

#. Define the ASP's `global and orchestration configurations </products/asp/latest/#global>`_ in a ConfigMap.

   .. literalinclude:: /_static/config_examples/f5-asp-k8s-example-configmap.yaml

   :fonticon:`fa fa-download` :download:`f5-asp-k8s-example-configmap.yaml </_static/config_examples/f5-asp-k8s-example-configmap.yaml>`

#. Upload the ConfigMap to Kubernetes.

   .. code-block:: bash

      user@k8s-master:~$ kubectl create -f f5-asp-configmap.yaml
      configmap "f5-asp-config" created

#. Verify creation of the ConfigMap.

   .. code-block:: bash

      user@k8s-master:~$ kubectl get configmap f5-asp-config -o yaml --namespace kube-system
      apiVersion: v1
      data:
        asp.config.json: |
          {
            "global": {
              "console-log-level": "debug"
            },
            "orchestration": {
              "kubernetes": {
                "config-file": "/var/run/kubernetes/proxy-plugin/service-ports.json",
                "poll-interval": 500
              }
            }
          }
      kind: ConfigMap
      metadata:
        creationTimestamp: 2017-02-16T17:55:04Z
        name: f5-asp-config
        namespace: kube-system
        resourceVersion: "1589344"
        selfLink: /api/v1/namespaces/kube-system/configmaps/f5-asp-config
        uid: 0bdc4be2-f471-11e6-92a8-fa163e4f44e9

.. _asp-deploy-k8s:

Create a DaemonSet and launch ASP Pods
--------------------------------------

#. Create a DaemonSet.

   .. important::

      Be sure to include the Secret containing your Docker login credentials.

   .. literalinclude:: /_static/config_examples/f5-asp-k8s-example-daemonset.yaml

   :fonticon:`fa fa-download` :download:`f5-asp-k8s-example-daemonset.yaml </_static/config_examples/f5-asp-k8s-example-daemonset.yaml>`

#. Upload the DaemonSet to Kubernetes.

   .. code-block:: bash

      user@k8s-master:~$ kubectl create -f f5-asp-daemonset.yaml
      daemonset "f5-asp" created

#. Verify the DaemonSet successfully created Pods for each node in the cluster.

   .. note::

      You should see one (1) ``f5-asp`` and one (1) ``kube-proxy`` per node in the cluster.

   .. code-block:: bash

      user@k8s-master:~$ kubectl get pods --namespace kube-system -o wide
      NAME                                  READY     STATUS    RESTARTS   AGE       IP            NODE
      f5-asp-2uore                          1/1       Running   0          55m       172.16.1.21   172.16.1.21
      f5-asp-r4e94                          1/1       Running   0          55m       172.16.1.19   172.16.1.19
      k8s-bigip-ctlr-1439955937-fkfb2       1/1       Running   0          1d        10.2.5.3      172.16.1.21
      kube-apiserver-172.16.1.19            1/1       Running   0          11d       172.16.1.19   172.16.1.19
      kube-controller-manager-172.16.1.19   1/1       Running   0          11d       172.16.1.19   172.16.1.19
      kube-dns-v11-mp8ts                    4/4       Running   0          2d        10.2.5.2      172.16.1.21
      kube-proxy-172.16.1.19                1/1       Running   7          12m       172.16.1.19   172.16.1.19
      kube-proxy-172.16.1.21                1/1       Running   11         4m        172.16.1.21   172.16.1.21
      kube-scheduler-172.16.1.19            1/1       Running   0          11d       172.16.1.19   172.16.1.19
      kubernetes-dashboard-172.16.1.19      1/1       Running   2          11d       172.16.1.19   172.16.1.19


Next Steps
----------

- :ref:`Replace kube-proxy with f5-kube-proxy <k8s-asp-deploy>`.

.. _DaemonSet: https://kubernetes.io/docs/admin/daemons/
.. _Cluster: https://kubernetes.io/docs/admin/cluster-management/
