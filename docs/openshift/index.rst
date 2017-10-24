.. _openshift-home:

F5 OpenShift Origin Container Integration
=========================================

Overview
--------

Red Hat's `OpenShift Origin`_ is a containerized application platform with a native Kubernetes integration.
The |kctlr-long| enables use of a BIG-IP device as an edge load balancer, proxying traffic from outside networks to pods inside an OpenShift cluster.
OpenShift Origin uses a pod network defined by the `OpenShift SDN`_.

The :ref:`F5 Integration for Kubernetes overview <k8s-home>` describes how the |kctlr| works with Kubernetes.
Because OpenShift has a native Kubernetes integration, the |kctlr| works essentially the same in both environments.
It does have a few OpenShift-specific prerequisites, noted below.

.. _openshift-origin-prereqs:

Prerequisites
`````````````

The following are in addition to the F5 Integration for Kubernetes' :ref:`general prerequisites <k8s-prereqs>`:

- Integration with `OpenShift SDN`_ requires a BIG-IP `Better or Best license`_ with SDN services.
- The |kctlr| needs a Cluster Role with the appropriate permissions.
  See :ref:`Set up RBAC Authentication for the BIG-IP Controller <k8s-openshift-serviceaccount>` for more information.

.. _kctlr-configure-openshift:

Required configuration parameters for OpenShift clusters
--------------------------------------------------------

Define the following parameters in your Deployment when using |kctlr| in an OpenShift cluster.

=====================   ===================================================
Parameter               Description
=====================   ===================================================
pool-member-type        Must be ``cluster``.
---------------------   ---------------------------------------------------
openshift-sdn-name      TMOS path to the BIG-IP VXLAN tunnel providing
                        access to the Openshift SDN and Pod network;
                        include the partition and vxlan name.

                        Example: ``/Common/openshift_vxlan`` [#tunnel]_
=====================   ===================================================

.. [#tunnel] The VXLAN tunnel does not need to reside in the same partition managed by the |kctlr-long|.

.. _openshift-origin-node-health:

OpenShift Node Health
---------------------

In OpenShift clusters, the Kubernetes NodeList records status for all nodes registered with the master.

When the |kctlr| runs with :code:`pool-member-type` set to :code:`cluster` – which integrates the BIG-IP device into the OpenShift cluster network – it watches the NodeList in OpenShift’s underlying Kubernetes API server.
The |kctlr| creates/updates FDB (Forwarding DataBase) entries for the configured VXLAN tunnel according to the NodeList.
This ensures the |kctlr| only makes VXLAN requests to reported nodes.

As a function of the BIG-IP VXLAN, the BIG-IP device only communicates with healthy cluster nodes.
The BIG-IP device does not attempt to route traffic to an unresponsive node, even if the node remains in the NodeList.

.. _openshift routes:

OpenShift Routes
----------------

.. include:: /_static/reuse/k8s-version-added-1_2.rst

In OpenShift, the |kctlr| can manage BIG-IP objects for routes, in addition to managing virtual servers for Services or Ingress resources.

The |kctlr| operates as follows when configured with `OpenShift route resources`_ :

- runs as non-root, unique user;
- listens for HTTP route events in OpenShift and can create/delete/expire routes on BIG-IP devices
  (including L7 config policies such as wildcard routes, prefixes, etc.);
- can apply client SSL certificates from Kubernetes/OpenShift Secrets to BIG-IP LTM objects;
- can apply existing BIG-IP SSL certificates to BIG-IP LTM objects;
- provides edge, passthrough, and re-encryption modes of SSL termination.

The |kctlr| OpenShift route integration follows what the OpenShift Origin documentation refers to as an `F5 Native Integration`_.
See :ref:`Add your BIG-IP device to an OpenShift Cluster <bigip-openshift-setup>` for deployment instructions.

The |kctlr| integration for OpenShift Routes works as follows:

- User creates a route in OpenShift --> The |kctlr| creates corresponding virtual servers (one HTTP and one HTTPS), pools, and pool members on BIG-IP system with the policies defined for OpenShift.

- User adds/removes endpoints in OpenShift --> The |kctlr| adds/removes pool members from the route's pool on the BIG-IP system.

- User deletes all routes (and associated endpoints) in OpenShift --> The |kctlr| deletes the associated virtual servers, pools, and pool members from the BIG-IP system.

See how to :ref:`expose OpenShift Services to external traffic <kctlr-openshift-routes>` for configuration details.

Related
-------

.. toctree::
   :glob:
   :titlesonly:

   *
   ../kubernetes/kctlr*
   BIG-IP Controller - K8s <http://clouddocs.f5.com/products/connectors/k8s-bigip-ctlr/latest>

.. _OpenShift Origin: https://www.openshift.org/
.. _OpenShift service account: https://docs.openshift.org/latest/admin_guide/service_accounts.html
.. _Authorization Policy: https://docs.openshift.org/latest/admin_guide/manage_authorization_policy.html
.. _OpenShift Origin CLI: https://docs.openshift.org/latest/cli_reference/index.html
.. _OpenShift SDN: https://docs.openshift.org/latest/architecture/networking/sdn.html
.. _Better or Best license: https://f5.com/products/how-to-buy/simplified-licensing
.. _F5 Native Integration: https://docs.openshift.org/1.4/architecture/additional_concepts/f5_big_ip.html#architecture-f5-native-integration
