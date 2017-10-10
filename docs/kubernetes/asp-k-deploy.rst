.. todo: MOVE TO ASP REPO

.. _k8s-asp-deploy:

Replace kube-proxy with the f5-kube-proxy
=========================================

.. sidebar:: Docs test matrix

   Documentation manually tested with:

   Kubernetes 1.4.8, coreos-beta-1465.3.0, ASP 1.1.0
   Kubernetes 1.4.8, coreos-7.2.1511, ASP 1.0.0

Summary
-------

The |aspk| is a container-based application that runs in a `Pod`_ on each `Node`_ in a Kubernetes `Cluster`_.
It takes the place of the standard Kubernetes ``kube-proxy`` component.

.. seealso::

   `Kubernetes Proxies <https://kubernetes.io/docs/concepts/cluster-administration/proxies/>`_


.. _k8s-pod-manifest:

Replace kube-proxy with |aspk| in the Pod Manifests
---------------------------------------------------

.. important::

   Kubernetes "master" and "worker" nodes have distinct Pod Manifests.
   You need to update both to use |aspk|.

   The `CoreOS on Kubernetes Getting Started Guide`_ provides instructions for setting up kube-proxy on master and worker nodes.

.. code-block:: console
   :caption: SSH to a node and edit the kube-proxy manifest

   ssh core@172.16.1.21
   Last login: Fri Feb 17 18:33:35 UTC 2017 from 172.16.1.20 on pts/0
   CoreOS alpha (1185.3.0)
   Update Strategy: No Reboots
   core@k8s-worker-0 ~ $ sudo su
   k8s-worker-0 core \# vim /etc/kubernetes/manifests/kube-proxy.yaml

#. Edit the `kube-proxy`_ manifest on each node to match the :ref:`manifest examples <k8s-pod-manifest-examples>`.

   The key additions/changes are:

   .. code-block:: bash
      :caption: Change the command to ``/proxy`` in the worker pod manifest(s).

      spec:
        containers:
          command: /proxy

   .. code-block:: bash
      :caption: Replace the image with the ``f5-kube-proxy`` image in both master and worker manifests.

      spec:
        containers:
          image: f5networks/f5-kube-proxy:1.0.0

   .. code-block:: bash
      :caption: Add a new ``mountPath`` to the ``volumeMounts`` section in both master and worker manifests.

      spec:
        containers:
          volumeMounts:
            ...
            - mountPath: /var/run/kubernetes/proxy-plugin
              name: plugin-config
              readOnly: false

   .. code-block:: bash
      :caption: Add ``plugin-config`` to the ``volumes`` section in both master and worker manifests.

      spec:
        volumes:
          ...
          - name: plugin-config
            hostPath:
              path: /var/run/kubernetes/proxy-plugin


.. _k8s-pod-manifest-examples:

Examples
--------

.. literalinclude:: /kubernetes/config_examples/f5-kube-proxy-manifest-master.yaml
    :caption: kube-proxy manifest on MASTER node
    :linenos:

:fonticon:`fa fa-download` :download:`f5-kube-proxy-manifest-master.yaml </kubernetes/config_examples/f5-kube-proxy-manifest-master.yaml>`

.. literalinclude:: /kubernetes/config_examples/f5-kube-proxy-manifest-worker.yaml
    :caption: kube-proxy manifest on WORKER node
    :linenos:

:fonticon:`fa fa-download` :download:`f5-kube-proxy-manifest-worker.yaml </kubernetes/config_examples/f5-kube-proxy-manifest-worker.yaml>`


.. _Pod: https://kubernetes.io/docs/user-guide/pods/
.. _Cluster: https://kubernetes.io/docs/admin/cluster-management/
.. _Node: https://kubernetes.io/docs/admin/node/
.. _CoreOS on Kubernetes Getting Started Guide: https://coreos.com/kubernetes/docs/1.6.1/deploy-master.html#set-up-the-kube-proxy-pod
