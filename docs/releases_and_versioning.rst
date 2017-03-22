.. _f5-csi_support-matrix:

Releases and Versioning
=======================

Documentation
-------------

This documentation release, |release|, applies to the following versions of each F5 Container Integrations component:

===================         =========
Component                   Version
===================         =========
``asp``                     v1.0.0
|kctlr|                     v1.0.0
|aspk|                      v1.0.0
|mctlr|                     v1.0.0
|aspm|                      v1.0.0
===================         =========

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

    =================== =========== =================== =============== ======================================= =======================
    Connector           Version     BIG-IP version(s)   ASP version(s)  Platform                                Version(s)
    =================== =========== =================== =============== ======================================= =======================
    |kctlr|             v1.0.0      v12.1.x, v13.0.x    N/A             Kubernetes                              v1.3.7, v1.4.x, v1.5.x
    ------------------- ----------- ------------------- --------------- --------------------------------------- -----------------------
    |aspk|              v1.0.0                                          Kubernetes                              v1.3.7, v1.4.x, v1.5.x
    ------------------- ----------- ------------------- --------------- --------------------------------------- -----------------------
    |mctlr|             v1.0.0      v12.1.x, v13.0.x    N/A             Apache Mesos                            v1.0.3

                                                                        Apache Marathon                         v1.3.9

                                                                        Apache Mesos DC/OS & DC/OS Enterprise   v1.7.x, v1.8.x
    ------------------- ----------- ------------------- --------------- --------------------------------------- -----------------------
    |aspm|              v1.0.0      N/A                 v1.0.0          Apache Mesos                            v1.0.3

                                                                        Apache Marathon                         v1.3.9

                                                                        Apache Mesos DC/OS & DC/OS Enterprise   v1.7.x, v1.8.x
    =================== =========== =================== =============== ======================================= =======================


Notice to Beta Customers
========================

Thank you for participating in the F5 Beta / Early Release program! As you were previously notified, there is no supported path from the beta release to v1.0.0 of all F5 Container Integration components.

If you require assistance with migration to v1.0.0, or have any questions, please contact your F5 Support Representative.

