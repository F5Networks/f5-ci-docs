.. _kctlr-pool-only:

Manage BIG-IP LTM pools without virtual servers
===============================================

.. versionadded:: k8s-bigip-ctlr_v1.1.0

The |kctlr-long| can create and manage BIG-IP Local Traffic Manager (LTM) pools that aren't attached to a front-end BIG-IP virtual server (also called, simply, "unattached pools").
To create unattached pools for a `Kubernetes Service`_, leave out the ``virtualServer`` section from your :ref:`F5 resource <k8s-f5-resources>` ConfigMap, or just leave the ``virtualServer.virtualAddress.bindAddr`` field blank.

When you create unattached pools, the |kctlr-long| applies the following naming convention to BIG-IP pool members: ``<namespace>_<configmap-name>``. For example, ``default_k8s.pool_only``.

.. important::

   Your BIG-IP device must have a virtual server with an `iRule`_ or `local traffic policy`_ in effect that can direct traffic to the unattached pool.
   Add the pool member to the iRule or policy to ensure proper handling of client connections to back-end applications.

.. _kctlr-create-unattached-pool:

Create an unattached pool for a Kubernetes Service
--------------------------------------------------

#. Create a `ConfigMap`_ and include the F5 resource JSON blob in the "data" section.

   .. literalinclude:: /_static/config_examples/f5-resource-pool-only-example.configmap.yaml
        :linenos:

   .. tip::

      You can download the example ConfigMap file below and modify it to suit your environment.

      :download:`f5-resource-pool-only-example.configmap.yaml </_static/config_examples/f5-resource-pool-only-example.configmap.yaml>`

#. Upload the ConfigMap to Kubernetes.

   .. code-block:: bash

      ubuntu@k8s-master:~$ kubectl create -f f5-resource-pool-only-example.configmap.yaml --namespace=<service-namespace>
      configmap "k8s.pool_only" created


.. _kctlr-attach-pool-vs:

Attach pools to a BIG-IP virtual server
---------------------------------------

#. Add the desired ``bindAddr`` (in other words, the virtual server IP address) to the F5 Resource ConfigMap using ``kubectl edit``.

   .. code-block:: bash
      :linenos:
      :emphasize-lines: 24

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
        schema: f5schemadb://bigip-virtual-server_v0.1.2.json
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

   You can :ref:`use an IPAM system <kctlr-ipam>` to populate the ``bindAddr`` field and attach a pool to a virtual server automatically.


.. _kctlr-delete-unattached-pool:

Delete an unattached pool
-------------------------

#. Remove the ConfigMap from the Kubernetes API server.

   .. code-block:: bash

      ubuntu@k8s-master:~$ kubectl delete configmap k8.pool_only
      configmap "k8s.pool_only" deleted

#. Use the BIG-IP configuration utility to verify deletion of the pool.

   :menuselection:`Local Traffic --> Pools`

.. _kctlr-detach-pool:

Detach a pool from a virtual server
-----------------------------------

If you want to delete a front-end BIG-IP virtual server and retain its associated pool(s)/pool member(s):

#. Remove the ``bindAddr`` field from the virtual server F5 resource ConfigMap.

   .. code-block:: bash
      :linenos:
      :emphasize-lines: 24

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
        schema: f5schemadb://bigip-virtual-server_v0.1.2.json
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

.. _local traffic policy: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/bigip-local-traffic-policies-getting-started-13-0-0/1.html#guid-a3079c71-8e53-4edf-b568-0a75d646ae44
.. _iRule: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/bigip-system-irules-concepts-11-6-0/1.html#conceptid
