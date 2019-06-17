:product: Container Ingress Services
:type: concept

.. _kctlr-managed-objects:

Managed BIG-IP objects
======================

You can deploy BIG-IP objects for Services and Ingresses in Kubernetes. In OpenShift, you can deploy BIG-IP objects for Services and Routes.
The |kctlr| can create, update, remove, and/or manage BIG-IP objects as noted in the table below.

+------------------------------+------------------------+---------------------------------+--------------------------------------------------------------------+
| Type                         | Create New Object      | Use Existing Object             | Notes                                                              |
+==============================+========================+=================================+====================================================================+
| health monitor               | X                      | X                               | The |kctlr| can *use existing* health monitors for all supported   |
|                              |                        |                                 | Kubernetes resources.                                              |
|                              |                        |                                 |                                                                    |
|                              |                        |                                 | The |kctlr| can *create* health monitors for certain types         |
|                              |                        |                                 | of Kubernetes resources, as described in the deployment            |
|                              |                        |                                 | guides.                                                            |
+------------------------------+------------------------+---------------------------------+--------------------------------------------------------------------+
| iApp                         |                        | X                               | The |kctlr| can deploy any iApp that already exists on             |
|                              |                        |                                 | the BIG-IP system.                                                 |
+------------------------------+------------------------+---------------------------------+--------------------------------------------------------------------+
| node                         | X                      |                                 | Applies to all supported Kubernetes resources.                     |
+------------------------------+------------------------+---------------------------------+--------------------------------------------------------------------+
| partition                    |                        | X                               | The |kctlr| cannot create or destroy BIG-IP partitions.            |
+------------------------------+------------------------+---------------------------------+--------------------------------------------------------------------+
| pool                         | X                      |                                 | Applies to all supported Kubernetes resources.                     |
+------------------------------+------------------------+---------------------------------+--------------------------------------------------------------------+
| pool member                  | X                      |                                 | Applies to all supported Kubernetes resources.                     |
+------------------------------+------------------------+---------------------------------+--------------------------------------------------------------------+
| self IP                      |                        | X                               | Applies to all supported Kubernetes resources.                     |
+------------------------------+------------------------+---------------------------------+--------------------------------------------------------------------+
| profiles                                                                                                                                                     |
+---+--------------------------+------------------------+---------------------------------+--------------------------------------------------------------------+
|   | HTTP                     |                        | X                               | :ref:`Kubernetes Ingress resources <kctlr-ingress-config>`         |
|   |                          |                        |                                 | (L7) only                                                          |
+---+--------------------------+------------------------+---------------------------------+--------------------------------------------------------------------+
|   | SSL                      | X                      | X                               | Supported functionality varies by resource and platform. See note  |
|   |                          |                        |                                 | below.                                                             |
+---+--------------------------+------------------------+---------------------------------+--------------------------------------------------------------------+
|   | TCP                      |                        | X                               | :ref:`F5 Resources <k8s-f5-resources>` (L4) only                   |
+---+--------------------------+------------------------+---------------------------------+--------------------------------------------------------------------+
|   | UDP                      |                        | X                               | :ref:`F5 Resources <k8s-f5-resources>` (L4) only                   |
+---+--------------------------+------------------------+---------------------------------+--------------------------------------------------------------------+
| traffic policy               | X                      |                                 | :ref:`Kubernetes Ingress resources <kctlr-ingress-config>` (L7)    |
|                              |                        |                                 | only; the Controller creates a BIG-IP traffic policy to            |
|                              |                        |                                 | use for routing.                                                   |
+------------------------------+------------------------+---------------------------------+--------------------------------------------------------------------+
| virtual server               | X                      |                                 | Applies to all supported Kubernetes resources.                     |
+------------------------------+------------------------+---------------------------------+--------------------------------------------------------------------+

.. note::

   The |kctlr| support for SSL profiles varies based on resource type:

   - :ref:`F5 Resources <k8s-f5-resources>`: use existing client SSL profile
   - :ref:`Kubernetes Ingress <kctlr-ingress-config>`: use existing client SSL profile
   - :ref:`OpenShift Routes <kctlr-openshift-routes>`: create new client or server SSL profile; use existing client or server SSL profile

   |kctlr| support for **all** profiles applies to basic profiles only. Optimized and/or customized versions aren't supported.


.. _k8s-vs-naming:

Object Naming Convention
````````````````````````

The |kctlr| prefaces all BIG-IP virtual server objects with :code:`[namespace]_[resource-name]`. For example, if :code:`default` is the namespace and ``k8s.vs`` is the ConfigMap name, the object preface is :code:`default_k8s.vs_173.16.2.2:80`.

High-availability and Multi-tenancy
```````````````````````````````````

If you're using a BIG-IP device pair or cluster, F5 recommends deploying multiple |kctlr| instances -- one Controller per BIG-IP device. You can also deploy multiple Controller instances to manage separate BIG-IP partitions (for example, one Controller:one namespace:one partition).
