:product: BIG-IP Controller for Kubernetes
:type: task

.. _kctlr-use-as3-backend:

Using AS3 for BIG-IP Orchestration
==================================

The `k8s-bigip-ctlr`_ can use Application Services 3 (AS3) for BIG-IP orchestration. When using AS3 for BIG-IP orchestration, `k8s-bigip-ctlr`_ uses a declaritive API to create Local Traffic Management (LTM) objects such as virtual servers, pools, and policies in a unique administrative partition.

Prerequisites
-------------
Ensure you meet the following requirements:

- BIG-IP Controller for Openshift 1.10 or higher
- BIG-IP system running version 12.1.x or later.
- BIG-IP system with AS3 3.11 or higher.
- A BIG-IP user account with **Administrator** role.

Enabling AS3 orchestration
--------------------------

You can use these steps to enable AS3 for BIG-IP orchestration:

1. Include the **--agent=as3** option in your Deployment's argument section. For example:
  
   **Note:** In this example, `k8s-bigip-ctlr`_ will create partition **myParition_AS3** to store LTM objects such as pools, and virtual servers. FDB, and Static ARP entries are stored in **myPartition**. These partitions should not be managed manually.

.. code-block:: YAML

   args: [
         "--bigip-username=$(BIGIP_USERNAME)",
         "--bigip-password=$(BIGIP_PASSWORD)",
         "--bigip-url=10.10.10.10",
         "--bigip-partition=myPartition",
         "--pool-member-type=cluster",
         "--openshift-sdn-name=/Common/openshift_vxlan",
         "--manage-routes=true",
         "--agent=as3"
         ]

2. Start the Controller: 

.. parsed-literal::

   oc apply -f f5-k8s-bigip-ctlr-openshift.yaml

Orchestration modes
-------------------

+------------------+------------------------------------------------------------------------------+
| --agent option   | Description                                                                  |
+==================+==============================================================================+
| as3              | Implements AS3 for BIG-IP orchestration. This option creates an additional   |
|                  | parition as <partition>_AS3. The <partition> name is provided by the         |
|                  | **--bigip-paritition=<name>** argument.                                      |
+------------------+------------------------------------------------------------------------------+
| cccl             | Implements Common Controller Core Library for BIG-IP orchestration.          |
|                  | This is the default setting.                                                 |
+------------------+------------------------------------------------------------------------------+

Supported Openshift Route Features
----------------------------------

+-------+---------------+-------------------------------+---------------------------+
| Route |  Termination  |          Option               |          Values           |
+=======+===============+===============================+===========================+
| Host  |               |                               |                           |
+-------+---------------+-------------------------------+---------------------------+
| Path  |               |                               |                           |
+-------+---------------+-------------------------------+---------------------------+
|  TLS  | - Passthrough | insecureEdgeTerminatoinPolicy | - None                    |
+-------+---------------+-------------------------------+---------------------------+
|       |  - Edge       | insecureEdgeTerminatoinPolicy | - None                    |
|       |               |                               | - Allow                   |
|       |               |                               | - Redirect                |
+-------+---------------+-------------------------------+---------------------------+
|       | - Reencrypt   | insecureEdgeTerminatoinPolicy | - None                    |
+-------+---------------+-------------------------------+---------------------------+

Annotations
```````````

- virtual-server.f5.com/balance
- virtual-server.f5.com/health
- virtual-server.f5.com/clientssl
- virtual-server.f5.com/serverssl
- virtual-server.f5.com/secure-serverssl

Known Issues
------------

v1.10.0
```````
- Controller does not overwrite manual changes in controller manager partitions on BIG-IP. A restart is required.
- Change in TLS Termination of a route is not detected by controller. A restart is required.
- Changing insecureEdgeTerminationPolicy is not detected by controller. A restart is required.
- Multiple ssl profiles are not supported through annotations.
- Combination of user specified certificates and ssl profile annotations are not supported.

AS3 Resources
-------------
- See the `F5 AS3 User Guide`_ to get started using F5 AS3 Extension declarations.
- See the `F5 AS3 Reference Guide`_ for an overview and list of F5 AS3 Extension declarations.

