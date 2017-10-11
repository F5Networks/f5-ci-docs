.. sidebar:: Docs test matrix

   We tested this documentation with:

   - Mesos 1.0.3, Marathon 1.3.9, Ubuntu 16.04, ASP 1.1.0, ASP Controller 1.0.0
   - Mesos 1.0.3, Marathon 1.3.9, Ubuntu 16.04, ASP 1.0.0, ASP Controller 1.0.0

.. _marathon-asp-deploy:

Create an ASP for a Marathon Application
========================================

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
        :emphasize-lines: 6-8, 24-34
        :linenos:

   - Send a PUT request to the Marathon API server to update the App definition.

     .. code-block:: bash

        $ curl -X PUT -H "Content-Type: application/json" http://<marathon-url>:8080/v2/apps -d @app_asp-enabled-custom.json




