.. _mctlr-configuration:

Configure the |mctlr-long|
==========================

When you launch the |mctlr-long|, you must provide the required configuration parameters shown in the table below.
Define these configuration parameters in the ``"env"`` section of the Marathon :ref:`Application definition file <install-mctlr>`.

Required configuration parameters
---------------------------------

=====================   =======================================================
Parameter               Description
=====================   =======================================================
MARATHON_URL            Marathon service URL (e.g., \http://10.190.25.75:8080)
---------------------   -------------------------------------------------------
F5_CC_BIGIP_USERNAME	Username for BIG-IP account with permission to
                        manage objects in the specified partition
---------------------   -------------------------------------------------------
F5_CC_BIGIP_PASSWORD    Password for BIG-IP account
---------------------   -------------------------------------------------------
F5_CC_BIGIP_HOSTNAME    BIG-IP Hostname/IP address
---------------------   -------------------------------------------------------
F5_CC_PARTITIONS	    The `BIG-IP partition`_ |mctlr| should manage
=====================   =======================================================


.. literalinclude:: /_static/config_examples/f5-marathon-bigip-ctlr-example.json
   :caption: Example Application definition
   :emphasize-lines: 17-21
   :linenos:

Required Application Labels
---------------------------

Use the :ref:`F5 application labels <app-labels>` listed in the table below when you're :ref:`managing BIG-IP Local Traffic Manager (LTM) objects directly <mctlr-manage-bigip-objects>`.

=====================   =======================================================
Parameter               Description
=====================   =======================================================
F5_PARTITION            The `BIG-IP partition`_ in which you want to create
                        a virtual server; cannot be "/Common".
---------------------   -------------------------------------------------------
F5\_{n}_BIND_ADDR       IP address to use for the BIG-IP LTM virtual server
                        created for the Marathon App service [#fn1]_

                        Example:
                        ``"F5_0_BIND_ADDR": "10.0.0.42"``
---------------------   -------------------------------------------------------
F5\_{n}_PORT            Service port to use on the BIG-IP LTM virtual server.
                        Overrides the ``servicePort`` configuration parameter.

                        Example: ``"F5_0_PORT": "80"``
=====================   =======================================================

.. [#fn1] Not required when creating :ref:`unattached pools <mctlr-pool-only>`.

.. _marathon-required-iapp-labels:

Required iApp Application Labels
--------------------------------

Use the :ref:`F5 application labels <app-labels>` when :ref:`deploying an iApp <mctlr-deploy-iapps>`.

=================================   ===========================================
Parameter                           Description
=================================   ===========================================
F5_PARTITION                        The BIG-IP partition in which you want to
                                    create a virtual server; cannot be
                                    "/Common".
---------------------------------   -------------------------------------------
F5\_{n}_IAPP_TEMPLATE               The iApp template you want to use to create
                                    the Application Service; must already
                                    exist on the BIG-IP.
---------------------------------   -------------------------------------------
F5\_{n}_IAPP_TABLE_*                Template-specific [#iapplabels]_
---------------------------------   -------------------------------------------
F5\_{n}_IAPP_POOL_MEMBER_TABLE      Template-specific [#iapplabels]_
---------------------------------   -------------------------------------------
F5\_{n}_IAPP_VARIABLE_*             Template-specific [#iapplabels]_
---------------------------------   -------------------------------------------
F5\_{n}_IAPP_OPTION_*               Template-specific [#iapplabels]_
=================================   ===========================================

.. [#iapplabels] See `Application Labels for iApp Mode </products/connectors/marathon-bigip-ctlr/latest/index.html#application-labels-for-iapp-mode>`_ for more information.


See Also
--------

See the `marathon-bigip-ctlr product documentation </products/connectors/marathon-bigip-ctlr/latest/index.html>`_ for the full list of available configuration parameters.

.. _BIG-IP partition: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/bigip-user-account-administration-13-0-0/2.html
