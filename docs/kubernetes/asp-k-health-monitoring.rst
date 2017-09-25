.. _configuring-asp-health-k8s:

Health monitoring with the Application Services Proxy in Kubernetes
===================================================================

.. include:: /_static/reuse/asp-version-added.rst

The |asp| (ASP) supports direct health monitoring of service endpoints. The ASP can obtain 
health information on the endpoints by employing two types of health checks:

* Active probing using HTTP requests
* Passive monitoring of client traffic

Using ASP health checks provides the following advantages over the `live probe <https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-probes/>`_
health checks that are part of the kubernetes orchestration environment:

* More accurate view of the services' health since the ASP is in the traffic path
* Finer control on issuing active health probes and the conditions which indicate a failure
* Quicker response to changing health conditions


Set up the ASP health monitor to use the ephemeral store
--------------------------------------------------------

You define active health checks on a service by service basis. The ASP will then send probes to each endpoint associate
with the service.  In kubernetes, since the ASP acts as a client proxy, each ASP will have the same configuration
for all services in the cluster.  This will result in endpoints receiving redundant probes, one from each ASP.

The ASP can solves the redundant probe issue by deploying an :ref:`ephemeral store database<install-ephemeral-store-k8s>`.
To enable health monitoring with ephemeral store support, you must make two modifications to the :ref:`ASP install<install-asp-k8s>`.

#. Modify the ASP ConfigMap

   Modify step 1 of :ref:`asp-configure-k8s` to define a ``health`` component as part of the ``ephemeral-store`` configuration.

   .. literalinclude:: /_static/config_examples/f5-asp-k8s-health-example-configmap.yaml
      :linenos:
      :emphasize-lines: 15-24

   :fonticon:`fa fa-download` :download:`f5-asp-k8s-health-example-configmap.yaml </_static/config_examples/f5-asp-k8s-health-example-configmap.yaml>`

   The ``nodes`` field should list unique identifiers for all ASPs in the cluster.  One such identifier can be the node IP address.

   .. code-block:: bash

     user@k8s-master:~$ kubectl get nodes -o 'custom-columns=IP:.spec.externalID'
     IP
     172.16.1.3
     172.16.1.5
     172.16.1.6

#. Modify the ASP DaemonSet

   Modify step 1 of :ref:`Creating a Daemon Set <asp-deploy-k8s>` to define an environment variable ASP_HEALTH_NODE_ID.  The
   value of the variable must identify the unique ID for that particular ASP.

   .. literalinclude:: /_static/config_examples/f5-asp-k8s-health-example-daemonset.yaml
      :linenos:
      :emphasize-lines: 23-27

   :fonticon:`fa fa-download` :download:`f5-asp-k8s-health-example-daemonset.yaml </_static/config_examples/f5-asp-k8s-health-example-daemonset.yaml>`


Configuring services for ASP health monitoring
----------------------------------------------

The user must update the annotation key ``asp.f5.com/config``
with a health monitor section for each :ref:`service<k8s-service-annotate>` that requires health monitoring.
We have enhanced the example used in :ref:`Annotate a Kubernetes Service<k8s-service-annotate>` to include a
health monitor section, as shown below.

   .. literalinclude:: /_static/config_examples/f5-asp-k8s-health-example-service.yaml
      :linenos:
      :emphasize-lines: 14-29

   :fonticon:`fa fa-download` :download:`f5-asp-k8s-health-example-service.yaml </_static/config_examples/f5-asp-k8s-health-example-service.yaml>`


Learn More
----------

You can find further details on the ASP health feature in the `health section </products/asp/latest/healthMonitorDoc.html>`_
of the `ASP product documentation </products/asp/latest/index.html>`_.
