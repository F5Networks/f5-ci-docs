.. _install-ephemeral-store-k8s:

.. index::
   single: Application Services Proxy, Ephemeral store

.. include:: /_static/reuse/asp-version-added-1_1.rst

.. sidebar:: Docs test matrix

   We tested this documentation with:

   - Kubernetes 1.4.8, coreos-beta-1465.3.0, ASP 1.1.0, f5-kube-proxy 1.0.0
   - Kubernetes 1.4.8, coreos-7.2.1511, ASP 1.0.0, f5-kube-proxy 1.0.0

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
   If you have a previous version of the ASP running, set up the ephemeral store, then :ref:`update the ASP <k8s-ephemeral-store-update>`.

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
   kubectl create secret tls ephemeral-store-myuser --cert=myuser.crt --key=myuser.key
   kubectl create secret generic ephemeral-store-user-rootca-cert --from-file=rootCA.crt -n kube-system

.. _deploy-ephemeral-store-k8s:

Deploy the ephemeral store
--------------------------

The ephemeral store deployment consists of a ConfigMap, two (2) Services, and a PetSet. [#petset]_
You can define all of the required resources in a single YAML file.

.. important::

   Each pod requires a **minimum of 1 CPU and 1Gi memory**. [#k8smemory]_

\

.. literalinclude:: /_static/config_examples/f5-ephemeral-store-k8s-example.yaml

:fonticon:`fa fa-download` :download:`ephemeral-store-k8s-example.yaml </_static/config_examples/f5-ephemeral-store-k8s-example.yaml>`

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

If you already have the ASP running, complete the update tasks provided in the next section.

.. _k8s-ephemeral-store-update:

Update an existing ASP to use the ephemeral store
-------------------------------------------------

#. Update the ASP resource manifest:

   - Add the ephemeral store section to the ASP ConfigMap.

   .. literalinclude:: /_static/config_examples/f5-asp-k8s.yaml
      :lines: 11-27

   - Update the DaemonSet:

     - Update the ASP image to v1.1.0 (:code:`image: "store/f5networks/asp:1.1.0"`)

     .. literalinclude:: /_static/config_examples/f5-asp-k8s.yaml
        :lines: 51

     - Add the ASP health sharding :code:`env` section.

     .. literalinclude:: /_static/config_examples/f5-asp-k8s.yaml
        :lines: 60-66

     - Add the ephemeral store :code:`volumeMounts` to the :code:`container` section.
     - Add the ephemeral store volumes.

     .. literalinclude:: /_static/config_examples/f5-asp-k8s.yaml
        :lines: 67-104


#. Upload the edited file to the Kubernetes API server.

   .. code-block:: bash

      $ kubectl replace -f f5-asp-k8s.yaml -n kube-system

#. Kill the existing ASP Pods, then verify that the new Pods run with the updated ASP version and configurations.

   .. code-block:: bash
      :emphasize-lines: 7, 25

      $ kubectl get pods -n kube-system
      NAME                                 READY     STATUS    RESTARTS   AGE
      f5-asp-543io                         1/1       Running   0          48m
      f5-asp-kkze3                         1/1       Running   0          48m
      ...

      $ kubectl delete pod f5-asp-543io f5-asp-kkze3 -n kube-system
      pod "f5-asp-543io" deleted
      pod "f5-asp-kkze3" deleted

      $ kubectl get pods -n kube-system
      NAME                                 READY     STATUS    RESTARTS   AGE
      f5-asp-t56e5                         1/1       Running   0          4s
      f5-asp-v2gxv                         1/1       Running   0          4s
      ...

      $ kubectl describe pod f5-asp-t56e5 -n kube-system
      Name:		f5-asp-t56e5
      Namespace:	kube-system
      Node:		172.16.1.5/172.16.1.5
      ...
      Containers:
        f5-asp:
          Container ID:	docker://a469ae3cb7591d37c93c529d1a0271348893e9605e64043e43ed477730913d23
          Image:		docker-registry.pdbld.f5net.com/velcro/asp:master
      ...


Learn More
----------

See the `ASP ephemeral store`_ and `ASP health monitor`_ documentation.

.. rubric:: Footnotes
.. [#k8smemory] See `Set Pod CPU & Memory Limit <https://kubernetes.io/docs/tasks/administer-cluster/cpu-memory-limit/>`_ :fonticon:`fa fa-external-link`.
.. [#petset] PetSets changed to StatefulSets in Kubernetes v1.5. F5 does not support deployment of the ASP on v1.5 or later.

