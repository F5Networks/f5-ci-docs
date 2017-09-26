.. todo: MOVE TO ASP REPO

.. index::
   single: Application Services Proxy; install; Kubernetes

.. sidebar:: Docs test matrix

   We tested this documentation with:

   - Kubernetes 1.4.8, coreos-beta-1465.3.0, ASP 1.1.0, f5-kube-proxy 1.0.0
   - Kubernetes 1.4.8, coreos-7.2.1511, ASP 1.0.0, f5-kube-proxy 1.0.0

.. _install-asp-k8s:

Install the ASP in Kubernetes
=============================

The |asp|, or ASP, runs on each node in a Kubernetes `Cluster`_.
Create a `ConfigMap`_ to configure the ASP; then, create a `DaemonSet`_ to run the ASP in a pod on each node in your cluster.

Initial Setup
-------------

.. include:: /_static/reuse/asp-initial-setup.rst

#. Create a Secret containing your Docker login credentials (required to pull the ``asp`` image from Docker Store).

   Kubernetes' documentation provides instructions for creating the Secret:

   - `Pull an Image from a Private Registry <https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/>`_
   - `Kubernetes API docs <https://kubernetes.io/docs/user-guide/kubectl/v1.6/>`_ (see :code:`secret docker-registry`)

   \

   .. important::

      - If you encounter an error when logging in to Docker, you may need to use sudo: :code:`sudo docker login`.
      - You must create the Secret in the ``kube-system`` namespace so the ASP can find it.

#. :ref:`Set up the ASP ephemeral store <install-ephemeral-store-k8s>`. [#aspreq]_

#. Find the unique identifier(s) for each node in the cluster (for example, the Node IP).
   You'll need to provide this information in the ASP ConfigMap if you want to set up health checks.

   .. code-block:: bash

      $ kubectl get nodes -o 'custom-columns=IP:.spec.externalID'
      IP
      172.16.1.3
      172.16.1.5
      172.16.1.6

.. _asp-configure-k8s:

.. _asp-deploy-k8s:

Set up and launch the ASP
-------------------------

The ASP consists of a ConfigMap and a DaemonSet.
The former contains the ASP's `global and orchestration configurations </products/asp/latest/#global>`_.
The latter launches and manages a set of Pods running the ASP application.
You can define both resources in a single YAML file.

.. important::

   - You can use the ASP with or without :ref:`ASP health checks <asp-health-k8s>`.

     The example shown below include the sections pertaining to health sharding (highlighted).
     Click the link below to download an example that excludes these sections.

     :fonticon:`fa fa-download` :download:`f5-asp-k8s-no-health-sharding.yaml </_static/config_examples/f5-asp-k8s-no-health-sharding.yaml>`

   - Be sure to include the Secret containing your Docker login credentials in the DaemonSet.


#. Define the ASP resources.

   .. literalinclude:: /_static/config_examples/f5-asp-k8s.yaml
      :linenos:
      :emphasize-lines: 15-26, 60-66

   :fonticon:`fa fa-download` :download:`f5-asp-k8s-example-daemonset.yaml </_static/config_examples/f5-asp-k8s.yaml>`

#. Upload the resources to the Kubernetes API server.

   .. code-block:: bash

      $ kubectl create -f f5-asp-k8s.yaml
      configmap "f5-asp-config" created
      daemonset "f5-asp" created

#. Verify creation of the resources.

   .. code-block:: bash
      :caption: ASP ConfigMap

      $ kubectl get configmap f5-asp-config -o yaml --namespace kube-system
      apiVersion: v1
      data:
        asp.config.json: |
          {
            "global": {
              "console-log-level": "info",
              "ephemeral-store": {
                # Cluster IP address of the ephemeral store Service
                "host": "10.2.11.4",
                "port": 8087
                "components": {
                  "health": {
                    "nodes": [
                      # values should match the node name/IP on which the ASP daemonset will be running.
                      "172.16.1.3",
                      "172.16.1.5"
                    ]
                    "replication-count": 2
                  }
                }
              }
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
        creationTimestamp: 2017-09-29T16:28:00Z
        name: f5-asp-config
        namespace: kube-system
        resourceVersion: "151448"
        selfLink: /api/v1/namespaces/kube-system/configmaps/f5-asp-config
        uid: 290f8517-a533-11e7-8fb7-fa163e4bc92a

   \

   .. code-block:: bash
      :caption: ASP Pods
      :emphasize-lines: 3-4

      $ kubectl get pods --namespace kube-system -o wide
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

   \

   .. note::

      - You should see one (1) ``f5-asp`` instance and one (1) ``kube-proxy`` instance for each node in the cluster.
      - The ASP instances may display an error status if all of the :ref:`ephemeral store` Pods haven't successfully launched yet.
        These errors will resolve once all Pods are online.



Next Steps
----------

- :ref:`Replace kube-proxy with f5-kube-proxy <k8s-asp-deploy>`.

.. rubric:: Footnotes
.. [#aspreq] *Required as of* ``asp v1.1.0``.

.. _DaemonSet: https://kubernetes.io/docs/admin/daemons/
.. _Cluster: https://kubernetes.io/docs/admin/cluster-management/
