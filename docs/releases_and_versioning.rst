.. _f5-csi_support-matrix:

Releases and Versioning
=======================

Documentation
-------------

This documentation release, |release|, applies to the following versions of each F5 Container Integrations component:

===================         ==============
Component                   Version
===================         ==============
``asp``                     v1.0.0
|kctlr|                     v1.0.0,
                            v1.1.0-beta.1
|aspk|                      v1.0.0
|mctlr|                     v1.0.0,
                            v1.1.0-beta.1
|aspm|                      v1.0.0
===================         ==============

|asp|
-----

=================   ====================    =======================
ASP Version         Platform                Version(s)
=================   ====================    =======================
v1.0.0              Kubernetes              v1.3.7, v1.4.x, v1.5.x
-----------------   --------------------    -----------------------
v1.0.0              Apache Mesos            v1.0.3
-----------------   --------------------    -----------------------
v1.0.0              Apache Marathon         v1.3.9
-----------------   --------------------    -----------------------
v1.0.0              Mesos DC/OS &           v1.7.x, v1.8.x
                    DC/OS Enterprise
=================   ====================    =======================


Container Connectors
--------------------

.. table::

    =================== =============== ======================= =============== ======================================= =======================
    Connector           Version         BIG-IP version(s)       ASP version(s)  Platform                                Version(s)
    =================== =============== ======================= =============== ======================================= =======================
    |kctlr|             v1.0.0,         v11.6.x, v12.x, v13.x   N/A             Kubernetes                              v1.3.7, v1.4.x, v1.5.x
                        v1.1.0-beta.1
    ------------------- --------------- ----------------------- --------------- --------------------------------------- -----------------------
    |aspk|              v1.0.0                                                  Kubernetes                              v1.3.7, v1.4.x, v1.5.x
    ------------------- --------------- ----------------------- --------------- --------------------------------------- -----------------------
    |mctlr|             v1.0.0,         v11.6.x, v12.x, v13.x   N/A             Apache Mesos                            v1.0.3
                        v1.1.0-beta.1
                                                                                Apache Marathon                         v1.3.9

                                                                                Apache Mesos DC/OS, DC/OS Enterprise    v1.7.x, v1.8.x
    ------------------- --------------- ----------------------- --------------- --------------------------------------- -----------------------
    |aspm|                  v1.0.0      N/A                     v1.0.0          Apache Mesos                            v1.0.3

                                                                                Apache Marathon                         v1.3.9

                                                                                Apache Mesos DC/OS, DC/OS Enterprise    v1.7.x, v1.8.x
    =================== =============== ======================= =============== ======================================= =======================


Notice to Beta Customers
========================

Thank you for participating in the F5 Beta/Early Release program!

Feature enhancements introduced as part of a beta release have a **"New in version"** tag like that below:

.. note::

   .. versionadded:: <product-name> <version>

   See the <product-name> beta documentation for more information.

If you require assistance with a beta version, please contact your F5 Sales Representative.

