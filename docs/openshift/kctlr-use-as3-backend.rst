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

Notable Changes
---------------
When deployed to use AS3 as an orchestration backend, the controller will create a new partition named
`<bigip-partition>_AS3` and put all the LTM objects in this partition. FDB entries and Static ARP entries continue to
exist in `<bigip-partition>`. In the above example, the controller uses `myParition_AS3` for LTM objects such as pools,
virtuals, policies. FDB and Static ARP entries will be in `myPartition`.

Supported Openshift Route Features
----------------------------------


Known Issues
------------
