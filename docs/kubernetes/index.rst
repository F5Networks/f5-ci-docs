:product: BIG-IP Container Ingress Services for Kubernetes
:type: concept

.. _k8s-home:

F5 Container Ingress Services - Kubernetes
==========================================

.. seealso::
   :class: sidebar

   :ref:`Learn about using the BIG-IP Controller in OpenShift <openshift-home>`.

The F5 BIG-IP Controller for Kubernetes lets you manage your F5 BIG-IP device from Kubernetes or OpenShift, using either environment’s native API.

.. _kctlr-features:

Features
--------

- Dynamically creates, manages, and destroys BIG-IP objects.
- Forwards traffic from the BIG-IP device to `Kubernetes clusters`_ via `NodePort`_ or `ClusterIP`_.
- Support for `F5 AS3 Extension`_ declarations.
- Support for F5 `iApps`_.
- Handles F5-specific VirtualServer objects created in Kubernetes.
- Handles standard `Kubernetes Ingress`_ objects using F5-specific extensions.
- Handles OpenShift Route objects using F5-specific extensions.

.. _kctlr-overview:

Overview
--------

The |kctlr-long| (:code:`k8s-bigip-ctlr`) is a cloud-native connector.
It enables use of an F5 BIG-IP device as an Application Delivery Controller (ADC) serving North-South traffic in a Kubernetes `Cluster`_.

See the :ref:`connector compatibility` table for platform compatibility information.

The |kctlr| watches the `Kubernetes API <https://kubernetes.io/docs/api/>`_ for specially-formatted resources and updates the BIG-IP system configurations accordingly.

.. image:: /_static/media/cc_solution.png
   :scale: 80%
   :alt: Solution design: The Container Connector runs as an App within the cluster; it configures the BIG-IP device as needed to handle traffic for Apps in the cluster

.. _k8s-prereqs:

Prerequisites
-------------

The |kctlr-long| documentation set assumes that you have:

- A running Kubernetes `Cluster`_.
- Experience with the `Kubernetes dashboard`_ and `kubectl`_.
- A BIG-IP device licensed and provisioned for your requirements.
- Experience with BIG-IP LTM concepts and ``tmsh`` commands.

.. note::

   When using the |kctlr| in :ref:`cluster mode`, your BIG-IP license must include SDN services.

.. include:: /_static/reuse/bigip-permissions-ctlr.rst

.. _k8s-installation:

Installation
------------

- You can :ref:`launch the k8s-bigip-ctlr application <install-kctlr>` in Kubernetes using a Deployment.
- If you use `helm`_ you can use the `f5-bigip-ctlr chart`_.

.. _k8s-upgrade:

Upgrades
--------

To upgrade an existing :code:`k8s-bigip-ctlr` instance to a newer version, take the steps below.

#. :ref:`Edit the Controller Deployment <k8s-bigip-ctlr-deployment>`.

   - Update the :code:`image` property to use the desired version.
   - Add/edit configuration parameters as desired.

#. :ref:`If using ConfigMap resources, you may also need to update the f5schemadb version <schema-table>`.

#. :ref:`Upload the Deployment to the Kubernetes API server <upload to k8s api>`.

.. include:: /_static/reuse/upgrade-warning.rst

.. _k8s-usage:

For deployment and usage instructions, please refer to the guides below.

User Guides
-----------

.. toctree::
   :maxdepth: 1

   flannel-bigip-info
   kctlr-use-bigip-k8s
   kctlr-app-install
   kctlr-k8s-as3
   kctlr-f5-resource
   kctlr-manage-bigip-objects
   kctlr-deploy-iapp
   ../troubleshooting/kubernetes
   k8s-bigip-ctlr Reference documentation <https://clouddocs.f5.com/products/connectors/k8s-bigip-ctlr/latest>

.. _apply-bigip-services-k8s:

Applying Services to Kubernetes Resources
-----------------------------------------

The |kctlr| enables :ref:`ingress <k8s-concept ingress>` into the cluster via :ref:`F5 Resources <k8s-f5-resources>` and :ref:`Kubernetes Ingress resources <kctlr-ingress-config>`.
For all ingress traffic, the |kctlr| creates a front-end virtual server that passes incoming requests to the appropriate endpoint(s) within the Cluster.

When using F5 Resources or Kubernetes Ingresses, the definitions you provide tell the |kctlr|:

- What Kubernetes resource(s) you want the |kctlr| to manage.
- What objects to create on the BIG-IP device(s) for the specified resource(s).
- How to configure those BIG-IP objects.

