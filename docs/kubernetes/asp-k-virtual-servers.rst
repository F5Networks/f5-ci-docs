.. todo: MOVE TO ASP REPO

.. _k8s-launch-asp:

Attach an ASP to a Kubernetes Service
=====================================

.. sidebar:: Docs test matrix

   We tested this documentation with:

   - Kubernetes 1.4.8, coreos-beta-1465.3.0, ASP 1.1.0, f5-kube-proxy 1.0.0
   - Kubernetes 1.4.8, coreos-7.2.1511, ASP 1.0.0, f5-kube-proxy 1.0.0
   - `kubernetes hello-world`_ service, with :ref:`ASP annotation <k8s-service-annotate>`


The |asp| (ASP) watches Kubernetes `Service`_ definitions for a set of annotations defining virtual server objects.
 The annotation should include a JSON blob defining of a set of `ASP configuration parameters </products/asp/latest/index.html#configuration-parameters>`_.
 When you add the ASP annotation to a Kubernetes `Service`_, the ASP creates a virtual server for that Service.

.. _k8s-service-annotate:

Add the ASP annotation to the Service
-------------------------------------

To attach an ASP to a Kubernetes `Service`_, add an Annotation containing the ASP configurations.

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
   :lines: 1-13, 31-48

:fonticon:`fa fa-download` :download:`f5-asp-k8s-example-service.yaml </_static/config_examples/f5-asp-k8s-example-service.yaml>`

.. code-block:: bash
   :caption: Upload the Service definition to the Kubernetes API server

   $ kubectl replace -f f5-asp-k8s-example-service.yaml
   service "myService" replaced

\

.. note::

   - Remove any comments from the annotation section of the example configuration file *before* uploading it to Kubernetes.
   - The downloadable example includes a health check section. If you want to attach an ASP instance to a Service *without* using health checks, **remove lines 14-30** from the example annotation.

.. _k8s-health-checks:

Add health checks to an ASP annotation
``````````````````````````````````````

.. include:: /_static/reuse/asp-version-added-1_1.rst

To activate the ASP's health monitor:

#. Add the desired `ASP health check parameters`_ to the ASP annotation in the Service definition.

   .. literalinclude:: /_static/config_examples/f5-asp-k8s-example-service.yaml
      :caption: Service definition with ASP health checks
      :linenos:

   :fonticon:`fa fa-download` :download:`f5-asp-k8s-example-service.yaml </_static/config_examples/f5-asp-k8s-example-service.yaml>`

#. Upload the edited definition to the Kubernetes API server.

   .. code-block:: bash

     $ kubectl replace -f f5-asp-k8s-example-service.yaml
     service "myService" replaced

Next Steps
----------

:ref:`Verify that the ASP handles traffic for the Service <k8s-asp-verify>`.


.. _kubernetes hello-world: https://kubernetes.io/docs/tutorials/stateless-application/expose-external-ip-address-service/
.. _Service: https://kubernetes.io/docs/user-guide/services/
