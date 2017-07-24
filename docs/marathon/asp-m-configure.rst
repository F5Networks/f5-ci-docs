.. _aspm-configuration:

Configure the ASP with the ASP Controller for Marathon
======================================================

The |aspm-long| dynamically deploys the |asp| (ASP) in `Apache Mesos Marathon`_ when it discovers a Marathon Application that has the ``f5-asp:enable`` label.

When you launch the |aspm-long|, provide the configuration parameter(s) you want the |aspm| to apply to the ASP.
Define these configuration parameters in the ``"env"`` section of the |aspm| :ref:`Application definition <install-asp-marathon>`.

Required configuration parameters
---------------------------------

=====================   =======================================================
Parameter               Description
=====================   =======================================================
MARATHON_URL            Marathon service URL (e.g., \http://10.190.25.75:8080)
---------------------   -------------------------------------------------------
ASP_DEFAULT_URIS        Marathon Docker Store credentials URI
                        (required to pull ASP image) [#dockerstore]_
=====================   =======================================================

.. [#dockerstore] See `Set up Marathon to use a private Docker registry <https://mesosphere.github.io/marathon/docs/native-docker-private-registry.html>`_.


.. _asp-defaults-marathon:

Default configurations
``````````````````````

The |aspm-long| applies the following configurations to the |asp| by default.
You can override any default settings using the `marathon-asp-ctlr override labels </products/connectors/marathon-asp-ctlr/latest/index.html#configuration-parameters>`_.

===========================     ===============================================
Parameter                       Value
===========================     ===============================================
ASP_ENABLE_LABEL                "f5-asp"
---------------------------     -----------------------------------------------
ASP_DEFAULT_CPU                 1.0
---------------------------     -----------------------------------------------
ASP_DEFAULT_MEM                 256.0
---------------------------     -----------------------------------------------
ASP_DEFAULT_COUNT_PER_APP       1
---------------------------     -----------------------------------------------
ASP_DEFAULT_CONTAINER           store/f5networks/asp:1.0.0
---------------------------     -----------------------------------------------
ASP_DEFAULT_CONTAINER_PORT      8000
===========================     ===============================================


.. literalinclude:: /_static/config_examples/f5-marathon-asp-ctlr-example.json
   :caption: Example Application definition
   :linenos:
   :emphasize-lines: 18-32


See Also
--------

See the `F5 Marathon ASP Controller documentation </products/connectors/marathon-asp-ctlr/latest/index.html#configuration-parameters>`_ for the full list of available configuration parameters.

