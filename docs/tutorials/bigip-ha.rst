.. index::
   single: BIG-IP Controller
   single: BIG-IP high availability
   single: Cloud Foundry
   single: Kubernetes
   single: OpenShift
   single: Marathon

.. _manage BIG-IP HA:

How to manage BIG-IP HA pairs
=============================

The F5 Container Connectors allow you to manage BIG-IP devices from PaaS providers (Cloud Foundry, Kubernetes, Mesos, & OpenShift). Each platform has a BIG-IP Controller, which translates platform-native commands to F5 Python SDK/iControl REST calls. [#cccl]_

You can use any BIG-IP Controller to manage a BIG-IP HA active-standby pair. While the platform details vary, all of the Controllers operate on the same basic principle: To provide redundancy, run a Controller instance(s) for each BIG-IP device in an HA pair.

**For example**, say the active and standby devices are in separate data centers. You would deploy the BIG-IP Controller in each data center as well:

.. figure:: /_static/media/bigip-ha.png
   :alt: A diagram showing 2 separate data centers. Each contains a BIG-IP device and a BIG-IP Controller.

Any given BIG-IP Controller instance is responsible for a single administrative partition on the BIG-IP system. To provide redundancy for all partitions, you should deploy a backup of each Controller instance in the "standby" data center.

Deploy backup BIG-Controllers for BIG-IP HA Pairs
-------------------------------------------------

Cloud Foundry
`````````````


Kubernetes/OpenShift
````````````````````


Mesos Marathon
``````````````


.. [#cccl] See `Introduction to F5 Common Controller Core Library <https://devcentral.f5.com/articles/introduction-to-f5-common-controller-core-library-cccl-28355>`_ on DevCentral for more information.