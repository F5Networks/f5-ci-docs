.. _configuring-asp-health-k8s:

Health monitoring with the Application Services Proxy in Kubernetes
===================================================================

.. include:: /_static/reuse/asp-version-added.rst

The |asp| (ASP) supports health monitoring of service endpoints to obtain health status
and using that information for load-balancing traffic across healthy endpoints.

ASP health monitoring offers the following advantages over `live probe <https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-probes/>`_

* Provides network health view of a service endpoint in addition to application
  health view provided by kubelet issuing node local liveness probes.
* ASP health monitoring detects if a service endpoint is healthy to receive
  client traffic and removes it from the load-balancing pool if found unhealthy.
* Opportunistic health checks by observing client traffic via passive
  health monitoring.
* Ability to combine health information from various health check types i.e.
  passive and active probing giving a more comprehensive health status of an endpoint.

Read more about health monitoring feature `here </products/asp/latest/healthMonitorDoc.html>`_.


Set up the ASP health sharding with ephemeral store support
-----------------------------------------------------------

You define active health checks on a service by service basis. The ASP will then send probes to each endpoint associate
with the service.  In kubernetes, since the ASP acts as a client proxy, each ASP will have the same configuration
for all services in the cluster.  This will result in endpoints receiving redundant probes, one from each ASP.

The ASP can solve the redundant probe issue by sharding health probes, where each ASP uses an identical algorithm
to determine a subset of endpoints to probe.  The ASPs can then share their health information with one another by
storing the results of the probes in an :ref:`ephemeral store database<install-ephemeral-store-k8s>`.

To enable health monitoring sharding with ephemeral store support, you must make the following modifications to the :ref:`ASP install<install-asp-k8s>`.

.. _asp-health-configure-k8s:

#. Modify the ASP ConfigMap

   Modify step 1 of :ref:`asp-configure-k8s` to define a ``health`` component as part of the ``ephemeral-store`` configuration.

   The ``nodes`` field should list unique identifiers for all ASPs in the cluster.  One such identifier can be the node IP address.

   .. code-block:: bash

     user@k8s-master:~$ kubectl get nodes -o 'custom-columns=IP:.spec.externalID'
     IP
     172.16.1.3
     172.16.1.5
     172.16.1.6

   .. _asp-health-deploy-k8s:

#. Modify the ASP DaemonSet

   Modify step 1 of :ref:`Creating a Daemon Set <asp-deploy-k8s>` to define an environment variable ASP_HEALTH_NODE_ID.  The
   value of the variable must identify the unique ID for that particular ASP.


.. _k8s-health-service-annotate:

Configuring services for ASP health monitoring
----------------------------------------------

The user must update the annotation key ``asp.f5.com/config`` of the :ref:`service definition file <k8s-service-annotate>`
with a health monitor section for each service that requires health monitoring.


.. _learn-more:

Learn More
----------

You can find further details on the ASP health monitoring feature in the `health monitor page </products/asp/latest/healthMonitorDoc.html>`_
of the `ASP product documentation`_.
