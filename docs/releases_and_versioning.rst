:product: Container Ingress Services
:product: BIG-IP Controller for Kubernetes
:product: BIG-IP Controller for Cloud Foundry
:product: BIG-IP Controller for Marathon
:product: BIG-IP Controller for OpenShift
:type: concept

.. _f5-csi_support-matrix:

Releases and Versioning
=======================

Documentation
-------------

.. important:: This page is for an older version of the Container Ingress Services documentation. `Go to the latest version of CIS documentation <https://clouddocs.f5.com/containers/latest/>`_.

This documentation set applies to the following versions of each F5 Container Integrations component:

===================         =====================
Component                   Version
===================         =====================
|kctlr-long|                v1.0.x-1.14.x, v2.0.0
|octlr-long|                v1.0.x-1.14.x, v2.0.0
===================         =====================

.. _connector compatibility:

Container Ingress Service compatibility
---------------------------------------

The tables below show the versions used in development testing. The F5 Container Ingress Service may work with versions not shown here; F5 has not verified functionality in those versions. 

.. table:: BIG-IP Controller/Platform compatibility
   :widths: 4 2 2 4 2 2

   +------------------------------------+-----------------------+-------------------------+--------------------------------------------+--------------------------+------------------------+
   | Connector                          | Version(s)            | Platform                | Version(s)                                 | BIG-IP version(s)        | AS3                    |
   +====================================+=======================+=========================+============================================+==========================+========================+
   | |kctlr-long|                       | v1.10-v1.14           | Kubernetes              | v1.13-v1.18                                | v12.x-v15.x              | v3.13-v3.18            |
   |                                    | v2.0.0                |                         |                                            |                          |                        |
   | ``k8s-bigip-ctlr``                 |                       |                         |                                            |                          |                        |
   +------------------------------------+-----------------------+-------------------------+--------------------------------------------+--------------------------+------------------------+
   | |octlr-long|                       | v1.10-v1.14           | OpenShift               | v3.11-v4.3                                 | v12.x-v15.x              | v3.13-v3.18            |
   |                                    | v2.0.0                |                         |                                            |                          |                        |
   | ``k8s-bigip-ctlr`` using AS3       |                       |                         |                                            |                          |                        |
   +------------------------------------+-----------------------+-------------------------+--------------------------------------------+--------------------------+------------------------+
   | ``k8s-bigip-ctrl`` using CCCL      | v1.10-v1.14           | OpenShift               | v3.11-v4.2                                 | v12.x-v13.x              | none                   |
   +------------------------------------+-----------------------+-------------------------+--------------------------------------------+--------------------------+------------------------+

.. important::

   F5 Networks is a `Red Hat Certified Container Partner <https://access.redhat.com/containers/#/vendor/f5networks>`_. Please see the Red Hat Container Catalog for more information.


F5 schema
---------

bigip-virtual-server
````````````````````

The :code:`k8s-bigip-ctlr` project has a built in :code:`bigip-virtual-server` schema.
All versions of the |kctlr-long| are backwards-compatible, but using an older version's schema may limit Controller functionality.

Be sure to use the **most recent** schema version that corresponds to your Controller version to ensure access to the full feature set.

.. _schema-table:

.. table:: F5 schema and ``k8s-bigip-ctlr`` version compatibility

   =============================================== =====================
   F5 Schema version                               ``k8s-bigip-ctlr``
   =============================================== =====================
   f5schemadb://bigip-virtual-server_v0.1.7.json   1.9.x, 1.8.x, 1.7.x, 
                                                   1.6.x, 1.5.x, 1.4.x
   ----------------------------------------------- ---------------------
   f5schemadb://bigip-virtual-server_v0.1.6.json   1.4.x
   ----------------------------------------------- ---------------------
   f5schemadb://bigip-virtual-server_v0.1.5.json   1.3.x
   ----------------------------------------------- ---------------------
   f5schemadb://bigip-virtual-server_v0.1.4.json   1.3.x
   ----------------------------------------------- ---------------------
   f5schemadb://bigip-virtual-server_v0.1.3.json   1.1.x, 1.2.x
   ----------------------------------------------- ---------------------
   f5schemadb://bigip-virtual-server_v0.1.2.json   1.0.x
   =============================================== =====================


Notice to Beta Customers
========================

.. sidebar:: :fonticon:`fa fa-flask` **Beta feature**

   Introduced in <product-name> <version>.

Thank you for participating in the F5 Beta/Early Release program!

Feature enhancements introduced as part of a beta release have a **"Beta feature"** tag like the example to the right.
If you require assistance with a beta version, please contact your F5 Sales Representative.

