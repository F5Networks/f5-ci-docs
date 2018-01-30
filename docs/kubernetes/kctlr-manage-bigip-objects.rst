:product: BIG-IP Controller for Kubernetes
:type: tutorial

.. _kctlr-manage-bigip-objects:

Manage Your BIG-IP Virtual Servers
==================================

.. tip:: You can use the |kctlr| to attach the BIG-IP virtual servers and pools to Services in Kubernetes and OpenShift environments.

You can use the |kctlr-long| and OpenShift to :ref:`kctlr-per-svc-vs` using :ref:`F5 resource ConfigMaps <k8s-f5-resources>`.
This document provides instructions for managing the virtual server(s) associated with your Service(s).

.. _kctlr-update-vs:

Edit an existing virtual server
-------------------------------

Services
````````

The basic steps listed below apply to any changes you may want to make to a virtual server associated with a Service, Ingress, or Route.

.. _kctlr upload resource api server:

- Make your desired changes to the resource YAML or JSON file.

- Upload the updated file to the Kubernetes or OpenShift API server using the commands shown below.

  .. rubric:: Kubernetes

  .. include:: /_static/reuse/kubectl-apply.rst

  .. rubric:: OpenShift

  .. include:: /_static/reuse/oc-apply.rst


Ingresses and Routes
````````````````````

In addition to the steps above, you can use the :command:`annotate` command to add/change the |kctlr| Annotations for an Ingress or Route resource.

For example, to change the load balancing mode to :code:`least-connections-member`:

.. rubric:: Kubernetes
.. parsed-literal::

   kubectl annotate ingress **myIngress** virtual-server.f5.com/balance=least-connections-member [--namespace=**myNamespace**]

.. rubric:: OpenShift
.. parsed-literal::

   oc annotate route **myRoute** virtual-server.f5.com/balance=least-connections-member [--namespace=**myProject**]

.. _k8s-config-bigip-health-monitor:

.. _k8s-service healthmonitor:

Add/Edit health monitors
------------------------

#. Define/edit the desired health monitor(s).
#. Add the health monitor(s) to the :code:`backend` section of the :ref:`F5 Resource <k8s-f5-resources>` ConfigMap.
#. :ref:`Update the API server <kctlr upload resource api server>`.

.. literalinclude:: /kubernetes/config_examples/f5-resource-vs-example.configmap.yaml
   :caption: Example F5 resource with health monitor
   :emphasize-lines: 16-22

:fonticon:`fa fa-download` :download:`f5-resource-vs-example.configmap.yaml </kubernetes/config_examples/f5-resource-vs-example.configmap.yaml>`

.. seealso::

   - :ref:`Health monitors for Ingress resources <add health monitor to ingress>`
   - :ref:`Health monitors for Route resources <add health monitor to route>`

.. _kctlr-delete-objects:

Delete a virtual server
-----------------------

When you delete any Kubernetes or OpenShift resource, the |kctlr| will delete all of the BIG-IP objects associated with the resource.

For example:

#. Delete the F5 Resource for myService from the API server.

   .. parsed-literal::

      kubectl delete configmap **myConfigMap** [--namespace=**<service_namespace>**]     \\ kubernetes
      oc delete configmap **myConfigMap** [--namespace=**<service_project>**]          \\ openshift

#. Verify the BIG-IP objects no longer exist.

   .. parsed-literal::

      admin@(bigip)(cfg-sync Standalone)(Active)(/Common) cd **my-partition**
      admin@(bigip)(cfg-sync Standalone)(Active)(/my-partition) **tmsh**
      admin@(bigip)(cfg-sync Standalone)(Active)(/my-partition)(tmos)$ **show ltm virtual**
      admin@(bigip)(cfg-sync Standalone)(Active)(/my-partition)(tmos)$

.. seealso::

   - :ref:`Delete virtual servers for Ingress resources <delete vs ingress>`
   - :ref:`Delete virtual servers for Route resources <delete vs route>`

.. _kctlr-pool-only:

Create unattached pools
-----------------------

.. include:: /_static/reuse/k8s-version-added-1_1.rst

You can use the |kctlr| to create and manage BIG-IP pools that aren't attached to a front-end virtual server (:dfn:`unattached pools`).

.. important::

   The primary use case for unattached pools is to allow the use of an IPAM system to allocate IP addresses for your virtual servers.

   If you create unattached pools and are not using IPAM, the BIG-IP system must have another way to route traffic to the pools (such as `iRules <https://devcentral.f5.com/irules>`_ or `local traffic policies`_).

.. _kctlr-create-unattached-pool:

Create an unattached pool
`````````````````````````

#. Create an :ref:`F5 resource <k8s-f5-resources>` **without the** :code:`bindAddr` **property**.

   .. literalinclude:: /kubernetes/config_examples/f5-resource-pool-only-example.configmap.yaml
      :linenos:
      :emphasize-lines: 25-27

   :fonticon:`fa fa-download` :download:`f5-resource-pool-only-example.configmap.yaml </kubernetes/config_examples/f5-resource-pool-only-example.configmap.yaml>`

#. :ref:`Update the Kubernetes API server <kctlr upload resource api server>`.

#. :ref:`kctlr-ipam` **--OR--**

   Use the BIG-IP configuration utility or TMSH to add the pool members to an iRule or traffic policy with the correct routing rules for your application.

.. _kctlr-ipam:

Attach pools to virtual servers using IPAM
``````````````````````````````````````````

.. include:: /_static/reuse/k8s-version-added-1_1.rst

Set up your IPAM system to annotate the F5 resource ConfigMap with the allocated IP address. Use the Annotation shown below.

:code:`virtual-server.f5.com/ip=<ip_address>`

When the |kctlr| discovers the annotated resource, it:

- creates a new BIG-IP virtual server with the designated IP address, and
- attaches the existing pool to the virtual server.

.. _kctlr-attach-pool-vs:

.. note::

   The Controller doesn't support attaching an unattached pool to an existing BIG-IP virtual server.

   - If you try to add the pool to an existing virtual that already has pools attached, you'll see errors.
   - If you try to use an existing virtual server residing in the /Common partition, you'll see conflict errors because the Controller will attempt to create a new virtual server in its managed partition.
   - If you manually create a virtual server in the managed partition, the Controller will delete it.

.. _kctlr-detach-pool:

Detach a pool from a virtual server
```````````````````````````````````

When you detach a pool from a virtual server, the |kctlr| will delete the virtual server but keep the pool(s)/pool member(s).

#. Remove the ``bindAddr`` field from the virtual server F5 resource ConfigMap.
#. :ref:`Update the API server <kctlr upload resource api server>`.
#. Verify the changes using :command:`kubectl get` (Kubernetes) or :command:`oc get` (OpenShift).

.. _kctlr-delete-unattached-pool:

Delete an unattached pool
`````````````````````````

The steps for deleting an unattached pool are the same as for :ref:`deleting a virtual server <kctlr-delete-objects>`.

.. _verify changes bigip services:

Verify changes on the BIG-IP system
-----------------------------------

.. include:: /_static/reuse/verify-bigip-objects.rst

.. _Annotation: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/
