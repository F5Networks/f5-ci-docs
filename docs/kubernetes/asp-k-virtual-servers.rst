.. _k8s-launch-asp:

Attach an ASP to a Kubernetes Service
=====================================

.. sidebar:: Docs test matrix

   We tested this documentation with:
   - ``kubernetes-v1.4.8_coreos.0``
   - ``k8s-bigip-ctlr v1.0.0``
   - `kubernetes hello-world`_ service, with :ref:`ASP annotation <k8s-service-annotate>`

Summary
-------

The |asp| (ASP) watches Kubernetes `Service`_ definitions for a set of annotations defining virtual server objects.
 The annotation should include a JSON blob defining of a set of `ASP configuration parameters </products/asp/latest/index.html#configuration-parameters>`_.
 When you add the ASP annotation to a Kubernetes `Service`_, the ASP creates a virtual server for that Service.

.. _k8s-service-annotate:

Annotate a Kubernetes Service
-----------------------------

Use one of the options below to attach an ASP to a Kubernetes `Service`_.

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
      :lines: 1-9,21-
      :emphasize-lines: 4-13

   :fonticon:`fa fa-download` :download:`Download an example Service definition with the ASP annotation </_static/config_examples/f5-asp-k8s-example-service.yaml>`

#. (Optional) :ref:`Verify that the ASP handles traffic for the Service <k8s-asp-verify>`

Configure Event Handlers
``````````````````````````
Event handlers can be configured for a service by augmenting the annotation described above.
Refer `this event handler document </products/asp/latest/eventHandlersDoc.html>`_ to know about event handlers and the supported events.

Following are the sample event handlers configured in the annotations below:

- For event ``http-request``:

  .. literalinclude:: /_static/config_examples/event-handler-http-request.js
      :language: javascript
      :linenos:

- For event ``http-response``:
   
  .. literalinclude:: /_static/config_examples/event-handler-http-response.js
     :language: javascript
     :linenos:

#. Refer to the `schema of event handlers </products/asp/latest/#event-handler>`_ to write a list of event handlers. Add the event-handlers list to the annotation JSON blob.

   .. important::

      When you add event handlers to the annotation, make sure the event handler code is converted to a valid JSON string as shown in the example below.

   .. comment for Jodie: the spinx literalinclude does not allow wrapping of these long lines, because it becomes an invalid JSON then. If you can render them it will be great

   .. literalinclude:: /_static/config_examples/f5-asp-k8s-example-service.yaml
      :linenos:
      :lines: 6-25
      :emphasize-lines: 5-15

#. Edit/annotate the service as mentioned in the :ref:`above section <k8s-service-annotate>`.

#. (Optional) :ref:`Verify execution of event handlers <k8s-asp-event-handlers-verify>`.

.. _kubernetes hello-world: https://kubernetes.io/docs/tutorials/stateless-application/expose-external-ip-address-service/
.. _Service: https://kubernetes.io/docs/user-guide/services/
