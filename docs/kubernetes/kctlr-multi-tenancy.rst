.. index::
   single: BIG-IP Controller; Kubernetes; multi-tenancy
   single: BIG-IP Controller; Openshift; multi-tenancy

.. _openshift multi-tenancy:

Multi-tenancy in Kubernetes and OpenShift
=========================================

Overview
--------

BIG-IP administrative partitions allow you to isolate tenants from each other and to configure objects for specific tenants, where only authorized users can access them. To manage multi-tenant BIG-IP systems with the |kctlr-long| and OpenShift, F5 recommends deploying one (1) instance of the :code:`k8s-bigip-ctlr` per BIG-IP partition.

You can set up the |kctlr| for multi-tenancy a few different ways, as described in the sections that follow. Each of the use cases described here uses namespaces (or projects, in OpenShift) to achieve multi-tenancy in the Kubernetes/OpenShift Cluster.

.. note::

   In each use case, the various Controller instances *can* use the same Service Account/Cluster Role/Cluster Role Binding. Whether or not the Controllers *should* use the same Service Account depends on the requirements of your tenants/Cluster.

.. sidebar:: :fonticon:`fa fa-question-circle-o` Did you know?

   You can create a separate `BIG-IP user account`_ for each :code:`k8s-bigip-ctlr` instance. The Controller can use any of the following roles:

   - Administrator
   - Resource Adminstrator
   - Manager

.. _multi-tenant use-case-1:

Use case 1: 1 partition, 1 Controller, all namespaces
-----------------------------------------------------

In this use case, one (1) :code:`k8s-bigip-ctlr` instance watches all of the namespaces in the Cluster and creates all objects in a single BIG-IP partition. You can isolate the Cluster tenants from each other on the BIG-IP system by creating virtual servers within each tenant's namespace.

.. figure:: /_static/media/kctlr-mt-1.png
   :scale: 70
   :alt: A diagram showing one BIG-IP Controller watching all namespaces in a multi-tenant cluster. The Controller creates all objects in a single BIG-IP partition.

**To set up this use case:**

#. :ref:`Deploy the k8s-bigip-ctlr <install-kctlr>` with the following configurations:

   - watch all namespaces (the default behavior);
   - manage a single BIG-IP partition (for example, "ose-cluster").

#. Create BIG-IP virtual servers for each namespace using an :ref:`Ingress <kctlr-ingress-config>`, :ref:`Virtual Server ConfigMaps <kctlr-create-vs>`, or :ref:`Route Resources <kctlr-openshift-routes>` (Route support available in OpenShift only).

**For example:**

You have multiple namespaces in your cluster, each representing a separate tenant. "Tenant1" deploys an application consisting of:

