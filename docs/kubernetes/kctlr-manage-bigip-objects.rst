.. index::
   single: Kubernetes; BIG-IP; virtual server
   single: OpenShift; BIG-IP; virtual server

.. sidebar:: Docs test matrix

   Documentation manually tested with:

   - kubernetes-v1.6.4_ubuntu-16.4.2
   - kubernetes-v1.4.8_coreos.0
   - ``k8s-bigip-ctlr`` v1.0.0-1.3.0

.. _kctlr-manage-bigip-objects:

Manage BIG-IP virtual servers - Kubernetes/OpenShift
====================================================

The |kctlr-long| and OpenShift watches the Kubernetes/OpenShift API for `Services`_ with associated :ref:`F5 resources <k8s-f5-resources>` and creates/modifies BIG-IP Local Traffic Manager (LTM) objects accordingly.
F5 resources provide the settings you want the |kctlr| to apply when creating objects on the BIG-IP system.

.. tip::

   The |kctlr| can also :ref:`deploy iApps <kctlr-deploy-iapps>`.


.. _kctlr-create-vs:

Create a BIG-IP front-end virtual server for a Service
------------------------------------------------------

.. _k8s-vs-naming:

.. note::

   The |kctlr| prefaces all BIG-IP virtual server objects with :code:`[namespace]_[resource-name]`.

   For example, if :code:`default` is the namespace and ``k8s.vs`` is the ConfigMap name, the object preface is :code:`default_k8s.vs_173.16.2.2:80`.


Take the steps below to create a new BIG-IP virtual server for a Service.

.. _kctlr configmap example:

#. Create a ConfigMap containing the :ref:`virtual server F5 resource JSON blob <f5-resource-blob>`.

   The example below creates one HTTP virtual server and one HTTPS virtual server for a Service, with health monitors defined for each.

   .. literalinclude:: /kubernetes/config_examples/f5-resource-vs-example.configmap.yaml
     :linenos:

   :fonticon:`fa fa-download` :download:`f5-resource-vs-example.configmap.yaml </kubernetes/config_examples/f5-resource-vs-example.configmap.yaml>`

#. Upload the ConfigMap to the Kubernetes/OpenShift API server. Be sure to provide the namespace the Service runs in (if something other than :code:`default`).

   .. code-block:: console
      :caption: kubectl

      kubectl create -f f5-resource-vs-example.configmap.yaml [--namespace=<service-namespace>]
      configmap "http.vs" created
      configmap "https.vs" created

   .. code-block:: console
      :caption: openshift cli

      oc create -f f5-resource-vs-example.configmap.yaml [--namespace=<service-namespace>]
      configmap "http.vs" created
      configmap "https.vs" create

#. Verify creation of the BIG-IP virtual server(s).

   .. code-block:: console

      admin@(bigip)(cfg-sync Standalone)(Active)(/kubernetes)(tmos)show ltm virtual
      ------------------------------------------------------------------
      Ltm::Virtual Server: frontend_173.16.2.2_80
      ------------------------------------------------------------------
      Status
        Availability     : available
        State            : enabled
        Reason           : The virtual server is available
        CMP              : enabled
        CMP Mode         : all-cpus
        Destination      : 173.16.2.2:80
      ...
      Ltm::Virtual Server: frontend_173.16.2.2_443
      ------------------------------------------------------------------
      Status
        Availability     : available
        State            : enabled
        Reason           : The virtual server is available
        CMP              : enabled
        CMP Mode         : all-cpus
        Destination      : 173.16.2.2:443
      ...


.. _kctlr-update-vs:

Update a Service's BIG-IP virtual server
----------------------------------------

The same basic steps apply to any changes you may want to make to an existing Service's virtual server's configurations.

#. Edit the ConfigMap and make your desired changes.
#. Upload your changes to the Kubernetes/OpenShift API server using :command:`kubectl apply` or :command:`oc apply`.

   .. code-block:: console
      :caption: kubectl

      kubectl apply -f <myConfigMap.yaml> [--namespace <service-namespace>]

   .. code-block:: console
      :caption: openshift cli

      oc apply -f <myConfigMap.yaml> [--namespace <service-namespace>]

