.. _aspm-configuration:

Configure the |aspm-long|
=========================

When you launch the |aspm-long|, provide the required configuration parameter(s) and any additional default configurations you want to apply to the |asp| instances it launches.
Define these configuration parameters in the ``"env"`` section of the |aspm| :ref:`Application definition file <install-asp-marathon>`.

Required configuration parameters
---------------------------------

=====================   =======================================================
Parameter               Description
=====================   =======================================================
MARATHON_URL            Marathon service URL (e.g., \http://10.190.25.75:8080)
=====================   =======================================================

.. _asp-defaults-marathon:

Default configurations
``````````````````````

The |aspm-long| applies the following configurations to the |asp| by default.

===========================     ===============================================
Parameter                       Value
===========================     ===============================================
ASP_ENABLE_LABEL                "asp"
---------------------------     -----------------------------------------------
ASP_DEFAULT_CPU                 1.0
---------------------------     -----------------------------------------------
ASP_DEFAULT_MEM                 256.0
---------------------------     -----------------------------------------------
ASP_DEFAULT_COUNT_PER_APP       1
---------------------------     -----------------------------------------------
ASP_DEFAULT_CONTAINER           f5networks/asp:v1.0.0
---------------------------     -----------------------------------------------
ASP_DEFAULT_CONTAINER_PORT      8000
===========================     ===============================================



.. literalinclude:: /_static/config_examples/f5-marathon-asp-ctlr-example.json
    :caption: Example Application definition
    :emphasize-lines: 17-31


See Also
--------

See the |aspm| :ref:`product documentation <tbd>` for the full list of available configuration parameters.

