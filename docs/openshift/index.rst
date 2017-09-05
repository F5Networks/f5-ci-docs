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
It does have a few :ref:`OpenShift-specific prerequisites <openshift-origin-prereqs>`, noted below.

.. _openshift-origin-prereqs:

OpenShift Prerequisites
-----------------------

The prerequisites below are in addition to the F5 Integration for Kubernetes' :ref:`general prerequisites <k8s-prereqs>`.

#. You'll need to use the `OpenShift Origin CLI`_, ``oc``.
#. To :ref:`integrate your BIG-IP device into an OpenShift cluster <bigip-openshift-setup>`, you'll need to :ref:`assign an OpenShift overlay address to the BIG-IP device <k8s-openshift-assign-ip>`.
#. The |kctlr-long| needs an `OpenShift service account`_ with permission to access the following:

   - nodes,
   - endpoints,
   - services,
   - configmaps,
   - ingresses,
   - ingresses/status, and
   - events.

Once you've added the BIG-IP device to the OpenShift overlay network, it will have access to all pods in the cluster.
You can then use the |kctlr| the same as you would in Kubernetes.

.. _openshift-origin-node-health:

OpenShift Origin Node Health
----------------------------

In OpenShift clusters, the Kubernetes NodeList records status for all nodes registered with the master.

When the |kctlr-long| runs with ``pool-member-type`` set to ``cluster`` -- which integrates the BIG-IP device into the OpenShift cluster network -- it watches the NodeList in OpenShift's underlying Kubernetes API server.
The |kctlr| creates/updates FDB (Forwarding DataBase) entries for the configured VXLAN tunnel according to the NodeList.
This ensures the |kctlr| only makes VXLAN requests to reported nodes.

As a function of the BIG-IP VXLAN, the BIG-IP device only communicates with healthy cluster nodes.
The BIG-IP device does not attempt to route traffic to an unresponsive node, even if the node remains in the NodeList.

Related
-------

.. toctree::
   :glob:

   *
   ../kubernetes/kctlr*
   k8s-bigip-ctlr docs <http://clouddocs.f5.com/products/connectors/k8s-bigip-ctlr/latest>

.. _OpenShift Origin: https://www.openshift.org/
.. _OpenShift service account: https://docs.openshift.org/latest/admin_guide/service_accounts.html
.. _Authorization Policy: https://docs.openshift.org/latest/admin_guide/manage_authorization_policy.html
.. _OpenShift Origin CLI: https://docs.openshift.org/latest/cli_reference/index.html
.. _OpenShift SDN: https://docs.openshift.org/latest/architecture/networking/sdn.html
