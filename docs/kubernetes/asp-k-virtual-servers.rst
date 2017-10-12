.. todo: MOVE TO ASP REPO

.. _k8s-launch-asp:

Attach an ASP to a Kubernetes Service
=====================================

.. sidebar:: Docs test matrix

   We tested this documentation with:

   - Kubernetes 1.4.8, coreos-beta-1465.3.0, ASP 1.1.0, f5-kube-proxy 1.0.0
   - Kubernetes 1.4.8, coreos-7.2.1511, ASP 1.0.0, f5-kube-proxy 1.0.0
   - `kubernetes hello-world`_ service, with :ref:`ASP annotation <k8s-service-annotate>`


The |asp| (ASP) watches the Kubernetes API for `Services`_ that contain an ASP virtual server `Annotation`_.
The `Annotation`_ consists of a specially-formatted JSON blob defining the `ASP virtual server configuration parameters`_.
When you add the ASP annotation to a Kubernetes `Service`_, the ASP creates a virtual server for the Service with the desired configurations.

.. _k8s-service-annotate:

Add the ASP annotation to the Service
-------------------------------------

To attach an ASP to a Kubernetes `Service`_, add an `Annotation`_ containing the ASP configurations. You can use either the :code:`annotate` CLI command or edit the Service definition.

.. tip::

   The :code:`annotate` command is better suited to adding shorter annotations, like that shown in the example below.
   If you intend to add event handlers, health checks, and/or flags, you may want to edit the Service definition directly.


Use ``kubectl annotate``
````````````````````````

Annotate the `Service`_ definition with the key-value pair ``asp.f5.com/config="<JSON-config-blob>"``.
The JSON config blob should contain the desired `ASP virtual server configuration parameters`_.

.. important::

   When you annotate the Service using :code:`kubectl annotate`, the JSON config blob must use the encoding shown in the example below. Use a backslash -- ``\"`` -- to escape all quotation marks.

\

.. code-block:: bash

   $ kubectl annotate service example-service asp.f5.com/config="{\"ip-protocol\":\"http\",\"load-balancing-mode\":\"round-robin\"}"
   service "example-service" annotated


Edit the Service definition
```````````````````````````

Edit the Service definition file, then upload the file to the Kubernetes API server.

.. literalinclude:: /_static/config_examples/f5-asp-k8s-example-service.yaml
   :caption: Service definition with ASP annotation
   :linenos:

:fonticon:`fa fa-download` :download:`f5-asp-k8s-example-service.yaml </_static/config_examples/f5-asp-k8s-example-service.yaml>`

.. code-block:: bash
   :caption: Upload the Service definition to the Kubernetes API server

   $ kubectl replace -f f5-asp-k8s-example-service.yaml
   service "myService" replaced

.. _event-handlers-k8s:

ASP event handlers
~~~~~~~~~~~~~~~~~~

You can set up `ASP event handlers`_ as part of the virtual server annotation.

.. seealso::

   - Learn about the `ASP event handlers`_.
   - Learn about the `ASP Middleware API`_.

Add the ``event-handlers`` JSON string to the Service definition.

.. important::

   Be sure to format the JSON list as a string as shown in the example below.

\

.. literalinclude:: /_static/config_examples/f5-asp-k8s-example-service.yaml
   :linenos:
   :lines: 12-19



.. _k8s-health-checks:

ASP health checks
~~~~~~~~~~~~~~~~~

.. include:: /_static/reuse/asp-version-added-1_1.rst

To activate the ASP's health monitor:

Add the desired `ASP health check parameters`_ to the ASP annotation in the Service definition.

.. literalinclude:: /_static/config_examples/f5-asp-k8s-example-service.yaml
   :linenos: 
   :lines: 24-39

:fonticon:`fa fa-download` :download:`f5-asp-k8s-example-service.yaml </_static/config_examples/f5-asp-k8s-example-service.yaml>`

.. important::

   Because each ASP instance (one per Node) shares the same global configurations, Service endpoints will receive health probes from all of the ASP instances. The ASP can use a health probe sharding algorithm to reduce probe redundancy.

   This algorithm allocates a subset of endpoints to each ASP instance. Each ASP instance adds the health data for its assigned endpoints to the :ref:`ephemeral store <ephemeral store>`, giving all ASP instances access to the data for all endpoints.

   You can set up ASP health sharding when you :ref:`deploy the ASP <asp-deploy-k8s>`.


Next Steps
----------

- :ref:`Verify that the ASP handles traffic for the Service <k8s-asp-verify>`.
- :ref:`Verify execution of event handlers <k8s-asp-event-handlers-verify>`.

.. _kubernetes hello-world: https://kubernetes.io/docs/tutorials/stateless-application/expose-external-ip-address-service/
.. _Service: https://kubernetes.io/docs/user-guide/services/
.. _Annotation: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/