.. _k8s-config-bigip-health-monitor:

Add health monitors
```````````````````

Take the steps below to add a BIG-IP health monitor(s) to an existing virtual server F5 Resource in standard Kubernetes or OpenShift.

#. Add the health monitor(s) to the backend section of the virtual server :ref:`F5 resource ConfigMap <k8s-f5-resources>`.

   .. literalinclude:: /kubernetes/config_examples/f5-resource-vs-example.configmap.yaml
      :linenos:
      :lines: 1-41
      :emphasize-lines: 24-29

#. Update the Kubernetes/OpenShift API server. Be sure to provide the namespace the Service runs in (if not :code:`default`).

   .. code-block:: console
      :caption: kubectl

      kubectl replace -f <myConfigMap.yaml> [--namespace <service-namespace>]

   .. code-block:: console
      :caption: openshift cli

      oc replace -f <myConfigMap.yaml> [--namespace <service-namespace>]

#. Use the BIG-IP management console to verify the Service's virtual server has an attached health monitor.

   .. code-block:: console

      admin@(bigip)(cfg-sync Standalone)(Active)(/kubernetes)(tmos)$ show ltm virtual <virtual-name>



.. _kctlr-delete-objects:

Delete BIG-IP virtual servers
-----------------------------

#. Delete the ConfigMap(s) from the Kubernetes/OpenShift API server.

   The Controller then deletes the corresponding BIG-IP virtual server(s) and its associated objects (pools, pool members, and health monitors).

   .. code-block:: console
      :caption: kubectl

      kubectl delete configmap http.vs
      configmap "http.vs" deleted

   .. code-block:: console
      :caption: openshift cli

      oc delete configmap http.vs
      configmap "http.vs" deleted

#. Verify the BIG-IP LTM objects associated with the Service no longer exist.

   .. code-block:: console

      admin@(bigip)(cfg-sync Standalone)(Active)(/kubernetes)(tmos)$ show ltm virtual frontend_173.16.2.2_80



.. _kctlr-downed-services:

Virtual servers for down or replaced Services
---------------------------------------------

- If you need to take a Service down temporarily and want to keep the associated BIG-IP objects, leave the F5 Resource ConfigMap in place. The |kctlr| will continue to manage the associated BIG-IP LTM objects when the Service comes back up.

- If you deploy a new Service with the same name as one you took down, the |kctlr| associates the existing BIG-IP LTM objects with the new Service.

- If you take down a Service and want to remove the corresponding BIG-IP LTM objects, :ref:`delete the F5 Resource ConfigMap <kctlr-delete-objects>`.

.. _kctlr-ipam:

Assign IP addresses to BIG-IP virtual servers using IPAM
--------------------------------------------------------

.. include:: /_static/reuse/k8s-version-added-1_1.rst

You can use an IPAM system to assign IP addresses to BIG-IP virtual servers managed by the |kctlr|. To do so, take the steps below:

#. :ref:`kctlr-create-unattached-pool` for the Service on the BIG-IP system.

#. Use your IPAM system to add the IP address to the ConfigMap.

   .. tip::

      F5 recommends using an `Annotation`_ to add the IP address allocated by the IPAM system to the F5 Resource ConfigMap for the unattached pool.

      The annotation should follow the format

      :code:`virtual-server.f5.com/ip=<ipaddress>`.

      This tells the |kctlr-long| to create a BIG-IP virtual server, assign the designated IP address to it, and attach the pool to the virtual server.

.. _kctlr-pool-only:

Pools without virtual servers
-----------------------------

.. include:: /_static/reuse/k8s-version-added-1_1.rst

The |kctlr-long| can create and manage BIG-IP Local Traffic Manager (LTM) pools that aren't attached to a front-end BIG-IP virtual server (also referred to as "unattached pools"). The |kctlr-long| applies the following naming convention when creating pool members for unattached pools:

``<namespace>_<configmap-name>``.

   For example, ``default_http.pool_only``.

.. important::

   Before creating unattached pools, make sure the BIG-IP system has another wat to route traffic to the Service(s), such as an `iRule`_ or a `local traffic policy`_. After creating an unattached pool for a Service, use the BIG-IP config utility to add the pool members to the iRule or traffic policy. This ensures proper handling of client connections to your back-end applications.

.. _kctlr-create-unattached-pool:

Create an unattached pool
`````````````````````````

