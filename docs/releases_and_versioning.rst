.. _f5-csi_support-matrix:

Releases and Versioning
=======================

Documentation
-------------

This documentation release, |release|, applies to the following versions of each F5 Container Integrations component:

===================         ==============
Component                   Version
===================         ==============
|cf-long|                   v1.0.0-beta.1
|kctlr-long|                v1.0.0,
                            v1.1.0
|mctlr-long|                v1.0.0,
                            v1.1.0
``asp``                     v1.0.0
|aspk-long|                 v1.0.0
|aspm-long|                 v1.0.0
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

   =============== =============== ======================= ===============   ======================================= =======================
   Connector       Version         BIG-IP version(s)       ASP version(s)    Platform                                Version(s)
   =============== =============== ======================= ===============   ======================================= =======================
   |cf-long|       v1.0.0-beta.1   v11.6.x, v12.x, v13.x   N/A               Pivotal Cloud Foundry (PCF)             v1.9.6
   --------------- --------------- ----------------------- ---------------   --------------------------------------- -----------------------
   |kctlr-long|    v1.0.0,         v11.6.x, v12.x, v13.x   N/A               Kubernetes                              v1.3.7, v1.4.x, v1.5.x
                   v1.1.0
   --------------- --------------- ----------------------- ---------------   --------------------------------------- -----------------------
   |mctlr-long|    v1.0.0,         v11.6.x, v12.x, v13.x   N/A               Apache Mesos                            v1.0.3
                   v1.1.0
                                                                             Apache Marathon                         v1.3.9

                                                                             Apache Mesos DC/OS, DC/OS Enterprise    v1.7.x, v1.8.x
   --------------- --------------- ----------------------- ---------------   --------------------------------------- -----------------------
   |aspk-long|     v1.0.0                                                    Kubernetes                              v1.3.7, v1.4.x, v1.5.x
   --------------- --------------- ----------------------- ---------------   --------------------------------------- -----------------------
   |aspm-long|     v1.0.0          N/A                     v1.0.0            Apache Mesos                            v1.0.3

                                                                             Apache Marathon                         v1.3.9

                                                                             Apache Mesos DC/OS, DC/OS Enterprise    v1.7.x, v1.8.x
   =============== =============== ======================= ===============   ======================================= =======================


Notice to Beta Customers
========================

Thank you for participating in the F5 Beta/Early Release program!

Feature enhancements introduced as part of a beta release have a **"New in version"** tag like the example below:

.. note::

   :fonticon:`fa fa-wrench` **Beta feature**

   Introduced in <product-name> <version>.

If you require assistance with a beta version, please contact your F5 Sales Representative.

