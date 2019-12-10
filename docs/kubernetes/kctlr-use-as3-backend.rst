:product: BIG-IP Controller for Kubernetes
:type: task

.. _kctlr-use-as3-backend:

Using AS3 for BIG-IP Orchestration in Kubernetes
================================================

The `k8s-bigip-ctlr`_ can use Application Services 3 (AS3) for BIG-IP orchestration. When using AS3 for BIG-IP orchestration, `k8s-bigip-ctlr`_ uses a declarative API to create Local Traffic Management (LTM) objects such as virtual servers, pools, and policies in a unique administrative partition.

Prerequisites
-------------

Ensure you meet the following requirements:

- BIG-IP system running version v12.1.x or later.
- BIG-IP system with AS3 v3.11 or higher.
- A BIG-IP user account with **Administrator** role.

Enabling AS3 orchestration
--------------------------

You can use these steps to enable AS3 for BIG-IP orchestration:

1. Include the **--agent=as3** option in your Deployment's argument section. For example:
  
   **Note:** In this example, `k8s-bigip-ctlr`_ will create partition **myParition_AS3** to store LTM objects such as pools, and virtual servers. FDB, and Static ARP entries are stored in **myPartition**. These partitions should not be managed manually.

.. code-block:: YAML
   :emphasize-lines: 7

   args: [
         "--bigip-username=$(BIGIP_USERNAME)",
         "--bigip-password=$(BIGIP_PASSWORD)",
         "--bigip-url=10.10.10.10",
         "--bigip-partition=myPartition",
         "--pool-member-type=cluster",
         "--agent=as3"
         ]

2. Start the Controller: 

.. parsed-literal::

   kubectl apply -f f5-k8s-bigip-ctlr.yaml

Orchestration modes
-------------------

+------------------+------------------------------------------------------------------------------+
| --agent option   | Description                                                                  |
+==================+==============================================================================+
| as3              | Implements AS3 for BIG-IP orchestration. This option creates an additional   |
|                  | partition as <partition>_AS3. The <partition> name is provided by the        |
|                  | **--bigip-partition=<name>** argument.                                       |
+------------------+------------------------------------------------------------------------------+
| cccl             | Implements Common Controller Core Library for BIG-IP orchestration.          |
|                  | This is the default setting.                                                 |
+------------------+------------------------------------------------------------------------------+

Supported Kubernetes Ingress Features
-------------------------------------

- :ref:`single service`
- :ref:`simple fanout`
- :ref:`name-based virtual hosting`
- :ref:`TLS <ingress-TLS>`

Supported Annotations
`````````````````````

- kubernetes.io/ingress.class
- virtual-server.f5.com/balance
- virtual-server.f5.com/health
- virtual-server.f5.com/ip
- virtual-server.f5.com/serverssl
- virtual-server.f5.com/http-port
- virtual-server.f5.com/https-port
- virtual-server.f5.com/ssl-redirect
- virtual-server.f5.com/allow-http
- virtual-server.f5.com/rewrite-app-root
- virtual-server.f5.com/rewrite-target-url

Known Issues
------------

v1.12.0
```````
- CIS does not support virtual-server.f5.com/partition annotation. 

AS3 Resources
-------------
- See the `F5 AS3 User Guide`_ to get started using F5 AS3 Extension declarations.
- See the `F5 AS3 Reference Guide`_ for an overview and list of F5 AS3 Extension declarations.
