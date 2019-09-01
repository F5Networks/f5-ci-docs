:product: BIG-IP Container Ingress Services for Kubernetes
:type: concept

.. _k8s-home:

F5 Container Ingress Services - Kubernetes
==========================================

------------

   `Current Release Notes <https://clouddocs.f5.com/products/connectors/k8s-bigip-ctlr/latest/RELEASE-NOTES.html>`_
   `Releases and Versioning <https://clouddocs.f5networks.net/containers/v2/releases_and_versioning.html#connector-compatibility>`_

.. seealso::
   :class: sidebar

   :ref:`Learn about using the BIG-IP Controller in OpenShift <openshift-home>`.

The F5 BIG-IP Controller, **k8s-bigip-ctlr**, is a cloud-native connector that can use either Kubernetes or OpenShift as a BIG-IP orchestration platform.

The |kctlr| watches the `Kubernetes API <https://kubernetes.io/docs/api/>`_ for specially formatted resources and updates the BIG-IP system configurations accordingly.

.. image:: /_static/media/cc_solution.png
   :scale: 60%

.. _kctlr-features:

Features
--------

- Dynamically create, and manage BIG-IP objects.
- Forward traffic from the BIG-IP device to `Kubernetes clusters`_ via `NodePort`_ or `ClusterIP`_.
- Support `F5 AS3 Extension`_ declarations.
- Support `F5 iApps`_.

User Guides
-----------

.. toctree::
   :maxdepth: 1

   flannel-bigip-info
   kctlr-use-bigip-k8s
   kctlr-app-install
   kctlr-managed-objects
   kctlr-k8s-as3
   kctlr-f5-resource
   kctlr-manage-bigip-objects
   kctlr-deploy-iapp
   ../troubleshooting/kubernetes

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

You can install the :code:`k8s-bigip-ctlr` using a :ref:`Kubernetes deployment<install-kctlr>`, or the `F5 Helm Chart`_.

.. _k8s-upgrade:

Upgrades
--------

You can upgrade your current :code:`k8s-bigip-ctlr` instance.

#. :ref:`Edit the Controller Deployment <k8s-bigip-ctlr-deployment>`.

   - Update the :code:`image` property to use the desired version.
   - Add/edit configuration parameters as desired.

#. :ref:`If using ConfigMap resources, you may also need to update the f5schemadb version <schema-table>`.

#. :ref:`Upload the Deployment to the Kubernetes API server <upload to k8s api>`.

.. include:: /_static/reuse/upgrade-warning.rst

.. _apply-bigip-services-k8s:

Ingress services
----------------

The |kctlr| enables :ref:`ingress <k8s-concept ingress>` into the cluster using either :ref:`F5 Resources <k8s-f5-resources>`, or `F5 AS3 Extension`_ declarations. For all ingress traffic, the |kctlr| creates a front-end virtual server that routes incoming requests to the appropriate endpoints within the Cluster.

When using F5 Resources or AS3 Extensions, the definitions you provide tell the |kctlr|:

- What Kubernetes resource(s) you want the |kctlr| to manage.
- What objects to create on the BIG-IP device(s) for the specified resource(s).
- How to configure those BIG-IP objects.

For a list of managed BIG-IP objects, refer to :ref:`Managed BIG-IP objects <kctlr-managed-objects>`

.. important::

   - The |kctlr| cannot manage objects in the ``/Common`` partition.
   - The |KCTLR| cannot create or destroy BIG-IP partitions.
   - The partition(s) in which you want to manage objects for your Kubernetes cluster must exist on the BIG-IP system before you deploy the |kctlr|.
   - CIS can use AS3 Extension declarations to create and use additional partitions. For more information, refer to `Container Ingress Services and AS3 Extension integration`_.

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

.. _Cluster Network: https://kubernetes.io/docs/concepts/cluster-administration/networking/
.. _Prometheus: https://prometheus.io/
