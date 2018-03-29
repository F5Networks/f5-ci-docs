.. _overview BIG-IP HA k8s:

Manage BIG-IP HA pairs in Kubernetes
====================================

You can use the |kctlr-long| to manage a BIG-IP HA active-standby pair or device group in an OpenShift environment. To do so, deploy one |kctlr| instance per BIG-IP device.

Complete the tasks below to set up the |kctlr| to manage a BIG-IP pair or device group.


Prerequisites
-------------

If you don't already have two or more BIG-IP devices configured for high availability (HA), follow the instructions in the BIG-IP documentation to set up.

.. include:: /_static/reuse/initial-setup-bigip-ha.rst

Tasks
-----

.. toctree::
   :maxdepth: 2

   Add BIG-IP devices to flannel VXLAN <kctlr-use-bigip-k8s>
   Deploy the BIG-IP Controller <kctlr-app-install>
