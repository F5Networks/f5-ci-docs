.. _k8s-home:

F5 Container Integration - Kubernetes
=====================================

This document provides general information regarding the F5 Integration for Kubernetes.
For deployment and usage instructions, please refer to the guides below.

.. toctree::
   :caption: BIG-IP Controller
   :maxdepth: 1

   Deploy the BIG-IP Controller <kctlr-app-install>
   Manage BIG-IP objects <kctlr-manage-bigip-objects>
   Deploy iApps <kctlr-deploy-iapp>
   k8s-bigip-ctlr reference <http://clouddocs.f5.com/products/connectors/k8s-bigip-ctlr/latest>

Overview
--------

The F5 Container Integration for `Kubernetes`_ consists of the `BIG-IP Controller for Kubernetes`_. The |kctlr| configures BIG-IP objects for applications in a Kubernetes `cluster`_, serving North-South traffic.

.. image:: /_static/media/kubernetes_solution.png
   :scale: 50 %
   :alt: F5 Container Solution for Kubernetes

.. _kctlr overview:

The |kctlr-long| is a Docker container that runs on a Kubernetes `Pod`_. You can `launch the k8s-bigip-ctlr application <install-kctlr>` in Kubernetes using a Deployment. Once the |kctlr| pod is running, it watches the `Kubernetes API <https://kubernetes.io/docs/api/>`_ for specially-formatted :ref:`"F5 Resource" <k8s-f5-resources>` ConfigMaps. The `ConfigMap`_ contains a JSON blob that tells the |kctlr|:

- what `Service`_ it should manage, and
- what objects it should create/update on the BIG-IP system for that Service.

You can use F5 Resource ConfigMaps to deploy BIG-IP :ref:`virtual servers <kctlr-create-vs>` or :ref:`iApps <kctlr-deploy-iapps>`.

.. sidebar:: :fonticon:`fa fa-exclamation-circle` Important:

   * The |kctlr-long| cannot manage objects in the ``/Common`` :term:`partition`.
   * The BIG-IP partition you want to manage must exist before you launch the |kctlr|.
   * The |kctlr-long| does not create or destroy BIG-IP partitions.
   * You can use multiple |kctlr| instances to manage **separate** BIG-IP partitions.
   * You can create one (1) BIG-IP virtual server per Service port.
     *Create a separate* :ref:`virtual server F5 Resource ConfigMap <kctlr-create-vs>` *for each Service port you wish to expose.*

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

   When using the |kctlr| in OpenShift, make sure your BIG-IP license includes SDN services.


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

The below example creates one (1) virtual server for the Service named "myService", with one (1) health monitor and one (1) pool. The Controller will create the virtual server in the :code:`kubernetes` partition on the BIG-IP system.

.. literalinclude:: /kubernetes/config_examples/f5-resource-vs-example.json
   :caption: Example F5 Resource definition

.. [#routes] The |kctlr| supports Routes in OpenShift deployments. See :ref:`OpenShift Routes` for more information.


Key Kubernetes Concepts
-----------------------

Cluster Network
```````````````

The basic assumption of the Kubernetes `Cluster Network`_ is that pods can communicate with other pods, regardless of what host they're on.
You have a few different options when connecting your BIG-IP device (platform or Virtual Edition) to a Kubernetes cluster network and the |kctlr|.
How (or whether) you choose to integrate your BIG-IP device into the cluster network -- and the framework you use -- impacts how the BIG-IP system forwards traffic to your Kubernetes Services.

See :ref:`Nodeport mode vs Cluster mode <kctlr modes>` for more information.

.. _k8s-namespaces:

Namespaces
``````````

.. include:: /_static/reuse/k8s-version-added-1_1.rst

The Kubernetes `Namespace`_ allows you to create/manage multiple cluster environments.
The |kctlr-long| can manage all namespaces; a single namespace; or pretty much anything in between.

When :ref:`creating a BIG-IP front-end virtual server <kctlr-create-vs>` for a `Service`_, you can:

- specify a single namespace to watch (*this is the only supported mode in k8s-bigip-ctlr v1.0.0*);
- specify multiple namespaces by passing each in as a separate flag; or
- watch all namespaces (by omitting the namespace flag); **this is the default setting** as of k8s-bigip-ctlr v1.1.0.

.. _k8s node health:

Node Health
```````````

When the |kctlr-long| runs in :ref:`nodeport mode` -- the default setting -- the |kctlr| doesn't have visibility into the health of individual Kubernetes Pods. It knows when Nodes are down and when **all Pods** are down.
Because of this limited visibility, a pool member may remain active on the BIG-IP system even if the corresponding Pod isn't available.

When running in :ref:`cluster mode`, the |kctlr| has visibility into the health of individual Pods.

.. tip::

   In either mode of operation, it's good practice to :ref:`add a BIG-IP health monitor <k8s-config-bigip-health-monitor>` to the virtual server to ensure the BIG-IP system knows when resources go down.

OpenShift
---------

The |kctlr| provides additional functionality in OpenShift deployments, including support for Routes.

:fonticon:`fa fa-info-circle` :ref:`Learn about using the BIG-IP Controller in OpenShift <openshift-home>`.


.. _Cluster Network: https://kubernetes.io/docs/concepts/cluster-administration/networking/
