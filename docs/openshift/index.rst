:product: BIG-IP Controller for Kubernetes
:type: concept

.. _openshift-home:

F5 Container Connector - OpenShift
==================================

This document provides general information regarding the F5 Integration for OpenShift.
For deployment and usage instructions, please refer to the guides below.

.. toctree::
   :caption: BIG-IP Controller Guides
   :maxdepth: 1

   Add BIG-IP device to OpenShift Cluster <kctlr-use-bigip-openshift>
   Deploy the BIG-IP Controller <kctlr-openshift-app-install>
   Manage BIG-IP objects <../kubernetes/kctlr-manage-bigip-objects>
   Deploy iApps <../kubernetes/kctlr-deploy-iapp>
   Expose Services using Routes <kctlr-openshift-routes>
   Troubleshooting <../troubleshooting/kubernetes>
   k8s-bigip-ctlr reference documentation <https://clouddocs.f5.com/products/connectors/k8s-bigip-ctlr/latest>

Overview
--------

The |octlr-long| enables use of a BIG-IP device in `OpenShift`_. Because OpenShift has a native Kubernetes integration, the F5 Integration for OpenShift utilizes the same controller as the :ref:`k8s-home` (``k8s-bigip-ctlr``). The |kctlr| configures BIG-IP objects for applications in an OpenShift `cluster`_, serving North-South traffic.

.. image:: /_static/media/cc_solution.png
   :scale: 60%
   :alt: Solution design: The Container Connector runs as an App within the cluster; it configures the BIG-IP device as needed to handle traffic for Apps in the cluster

In OpenShift, you can use the |kctlr| to use a BIG-IP device(s) to:

- :ref:`proxy traffic for Services <kctlr-per-svc-vs>` --OR--
- :ref:`proxy traffic for OpenShift routes <kctlr-openshift-routes>`.

.. _openshift-origin-prereqs:

.. note::

   Integration with `OpenShift SDN`_  requires a BIG-IP `Better or Best license`_ with SDN services.

.. _openshift-origin-node-health:

Installation
------------

- You can :ref:`launch the k8s-bigip-ctlr application <install-kctlr-openshift>` in OpenShift using a Deployment.
- If you use `helm`_ you can use the `f5-bigip-ctlr chart`_.

.. include:: /_static/reuse/bigip-permissions-ctlr.rst

OpenShift Node Health
---------------------

In OpenShift clusters, the Kubernetes NodeList records status for all nodes registered with the master. Because the |kctlr| integrates with the cluster network, it can access the NodeList in OpenShift’s underlying Kubernetes API server and watch it for changes. The |kctlr| creates/updates FDB (Forwarding DataBase) entries for the configured VXLAN tunnel according to the NodeList. This ensures the |kctlr| only makes VXLAN requests to reported nodes.

As a function of the BIG-IP VXLAN, the BIG-IP device only communicates with healthy cluster nodes. The BIG-IP device does not attempt to route traffic to an unresponsive node, even if the node remains in the NodeList.

.. tip::

   You can also :ref:`set up BIG-IP health monitors <k8s-config-bigip-health-monitor>` for OpenShift Services.


.. _openshift routes:

OpenShift Routes
----------------

In OpenShift, the |kctlr| can manage BIG-IP objects for routes.

.. tip::

   See :ref:`manage OpenShift Routes with the BIG-IP Controller <kctlr-openshift-routes>` for configuration instructions.

Setting up `OpenShift Route resources`_ provides the following functionality:

- listen for HTTP route events in OpenShift and create/delete/expire routes on BIG-IP devices (including L7 config policies such as wildcard routes, prefixes, etc.);
- apply client SSL certificates from Kubernetes/OpenShift Secrets to BIG-IP LTM objects;
- apply existing BIG-IP SSL certificates to BIG-IP LTM objects;
- SSL termination using edge, passthrough, or re-encryption mode.