#. Create an :ref:`F5 resource <k8s-f5-resources>` `ConfigMap`_, but leave out the ``bindAddr`` field.

   .. literalinclude:: /kubernetes/config_examples/f5-resource-pool-only-example.configmap.yaml
      :linenos:
      :emphasize-lines: 25-27

   :fonticon:`fa fa-download` :download:`f5-resource-pool-only-example.configmap.yaml </kubernetes/config_examples/f5-resource-pool-only-example.configmap.yaml>`

#. Upload the ConfigMap to the Kubernetes/OpenShift API server.

   .. code-block:: console
      :caption: kubectl

      kubectl create -f f5-resource-pool-only-example.configmap.yaml [--namespace=<service-namespace>]
      configmap "http.pool_only" created

   .. code-block:: console
      :caption: openshift cli

      oc create -f f5-resource-pool-only-example.configmap.yaml [--namespace=<service-namespace>]
      configmap "http.pool_only" created

.. important::

   Don't forget to attach the pool to the iRule or traffic policy on the BIG-IP system that knows how to route traffic for the Service.

.. _kctlr-attach-pool-vs:

Attach a pool to an existing virtual server
```````````````````````````````````````````

#. Add the desired :code:`bindAddr` to the F5 virtual server resource definition.

   .. tip::

      You can configure your IPAM system to do this automatically. For example:

      :code:`kubectl annotate configmap http.pool_only virtual-server.f5.com/ip=1.2.3.4`

#. Verify the changes using :command:`kubectl get` or :command:`oc get`.

   .. code-block:: console

      kubectl get configmap http.pool_only -o yaml \\
      oc get configmap http.pool_only -o yaml

#. Go to :menuselection:`Local Traffic --> Virtual Servers` in the BIG-IP configuration utility to verify the pool attached to the virtual server. (Be sure to look in the correct BIG-IP partition.)


.. _kctlr-delete-unattached-pool:

Delete an "unattached" pool
```````````````````````````

#. Remove the ConfigMap from the Kubernetes/OpenShift API server.

   .. code-block:: console

      kubectl delete configmap http.pool_only
      configmap "http.pool_only" deleted

#. Go to :menuselection:`Local Traffic --> Pools` in the BIG-IP configuration utility to verify deletion of the pool.

.. _kctlr-detach-pool:

Detach a pool from a virtual server
```````````````````````````````````

If you want to delete a front-end BIG-IP virtual server, but keep its associated pool(s)/pool member(s):

#. Remove the ``bindAddr`` field from the virtual server F5 resource ConfigMap.

   .. code-block:: console
      :linenos:
      :emphasize-lines: 18-19

      kubectl edit configmap http.vs [--namespace <service-namespace>] \\
      oc edit configmap http.vs [--namespace <service-namespace>]
      ----
      # Please edit the object below.
      # ...
      #
      apiVersion: v1
      data:
        data: |
          {
            "virtualServer": {
              "backend": {
                ...
                }]
              },
              "frontend": {
                "virtualAddress": {
                  "port": 80,
                  \\ REMOVE THE LINE BELOW
                  "bindAddr": "1.2.3.4"
                },
                "partition": "kubernetes",
                "balance": "round-robin",
                "mode": "http"
              }
            }
          }
        schema: f5schemadb://bigip-virtual-server_v0.1.4.json
      kind: ConfigMap
      metadata:
        creationTimestamp: 2017-02-14T17:24:34Z
        labels:
          f5type: virtual-server
        name: http.vs
        namespace: default

#. Verify the changes using :command:`kubectl get` or :command:`oc get`.

   .. code-block:: console

      kubectl get configmap http.vs -o yaml \\
      oc get configmap http.vs -o yaml

#. Go to :menuselection:`Local Traffic --> Virtual Servers` in the BIG-IP configuration utility to verify the virtual server no longer exists.


.. _local traffic policy: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/bigip-local-traffic-policies-getting-started-13-0-0/1.html
.. _iRule: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/bigip-system-irules-concepts-11-6-0/1.html
.. _Annotation: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/

