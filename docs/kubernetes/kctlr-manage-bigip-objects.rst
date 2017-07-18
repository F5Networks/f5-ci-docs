.. _kctlr-manage-bigip-objects:

Manage BIG-IP LTM objects in Kubernetes
=======================================

.. sidebar:: Docs test matrix

   We tested this documentation with:

   - ``kubernetes-v1.4.8_coreos.0``
   - ``k8s-bigip-ctlr v1.0.0``


The |kctlr-long| watches the Kubernetes API for `Services`_ with associated :ref:`F5 resources <k8s-f5-resources>` and creates/modifies BIG-IP Local Traffic Manager (LTM) objects accordingly.
F5 resources contain the settings |kctlr| should apply to the BIG-IP LTM objects.

.. _f5-resource-blob:

.. rubric:: Example:

The example virtual server F5 resource JSON blob shown below tells |kctlr| to create one (1) virtual server - with one (1) health monitor and one (1) pool - in the kubernetes partition on the BIG-IP device.

.. literalinclude:: /_static/config_examples/f5-resource-vs-example.json
   :caption: Example F5 Resource definition

.. tip::

   You can also :ref:`deploy iApps with the k8s-bigip-ctlr <kctlr-deploy-iapps>`.

.. _kctlr-create-vs:

Create a BIG-IP front-end virtual server for a Kubernetes Service
-----------------------------------------------------------------

.. note::

   The |kctlr| prefaces all BIG-IP virtual server objects with ``[namespace]_[configmap-name]``.
   For example, ``default_k8s.vs_173.16.2.2:80``, where ``default`` is the Kubernetes namespace and ``k8s.vs`` is the ConfigMap name.

#. Create a `ConfigMap`_ with the virtual server F5 resource JSON blob in the "data" section.

   .. literalinclude:: /_static/config_examples/f5-resource-vs-example.configmap.yaml
      :linenos:

   :fonticon:`fa fa-download` :download:`f5-resource-vs-example.configmap.yaml </_static/config_examples/f5-resource-vs-example.configmap.yaml>`

#. Upload the ConfigMap to Kubernetes.

   .. code-block:: bash

      ubuntu@k8s-master:~$ kubectl create -f f5-resource-vs-example.configmap.yaml --namespace=<service-namespace>
      configmap "k8s.vs" created

#. Verify creation of the BIG-IP virtual server.

   .. admonition:: TMSH

      ::

         admin@(bigip)(cfg-sync Standalone)(Active)(/kubernetes)$ tmsh show ltm virtual
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

.. _kctlr-update-vs:

Update a BIG-IP virtual server
------------------------------

Use ``kubectl edit`` to open the ConfigMap in your default text editor and make your desired changes.

.. hint::

   Kubernetes disregards any breaking or syntactically-incorrect changes.


.. code-block:: bash
   :linenos:

   ubuntu@k8s-master:~$ kubectl edit configmap k8s.vs

   # Please edit the object below.
   # ...
   #
   apiVersion: v1
   data:
     data: |
       {
         "virtualServer": {
           "backend": {
             "servicePort": 3000,
             "serviceName": "myService",
             "healthMonitors": [{
               "interval": 30,
               "protocol": "http",
               "send": "GET",
               "timeout": 86400
             }]
           },
           "frontend": {
             "virtualAddress": {
               "port": 80,
               "bindAddr": "173.16.2.2"
             },
             "partition": "kubernetes",
             "balance": "round-robin",
             "mode": "http"
           }
         }
       }
     # If you're running v1.0, use schema v0.1.2
     schema: f5schemadb://bigip-virtual-server_v0.1.3.json
   kind: ConfigMap
   metadata:
     creationTimestamp: 2017-02-14T17:24:34Z
     labels:
       f5type: virtual-server
     name: k8s.vs
     namespace: default


After you save your changes and exit, you can verify the changes using ``kubectl get``.

.. code-block:: bash

   ubuntu@k8s-master:~$ kubectl get configmap k8s.vs -o yaml

You can also verify the changes on your BIG-IP device using ``tmsh`` or the configuration utility.

.. admonition:: TMSH

   tmsh show ltm virtual

.. _kctlr-delete-objects:

Delete BIG-IP LTM objects
-------------------------

