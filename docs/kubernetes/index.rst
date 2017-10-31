.. _k8s-home:

F5 Kubernetes Container Integration
===================================

This document provides general information regarding the F5 Integration for Kubernetes.
For deployment and usage instructions, please refer to the guides below.

.. toctree::
   :caption: BIG-IP Controller
   :maxdepth: 1

   Deploy the BIG-IP Controller <kctlr-app-install>
   Manage BIG-IP objects <kctlr-manage-bigip-objects>
   Deploy iApps <kctlr-deploy-iapp>
   k8s-bigip-ctlr product information <http://clouddocs.f5.com/products/connectors/k8s-bigip-ctlr/latest>
   f5-kube-proxy product information <http://clouddocs.f5.com/products/connectors/f5-kube-proxy/latest>


.. toctree::
   :caption: Application Services Proxy
   :maxdepth: 1

   Set up the ASP ephemeral store <asp-k-ephemeral-store>
   Install the ASP <asp-install-k8s>
   Replace kube-proxy with the f5-kube-proxy <asp-k-deploy>
   Attach an ASP to a Service <asp-k-virtual-servers>
   ASP product information <http://clouddocs.f5.com/products/asp/latest>


Related
-------

.. toctree::
   :glob:
   :maxdepth: 1

   asp*
   k8s-bigip-ctlr docs <http://clouddocs.f5.com/products/connectors/k8s-bigip-ctlr/latest>

   F5 ASP docs <http://clouddocs.f5.com/products/asp/latest>


Overview
--------

The F5 Container Integration for `Kubernetes`_ consists of the `F5 BIG-IP Controller for Kubernetes </products/connectors/k8s-bigip-ctlr/latest>`_ and the `F5 Application Services Proxy </products/asp/latest>`_ (ASP).

The |kctlr-long| configures BIG-IP Local Traffic Manager (LTM) objects for applications in a `Kubernetes cluster`_, serving North-South traffic.

The |asp| provides load balancing and telemetry for containerized applications, serving East-West traffic.

.. image:: /_static/media/kubernetes_solution.png
   :scale: 50 %
   :alt: F5 Container Solution for Kubernetes


.. _k8s-prereqs:

General Prerequisites
`````````````````````

The F5 Integration for Kubernetes documentation set assumes that you:

- already have a `Kubernetes cluster`_ running;
- are familiar with the `Kubernetes dashboard`_ and `kubectl`_ ;
- already have a BIG-IP :term:`device` licensed and provisioned for your requirements; [#bigipcaveat]_ and
- are familiar with BIG-IP LTM concepts and ``tmsh`` commands. [#bigipcaveat]_

.. seealso::

    :ref:`OpenShift Origin Prerequisites <openshift-origin-prereqs>`

.. [#bigipcaveat] Not required for the |asp| and ASP controllers (|aspk|, |aspm|).


|asp|
-----

The |asp| (ASP) provides container-to-container load balancing, traffic visibility, and inline programmability for applications.
Its light form factor allows for rapid deployment in datacenters and across cloud services.
The ASP integrates with container environment management and orchestration systems and enables application delivery service automation.

.. important::

   In Kubernetes, the ASP runs as a forward, or client-side, proxy.


Ephemeral store
```````````````

.. include:: /_static/reuse/asp-version-added-1_1.rst

The `ASP ephemeral store`_ is a distributed, in-memory, secure key-value store.
It allows ASP instances to share non-persistent, or :dfn:`ephemeral`, data.

.. _asp-health-k8s:

Health monitors
```````````````

The ASP's built-in `health monitor </products/asp/latest/#health-monitors>`_ detects endpoint health using both active and passive checks.
The ASP adds and removes endpoints from load balancing pools based on the health status determined by these checks.
The ASP's health monitor enhances Kubernetes' native "liveness probes" as follows:

- provides a network view of service health;
- adds/removes endpoints from load balancing pool automatically based on health status;
- provides opportunistic health checks by observing client traffic;
- combines data from various health check types -- passive and active -- to provide a more comprehensive view of endpoints' health status.

Statistics
``````````

The |asp| collects traffic statistics for the Services it load balances.
These stats are either logged locally or sent to an external analytics application, like :ref:`Splunk <send-stats-splunk>`.

You can set the location and type of the analytics application in the `stats </products/asp/latest/index.html#stats>`_ section of the :ref:`ASP ConfigMap <asp-configure-k8s>`.


F5-kube-proxy
-------------

The |aspk-long| -- |aspk| -- replaces the standard Kubernetes network proxy, or `kube-proxy`_.

The ASP and |aspk| work together to proxy traffic for Kubernetes `Services`_ as follows:

- The |aspk| provides the same L4 services as `kube-proxy`_, include iptables and basic load balancing.
- For Services that have the :ref:`ASP Service annotation <k8s-service-annotate>`, the |aspk| hands off traffic to the ASP running on the same node as the client.
- The ASP then provides `L7 traffic services </products/asp/latest/index.html#built-in-middleware>`_ and `L7 telemetry </products/asp/latest/index.html#telemetry>`_ to your Kubernetes `Service`_.

.. important::

   By default, the |aspk| forwards traffic to ASP on port 10000.
   You can change this, if needed, to avoid port conflicts.

   See the `f5-kube-proxy product documentation`_ for more information.


|kctlr-long|
------------

The |kctlr-long| is a Docker container that runs on a `Kubernetes Pod`_.
You can `launch the k8s-bigip-ctlr application <install-kctlr>` in Kubernetes using a Deployment.

