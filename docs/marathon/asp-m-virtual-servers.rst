.. sidebar:: Docs test matrix

   Documentation manually tested with:

   - Mesos 1.0.3, Marathon 1.3.9, Ubuntu 16.04, ASP 1.1.0, ASP Controller 1.0.0
   - Mesos 1.0.3, Marathon 1.3.9, Ubuntu 16.04, ASP 1.0.0, ASP Controller 1.0.0

.. _marathon-asp-deploy:

Launch an ASP instance for a Marathon Application
=================================================

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

     .. literalinclude:: /marathon/config_examples/app_asp-enabled-defaults.json
        :language: javascript
        :linenos:
        :emphasize-lines: 22-25

     :fonticon:`fa fa-download` :download:`app_asp-enabled-defaults.json </marathon/config_examples/app_asp-enabled-defaults.json>`

   - Send a PUT request to the Marathon API server to update the App.

     .. code-block:: bash

        curl -X PUT -H "Content-Type: application/json" http://10.190.25.75:8080/v2/apps/basic-0 -d @app_asp-enabled-defaults.json

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

     .. literalinclude:: /marathon/config_examples/app_asp-enabled-custom.json
        :language: javascript
        :linenos:
        :emphasize-lines: 27-31

     :fonticon:`fa fa-download` :download:`app_asp-enabled-custom.json </marathon/config_examples/app_asp-enabled-custom.json>`

   - Send a PUT request to the Marathon API server to update the App definition.

     .. code-block:: bash

        curl -X PUT -H "Content-Type: application/json" http://<marathon-url>:8080/v2/apps -d @app_asp-enabled-custom.json


.. _event-handlers-marathon:

Add Event Handlers
``````````````````

You can set up `ASP event handlers`_ as part of the virtual server configuration.

.. seealso::

   - Learn about the `ASP event handlers`_.
   - Learn about the `ASP Middleware API`_.

Take the steps below to add event handlers to an ASP.

#. Define the ``ASP_VS_EVENT_HANDLERS`` label with a JSON string.

   .. important::

      Convert the JSON list to a string, like that shown in the example.

   \

   .. literalinclude:: /marathon/config_examples/app_asp-enabled-custom.json
      :language: javascript
      :lines: 25-36
      :linenos:
      :emphasize-lines: 6

   :fonticon:`fa fa-download` :download:`app_asp-enabled-custom.json </marathon/config_examples/app_asp-enabled-custom.json>`

#. Deploy the updated service definition to the Marathon API server.

   .. code-block:: bash

      curl -X PUT -H "Content-Type: application/json" http://<marathon-url>:8080/v2/apps -d @app_asp-enabled-custom.json