#. Remove the ConfigMap from the Kubernetes API server to delete the corresponding BIG-IP LTM objects.

   .. code-block:: bash

      ubuntu@k8s-master:~$ kubectl delete configmap k8s.vs
      configmap "k8s.vs" deleted

#. Verify the BIG-IP LTM objects no longer exist.

   .. admonition:: TMSH

      admin@(bigip)(cfg-sync Standalone)(Active)(/kubernetes)$ tmsh show ltm virtual
      admin@(bigip)(cfg-sync Standalone)(Active)(/kubernetes)$


.. _k8s-config-bigip-health-monitor:

Create a BIG-IP health monitor for a Kubernetes Service
-------------------------------------------------------

When running in the default ``nodeport`` mode, the |kctlr-long| is not aware of Kubernetes node health.
Configure BIG-IP LTM health monitors for Kubernetes Services to help ensure that |kctlr| doesn't send traffic to unhealthy nodes.

#. Edit the Service definition.

   .. code-block:: bash

      ubuntu@k8s-master:~$ kubectl edit configmap k8s.vs

      # Please edit the object below.
      # ...


#. Define the desired health monitor in the ``backend`` section of the F5 resource.

   .. literalinclude:: /_static/config_examples/f5-resource-vs-example.configmap.yaml
      :linenos:

#. Use the BIG-IP configuration utility to verify that the health monitor exists.

   :menuselection:`Local Traffic --> Monitors`

.. _kctlr-ipam:

Use IPAM to assign IP addresses to BIG-IP LTM virtual servers
-------------------------------------------------------------

.. include:: /_static/reuse/k8s-version-added-1_1.rst


The |kctlr-long| has a built-in hook that allows you to integrate an IPAM system using a custom plugin.
The basic elements required are:

#. Add an F5 resource ConfigMap set up for :ref:`unattached pools <kctlr-pool-only>` to the Service definition.
   The |kctlr-long| creates a BIG-IP pool that isn't attached to a virtual server.

#. Use your IPAM system to `annotate the ConfigMap`_.
   The annotation should follow the format ``virtual-server.f5.com/ip=<ipaddress>``.

   The annotation tells the |kctlr-long| to create a BIG-IP virtual server with the designated IP address and attach the pool to it.

.. _kctlr-downed-services:

Connectivity for down or replaced Services
------------------------------------------

If you need to take down a `Kubernetes Service`_  temporarily and want to keep the associated BIG-IP LTM objects, leave the corresponding F5 Resource ConfigMap in place.
The |kctlr| will continue to manage the associated BIG-IP LTM objects when the Service comes back up.
If you deploy a new Service with the same name as the one you took down, the |kctlr| associates the existing BIG-IP LTM objects with the new Service.

If you take down a Service and want to remove the corresponding BIG-IP LTM objects, :ref:`delete the F5 Resource ConfigMap <kctlr-delete-objects>`.

.. _kctlr-pool-only:

Manage pools without virtual servers
------------------------------------

.. include:: /_static/reuse/k8s-version-added-1_1.rst

The |kctlr-long| can create and manage BIG-IP Local Traffic Manager (LTM) pools that aren't attached to a front-end BIG-IP virtual server (also referred to as "unattached pools").
When you create a pool without a virtual server, the |kctlr-long| applies the following naming convention to the pool members: ``<namespace>_<configmap-name>``.
For example, ``default_k8s.pool_only``.

.. important::

   Your BIG-IP device must have a virtual server with an `iRule`_, or a `local traffic policy`_, that can direct traffic to the unattached pool.
   After creating an unattached pool, add its member(s) to the iRule or traffic policy to ensure proper handling of client connections to your back-end applications.

.. _kctlr-create-unattached-pool:

Create a pool without a virtual server
``````````````````````````````````````

#. Create an :ref:`F5 resource <k8s-f5-resources>` `ConfigMap`_, omitting the ``bindAddr`` field from the ``virtualAddress`` section.

   .. include:: /_static/reuse/k8s-schema-note.rst

   .. literalinclude:: /_static/config_examples/f5-resource-pool-only-example.configmap.yaml
        :linenos:

   :fonticon:`fa fa-download` :download:`f5-resource-pool-only-example.configmap.yaml </_static/config_examples/f5-resource-pool-only-example.configmap.yaml>`