Once the |kctlr| pod is running, it watches the `Kubernetes API <https://kubernetes.io/docs/api/>`_ for special Kubernetes "F5 Resource" `ConfigMap`_ s.
An F5 Resource ConfigMap contains a JSON blob that tells |kctlr|:

- what `Kubernetes Service`_ it should manage, and
- what objects it should create/update on the BIG-IP system for that Service.

When the |kctlr| discovers new or updated :ref:`virtual server <kctlr-create-vs>` or :ref:`iApp <kctlr-deploy-iapps>` F5 Resource ConfigMaps, it configures the BIG-IP system accordingly.

.. caution::

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

The `Kubernetes namespace`_ allows you to create/manage multiple environments within a cluster.
The |kctlr-long| can manage all namespaces; a single namespace; or pretty much anything in between.

When :ref:`creating a BIG-IP front-end virtual server <kctlr-create-vs>` for a `Kubernetes Service`_, you can:

- specify a single namespace to watch (this is the only supported mode prior to k8s-bigip-ctlr v1.1.0);
- specify multiple namespaces (pass in each as a separate flag); or
- omit the namespace flag (meaning you want to watch all namespaces); **this is the default setting** as of k8s-bigip-ctlr v1.1.0.

.. _k8s-f5-resources:

F5 Resource Properties
``````````````````````

The |kctlr-long| uses special 'F5 Resources' to identify what BIG-IP LTM objects it should create.
An F5 resource is a JSON blob included in a Kubernetes `ConfigMap`_.

An :ref:`F5 Resource JSON blob <f5-resource-blob>` may contain the properties shown below.

.. table:: F5 Resource properties

   ======================= ======================================================== ===========
   Property                Description                                              Required
   ======================= ======================================================== ===========
   f5type                  A ``label`` property watched by the |kctlr|.             Optional
   ----------------------- -------------------------------------------------------- -----------
   schema                  The schema |kctlr| uses to interpret the                 Required
                           encoded data.

                           **BE SURE TO USE THE CORRECT SCHEMA VERSION FOR YOUR**
                           **VERSION OF THE CONTROLLER** (see below)
   ----------------------- -------------------------------------------------------- -----------
   data                    A JSON object                                            Required
   ----------------------- -------------------------------------------------------- -----------
     frontend              Defines the BIG-IP LTM objects you want to create.
   ----------------------- -------------------------------------------------------- -----------
     backend               Identifies the Service you want to proxy.
   ======================= ======================================================== ===========

\

.. table:: F5 schema and k8s-bigip-ctlr version compatibility

   =============================================== ============================
   Schema version                                  k8s-bigip-ctlr version
   =============================================== ============================
   f5schemadb://bigip-virtual-server_v0.1.4.json   1.3.0
   ----------------------------------------------- ----------------------------
   f5schemadb://bigip-virtual-server_v0.1.3.json   1.1.0, 1.2.0
   ----------------------------------------------- ----------------------------
   f5schemadb://bigip-virtual-server_v0.1.2.json   1.0.0
   =============================================== ============================


The |kctlr| uses the ``f5type`` property differently depending on the use case.

- **When used in a virtual server F5 Resource** ConfigMap, set :code:`f5type: virtual-server`.
  This tells the |kctlr| what type of resource you want to create.
- **When used in Route definitions**, you can define it any way you like.
  You can set the |kctlr| to only watch for Routes configured with a specific ``f5type`` label.
  For example: :code:`f5type: App1` [#routes]_

The ``frontend`` property defines how to expose a Service on a BIG-IP device.

- You can define ``frontend`` using the standard `k8s-bigip-ctlr virtualServer parameters </products/connectors/k8s-bigip-ctlr/latest/index.html#virtualserver>`_ or the `k8s-bigip-ctlr iApp parameters </products/connectors/k8s-bigip-ctlr/latest/index.html#iapps>`_.

- The ``frontend`` iApp configuration parameters include a set of customizable ``iappVariables`` parameters.
  These custom user-defined parameters must correspond to fields in the iApp template you want to launch.
  In addition, you can define the `iApp Pool Member Table </products/connectors/k8s-bigip-ctlr/latest/index.html#iapp-pool-member-table>`_ that the iApp creates on the BIG-IP system.

The ``backend`` property identifies the `Kubernetes Service`_ that makes up the server pool.
You can define health monitors for your BIG-IP LTM virtual server(s) and pool(s) in this section.

.. [#routes] The |kctlr| only supports routes in OpenShift deployments. See :ref:`OpenShift Routes` for more information.

Kubernetes and OpenShift
------------------------

Find out more about :ref:`using the BIG-IP Controller for Kubernetes in OpenShift <openshift-home>`.

Node Health
-----------

When the |kctlr-long| runs in :ref:`nodeport mode` -- the default setting -- the |kctlr| doesn't have visibility into the health of Kubernetes Pods.
It knows when Nodes are down and when all Pods are down.
Because of this limited visibility, a pool member may remain active on the BIG-IP system even if the corresponding Pod isn't available.

When running in :ref:`cluster mode`, the |kctlr| has visibility into the health of individual Pods.

.. tip::

   In either mode of operation, it's good practice to :ref:`add a BIG-IP health monitor <k8s-config-bigip-health-monitor>` to the virtual server to ensure the BIG-IP system knows when resources go down.

.. _Cluster Network: https://kubernetes.io/docs/concepts/cluster-administration/networking/
