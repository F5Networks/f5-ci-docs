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

Annotate the Service
--------------------

To attach an ASP to a Kubernetes `Service`_, add an Annotation containing the ASP configurations.
There are a few ways to do so:

- Annotate the `Service`_ definition with the key-value pair ``asp.f5.com/config="<JSON-config-blob>"``.

  .. important::

     When you annotate the Service using :code:`kubectl annotate`, the JSON config blob must use the encoding shown in the example below.
     Use a backslash -- ``\"`` -- to escape all quotation marks.

  \

  .. code-block:: bash

     $ kubectl annotate service example-service asp.f5.com/config="{\"ip-protocol\":\"http\",\"load-balancing-mode\":\"round-robin\"}"
     service "example-service" annotated


- Add the desired ASP configurations to the Service definition file and update the Kubernetes API server.

  .. tip::

     If you choose to use the example file below, remember to remove the comments from the annotation before uploading it to Kubernetes.

  \

  .. literalinclude:: /_static/config_examples/f5-asp-k8s-example-service.yaml
     :caption: Service definition with ASP annotation
     :linenos:
     :emphasize-lines: 4-30

  :fonticon:`fa fa-download` :download:`f5-asp-k8s-example-service.yaml </_static/config_examples/f5-asp-k8s-example-service.yaml>`

  .. code-block:: bash
     :caption: Upload the Service definition to the Kubernetes API server

     $ kubectl replace -f f5-asp-k8s-example-service.yaml
     service "myService" replaced

Next Steps
----------

:ref:`Verify that the ASP handles traffic for the Service <k8s-asp-verify>`.


.. _kubernetes hello-world: https://kubernetes.io/docs/tutorials/stateless-application/expose-external-ip-address-service/
.. _Service: https://kubernetes.io/docs/user-guide/services/
