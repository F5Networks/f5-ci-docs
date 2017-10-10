.. index::
   single: kubernetes; multi-tenancy
   single: openshift; multi-tenancy

.. _openshift multi-tenancy:

Multi-tenancy in Kubernetes and OpenShift
=========================================

Overview
--------

BIG-IP administrative partitions allow you to isolate tenants from each other and to configure objects for specific tenants, where only authorized users can access them. To manage multi-tenant BIG-IP systems with the |kctlr-long| and OpenShift, F5 recommends deploying one (1) instance of the :code:`k8s-bigip-ctlr` per BIG-IP partition.

There are a few different ways you can set up the |kctlr| for multi-tenancy...

Use case 1: Use one (1) BIG-IP partition and one (1) |kctlr| for all tenants in the Cluster
-------------------------------------------------------------------------------------------

1:1 - 1 BIG-IP partition, 1 Controller managing all tenants in cluster

- Use separate namespaces to achieve multi-tenancy in the k8s or OpenShift cluster.
- Deploy a single k8s-bigip-ctlr instance.
- Set the |kctlr| to watch all namespaces (default) and to manage a single BIG-IP partition (e.g., ose-cluster).
- Create Ingress, Virtual Server ConfigMap, and Route (**OpenShift only**) resources in each tenant namespace.

.. figure:: /_static/media/kctlr-mt-1.png
   :alt: A diagram showing one BIG-IP Controller watching all namespaces in a multi-tenant cluster. The Controller creates all objects in a single BIG-IP partition.

Use case 2: Use one (1) BIG-IP partition and one (1) |kctlr| per tenant
-----------------------------------------------------------------------

2A: Tenants with one namespace
``````````````````````````````

1:1:1 - 1 BIG-IP partition:1 Controller:1 namespace

- Use separate namespaces/projects to achieve multi-tenancy in the cluster
- Deploy one controller instance in each namespace
- Each controller manages a specific BIG-IP partition
- Create Ingress, Virtual Server ConfigMap, and Route (**OpenShift only**) resources in each tenant namespace/partition.

.. todo:: insert diagram

2B: Tenants with two or more namespaces
```````````````````````````````````````

1:1:x - 1 BIG-IP partition:1 Controller:1 or more namespaces/projects

- Use separate namespaces/projects to achieve multi-tenancy in the k8s or OpenShift cluster.
- Deploy multiple k8s-bigip-ctlr instances.
- Set each instance to watch one (1) or more specific namespaces (e.g., "customerA-test" and "customerA-prod") and manage a single BIG-IP partition (e.g., "customerA").
- Create Ingress, Virtual Server ConfigMap, and Route (**OpenShift only**) resources in each tenant namespace/partition.

.. todo:: insert diagram

Use case 3: Use multiple BIG-IP partitions and let applications choose which partition
--------------------------------------------------------------------------------------

- Use separate namespaces/projects to achieve multitenancy in the k8s or OpenShift cluster.
- Deploy multiple k8s-bigip-ctlr instances.
- Set each |kctlr| to watch all namespaces and manage a different BIG-IP partition (for instance, one |kctlr| manages "partitionA" on BIG-IP, and the other |kctlr| manages "partitionB" on BIG-IP)
- Applications choose which partition they are configured in (and therefore which controller manages them) by setting the partition property in the virtual-server or Ingress configuration.
  - For VirtualServer ConfigMap resources, this is the frontend.partition property.
  - For Ingress resources, this is the virtual-server.f5.com/partition annotation.

.. todo:: insert diagram



.. _global configuration parameters: /products/connectors/k8s-bigip-ctlr/latest/#controller-configuration-parameters
.. _Projects: https://docs.openshift.org/1.4/architecture/core_concepts/projects_and_users.html#projects