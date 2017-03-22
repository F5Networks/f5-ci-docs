.. _k8s-home:

F5 Kubernetes Container Integration
===================================

Overview
--------

The F5 `Kubernetes`_ Container Integration consists of the `F5 Kubernetes BIG-IP Controller </products/connectors/k8s-bigip-ctlr/latest>`_ and the `F5 Application Service Proxy </products/asp/latest>`_ (ASP).

The |kctlr-long| configures a BIG-IP to expose applications in a `Kubernetes cluster`_ as BIG-IP virtual servers, serving North-South traffic.

The |asp| provides load balancing and telemetry for containerized applications, serving East-West traffic.

.. image:: /_static/media/kubernetes_solution.png
    :scale: 50 %
    :alt: F5 Container Solution for Kubernetes

.. _k8s-prereqs:

General Prerequisites
---------------------

The F5 Kubernetes Integration's documentation set assumes that you:

- already have a `Kubernetes cluster`_ running;
- are familiar with the `Kubernetes dashboard`_ and `kubectl`_ ;
- already have a BIG-IP :term:`device` licensed and provisioned for your requirements; [#bigipcaveat]_ and
- are familiar with BIG-IP Local Traffic Manager (LTM) concepts and ``tmsh`` commands. [#bigipcaveat]_

.. seealso::

    :ref:`OpenShift Origin Prerequisites <openshift-origin-prereqs>`

.. [#bigipcaveat] Not required for the |asp| and ASP controllers (|aspk|, |aspm|).


|asp|
-----

The |asp| (ASP) provides container-to-container load balancing, traffic visibility, and inline programmability for applications. Its light form factor allows for rapid deployment in datacenters and across cloud services. The ASP integrates with container environment management and orchestration systems and enables application delivery service automation.

The |asp| collects traffic statistics for the Services it load balances; these stats are either logged locally or sent to an external analytics application. You can set the location and type of the analytics application in the `stats </products/asp/latest/index.html#stats>`_ section of the :ref:`Service annotation <k8s-service-annotate>`.

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

The |kctlr-long| is a docker container that runs on a `Kubernetes Pod`_. To launch the |kctlr| application in Kubernetes, just :ref:`create a Deployment <install-kctlr>`.

Once the |kctlr| pod is running, it watches the `Kubernetes API <https://kubernetes.io/docs/api/>`_ for special Kubernetes "F5 Resource" `ConfigMap`_ s. These ConfigMaps contain an F5 Resource JSON blob that tells |kctlr|:

- what `Kubernetes Service`_ we want it to manage, and
- how we want to configure the BIG-IP for that specific Service.

When the |kctlr| discovers new or updated :ref:`F5 Resource ConfigMaps <kctlr-create-vs>`, it dynamically applies the configurations to the BIG-IP.

.. important::

    * The |kctlr-long| cannot manage objects in the BIG-IP's ``/Common`` :term:`partition`.
    * Each |kctlr-long| deployment monitors one (1) Kubernetes `namespace`_ and manages objects in its assigned BIG-IP :term:`partition`. *If you create more than one (1)* :ref:`k8s-bigip-ctlr deployment <k8s-bigip-ctlr-deployment>`, *each must manage a different BIG-IP partition.*
    * Each F5 Resource defines a virtual server on the BIG-IP for one (1) port associated with one (1) `Service`_. *Create a separate* :ref:`F5 Resource ConfigMap <kctlr-create-vs>` *for each Service port you wish to expose to the BIG-IP.*

You can use the |kctlr-long| to :ref:`manage BIG-IP objects <kctlr-manage-bigip-objects>` directly, or :ref:`deploy iApps <kctlr-deploy-iapps>`.

Key Kubernetes Concepts
-----------------------

.. _k8s-f5-resources:

F5 Resource Properties
``````````````````````

The |kctlr-long| uses special 'F5 Resources' to identify what objects it should create on the BIG-IP. An F5 resource is a JSON blob included in a Kubernetes `ConfigMap`_.

The :ref:`F5 Resource JSON blob <f5-resource-blob>` must contain the following properties.

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
| - frontend          | - a subset of ``data``; defines the virtualServer     |
|                     |   object                                              |
| - backend           | - a subset of ``data``; identifies the                |
|                     |   `Kubernetes Service`_ to proxy                      |
+---------------------+-------------------------------------------------------+

The frontend property defines how to expose a Service on the BIG-IP.
You can define the frontend using the standard `k8s-bigip-ctlr virtualServer parameters </products/connectors/k8s-bigip-ctlr/index.html#virtualserver>`_ or the `k8s-bigip-ctlr iApp parameters </products/connectors/k8s-bigip-ctlr/index.html#iapps>`_.

The frontend iApp configuration parameters include a set of customizable ``iappVariables`` parameters. These parameters must be custom-defined to correspond to fields in the iApp template you want to launch. In addition, you'll need to define the `iApp Pool Member Table </products/connectors/k8s-bigip-ctlr/index.html#iapp-pool-member-table>`_ that the iApp creates on the BIG-IP.

The backend property identifies the `Kubernetes Service`_ that makes up the server pool. You can also define health monitors for the virtual server and pool(s) in this section.


Kubernetes and OpenShift Origin
-------------------------------

See :ref:`F5 OpenShift Origin Integration <openshift-home>`.

Monitors and Node Health
------------------------

When the |kctlr-long| runs with ``pool-member-type`` set to ``nodeport`` -- the default setting -- the |kctlr| is not aware that Kubernetes nodes are down. This means that all pool members on a down Kubernetes node remain active even if the node itself is unavailable. When using ``nodeport`` mode, it's important to :ref:`configure a BIG-IP health monitor <k8s-config-bigip-health-monitor>` for the virtual server to mark the Kubernetes node as unhealthy if it's rebooting or otherwise unavailable.

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
    F5 Application Service Proxy docs <http://clouddocs.f5.com/products/asp/latest>


.. _f5-kube-proxy product documentation: </products/connectors/f5-kube-proxy/latest/>
.. _ASP product documentation: /products/asp/latest/




