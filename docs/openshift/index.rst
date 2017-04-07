.. _openshift-home:

F5 OpenShift Origin Container Integration
=========================================

Overview
--------

Red Hat's `OpenShift Origin`_ is a containerized application platform with a native Kubernetes integration. The |kctlr-long| enables use of a BIG-IP as an edge load balancer, proxying traffic from outside networks to pods inside an OpenShift cluster. OpenShift Origin uses a pod network defined by the `OpenShift SDN`_.

The :ref:`F5 Kubernetes Integration doc <k8s-home>` provides an overview of how the |kctlr-long| works with Kubernetes. Because OpenShift has a native Kubernetes integration, the |kctlr-long| works the same in both environments. The |kctlr-long| does have a few :ref:`OpenShift-specific prerequisites <openshift-origin-prereqs>`, noted below.


.. _openshift-origin-prereqs:

OpenShift Prerequisites
-----------------------

The prerequisites below are in addition to the :ref:`F5 Kubernetes Integration's general prerequisites <k8s-prereqs>`.

#. The |kctlr-long| needs an `OpenShift user account`_ with permission to access nodes, endpoints, services, and configmaps. Specifically, the `Verbs and Resources`_ needed are:

   #. ``[get list] [nodes endpoints services]``
   #. ``[get list update] [configmaps]``

#. You'll need to use the `OpenShift Origin CLI`_, in addition to ``kubectl``, to execute OpenShift-specific commands.
#. To :ref:`integrate your BIG-IP into an OpenShift cluster <bigip-openshift-setup>`, you'll need to :ref:`assign an OpenShift overlay address to the BIG-IP <k8s-openshift-assign-ip>`.

Once you've added the BIG-IP to the OpenShift overlay network, it will have access to all pods in the cluster. You can then use the |kctlr| the same as you would in Kubernetes.

.. _openshift-origin-node-health:

OpenShift Origin Node Health
----------------------------

In OpenShift clusters, the Kubernetes NodeList records status for all nodes registered with the master.

When the |kctlr-long| runs with ``pool-member-type`` set to ``cluster`` -- which integrates the BIG-IP into the OpenShift cluster network -- it watches the NodeList in OpenShift's underlying Kubernetes API server. The |kctlr-long| creates/updates FDB (Forwarding DataBase) entries according to the NodeList. This ensures the |kctlr| only makes VXLAN requests to reported nodes.

As a function of the BIG-IP VXLAN, the BIG-IP only communicates with healthy cluster nodes. BIG-IP does not attempt to route traffic to an unresponsive node, even if the node remains in the NodeList.

Related
-------

.. toctree::
    :glob:

    *
    ../kubernetes/kctlr*
    k8s-bigip-ctlr docs <http://clouddocs.f5.com/products/connectors/k8s-bigip-ctlr/latest>

.. _OpenShift Origin: https://www.openshift.org/
.. _OpenShift user account: https://docs.openshift.org/1.2/admin_guide/manage_users.html
.. _Verbs and Resources: https://docs.openshift.com/enterprise/3.0/admin_guide/manage_authorization_policy.html#viewing-cluster-policy
.. _OpenShift Origin CLI: https://docs.openshift.org/1.2/cli_reference/index.html
.. _OpenShift SDN: https://docs.openshift.org/latest/architecture/additional_concepts/sdn.html

