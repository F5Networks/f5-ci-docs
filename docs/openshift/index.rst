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
```````````````````````

The prerequisites below are in addition to the F5 Integration for Kubernetes' :ref:`general prerequisites <k8s-prereqs>`.

- Integration with `OpenShift SDN`_ requires a BIG-IP `Better or Best license`_, or a Good license with the optional SDN services added.


Initial Setup
`````````````

#. :ref:`Add your BIG-IP device to the OpenShift cluster network <bigip-openshift-setup>`.
#. :ref:`Create an OpenShift service account <k8s-openshift-serviceaccount>` with the following role permissions and assign it to the |kctlr|.

   ========================== =================================================
   Resources                  Actions
   ========================== =================================================
   - endpoints                get, list, watch
   - ingresses
   - namespaces
   - nodes
   - services
   -------------------------- -------------------------------------------------
   - configmaps               get, list, watch, update, create, patch
   - ingresses/status
   - events
   ========================== =================================================

See :ref:`How to add your BIG-IP device to an OpenShift Cluster <bigip-openshift-setup>` for complete setup instructions.

.. _openshift-origin-node-health:

Node Health
-----------

The |kctlr| runs in :ref:`cluster mode` in OpenShift.
Because the BIG-IP device is part of the OpenShift cluster network, it has visibility into the health of individual Pods, as well as Nodes.
This means that the BIG-IP device knows when Nodes/Pods are down and routes traffic to others that it knows are available.

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
