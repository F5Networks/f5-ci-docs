.. index::
   single: Application Services Proxy; Ephemeral store; Kubernetes

.. include:: /_static/reuse/asp-version-added-1_1.rst

.. sidebar:: Docs test matrix

   We tested this documentation with:

   - Kubernetes 1.4.8, coreos-beta-1465.3.0, ASP 1.1.0, f5-kube-proxy 1.0.0

.. _install-ephemeral-store-k8s:
.. _ephemeral store:

Set up the ASP ephemeral store - Kubernetes
===========================================

The |asp| (ASP) ephemeral store is a distributed, in-memory, secure key-value store.
It allows multiple ASP instances to share non-persistent, or :dfn:`ephemeral`, data.

.. attention::

   The ASP ephemeral store requires a Kubernetes alpha resource (PetSet).
   You must have alpha resources enabled on the Kubernetes API server in order to use the ASP with the ephemeral store.

   See the `Kubernetes API overview <https://kubernetes.io/docs/concepts/overview/kubernetes-api/>`_ for more information.

.. important::

   The ASP does not watch the Kubernetes API for changes to ConfigMaps.
   This means that you must set up the ASP ephemeral store *before* you `deploy the ASP <install-asp-k8s>`_.

.. warning::

   The ephemeral store is not compatible with ASP v1.0.0.
   If you have a previous version of the ASP running, remove it and :ref:`create new resources <asp-deploy-k8s>` for ASP v1.1.0.

   Delete the ConfigMap, Deployment, and kill all ASP pods:

   .. code-block:: bash

      $ kubectl delete -f f5-asp-k8s-example-configmap.yaml
      $ kubectl delete -f f5-asp-k8s-example-daemonset.yaml
      $ kubectl delete pods -l name=f5-asp -n kube-system


.. _k8s ephemeral store auth:

Set up authentication to the ephemeral store
--------------------------------------------

All communications between clients and the ASP ephemeral store use SSL encryption.
Complete the tasks in this section to create and secure the certificates required for authentication to the ephemeral store.

.. _generate_ephemeral_store_certs-k8s:

Generate certificates
`````````````````````

.. tip::

   When working from the examples provided below, change "myuser" to the username of the account needing access the ephemeral store data.

.. include:: /_static/reuse/generate-ephemeral-store-certs.rst


.. _secret-ephemeral-store:

Create Secrets for the certificates
```````````````````````````````````

Run the commands shown below to encrypt the certificates as Kubernetes Secrets.
This example creates three (3) Secrets:

- Provide the first (``ephemeral-store-root``) in the ephemeral store PetSet.
- Provide the second and third in the :ref:`ASP Daemonset <asp-deploy-k8s>`.
  These allow ASP instances to access the ephemeral store.

  .. note::

     The third secret should contain only the root certificate, **without the key**.
     Be sure to create this certificate-only secret in the ``kube-system`` namespace.

\

.. code-block:: bash

   kubectl create secret tls ephemeral-store-root --cert=rootCA.crt --key=rootCA.key
   kubectl create secret tls ephemeral-store-myuser --cert=myuser.crt --key=myuser.key -n kube-system
   kubectl create secret generic ephemeral-store-user-rootca-cert --from-file=rootCA.crt -n kube-system

.. _deploy-ephemeral-store-k8s:

Deploy the ephemeral store
--------------------------

The ephemeral store deployment consists of a ConfigMap, two (2) Services, and a PetSet. [#petset]_
You can define all of the required resources in a single YAML file.

.. important::

   - Each ephemeral store Pod requires 1 CPU and at least 1Gi memory.
   - By default, the ephemeral store PetSet deploys five (5) Pods.
     **Do not deploy the ephemeral store with fewer than five instances or you may experience data loss.**

\

.. literalinclude:: /kubernetes/config_examples/f5-ephemeral-store-k8s-example.yaml

:fonticon:`fa fa-download` :download:`ephemeral-store-k8s-example.yaml </kubernetes/config_examples/f5-ephemeral-store-k8s-example.yaml>`

.. note for kubernetes v1.5 and higher support -- PetSet changed to StatefulSet and requires apps/v1beta1

#. Upload the YAML file containing the ConfigMap, Services, and PetSet to the Kubernetes API server.

   .. code-block:: bash

      kubectl create -f f5-ephemeral-store-k8s-example.yaml
      configmap "ephemeral-store-users" created
      service "ephemeral-store-info" created
      service "ephemeral-store" created
      petset "ephemeral-store" created

#. Verify creation of the ephemeral store cluster, which should consist of five (5) Pods.

   .. important::

      Due to the ephemeral store size requirements, the initial launch of these Pods can take a few minutes.
      If a Pod stays in pending status for an extended period of time, you may have run out of CPU.

      Run :code:`kubectl describe pods <pod_name>` to debug.

   \

   .. code-block:: bash

      kubectl get pods -o wide
      NAME                       READY     STATUS              RESTARTS   AGE       IP          NODE
      ephemeral-store-0          1/1       Running             0          1m        10.2.55.3   172.16.1.183
      ephemeral-store-1          1/1       Running             0          1m        10.2.76.3   172.16.1.184
      ephemeral-store-2          1/1       Running             0          1m        10.2.76.4   172.16.1.184
      ephemeral-store-3          1/1       Running             0          1m        10.2.55.5   172.16.1.183
      ephemeral-store-4          1/1       Running             0          1m        10.2.76.5   172.16.1.184

Next Steps
----------

Once you've set up the ephemeral store, :ref:`install and deploy the ASP <install-asp-k8s>`.

.. _k8s-ephemeral-store-update:


Learn More
----------

See the `ASP ephemeral store`_ and `ASP health monitor`_ documentation.

.. rubric:: Footnotes
.. [#k8smemory] See `Set Pod CPU & Memory Limit <https://kubernetes.io/docs/tasks/administer-cluster/memory-default-namespace/>`_ :fonticon:`fa fa-external-link`.
.. [#petset] PetSets changed to StatefulSets in Kubernetes v1.5.

