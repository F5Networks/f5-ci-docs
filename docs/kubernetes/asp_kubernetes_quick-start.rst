.. _asp-k8s-quickstart:

Launch the |asp| in Kubernetes
==============================

.. toctree::
     :caption: Contents
     :maxdepth: 4

The F5 |asp| runs on each node in a `Kubernetes Cluster`_. It load balances requests to the correct `Kubernetes Pod`_ for each `Kubernetes Service`_ it manages.

Objectives
----------

The purpose of this tutorial is to walk through the tasks necessary to run the F5 |asp| in `Kubernetes`_.

- Deploy the |asp| with a `Kubernetes DaemonSet`_.
- Run ``f5-kube-proxy`` on each `Kubernetes Pod`_ in your cluster.

Requirements
------------

- `Kubernetes`_ 1.3.7+

Before you begin
----------------

To complete this tutorial, you need:

- a running `Kubernetes Cluster`_ ;
- `kubectl <https://kubernetes.io/docs/user-guide/kubectl-overview/>`_ (the Kubernetes CLI) configured to communicate with your cluster.


Deploy the |asp|
----------------

#. Define the |asp| :ref:`global <tbd>` settings in a `ConfigMap`_.

    .. literalinclude:: /_static/config_examples/f5-asp-k8s-example-configmap.yaml
        :linenos:
        :emphasize-lines: 7-18

    :download:`f5-asp-k8s-example-configmap.yaml </_static/config_examples/f5-asp-k8s-example-configmap.yaml>`

#. Create a `Kubernetes Daemonset`_.

    .. literalinclude:: /_static/config_examples/f5-asp-k8s-example-daemonset.yaml
        :linenos:
        :emphasize-lines: 4, 5, 10, 14-26, 28-33

    :download:`f5-asp-k8s-example-daemonset.yaml </_static/config_examples/f5-asp-k8s-example-daemonset.yaml>`

#. Upload the ConfigMap and DaemonSet to Kubernetes with ``kubectl``.

    .. code-block:: bash

        $ kubectl create -f example-lwp-configmap.yaml
        configmap "lwp-config" created
        $ kubectl create -f quickstart-lwp-daemonset.yaml
        daemonset "lightweight-proxy" created

#. Verify that the |asp| is running:

    .. code-block:: bash

        $ kubectl get pods -l name=lightweight-proxy --namespace kube-system
        NAME                      READY     STATUS    RESTARTS   AGE
        lightweight-proxy-f0tt9   1/1       Running   0          5m
        lightweight-proxy-gt0i2   1/1       Running   0          5m
        lightweight-proxy-l4swr   1/1       Running   0          5m
        lightweight-proxy-p5uit   1/1       Running   0          5m


Run f5-kube-proxy on Kubernetes pods
------------------------------------

#. Edit the `Static Pod`_ manifest on each `Kubernetes node`_ (for example, :file:`/etc/kubernetes/kube-proxy.yaml`).

    .. literalinclude:: /_static/config_examples/f5-asp-k8s-example-pod-manifest.yaml
        :linenos:
        :emphasize-lines: 10

    :download:`quickstart-kube-proxy.yaml </_static/config_examples/f5-asp-k8s-example-pod-manifest.yaml>`

#. Verify that the kube-proxy pods are up and running.

    .. code-block:: bash

        kubectl get pods -l name=kube-proxy --namespace kube-system
        NAME                                   READY     STATUS    RESTARTS   AGE
        f5-k8s-controller-1659257167-ftfx9     1/1       Running   0          1h
        heapster-v1.2.0-4088228293-05kbm       2/2       Running   2          4d
        kube-apiserver-172.17.4.101            1/1       Running   1          4d
        kube-controller-manager-172.17.4.101   1/1       Running   1          4d
        kube-dns-v20-tw5b2                     3/3       Running   3          4d
        kube-proxy-172.17.4.101                1/1       Running   1          4d
        kube-proxy-172.17.4.201                1/1       Running   2          3m
        kube-proxy-172.17.4.202                1/1       Running   2          4m
        kube-proxy-172.17.4.203                1/1       Running   3          13m

