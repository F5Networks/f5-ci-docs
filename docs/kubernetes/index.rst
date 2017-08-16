.. _k8s-home:

F5 Kubernetes Container Integration
===================================

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
---------------------

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

The |asp| (ASP) provides container-to-container load balancing, traffic visibility, and inline programmability for applications. Its light form factor allows for rapid deployment in datacenters and across cloud services. The ASP integrates with container environment management and orchestration systems and enables application delivery service automation.

The |asp| collects traffic statistics for the Services it load balances; these stats are either logged locally or sent to an external analytics application. You can set the location and type of the analytics application in the `stats </products/asp/latest/index.html#stats>`_ section of the :ref:`Service annotation <k8s-service-annotate>`.

.. important::

   In Kubernetes, the ASP runs as a forward, or client-side, proxy.

.. todo:: add "Export ASP Stats to an analytics provider"

.. seealso::

    `ASP product documentation`_


|aspk-long|
-----------

The |aspk-long| -- |aspk| -- replaces the standard Kubernetes network proxy, or `kube-proxy`_. The ``asp`` and |aspk| work together to proxy traffic for Kubernetes `Services`_ as follows:

- The |aspk| provides the same L4 services as `kube-proxy`_, include iptables and basic load balancing.
- For Services that have the :ref:`ASP Service annotation <k8s-service-annotate>`, the |aspk| hands off traffic to the ASP running on the same node as the client.
- The ASP then provides `L7 traffic services </products/asp/latest/index.html#built-in-middleware>`_ and `L7 telemetry </products/asp/latest/index.html#telemetry>`_ to your Kubernetes `Service`_.

By default, the |aspk| forwards traffic to ASP on port 10000. You can change this, if needed, to avoid port conflicts. See the `f5-kube-proxy product documentation`_ for more information.


|kctlr-long|
------------

The |kctlr-long| is a Docker container that runs on a `Kubernetes Pod`_.
To launch the |kctlr| application in Kubernetes, :ref:`create a Deployment <install-kctlr>`.

Once the |kctlr| pod is running, it watches the `Kubernetes API <https://kubernetes.io/docs/api/>`_ for special Kubernetes "F5 Resource" `ConfigMap`_ s.
These ConfigMaps contain an F5 Resource JSON blob that tells |kctlr|:

- what `Kubernetes Service`_ we want it to manage, and
- what BIG-IP LTM objects we want to create for that specific Service.

When the |kctlr| discovers new or updated :ref:`virtual server F5 Resource ConfigMaps <kctlr-create-vs>`, it dynamically applies the desired settings to the BIG-IP device.

.. caution::

   * The |kctlr-long| cannot manage objects in the ``/Common`` :term:`partition` on a BIG-IP device.
   * The BIG-IP partition must exist before you launch a |kctlr-long| to manage it.
   * The |kctlr-long| can't create or destroy BIG-IP partitions.
   * *Each* |kctlr| *instance must manage a different BIG-IP partition*.
   * Each :ref:`virtual server F5 Resource <kctlr-create-vs>` defines a BIG-IP LTM virtual server object for one (1) port associated with one (1) `Service`_.
     *Create a separate* :ref:`virtual server F5 Resource ConfigMap <kctlr-create-vs>` *for each Service port you wish to expose.*

The |kctlr-long| can:

- :ref:`create a BIG-IP LTM virtual servers <kctlr-create-vs>` for a `Kubernetes Service`_
- :ref:`use an IPAM system to assign IP addresses to virtual servers <kctlr-ipam>`
- :ref:`create unattached pools <kctlr-pool-only>` (pools without virtual servers)
- :ref:`deploy iApps <kctlr-deploy-iapps>`
- act as a `Kubernetes Ingress controller`_ to :ref:`expose Kubernetes Services to external traffic <kctlr-ingress-config>`

Networking
----------

The |kctlr-long| configures services on the BIG-IP device to expose applications inside your Kubernetes cluster to external users.
In certain deployments, the |kctlr| also handles some networking configurations on BIG-IP devices.

There are a number of options when it comes to connecting a BIG-IP device (physical or Virtual Edition) to a Kubernetes `Cluster Network`_, as noted below.
You can choose the one that best applies to your Kubernetes environment.

