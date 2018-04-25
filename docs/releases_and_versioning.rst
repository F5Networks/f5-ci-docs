.. _f5-csi_support-matrix:

Releases and Versioning
=======================

Documentation
-------------

This documentation release, |release|, applies to the following versions of each F5 Container Integrations component:

===================         ==============
Component                   Version
===================         ==============
|cf-long|                   v1.0.x-1.2.x
|kctlr-long|                v1.0.x-1.4.x
|mctlr-long|                v1.0.x-v1.2.x
===================         ==============

.. _connector compatibility:

Container Connector compatibility
---------------------------------

The tables below show the versions used in development testing. The F5 Container Connectors may work with versions not shown here; F5 has not verified functionality in those versions.

.. table:: BIG-IP Controller/Platform compatibility
   :widths: 4 2 2 4 2

   +--------------------------+-----------------------+--------------------------------------------+--------------------------------+--------------------------+
   | Connector                | Version(s)            | Platform                                   | Version(s)                     | BIG-IP version(s)        |
   +==========================+=======================+============================================+================================+==========================+
   | |cf-long|                | v1.0.x-v1.2.x         | Pivotal Cloud Foundry (PCF)                | v1.9.6                         | v12.x, v13.x             |
   |                          |                       |                                            |                                |                          |
   | ``cf-bigip-ctlr``        |                       |                                            |                                |                          |
   +--------------------------+-----------------------+--------------------------------------------+--------------------------------+--------------------------+
   |                                                                                                                                                           |
   +--------------------------+-----------------------+--------------------------------------------+--------------------------------+--------------------------+
   | |kctlr-long|             | v1.0.x, v1.1.x        | Kubernetes                                 | v1.3.7, v1.4.x, v1.5.x         | v12.x, v13.x             |
   |                          +-----------------------+                                            +--------------------------------+                          |
   | ``k8s-bigip-ctlr``       | v1.2.x-v1.4.x         |                                            | v1.4.x, v1.5.x, v1.6.x, v1.7.x |                          |
   |                          +-----------------------+                                            +--------------------------------+                          |
   |                          | v1.5.x                |                                            | v1.6.x, v1.7.x, v1.8.x         |                          |
   +--------------------------+-----------------------+--------------------------------------------+--------------------------------+--------------------------+
   |                                                                                                                                                           |
   +--------------------------+-----------------------+--------------------------------------------+--------------------------------+--------------------------+
   | |mctlr-long|             | v1.0.x, v1.1.0        | Apache Mesos                               | v1.0.3                         | v12.x, v13.x             |
   |                          |                       +--------------------------------------------+--------------------------------+                          |
   | ``marathon-bigip-ctlr``  |                       | Apache Marathon                            | v1.3.9                         |                          |
   |                          |                       +--------------------------------------------+--------------------------------+                          |
   |                          |                       | Apache Mesos DC/OS                         | v1.7.x, v1.8.x                 |                          |
   |                          |                       |                                            |                                |                          |
   |                          |                       | DC/OS Enterprise                           |                                |                          |
   |                          +-----------------------+--------------------------------------------+--------------------------------+                          |
   |                          | v1.1.1+, v1.2.x,      | Apache Marathon                            | v1.3.9, v1.5.x                 |                          |
   |                          | v1.3.x                +--------------------------------------------+--------------------------------+                          |
   |                          |                       | Apache Mesos DC/OS &                       | v1.7.x, v1.8.x, v1.9.x,        |                          |
   |                          |                       |                                            | v1.10.x                        |                          |
   |                          |                       | DC/OS Enterprise                           |                                |                          |
   +--------------------------+-----------------------+--------------------------------------------+--------------------------------+--------------------------+
   |                                                                                                                                                           |
   +--------------------------+-----------------------+--------------------------------------------+--------------------------------+--------------------------+
   | |octlr-long|             | v1.0.x-v1.2.x         | OpenShift Origin                           | v1.4.x                         | v12.x, v13.x             |
   |                          +-----------------------+--------------------------------------------+--------------------------------+                          |
   | ``k8s-bigip-ctlr``       | v1.3.x, v1.4.x        | OpenShift Origin                           | v1.4.x, v1.5.x, v3.6.x, v3.7.x |                          |
   |                          |                       +--------------------------------------------+--------------------------------+                          |
   |                          |                       | Red Hat OpenShift Container Platform       | v3.6.x, v3.7.x                 |                          |
   |                          +-----------------------+--------------------------------------------+--------------------------------+                          |
   |                          | v1.5.x                | OpenShift Origin                           | v3.6.x, v3.7.x                 |                          |
   |                          |                       +--------------------------------------------+                                |                          |
   |                          |                       | Red Hat OpenShift Container Platform       |                                |                          |
   +--------------------------+-----------------------+--------------------------------------------+--------------------------------+--------------------------+

.. important::

   F5 Networks is a `Red Hat Certified Container Partner <https://access.redhat.com/containers/#/vendor/f5networks>`_. Please see the Red Hat Container Catalog for more information.

.. _f5-schema:

F5 schema
---------

bigip-virtual-server
````````````````````

The :code:`k8s-bigip-ctlr` project has a built in :code:`bigip-virtual-server` schema.
All versions of the |kctlr-long| are backwards-compatible, but using an older version's schema may limit Controller functionality.

Be sure to use the **most recent** schema version that corresponds to your Controller version to ensure access to the full feature set.

.. _schema-table:

.. table:: F5 schema and ``k8s-bigip-ctlr`` version compatibility

   =============================================== ===================
   F5 Schema version                               ``k8s-bigip-ctlr``
   =============================================== ===================
   f5schemadb://bigip-virtual-server_v0.1.7.json   1.5.x, 1.4.x
   ----------------------------------------------- -------------------
   f5schemadb://bigip-virtual-server_v0.1.6.json   1.4.x
   ----------------------------------------------- -------------------
   f5schemadb://bigip-virtual-server_v0.1.5.json   1.3.x
   ----------------------------------------------- -------------------
   f5schemadb://bigip-virtual-server_v0.1.4.json   1.3.x
   ----------------------------------------------- -------------------
   f5schemadb://bigip-virtual-server_v0.1.3.json   1.1.x, 1.2.x
   ----------------------------------------------- -------------------
   f5schemadb://bigip-virtual-server_v0.1.2.json   1.0.x
   =============================================== ===================


Notice to Beta Customers
========================

Thank you for participating in the F5 Beta/Early Release program!

Feature enhancements introduced as part of a beta release have a **"Beta feature"** tag like the example below to the right.
If you require assistance with a beta version, please contact your F5 Sales Representative.

.. sidebar:: :fonticon:`fa fa-flask` **Beta feature**

   Introduced in <product-name> <version>.

