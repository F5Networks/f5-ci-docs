.. _k8s-home:

F5 Container Integration - Kubernetes
=====================================

This document provides general information regarding the F5 Integration for Kubernetes.
For deployment and usage instructions, please refer to the guides below.

.. toctree::
   :caption: BIG-IP Controller Guides
   :maxdepth: 1

   Add BIG-IP device to the Kubernetes Cluster <kctlr-use-bigip-k8s>
   Deploy the BIG-IP Controller <kctlr-app-install>
   Manage BIG-IP objects <kctlr-manage-bigip-objects>
   Deploy iApps <kctlr-deploy-iapp>
   Troubleshooting <../troubleshooting/kubernetes>
   k8s-bigip-ctlr reference documentation <http://clouddocs.f5.com/products/connectors/k8s-bigip-ctlr/latest>

   Extended information: flannel VXLAN, Kubernetes, and BIG-IP <flannel-bigip-info>

Overview
--------

The |kctlr-long| (``k8s-bigip-ctlr``) configures BIG-IP objects for applications in a Kubernetes `cluster`_, serving North-South traffic.

.. image:: /_static/media/cc_solution.png
   :scale: 60%
   :alt: Solution design: The Container Connector runs as an App within the cluster; it configures the BIG-IP device as needed to handle traffic for Apps in the cluster

.. _kctlr overview:

The |kctlr-long| is a Docker container that runs on a Kubernetes `Pod`_. You can :Ref:`launch the k8s-bigip-ctlr application <install-kctlr>` in Kubernetes using a Deployment. Once the |kctlr| Pod is running, it watches the `Kubernetes API <https://kubernetes.io/docs/api/>`_ for specially-formatted :ref:`"F5 Resource" <k8s-f5-resources>` ConfigMaps. The `ConfigMap`_ contains a JSON blob that tells the |kctlr|:

.. sidebar:: :fonticon:`fa fa-exclamation-circle` Important:

   * The |kctlr| cannot manage objects in the ``/Common`` :term:`partition`.
   * The BIG-IP partition you want to manage must exist before you launch the |kctlr|.
   * The |kctlr| does not create or destroy BIG-IP partitions.
   * You can use multiple |kctlr| instances to manage **separate** BIG-IP partitions.
   * You can create one (1) BIG-IP virtual server per Service port.
     *Create a separate* :ref:`virtual server F5 Resource ConfigMap <kctlr-create-vs>` *for each Service port you wish to expose.*

- what `Service`_ it should manage, and
- what objects it should create/update on the BIG-IP system for that Service.

You can use F5 Resource ConfigMaps to deploy BIG-IP :ref:`virtual servers <kctlr-create-vs>` or :ref:`iApps <kctlr-deploy-iapps>`.

The |kctlr| can:

