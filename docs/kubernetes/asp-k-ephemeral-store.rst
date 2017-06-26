.. _install-ephemeral-store-k8s:

Set up ephemeral data storage for the Application Services Proxy
================================================================

.. sidebar Docs test matrix
   We tested this documentation with:
   - ``kubernetes-v1.4.8_coreos.0``
   - ``asp v1.1.0``

.. include:: /_static/reuse/asp-version-added.rst

The |asp| (ASP) shares non-persistent, or ephemeral, data across instances.
It does so by way of a distributed, secure, key-value store called the Ephemeral Store.

You can set up the ASP ephemeral store *before* you `deploy the ASP in Kubernetes <install-asp-k8s>`_,  or add the ephemeral store configurations to an existing ASP.

.. attention::

   The ASP ephemeral store relies on a Kubernetes alpha resource (`PetSet`_).
   You must have Alpha resources enabled on the Kubernetes API server in order to use the ASP.

   See the `Kubernetes API overview <https://kubernetes.io/docs/concepts/overview/kubernetes-api/>`_ for more information.

Set up authentication to the ephemeral store
--------------------------------------------

All communications between clients and the ASP ephemeral store use SSL encryption.
Perform the tasks in this section to set up the certificates required for authentication to the ephemeral store and to secure the certificates using a `Kubernetes Secret`_.

.. _generate_ephemeral_store_certs-k8s:

Generate root and user certificates
```````````````````````````````````

.. include:: /_static/reuse/generate-ephemeral-store-certs.rst


.. _secret-asp-ephemeral-store:

Create Secrets for the root and user certificates
`````````````````````````````````````````````````

Encrypt the :file:`rootCA.key` and :file:`rootCA.crt` as a Kubernetes `Secret`_.

.. code-block:: console

   kubectl create secret tls ephemeral-store-secret --cert=rootCA.crt --key=rootCA.key
   kubectl create secret tls ephemeral-store-secret --cert=myuserCA.crt --key=myuserCA.key


Deploy the ephemeral store
--------------------------

To deploy the ephemeral store, you'll need to:

- Specify configurations in a `ConfigMap`_.
- Create two (2) `Service`_ definitions:

  - one (1) for the ephemeral store,
  - one (1) to manage the `PetSet`_.

- Create a `PetSet`_ to manage the ephemeral store Pods.

.. tip::

   All of the examples presented in the sections that follow are in the same YAML file.
   You can download the example file and modify it to suit your environment, then upload it to Kubernetes to create all of the resources at once.

   :fonticon:`fa fa-download` :download:`ephemeral-store-k8s-example.yaml </_static/config_examples/f5-ephemeral-store-k8s-example.yaml>`


Specify the ASP ephemeral store configurations in a ConfigMap
`````````````````````````````````````````````````````````````

#. Specify the ephemeral store user(s) in a `ConfigMap`_.

   .. note::

      Each user name should match the ``/CN``, or Common Name, defined for a user certificate.

   .. literalinclude:: /_static/config_examples/f5-ephemeral-store-k8s-example.yaml
      :linenos:
      :lines: 1-7

#. Create the ephemeral store Services.

   .. literalinclude:: /_static/config_examples/f5-ephemeral-store-k8s-example.yaml
      :linenos:
      :caption: Ephemeral store Services
      :lines: 9-38

   \

   .. note::

      The first Service - "ephemeral-store-info" - is the PetSet's “governing service”.

#. Create a `PetSet`_.

   The PetSet creates a cluster of five (5) pods running the ephemeral store Services.
   Each pod requires a minimum of **1 CPU** and **1Gi memory**. [#k8smemory]_

   .. literalinclude:: /_static/config_examples/f5-ephemeral-store-k8s-example.yaml
      :linenos:
      :lines: 40-106


#. Upload the YAML file containing the ConfigMap, Services, and PetSet to the Kubernetes API server.

   .. code-block:: bash

      user@k8s-master:~$ kubectl create -f f5-ephemeral-store-k8s-example.yaml
      configmap "ephemeral-store-users" created
      service "ephemeral-store-info" created
      service "ephemeral-store" created
      petset "ephemeral-store" created


#. Verify creation of the ephemeral store cluster, which should consist of five (5) nodes.

   .. code-block:: bash

      user@k8s-master:~$ kubectl get pods --namespace kube-system -o wide
      NAME                       READY     STATUS              RESTARTS   AGE       IP          NODE
      ephemeral-store-0          1/1       Running             0          1m        10.2.55.3   172.16.1.183
      ephemeral-store-1          1/1       Running             0          1m        10.2.76.3   172.16.1.184
      ephemeral-store-2          1/1       Running             0          1m        10.2.76.4   172.16.1.184
      ephemeral-store-3          1/1       Running             0          1m        10.2.55.5   172.16.1.183
      ephemeral-store-4          1/1       Running             0          1m        10.2.76.5   172.16.1.184


Learn More
----------

The ephemeral store is a distributed, secure, key-value store used by ASP instances to store and quickly share non-persistent data.
For example, if an :code:`asp` instance learns that a pool member it monitors is unhealthy, it needs to share that information with other instances monitoring the same pool.
The :code:`asp` instance adds the information to the ephemeral store, so all other :code:`asp` instances immediately have access to the pool's updated health status.
When new data added to the ephemeral store marks the pool member as healthy, the stale information gets deleted.

The ASP also reports session data to the ephemeral store.
Sharing client session information across servers means, for example, that if multiple servers try to establish a session with a client, one will succeed and the others will fail.

Next Steps
----------

Once you've set up the ephemeral store, you can :ref:`install and deploy the ASP <install-asp-k8s>`.

.. rubric:: Footnotes
.. [#k8smemory] See `Set Pod CPU & Memory Limit <https://kubernetes.io/docs/tasks/administer-cluster/cpu-memory-limit/>`_ :fonticon:`fa fa-external-link`.

.. _PetSet: https://kubernetes.io/docs/concepts/workloads/controllers/petset/
