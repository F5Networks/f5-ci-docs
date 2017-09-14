.. _marathon-asp-deploy:

Create an ASP for a Marathon Application
========================================

.. sidebar:: Docs test matrix

   We tested this documentation with:

   - ``marathon-1.3.9``
   - ``mesos-1.0.3``
   - ``marathon-bigip-ctlr v1.0.0``
   - ``asp v1.0.0``

The |aspm-long| launches |asp| instances automatically for Apps that have the ``ASP_ENABLE_LABEL`` value set to "enabled" (for example, ``f5-asp:enable``).

Launch an ASP instance with the default configurations
------------------------------------------------------

Add the label ``"f5-asp": "enable"`` to the App's service definition.

#. Via the Marathon web interface:

   - Click on the App name in the :guilabel:`Applications` list.
   - Click :guilabel:`Configuration`.
   - Click :guilabel:`Edit`.
   - Click :guilabel:`Labels`.
   - Click the :guilabel:`+` icon and add the label "f5-asp: enable".
   - Click :guilabel:`Change and deploy configuration`.

#. Via the REST API:

   - Edit the App definition

   .. literalinclude:: /_static/config_examples/app_asp-enabled-defaults.json
      :linenos:
      :emphasize-lines: 22-25


   - Send a PUT request to the Marathon API server to update the App.

   .. code-block:: bash

      $ curl -X PUT -H "Content-Type: application/json" http://10.190.25.75:8080/v2/apps/basic-0 -d @app_asp-enabled-defaults.json

.. _marathon-asp-custom-config:

Launch an ASP instance with custom configurations
-------------------------------------------------

Add the label ``"f5-asp": "enable"`` to the App's service definition.

#. Via the Marathon web interface:

   - Click on the App name in the :guilabel:`Applications` list.
   - Click :guilabel:`Configuration`.
   - Click :guilabel:`Edit`.
   - Click :guilabel:`Labels`.
   - Click the :guilabel:`plus sign icon` and add your override labels.
   - Click :guilabel:`Change and deploy configuration`.

#. Via the REST API:

   - Add your desired `override labels </products/connectors/marathon-asp-ctlr/latest/index.html#configuration-parameters>`_ to the App's service definition.

     .. literalinclude:: /_static/config_examples/app_asp-enabled-custom.json
        :lines: 1-32, 35-
        :emphasize-lines: 6-8, 24-34
        :linenos:

   - Send a PUT request to the Marathon API server to update the App definition.

     .. code-block:: bash

        $ curl -X PUT -H "Content-Type: application/json" http://<marathon-url>:8080/v2/apps -d @app_asp-enabled-custom.json

Configure Event Handlers
``````````````````````````

Refer `this event handler document </products/asp/latest/eventHandlersDoc.html>`_ to know about event handlers and the supported events.

Following are the sample event handlers used to configure the App:

- For event ``http-request``:

  .. literalinclude:: /_static/config_examples/event-handler-http-request.js
      :language: javascript
      :linenos:

- For event ``http-response``:

  .. literalinclude:: /_static/config_examples/event-handler-http-response.js
     :language: javascript
     :linenos:

#. Refer to the `schema of event handlers </products/asp/latest/#event-handler>`_ to write a list of event handlers.

#. Set the label ``ASP_VS_EVENT_HANDLERS`` with value as the list of event handlers.

   .. important::

      When you set the value of the label ``ASP_VS_EVENT_HANDLERS``, make sure the JSON list of event handlers is converted to a string like in the example given below.

   .. comment for Jodie: the spinx literalinclude does not allow wrapping of these long lines, because it becomes an invalid JSON then. If you can render them it will begreat


   .. literalinclude:: /_static/config_examples/app_asp-enabled-custom.json
      :lines: 25-36
      :emphasize-lines: 9
      :linenos:

#.  Refer to the :ref:`above section <marathon-asp-custom-config>` for adding ``ASP_VS_EVENT_HANDLERS`` label.
