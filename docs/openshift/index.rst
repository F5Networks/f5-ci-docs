:product: BIG-IP Controller for Kubernetes
:type: concept

.. _openshift-home:

F5 Container Connector - OpenShift
==================================

`Current Release Notes <https://clouddocs.f5.com/products/connectors/k8s-bigip-ctlr/latest/RELEASE-NOTES.html>`_

`Releases and Versioning <https://clouddocs.f5networks.net/containers/v2/releases_and_versioning.html#connector-compatibility>`_

The F5 BIG-IP Controller, **k8s-bigip-ctlr**, is a cloud-native connector that can use either Kubernetes or OpenShift as a BIG-IP orchestration platform.

The |kctlr| watches the `Kubernetes API <https://kubernetes.io/docs/api/>`_ for specially formatted resources and updates the BIG-IP system configurations accordingly.

.. image:: /_static/media/cc_solution.png
   :scale: 60%

User Guides
-----------

.. toctree::
   :maxdepth: 1

   Add BIG-IP device to OpenShift Cluster <kctlr-use-bigip-openshift>
   Deploy the BIG-IP Controller <kctlr-openshift-app-install>
   Manage BIG-IP objects <../kubernetes/kctlr-manage-bigip-objects>
   Use AS3 for BIG-IP orchestration <kctlr-use-as3-backend>
   Deploy iApps <../kubernetes/kctlr-deploy-iapp>
   Expose Services using Routes <kctlr-openshift-routes>
   Troubleshooting <../troubleshooting/kubernetes>
   k8s-bigip-ctlr reference documentation <https://clouddocs.f5.com/products/connectors/k8s-bigip-ctlr/latest>

BIG-IP Orchestration
--------------------

When using |kctlr| and Openshift, you can configure the BIG-IP system to process traffic for:

- :ref:`OpenShift Services <kctlr-per-svc-vs>`
- :ref:`OpenShift Routes <kctlr-openshift-routes>`

.. _openshift-origin-prereqs:

.. note::

   Integration with `OpenShift SDN`_  requires a BIG-IP `Better or Best license`_ with SDN services.

.. _openshift-origin-node-health:

Installation
------------

- You can deploy |kctlr| in OpenShift :ref:`using a Deployment <install-kctlr-openshift>`.
- If you use `helm`_ you can use the `F5 Helm Chart`_.

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

- Listen for HTTP route events, and modify routes on BIG-IP. This includes L7 config policies such as wildcard routes, and prefixes.
- Apply Client SSL certificates from Kubernetes/OpenShift Secrets to BIG-IP LTM objects.
- Provide SSL termination using edge, passthrough, or re-encryption modes.

This table shows how |kctlr| and OpenShift perform BIG-IP orchestration:

.. table::

   ============================  ==========================================================
   |kctlr| and OpenShift         BIG-IP configuration
   ============================  ==========================================================
   Create OpenShift Route        - Creates two virtual servers:

                                   - One HTTP
                                   - One HTTPS

                                 - Creates pools and pool members with policies attached.
                                 - Attaches defined policies to virtual servers.
   ----------------------------  ----------------------------------------------------------
   Add/remove endpoints          - Adds/removes pool members correspondng to the
                                   endpoints from the Route's pool.
   ----------------------------  ----------------------------------------------------------
   Delete Routes                 - Removes all BIG-IP objects associated with the Routes:
                                   Virtual servers, pools, and policies.
   ============================  ==========================================================

Advanced Deployments
````````````````````

The |octlr-long| supports these OpenShift `Advanced Deployment Strategies`_:

- `Blue-Green Deployment`_
- `A/B Deployment`_

Advantages over HAProxy
```````````````````````

The |octlr-long| provides a number of advantages over the native HAProxy when working with `alternate backends`_:

- Use any of the BIG-IP load balancing algorithms the Controller supports, not just round robin. [#lb]_
- Weights assigned to a Service in an OpenShift Route, are assigned by |kctlr| to the Service's pool on BIG-IP. Weights are not split across the Service's endpoints, and there are no per-endpoint weight restrictions.

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
