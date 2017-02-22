F5 Kubernetes Container Integration
===================================

Overview
--------

The F5 `Kubernetes`_ Container Integration consists of the `F5 Kubernetes BIG-IP Controller </products/connectors/k8s-bigip-ctlr/latest>`_ and the `F5 Application Service Proxy </products/asp/latest>`_ (ASP).

The |kctlr-long| configures a BIG-IP to expose applications in a `Kubernetes cluster`_ as BIG-IP virtual servers, serving North-South traffic.

The |asp| provides load balancing and telemetry for containerized applications, serving East-West traffic.

General Prerequisites
---------------------

This documentation set assumes that you:

- already have a `Kubernetes cluster`_ running;
- are familiar with the `Kubernetes dashboard`_ and `kubectl`_ ;
- already have a BIG-IP :term:`device` licensed and provisioned for your requirements; [#bigipcaveat]_ and
- are familiar with BIG-IP Local Traffic Manager (LTM) concepts and ``tmsh`` commands. [#bigipcaveat]_

.. [#bigipcaveat] Not required for the |asp|.


|asp|
-----

The |asp| (ASP) provides container-to-container load balancing, traffic visibility, and inline programmability for applications. Its light form factor allows for rapid deployment in datacenters and across cloud services. The ASP integrates with container environment management and orchestration systems and enables application delivery service automation. The ASP's `Kubernetes`_ integration, |aspk|, builds on Kubernetes' existing `network proxy <https://kubernetes.io/docs/admin/kube-proxy/>`_ functionality.

.. seealso:: `ASP product documentation </products/asp/latest/index.html>`_


|kctlr-long|
------------

The |kctlr-long| is a docker container that runs on a `Kubernetes Pod`_. To launch the |kctlr| application in Kubernetes, just :ref:`create a Deployment <install-kctlr>`.

Once the |kctlr| pod is running, it watches the `Kubernetes API <https://kubernetes.io/docs/api/>`_ for special Kubernetes "F5 Resource `ConfigMap`_ "s. These ConfigMaps contain an F5 Resource JSON blob that tells |kctlr|:

- what `Kubernetes Service`_ we want it to manage, and
- how we want to configure the BIG-IP for that specific Service.

.. important::

    Each F5 Resource defines a virtual server on the BIG-IP for one (1) port, associated with one (1) `Kubernetes Service`_. *Create a separate F5 Resource ConfigMap for each Service port you wish to expose to the BIG-IP.*

When the |kctlr| discovers new or updated F5 Resource ConfigMaps, it dynamically applies the configurations to the BIG-IP.

F5 Resource Properties
``````````````````````

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
You can use either the Standard or iApp `configuration parameters <tbd>`_ in this section.

The frontend iApp configuration parameters include the customizable ``iappVariables`` parameter. This parameter corresponds to the user-populated fields in the iApp template you want to launch.


The backend property identifies the `Kubernetes Service`_ that makes up the server pool. You can also define health monitors for the virtual server and pool(s) in this section.

Related
```````

.. toctree::
    :glob:

    kctlr*
    asp*

- `|kctlr| </products/connectors/k8s-bigip-ctlr/latest/>`_
- `asp </products/asp/latest>`_