- :ref:`OpenShift clusters using the default VXLAN overlay network`.
- :ref:`Kubernetes clusters where pods are directly addressable` (like Calico BGP).
- :ref:`Kubernetes clusters using an overlay with manual config` (like VXLAN).
- :ref:`All other Kubernetes clusters using NodePort`.
.. Kubernetes clusters using Flannel VXLAN overlay network (since 1.2.0). Not available yet.

Key Kubernetes Concepts
-----------------------

.. _k8s-namespaces:

Namespaces
``````````

.. include:: /_static/reuse/k8s-version-added-1_1.rst

The `Kubernetes namespace`_ allows you to create/manage multiple environments within a cluster.
The |kctlr-long| can manage all namespaces; a single namespace; or pretty much anything in between.

When :ref:`creating a BIG-IP front-end virtual server <kctlr-create-vs>` for a `Kubernetes Service`_, you can:

- specify a single namespace to watch (this is the only supported mode prior to |kctlr| v1.1.0-beta.1);
- specify multiple namespaces (pass in each as a separate flag); or
- don't specify any namespace (meaning you want to watch all namespaces; **this is the default setting** as of |kctlr| v1.1.0-beta.1).

.. _k8s-f5-resources:

F5 Resource Properties
``````````````````````

The |kctlr-long| uses special 'F5 Resources' to identify what BIG-IP LTM objects it should create.
An F5 resource is a JSON blob included in a Kubernetes `ConfigMap`_.

The virtual server :ref:`F5 Resource JSON blob <f5-resource-blob>` must contain the following properties.

+---------------------+-------------------------------------------------------+
| Property            | Description                                           |
+=====================+=======================================================+
| f5type              | a ``label`` property defining the type of resource    |
|                     | to create on the BIG-IP;                              |
|                     |                                                       |
|                     | e.g., ``f5type: virtual-server``                      |
+---------------------+-------------------------------------------------------+
| schema              | identifies the schema |kctlr| uses to interpret the   |
|                     | encoded data                                          |
+---------------------+-------------------------------------------------------+
| data                | a JSON blob                                           |
|                     |                                                       |
| - frontend          | - a subset of ``data``; defines BIG-IP LTM objects    |
|                     |                                                       |
| - backend           | - a subset of ``data``; identifies the                |
|                     |   `Kubernetes Service`_ to proxy                      |
+---------------------+-------------------------------------------------------+

.. include:: /_static/reuse/k8s-schema-note.rst

The ``frontend`` property defines how to expose a Service on a BIG-IP device.
You can define ``frontend`` using the standard `k8s-bigip-ctlr virtualServer parameters </products/connectors/k8s-bigip-ctlr/latest/index.html#virtualserver>`_ or the `k8s-bigip-ctlr iApp parameters </products/connectors/k8s-bigip-ctlr/latest/index.html#iapps>`_.

The ``frontend`` iApp configuration parameters include a set of customizable ``iappVariables`` parameters.
These custom user-defined parameters must correspond to fields in the iApp template you want to launch.
In addition, you'll need to define the `iApp Pool Member Table </products/connectors/k8s-bigip-ctlr/latest/index.html#iapp-pool-member-table>`_ that the iApp creates on the BIG-IP device.

The ``backend`` property identifies the `Kubernetes Service`_ that makes up the server pool.
You can also define health monitors for your BIG-IP LTM virtual server(s) and pool(s) in this section.


Kubernetes and OpenShift Origin
-------------------------------

See :ref:`F5 OpenShift Origin Integration <openshift-home>`.

Monitors and Node Health
------------------------

When the |kctlr-long| runs with ``pool-member-type`` set to ``nodeport`` -- the default setting -- the |kctlr| is not aware that Kubernetes nodes are down.
This means that all pool members on a down Kubernetes node remain active even if the node itself is unavailable.
When using ``nodeport`` mode, it's important to :ref:`configure a BIG-IP health monitor <k8s-config-bigip-health-monitor>` for the virtual server to mark the Kubernetes node as unhealthy if it's rebooting or otherwise unavailable.

.. seealso::

   :ref:`OpenShift Origin node health <openshift-origin-node-health>`


Related
-------

.. toctree::
   :glob:

   kctlr*
   asp*
   k8s-bigip-ctlr docs <http://clouddocs.f5.com/products/connectors/k8s-bigip-ctlr/latest>
   f5-kube-proxy docs <http://clouddocs.f5.com/products/connectors/f5-kube-proxy/latest>
   F5 Application Services Proxy docs <http://clouddocs.f5.com/products/asp/latest>