The table below shows what BIG-IP configurations the |kctlr| applies for common admin tasks in OpenShift.

.. table::

   ============================  ==========================================================
   User action                   Controller action
   ============================  ==========================================================
   Create OpenShift Route        - Create two virtual servers:

                                   - one (1) HTTP
                                   - one (1) HTTPS

                                 - Create pools and pool members with policies attached.
                                 - Attach defined policies to virtual servers.
   ----------------------------  ----------------------------------------------------------
   Add/remove endpoint(s)        - Add/remove the pool member(s) that correspond to the
                                   endpoint(s) from the Route's pool.
   ----------------------------  ----------------------------------------------------------
   Delete all Routes             - Remove all objects associated with the Routes
                                   (virtual servers, pools, and pool members) from the
                                   BIG-IP system.
   ============================  ==========================================================

Advanced Deployments
````````````````````

The |octlr-long| supports the following OpenShift `Advanced Deployment Strategies`_:

- `Blue-Green Deployment`_
- `A/B Deployment`_

Follow the instructions provided in the OpenShift documentation to use these deployment strategies with your BIG-IP Controller and BIG-IP device(s).

.. important::

   The |octlr-long| provides the following advantages over the native HAProxy when working with `alternate backends`_:

   - You use any of the BIG-IP load balancing algorithms the Controller supports (not just round robin). [#lb]_
   - When you assign a weight to a Service in an OpenShift Route, the |kctlr| assigns that weight to the Service's pool on the BIG-IP device. The weight isn't split across the Service's endpoints and there are no per-endpoint weight restrictions.


What's Next
-----------

Refer to the docs below for setup and configuration instructions.

- :ref:`Add your BIG-IP device to an OpenShift Cluster <bigip-openshift-setup>`.
- :ref:`Use the BIG-IP Controller to manage Routes <kctlr-openshift-routes>`.
- :ref:`Manage BIG-IP objects <kctlr-manage-bigip-objects>` with the |octlr-long|.
- See the `k8s-bigip-ctlr reference documentation`_.

.. rubric:: **Footnotes**
.. [#lb] The |kctlr| supports BIG-IP load balancing algorithms that do not require additional configuration parameters. You can view the full list of supported algorithms in the `f5-cccl schema <https://github.com/f5devcentral/f5-cccl/blob/03e22c4779ceb88f529337ade3ca31ddcd57e4c8/f5_cccl/schemas/cccl-ltm-api-schema.yml#L515>`_. See the `BIG-IP Local Traffic Management Basics user guide <https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/ltm-basics-13-0-0/4.html>`_ for information about each load balancing mode.

.. _OpenShift: https://www.openshift.org/
.. _OpenShift service account: https://docs.openshift.org/latest/admin_guide/service_accounts.html
.. _Authorization Policy: https://docs.openshift.org/latest/admin_guide/manage_authorization_policy.html
.. _OpenShift CLI: https://docs.openshift.org/latest/cli_reference/index.html
.. _OpenShift SDN: https://docs.openshift.org/latest/architecture/networking/sdn.html
.. _Better or Best license: https://f5.com/products/how-to-buy/simplified-licensing
.. _F5 Native Integration: https://docs.openshift.org/1.4/architecture/additional_concepts/f5_big_ip.html#architecture-f5-native-integration
.. _Advanced Deployment Strategies: https://docs.openshift.com/container-platform/3.6/dev_guide/deployments/advanced_deployment_strategies.html
.. _Blue-Green Deployment: https://docs.openshift.com/container-platform/3.6/dev_guide/deployments/advanced_deployment_strategies.html#advanced-deployment-strategies-blue-green-deployments
.. _A/B Deployment: https://docs.openshift.com/container-platform/3.6/dev_guide/deployments/advanced_deployment_strategies.html#advanced-deployment-a-b-deployment
.. _alternate backends: https://docs.openshift.com/container-platform/3.7/architecture/networking/routes.html#alternateBackends
