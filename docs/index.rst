:product: Container Ingress Services
:product: BIG-IP Controller for Kubernetes
:product: BIG-IP Controller for Cloud Foundry
:product: BIG-IP Controller for Marathon
:type: concept

.. _containers-home:

Introduction to F5 Container Ingress Services
=============================================

The F5 Container Ingress Services ('CIS') provide platform-native integrations for BIG-IP devices from PaaS providers like Cloud Foundry, Kubernetes, Mesos, & OpenShift. The CCs make it possible to dynamically allocate BIG-IP L4-L7 services in container orchestration environments by translating native commands to F5 Python SDK/iControl REST calls. [#cccl]_

=======================     ===================================================
Container Connector         Environment
=======================     ===================================================
`cf-bigip-ctlr`_            `Cloud Foundry`_ and `Pivotal Cloud Foundry`_
-----------------------     ---------------------------------------------------
`k8s-bigip-ctlr`_           `Kubernetes`_ and `Red Hat OpenShift`_
-----------------------     ---------------------------------------------------
`marathon-bigip-ctlr`_      `Apache Mesos`_ `Marathon`_,
                            `DC/OS and DC/OS Enterprise`_
=======================     ===================================================

.. figure:: /_static/media/container_connectors_north-south.png
   :scale: 80%
   :align: center
   :alt: North-South architecture

   Container Connector architecture

.. [#cccl] See `Introduction to F5 Common Controller Core Library <https://devcentral.f5.com/articles/introduction-to-f5-common-controller-core-library-cccl-28355>`_ on DevCentral for more information.

---------------------------------

.. _CC design:

Design
------

Each Container Ingress Services is uniquely suited to its specific container orchestration environment and purpose, utilizing the architecture and language appropriate for the environment. Application Developers interact with the platform's API; the CCs watch the API for certain events, then act accordingly.

The Container Ingress Services is stateless. The inputs are:

- the container orchestration environment's config,
- the BIG-IP device config, and
- the CC config (provided via the appropriate means for the container orchestration environment).

This means an instance of a Container Ingress Services can be readily discarded. Migrating a CC is as easy as destroying it in one place and spinning up a new one somewhere else. Wherever a Container Connector runs, it always watches the API and attempts to bring the BIG-IP up-to-date with the latest applicable configurations.

Working with BIG-IP HA pairs or device groups
---------------------------------------------

You can use the F5 Container Ingress Services to manage a BIG-IP HA active-standby pair or device group. The deployment details vary depending on the platform. For most, the basic principle is the same: You should run one |kctlr| instance for each BIG-IP device.

**For example**:

You have one active and one standby BIG-IP device. You want to manage a Kubernetes Cluster using a single BIG-IP partition. For your HA setup, you'd deploy two |kctlr| instances - one for each BIG-IP device. To help ensure Controller HA, you can deploy each Controller instance on a separate Node in the cluster.

.. figure:: /_static/media/bigip-ha.png
   :alt: A diagram showing a BIG-IP active-standby device pair and 2 BIG-IP Controllers, running on separate nodes in a Kubernetes Cluster.
   :scale: 65%

BIG-IP config sync
``````````````````

Each Container Connector monitors the BIG-IP partition it manages for configuration changes. If it discovers changes, the Connector reapplies its own configuration to the BIG-IP system.

F5 does not recommend making configuration changes to objects in any partition managed by a |kctlr| via any other means (for example, the configuration utility, TMOS, or by syncing configuration from another device or service group). Doing so may result in disruption of service or unexpected behavior.

.. important::

   If you use tunnels to connect your BIG-IP device(s) to the Cluster network, you should `disable config sync for tunnels`_.

Notice for Kubernetes and OpenShift users
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. danger::

   The Container Connector for Kubernetes and OpenShift uses FDB entries and ARP records to identify the Cluster resources associated with BIG-IP Nodes. Because BIG-IP config sync doesn't include FDB entries or ARP records, F5 does not recommend using automatic configuration sync when managing a BIG-IP HA pair or cluster with the |kctlr|.

If you use automatic config sync on devices managed by the |kctlr|, there will be a service interruption window when failover occurs. This window will occur between the standby device activating and the |kctlr| updating the FDB and ARP records on the device.

The length of time for the service interruption will be, at minumum, the length of the :code:`k8s-bigip-ctlr` :code:`--node-poll-interval` setting (the interval at which the Controller polls the Kubernetes or OpenShift API server for updates). You can reduce this window by setting the :code:`node-poll-interval` to 5-10 seconds instead of using the default (30).

When you deploy one Controller per device, both devices receive the same FDB record updates. This translates to a shorter potential delay if/when failover happens.

If you choose to deploy one |kctlr| instance and manually sync configurations to the standby device, be sure to always sync *from* the BIG-IP device managed by the |kctlr| *to* the other device(s) in the group.

.. seealso:: :ref:`bigip ha openshift`

.. _bigip snats:

BIG-IP SNATs and SNAT automap
`````````````````````````````

All virtual servers created by the Container Connectors use `BIG-IP Automap SNAT`_ by default. This feature lets you map origin IP addresses -- for example, the flannel or OpenShift SDN :code:`public-ip` for each Pod -- to a pool of translation addresses on the BIG-IP system.

When the BIG-IP system processes connections from inside the Cluster network, it chooses a translation address from the pool of available self IP addresses. SNAT automap prefers floating self IP addresses to static ones, to support seamless failover between paired or clustered devices.

.. danger::

   If the SNAT automap feature can't find an available floating self IP in the VXLAN tunnel, it may use a floating self IP from another VLAN as the translation address. If the BIG-IP selects a floating IP from another VLAN as the translation address, you will not be able to pass traffic to your Cluster.

   Refer to `Overview of SNAT features`_ and `SNAT Automap and self IP address selection`_ in the AskF5 Knowledge Base for more information.

---------------------------------

.. include:: master_toc.rst
