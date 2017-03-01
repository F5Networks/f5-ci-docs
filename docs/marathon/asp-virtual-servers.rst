Launch an |asp| instance for a Marathon Application
===================================================

The |aspm-long| launches |asp| instances automatically for Apps that have the ``ASP_ENABLE_LABEL`` set to "enabled".
The :ref:`default value <asp-defaults-marathon>` for ``ASP_ENABLE_LABEL`` is "asp".


Launch an ASP instance with the default configurations
------------------------------------------------------

#. Add the label ``"asp": "enable"`` to the App's service definition.

    .. literalinclude:: /_static/config_examples/app_asp-enabled-defaults.json
        :linenos:
        :emphasize-lines: 21-23

    Download :download:`app_asp-enabled-defaults.json </_static/config_examples/app_asp-enabled-defaults.json>`

#. Send a PUT request to the Marathon API server to update the App definition.

    .. code-block:: bash

        $ curl -X PUT -H "Content-Type: application/json" http://10.190.25.75:8080/v2/apps/basic-0 -d @app_asp-enabled-defaults.json



Launch an ASP instance with custom configurations
-------------------------------------------------

#. Add the label ``"asp": "enable"`` to the App's service definition.

#. Add your desired `override labels </products/connectors/marathon-asp-ctlr/latest/index.html#configuration-parameters>`_ to the App's service definition.

    .. literalinclude:: /_static/config_examples/app_asp-enabled-custom.json
        :emphasize-lines: 22-31
        :linenos:

    :download:`app_asp-enabled-custom.json </_static/config_examples/app_asp-enabled-custom.json>`

#. Send a PUT request to the Marathon API server to update the App definition.

    .. code-block:: bash

        $ curl -X PUT -H "Content-Type: application/json" http://<marathon-url>:8080/v2/apps -d @app_asp-enabled-custom.json