#. Upload the ConfigMap to Kubernetes.

   .. code-block:: bash

      ubuntu@k8s-master:~$ kubectl create -f f5-resource-pool-only-example.configmap.yaml --namespace=<service-namespace>
      configmap "k8s.pool_only" created


.. _kctlr-attach-pool-vs:

Attach a pool to a virtual server
`````````````````````````````````

#. Add the desired ``bindAddr`` (in other words, the virtual server IP address) to the F5 Resource ConfigMap using ``kubectl edit``.

   .. code-block:: bash
      :linenos:

      ubuntu@k8s-master:~$ kubectl edit configmap k8s.pool_only

      # Please edit the object below.
      # ...
      #
      apiVersion: v1
      data:
        data: |
          {
            "virtualServer": {
              "backend": {
                "servicePort": 3000,
                "serviceName": "myService",
                "healthMonitors": [{
                  "interval": 30,
                  "protocol": "http",
                  "send": "GET",
                  "timeout": 86400
                }]
              },
              "frontend": {
                "virtualAddress": {
                  "port": 80,
                  "bindAddr": "1.2.3.4" \\ add this line, using a valid IP address
                },
                "partition": "kubernetes",
                "balance": "round-robin",
                "mode": "http"
              }
            }
          }
        schema: f5schemadb://bigip-virtual-server_v0.1.3.json
      kind: ConfigMap
      metadata:
        creationTimestamp: 2017-02-14T17:24:34Z
        labels:
          f5type: virtual-server
        name: k8s.pool_only
        namespace: default

#. Verify the changes using ``kubectl get``.

   .. code-block:: bash

      ubuntu@k8s-master:~$ kubectl get configmap k8s.pool_only -o yaml

#. Use the BIG-IP configuration utility to verify the pool attached to the virtual server.

   :menuselection:`Local Traffic --> Virtual Servers`

.. tip::

   You can :ref:`use an IPAM system <kctlr-ipam>` to populate the ``bindAddr`` field automatically.


.. _kctlr-delete-unattached-pool:

Delete an "unattached" pool
```````````````````````````

#. Remove the ConfigMap from the Kubernetes API server.

   .. code-block:: bash

      ubuntu@k8s-master:~$ kubectl delete configmap k8.pool_only
      configmap "k8s.pool_only" deleted

#. Use the BIG-IP configuration utility to verify deletion of the pool.

   :menuselection:`Local Traffic --> Pools`

.. _kctlr-detach-pool:

Detach a pool from a virtual server
```````````````````````````````````

If you want to delete a front-end BIG-IP virtual server, but keep its associated pool(s)/pool member(s):

#. Remove the ``bindAddr`` field from the virtual server F5 resource ConfigMap.

   .. code-block:: bash
      :linenos:

      ubuntu@k8s-master:~$ kubectl edit configmap k8s.vs

      # Please edit the object below.
      # ...
      #
      apiVersion: v1
      data:
        data: |
          {
            "virtualServer": {
              "backend": {
                "servicePort": 3000,
                "serviceName": "myService",
                "healthMonitors": [{
                  "interval": 30,
                  "protocol": "http",
                  "send": "GET",
                  "timeout": 86400
                }]
              },
              "frontend": {
                "virtualAddress": {
                  "port": 80,
                  "bindAddr": "1.2.3.4" \\ remove this line
                },
                "partition": "kubernetes",
                "balance": "round-robin",
                "mode": "http"
              }
            }
          }
        schema: f5schemadb://bigip-virtual-server_v0.1.3.json
      kind: ConfigMap
      metadata:
        creationTimestamp: 2017-02-14T17:24:34Z
        labels:
          f5type: virtual-server
        name: k8s.vs
        namespace: default

#. Verify the changes using ``kubectl get``.

   .. code-block:: bash

      ubuntu@k8s-master:~$ kubectl get configmap k8s.vs -o yaml

#. Use the BIG-IP configuration utility to verify the virtual server no longer exists.

   :menuselection:`Local Traffic --> Virtual Servers`

.. _local traffic policy: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/bigip-local-traffic-policies-getting-started-13-0-0/1.html
.. _iRule: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/bigip-system-irules-concepts-11-6-0/1.html
.. _annotate the ConfigMap: https://kubernetes.io/docs/concepts/overview/working-with-objects/annotations/