- a web front end (www.myapp.com);
- a set of app services that hold images (\https://myapp.com/images);
- a set of app services that hold videos (\https://myapp.com/videos); and
- a set of app services that deal with 3rd party ad servers (\https://myapp.com/ads).

For Tenant1, you'll create one (1) BIG-IP virtual server that has one (1) pool for each of its applications.

#. Create a :ref:`simple fanout <simple fanout>` Ingress that includes the path for each application.

   .. tip::

      You can use any existing BIG-IP SSL profile with a Kubernetes :ref:`TLS ingress <ingress-TLS>` to secure traffic.

The |kctlr| creates an HTTPS virtual server and pools on the BIG-IP system to expose the app Services to external traffic. Following the :ref:`standard naming convention <k8s-vs-naming>`, Tenant1's virtual server would appear on the BIG-IP system as "tenant1_myapp.https_1.2.3.4".

.. literalinclude:: /kubernetes/config_examples/f5-k8s_multi-tenant-1.yaml

:fonticon:`fa fa-download` :download:`Download the example manifest for this use case </kubernetes/config_examples/f5-k8s_multi-tenant-1.yaml>`

.. _multi-tenant use-case-2A:

Use case 2A: 1 partition and 1 Controller per namespace
-------------------------------------------------------

In this use case, you have multiple namespaces in your Cluster that each have 1:1 affinity with partitions on the BIG-IP system. You deploy one (1) :code:`k8s-bigip-ctlr` instance in each namespace; each |kctlr| instance manages objects in a BIG-IP partition allocated for its namespace. You can create virtual servers in each namespace as needed.

.. figure:: /_static/media/kctlr-mt-2a.png
   :scale: 70
   :alt: A diagram showing multiple BIG-IP Controllers in a multi-tenant cluster. Each Controller instance resides in a specific namespace; it creates objects for resources in that namespace in a specific BIG-IP partition.

**To set up this use case:**

#. :ref:`Deploy the k8s-bigip-ctlr <install-kctlr>` in each namespace. Each instance should:

   - watch a single namespace, and
   - manage a single BIG-IP partition.

#. Create BIG-IP virtual servers for each namespace using an :ref:`Ingress <kctlr-ingress-config>`, :ref:`Virtual Server ConfigMaps <kctlr-create-vs>`, or :ref:`Route Resources <kctlr-openshift-routes>` (Route support is available in OpenShift only).

**For example:**

You have two (2) namespaces in your Cluster: "test" and "prod". You use the "prod" namespace for mission-critical Apps. You want to use the "test" namespace to test an upgrade of the k8s-bigip-ctlr to version 1.3.0 by deploying an iApp.

- The ``test_k8s-bigip-ctlr`` will run in the "k8s_test" namespace; it will deploy the ``f5.http`` iApp in the "test" partition on the BIG-IP system.
- The ``prod_k8s-bigip-ctlr`` runs in the "k8s_prod" namespace; it manages objects in the in the "prod" partition on the BIG-IP system.

:fonticon:`fa fa-download` :download:`Download an example manifest for this use case </kubernetes/config_examples/f5-k8s_multi-tenant-2a.yaml>`

.. _multi-tenant use-case-2B:

Use case 2B: 1 partition and 1 Controller for 2 or more namespaces
------------------------------------------------------------------

In this use case, namespaces in your Cluster correspond to specific partitions on the BIG-IP system. The key difference between this use case and #2A is that you may have two (2) or more namespaces that correspond to a single BIG-IP partition. The |kctlr| instances do not need to run within a tenant's namespace, since each may manage more than just a single namespace. You can create virtual servers in each namespace as needed.

.. tip::

   You can `create a new namespace`_ for your Controllers to run in (for example: "bigip-controllers"). To see all of your |kctlr| instances at once, you'd run :code:`kubectl get pods -n bigip-controllers`.

\

.. figure:: /_static/media/kctlr-mt-2b.png
   :scale: 70
   :alt: A diagram showing 2 BIG-IP Controllers in a multi-tenant cluster. One Controller instance manages objects for 2 namespaces in a specific BIG-IP partition. The other Controller instance manages objects for a single, separate namespace in its own BIG-IP partition.

**To set up this use case:**

#. `Create a new namespace`_ for your |kctlr| instances (*OPTIONAL*).
#. :ref:`Create a Secret with the BIG-IP login credentials <secret-bigip-login>` for each |kctlr| instance.
#. Deploy two (2) :code:`k8s-bigip-ctlr` instances in the Controller namespace. Set each instance to:

   - watch one (1) or more specific namespaces (e.g., :code:`--namespace=customerA-test` and :code:`--namespace=customerA-prod`), and
   - manage a single BIG-IP partition (e.g., "customerA").

#. Create BIG-IP virtual servers using an :ref:`Ingress <kctlr-ingress-config>`, :ref:`Virtual Server ConfigMaps <kctlr-create-vs>`, or :ref:`Route Resources <kctlr-openshift-routes>` (Route support is available in OpenShift only).

**For example:**

You have two (2) tenants in your Cluster: "customerA" and "customerB". Customer A uses "test" and "prod" environments that each have a dedicated namespace (like in use case 2A). Customer B has a single namespace. You have a single BIG-IP partition dedicated to each customer.

**For Customer A:**

- You deploy one (1) :code:`k8s-bigip-ctlr` instance.
- The Controller manages two (2) namespaces - ``custA_test`` and ``custA_prod``.
- The Controller creates objects in the "customerA" BIG-IP partition.
- You use two (2) :ref:`simple fanout <simple fanout>` Ingresses to create separate virtual servers for the test and production versions of Customer A's website.

:fonticon:`fa fa-download` :download:`Download an example manifest for Customer A </kubernetes/config_examples/f5-k8s_multi-tenant-2b_custA.yaml>`

**For Customer B:**

- You deploy one (1) :code:`k8s-bigip-ctlr` instance.
- The Controller manages one (1) namespace - ``custB``.
- The Controller creates objects in the "customerB" BIG-IP partition.
- You create one (1) :ref:`simple fanout <simple fanout>` Ingress to create a virtual server for Customer B's website.

:fonticon:`fa fa-download` :download:`Download an example manifest for Customer B </kubernetes/config_examples/f5-k8s_multi-tenant-2b_custB.yaml>`

.. _multi-tenant use-case-3:

Use case 3: Partition/Controller selected by Application
--------------------------------------------------------

In this use case, you have a number of :code:`k8s-bigip-ctlr` instances deployed. Each manages a separate BIG-IP partition. You create virtual servers for your Apps individually, identifying the BIG-IP partition for each in the virtual server definition.

.. figure:: /_static/media/kctlr-mt-3.png
   :scale: 70
   :alt: A diagram showing 3 BIG-IP Controllers. Each manages a separate BIG-IP partition. Applications use the "partition" configuration parameter to tell the BIG-IP Controllers in which BIG-IP partition they should create objects for the Apps.

**To set up this use case:**

- Deploy multiple :code:`k8s-bigip-ctlr` instances.
- Set each Controller to watch all namespaces and manage a different BIG-IP partition.
- For each Service needing a BIG-IP virtual server:

  - Create a :ref:`single service` Ingress --OR-- an F5 resource :ref:`virtual server ConfigMap <kctlr-create-vs>`.
  - Specify the desired BIG-IP partition for the Service - :code:`virtual-server.f5.com/partition` or :code:`frontend.partition`, respectively.

**For example:**

You have two (2) :code:`k8s-bigip-ctlr` instances running. Each manages a separate BIG-IP partition (ctlr1 and ctlr2). You set the partition you want to create objects in on a per-Service basis using an Ingress and a virtual server ConfigMap. The |kctlr| instance responsible for the selected partition will configure objects on the BIG-IP system for each Service.

:fonticon:`fa fa-download` :download:`Download an example manifest for this use case </kubernetes/config_examples/f5-k8s_multi-tenant-3.yaml>`


Related
-------

- :ref:`kctlr-manage-bigip-objects`
- :ref:`kctlr-ingress-config`
- :ref:`kctlr-deploy-iapps`
- :ref:`kctlr-openshift-routes`

.. _Projects: https://docs.openshift.org/1.4/architecture/core_concepts/projects_and_users.html#projects
.. _BIG-IP user account: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/bigip-user-account-administration-13-0-0/1.html
.. _Create a new namespace: https://kubernetes.io/docs/tasks/administer-cluster/namespaces/