- :ref:`create a BIG-IP LTM virtual servers <kctlr-create-vs>` for a `Kubernetes Service`_
- :ref:`use an IPAM system to assign IP addresses to virtual servers <kctlr-ipam>`
- :ref:`create unattached pools <kctlr-pool-only>` (pools that aren't attached to virtual servers)
- :ref:`deploy iApps <kctlr-deploy-iapps>`
- act as a `Kubernetes Ingress controller`_ to :ref:`expose Kubernetes Services to external traffic <kctlr-ingress-config>`.


.. _k8s-prereqs:

General Prerequisites
`````````````````````

The F5 Integration for Kubernetes documentation set assumes that you:

- already have a Kubernetes `cluster`_ running;
- are familiar with the `Kubernetes dashboard`_ and `kubectl`_ ;
- already have a BIG-IP :term:`device` licensed and provisioned for your requirements; and
- are familiar with BIG-IP LTM concepts and ``tmsh`` commands.

.. note::

   When using the |kctlr| in :ref:`cluster mode`, your BIG-IP license must include SDN services.

.. include:: /_static/reuse/bigip-permissions-ctlr.rst

.. _k8s-installation:

Installation
------------

- You can :ref:`launch the k8s-bigip-ctlr application <install-kctlr>` in Kubernetes using a Deployment.
- If you use `helm`_ you can use the `f5-bigip-ctlr chart`_.

.. _k8s-upgrade:

Upgrade
-------

To upgrade an existing :code:`k8s-bigip-ctlr` instance to a newer version, take the steps below.

#. :ref:`Edit the Controller Deployment <k8s-bigip-ctlr-deployment>`.

   - Update the :code:`image` property to use the desired version.
   - Add/edit configuration parameters as desired.

#. :ref:`Upload the Deployment to the Kubernetes API server <upload to k8s api>`.

.. include:: /_static/reuse/upgrade-warning.rst

.. _apply bigip services k8s:

Applying BIG-IP Services to Kubernetes Resources
------------------------------------------------

The |kctlr| enables :ref:`ingress <k8s-concept ingress>` into the cluster via :ref:`F5 Resources <k8s-f5-resources>` and :ref:`Kubernetes Ingress resources <kctlr-ingress-config>`.
For all ingress traffic, the |kctlr| creates a front-end virtual server that passes incoming requests to the appropriate endpoint(s) within the Cluster.

When using F5 Resources or Kubernetes Ingresses, the definitions you provide tell the |kctlr|:

- what Kubernetes resource(s) you want the |kctlr| to manage;
- what objects to create on the BIG-IP device(s) for the specified resource(s); and
- how to configure those BIG-IP objects.

.. important::

   - The |kctlr| cannot manage objects in the ``/Common`` partition.
   - The |KCTLR| cannot create or destroy BIG-IP partitions.
   - The partition(s) in which you want to manage objects for your Kubernetes cluster must exist on the BIG-IP system before you deploy the |kctlr|.

What BIG-IP Objects can the Controller Manage?
``````````````````````````````````````````````
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


.. _k8s-f5-resources:

F5 Resource Properties
``````````````````````

The |kctlr-long| uses special 'F5 Resources' to identify what BIG-IP objects it should create.
An F5 resource is a JSON blob defined in a Kubernetes `ConfigMap`_.

An :ref:`F5 Resource JSON blob <f5-resource-blob>` may contain the properties shown below.

.. table:: F5 Resource properties

   ======================= ======================================================== ===========
   Property                Description                                              Required
   ======================= ======================================================== ===========
   f5type                  A ``label`` property watched by the |kctlr|.             Optional
   ----------------------- -------------------------------------------------------- -----------
   schema                  The schema |kctlr| uses to interpret the                 Required
                           encoded data. [#schema]_
   ----------------------- -------------------------------------------------------- -----------
   data                    A JSON object                                            Required
   ----------------------- -------------------------------------------------------- -----------
     frontend              Defines the BIG-IP virtual server.
   ----------------------- -------------------------------------------------------- -----------
     backend               Identifies the Service you want to proxy.

                           Defines BIG-IP health monitor(s) for the Service.
   ======================= ======================================================== ===========


.. [#schema] See the :ref:`F5 schema compatibility table <schema-table>` for more information.

The |kctlr| uses the ``f5type`` property differently depending on the use case.

- **When used in a virtual server F5 Resource** ConfigMap, set :code:`f5type: virtual-server`.
  This tells the |kctlr| what type of resource you want to create.
- **When used in OpenShift Route definitions**, you can define it any way you like.
  You can set the |kctlr| to watch for Routes configured with a specific ``f5type`` label.
  For example: :code:`f5type: App1` [#routes]_

The ``frontend`` property defines how to expose a Service on a BIG-IP device.

- You can define ``frontend`` using the standard `k8s-bigip-ctlr Virtual Server configuration parameters`_ or the `k8s-bigip-ctlr iApp configuration parameters`_.

- The ``frontend`` iApp configuration parameters include a set of customizable ``iappVariables`` parameters.
  These custom user-defined parameters must correspond to fields in the iApp template you want to launch.
  You can also define the `iApp pool member table`_ that the iApp creates on the BIG-IP system.

The ``backend`` property identifies the `Kubernetes Service`_ that makes up the server pool.
You can define BIG-IP health monitors in this section.

.. _f5-resource-blob:

Example F5 virtual server resource
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The below example creates one (1) virtual server for the Service named "myService", with one (1) health monitor and one (1) pool. The Controller will create the virtual server in the :code:`k8s` partition on the BIG-IP system.

.. literalinclude:: /kubernetes/config_examples/f5-resource-vs-example.json
   :caption: Example F5 Resource definition

.. [#routes] The |kctlr| supports Routes in OpenShift deployments. See :ref:`OpenShift Routes` for more information.


Key Kubernetes Concepts
-----------------------

Cluster Network
```````````````

The basic assumption of the Kubernetes `Cluster Network`_ is that Pods can communicate with other Pods, regardless of what host they're on.
You have a few different options when connecting your BIG-IP device (platform or Virtual Edition) to a Kubernetes cluster network and the |kctlr|.
How (or whether) you choose to integrate your BIG-IP device into the cluster network -- and the framework you use -- impacts how the BIG-IP system forwards traffic to your Kubernetes Services.

See :ref:`Nodeport mode vs Cluster mode <kctlr modes>` for more information.

.. _k8s-namespaces:

Namespaces
``````````

The Kubernetes `Namespace`_ allows you to create/manage multiple cluster environments.
The |kctlr-long| can manage all namespaces; a single namespace; or pretty much anything in between.

When :ref:`creating a BIG-IP front-end virtual server <kctlr-create-vs>` for a `Service`_, you can:

- specify a single namespace to watch (*this is the only supported mode in ``k8s-bigip-ctlr`` v1.0.0*);
- specify multiple namespaces by passing each in as a separate flag; or
- watch all namespaces (by omitting the namespace flag); **this is the default setting** as of ``k8s-bigip-ctlr`` v1.1.0.

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

.. _Cluster Network: https://kubernetes.io/docs/concepts/cluster-administration/networking/
.. _Prometheus: https://prometheus.io/
