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
F5_CC_PARTITIONS	    The BIG-IP partition |mctlr| manages
=====================   =======================================================


.. literalinclude:: /_static/config_examples/f5-marathon-bigip-ctlr-example.json
    :caption: Example Application definition
    :emphasize-lines: 13-18
    :linenos:

Required Application Labels
---------------------------

The parameter(s) listed in the table below are required :ref:`F5 application labels <app-labels>`.

=====================   ===================================================
Parameter               Description
=====================   ===================================================
F5_PARTITION            The BIG-IP partition in which you want to create
                        a virtual server; cannot be "/Common"
=====================   ===================================================


See Also
--------

Additional |mctlr| :ref:`configuration parameters <tbd>` define the BIG-IP objects that |mctlr| manages. See the |mctlr| :ref:`product documentation <tbd>` for more information.

