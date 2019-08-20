:product: BIG-IP Controller for Kubernetes
:type: task

.. _use_as3_backend:

Use AS3 as Orchestration Backend
================================

This document provides step-by-step instructions for using `**AS3** <http://example.com>` as orchestration back end. An
orchestration backend is a component of the controller that creates objects in the BIG-IP.

Requirements
------------
1. BIG-IP Controller for Openshift 1.10 or higher
2. BIG-IP version 12.1.x or later.
3. AS3 3.11 or higher.
4. A BIG-IP user account with **Administrator** role.

Installation and Configuration
------------------------------
Before operating the controller with AS3 orchestration backend, you need to install AS3 package in BIG-IP as in the
`AS3 Installation Guide <https://clouddocs.f5.com/products/extensions/f5-appsvcs-extension/latest/userguide/installation.html>`.

Once AS3 package is installed in BIG-IP, restart the controller with the following command line parameter
`--agent=as3`. A sample controller deployment is provided below:

.. code-block:: YAML
   :emphasize-lines: 9
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

+---------------------+---------------+---------+--------------------------------------------------------------+
| Argument            | Values        | Default |                      Description                             |
+=====================+===============+=========+==============================================================+
| --agent             | as3, cccl     | cccl    | If as3 is given CIS creates one additional partition with    |
|                     |               |         | name <partition>_AS3 where <partition> is provided through   |
|                     |               |         | argument --bigip-paritition                                  |
+---------------------+---------------+---------+--------------------------------------------------------------+

Notable Changes
---------------
When deployed to use AS3 as an orchestration backend, the controller will create a new partition named
`<bigip-partition>_AS3` and put all the LTM objects in this partition. FDB entries and Static ARP entries continue to
exist in `<bigip-partition>`. In the above example, the controller uses `myParition_AS3` for LTM objects such as pools,
virtuals, policies. FDB and Static ARP entries will be in `myPartition`. These partitions should not be controlled by
users manually.

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

**Annotations**
- virtual-server.f5.com/balance
- virtual-server.f5.com/clientssl
- virtual-server.f5.com/serverssl
- virtual-server.f5.com/secure-serverssl
- virtual-server.f5.com/balance

Known Issues
------------
v1.10.0
```````
- Controller does not overwrite manual changes in controller manager partitions on BIG-IP. A restart is required.
- Change in TLS Termination of a route is not detected by controller. A restart is required.
- Changing insecureEdgeTerminationPolicy is not detected by controller. A restart is required.
- Multiple ssl profiles are not supported through annotations.
- Combination of user specified certificates and ssl profile annotations are not supported.