.. important::

   - The |kctlr| cannot manage objects in the ``/Common`` partition.
   - The |KCTLR| cannot create or destroy BIG-IP partitions.
   - The partition(s) in which you want to manage objects for your Kubernetes cluster must exist on the BIG-IP system before you deploy the |kctlr|.
   - CIS can use AS3 Extension declarations to create and use additional partitions. For more information, refer to `Container Ingress Services and AS3 Extension integration`_.

Managed Objects
---------------

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
|                              |                        |                                 | the BIG-IP system. [#iapp]_                                        |
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
| profiles [#prof]_                                                                                                                                            |
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
| traffic policy [#traffic]_   | X                      |                                 | :ref:`Kubernetes Ingress resources <kctlr-ingress-config>` (L7)    |
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

Object Naming
-------------

.. note::

   The |kctlr| prefaces all BIG-IP virtual server objects with :code:`[namespace]_[resource-name]`.

   For example, if :code:`default` is the namespace and ``k8s.vs`` is the ConfigMap name, the object preface is :code:`default_k8s.vs_173.16.2.2:80`.

High Availability and Multi-tenancy
-----------------------------------

If you're using a BIG-IP device pair or cluster, F5 recommends deploying multiple |kctlr| instances -- one Controller per BIG-IP device. You can also deploy multiple Controller instances to manage separate BIG-IP partitions (for example, one Controller:one namespace:one partition).

.. _k8s-concepts:

Key Kubernetes Concepts
-----------------------

Cluster Network
```````````````

The basic assumption of the Kubernetes `Cluster Network`_ is that Pods can communicate with other Pods, regardless of what host they're on.
You have a few different options when connecting your BIG-IP device (platform or Virtual Edition) to a Kubernetes cluster network and the |kctlr|.
How (or whether) you choose to integrate your BIG-IP device into the cluster network -- and the framework you use -- impacts how the BIG-IP system forwards traffic to your Kubernetes Services.

See :ref:`Nodeport mode vs Cluster mode <kctlr modes>` for more information.

.. _k8s-concept ingress:

"ingress" vs Ingress
````````````````````

It's important to understand the difference between the term "ingress" and the Kubernetes "Ingress resource":

- In general, **"ingress"** refers to all traffic to resources in the cloud (L4 or L7).
- In Kubernetes, **"Ingress"** (with a capital "I") refers to a specific type of resource via which you can configure L7 HTTP traffic.

.. seealso::

   - :ref:`kctlr-ingress-config` (L7)
   - :ref:`kctlr-openshift-routes` (L7)
   - :ref:`kctlr-per-svc-vs` (L4, L7)

.. _k8s-namespaces:

Namespaces
``````````

The Kubernetes `Namespace`_ allows you to create/manage multiple cluster environments.
The |kctlr-long| can manage all namespaces; a single namespace; or pretty much anything in between.

When you deploy the |kctlr|, you can:

- omit the :code:`--namespace` flag to watch all namespaces (**this is the default setting** as of :code:`k8s-bigip-ctlr v1.1.0`);
- specify a single namespace to watch (*this is the only supported mode in* :code:`k8s-bigip-ctlr v1.0.0`); or
- specify multiple namespaces to watch.

.. _k8s node health:

Node Health
```````````

When the |kctlr-long| runs in :ref:`nodeport mode` -- the default setting -- the |kctlr| doesn't have visibility into the health of individual Kubernetes Pods. It knows when Nodes are down and when **all Pods** are down.
Because of this limited visibility, a pool member may remain active on the BIG-IP system even if the corresponding Pod isn't available.

When running in :ref:`cluster mode`, the |kctlr| has visibility into the health of individual Pods.

.. tip::

   In either mode of operation, it's good practice to :ref:`add a BIG-IP health monitor <k8s-config-bigip-health-monitor>` to the virtual server to ensure the BIG-IP system knows when resources go down.

Prometheus Support :fonticon:`fa fa-flask`
------------------------------------------

.. include:: /_static/reuse/beta-announcement-k8s.rst

The |kctlr| provides a basic integration with `Prometheus`_ that allows you to retrieve information about the running state of a Controller.
Prometheus users can view the following Gauges for the |kctlr|:

- monitored Nodes
- managed Services
- malformed configurations
- Controller health

Define the :code:`http-listen-address` arg in your Controller Deployment to tell Prometheus on which IP address and port it should listen.

.. rubric:: **Footnotes**
.. [#iapp] Custom configurations required. See `k8s-bigip-ctlr iApp configuration parameters` for more information.
.. [#prof] See the `BIG-IP Local Traffic Management - Profiles Reference Guide`_ for more information.
.. [#traffic] See `BIG-IP Local Traffic Management - Getting Started with Policies`_ for more information.

.. _Cluster Network: https://kubernetes.io/docs/concepts/cluster-administration/networking/
.. _Prometheus: https://prometheus.io/
