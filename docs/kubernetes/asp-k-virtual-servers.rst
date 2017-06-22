.. _k8s-launch-asp:

Launch an |asp| instance for a Kubernetes Service
=================================================

.. sidebar:: Docs test matrix

   We tested this documentation with:
   - ``kubernetes-v1.4.8_coreos.0``
   - |kctlr| ``v1.0.0``
   - `kubernetes hello-world`_ service, with :ref:`ASP annotation <k8s-service-annotate>`

Summary
-------

The |asp| watches Kubernetes `Service`_ definitions for a set of annotations defining virtual server objects.
 The annotation should include a JSON blob defining of a set of `ASP configuration parameters </products/asp/latest/index.html#configuration-parameters>`_.
 When you annotate an existing Kubernetes `Service`_, the ASP creates a virtual server for that Service.

.. _k8s-service-annotate:

Annotate a Kubernetes Service
-----------------------------

Use one of the options below to annotate your Kubernetes `Service`_ and deploy the |asp|.

#. Annotate the `Service`_ definition with the key-value pair ``asp.f5.com/config="<JSON-config-blob>"``.

   .. important::

      When you annotate the Service this way, you must encode the JSON config blob as shown in the example below (escape all quotes -- ``\"``).


   .. code-block:: bash

      user@k8s-master:~$ kubectl annotate service example-service asp.f5.com/config="{\"ip-protocol\":\"http\",\"load-balancing-mode\":\"round-robin\"}"
      service "example-service" annotated


#. Edit the Service definition and add the annotation section with the `ASP configurations </products/asp/latest/#configuration-parameters>`_.

   .. code-block:: bash

      user@k8s-master:~$ kubectl edit service example-service

   .. literalinclude:: /_static/config_examples/f5-asp-k8s-example-service.yaml
      :linenos:
      :emphasize-lines: 4-13

   :fonticon:`fa fa-download` :download:`Download an example Service definition with the ASP annotation </_static/config_examples/f5-asp-k8s-example-service.yaml>`

#. (Optional) :ref:`Verify that the ASP handles traffic for the Service <k8s-asp-verify>`


.. _kubernetes hello-world: https://kubernetes.io/docs/tutorials/stateless-application/expose-external-ip-address-service/
.. _Service: https://kubernetes.io/docs/user-guide/services/
