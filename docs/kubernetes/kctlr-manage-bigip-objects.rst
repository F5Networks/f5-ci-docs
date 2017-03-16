.. _kctlr-manage-bigip-objects:

Manage BIG-IP objects with |kctlr-long|
=======================================

The |kctlr-long| watches the Kubernetes API for :ref:`F5 resources <k8s-f5-resources>` and creates/modifies BIG-IP objects accordingly. F5 resources contain the configurations |kctlr| should apply to the BIG-IP objects.

.. _f5-resource-blob:

.. rubric:: Example:

The example F5 resource JSON blob shown below tells  |kctlr| to create one (1) virtual server - with one (1) health monitor and one (1) pool - in the kubernetes partition on the BIG-IP.

.. literalinclude:: /_static/config_examples/f5-resource-vs-example.json
    :caption: Example F5 Resource definition

.. tip::

    You can also :ref:`deploy iApps with the k8s-bigip-ctlr <kctlr-deploy-iapps>`.

.. _kctlr-create-vs:

Create a virtual server for a Kubernetes Service
------------------------------------------------

.. note::

    All BIG-IP objects created by |kctlr| use the preface ``[namespace]_[configmap-name]``. For example, ``default_k8s.vs_173.16.2.2:80``.

#. Create a `ConfigMap`_ and include the F5 resource JSON blob in the "data" section.

    .. literalinclude:: /_static/config_examples/f5-resource-vs-example.configmap.yaml
        :linenos:

    .. tip::

        You can download the example ConfigMap file below and modify it to suit your environment.

        :download:`f5-resource-vs-example.configmap.yaml </_static/config_examples/f5-resource-vs-example.configmap.yaml>`

#. Upload the ConfigMap to Kubernetes.

    .. code-block:: bash

        ubuntu@k8s-master:~$ kubectl create -f f5-resource-vs-example.configmap.yaml --namespace=<service-namespace>
        configmap "k8s.vs" created

#. Verify creation of the virtual server on the BIG-IP.

    .. code-block:: shell

        root@(bigip)(cfg-sync Standalone)(Active)(/kubernetes)(tmos)# show ltm virtual
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


Update a virtual server
-----------------------

Use ``kubectl edit`` to open the ConfigMap in your default text editor and make your desired changes.

.. note:: Kubernetes disregards any breaking or syntactically-incorrect changes.


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
                  "serviceName": "frontend",
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
          schema: f5schemadb://bigip-virtual-server_v0.1.2.json
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

You can also verify the changes on the BIG-IP using ``tmsh`` or the configuration utility.

.. code-block:: shell

    root@(bigip)(cfg-sync Standalone)(Active)(/kubernetes)(tmos)# show ltm virtual


Delete a virtual server
-----------------------

#. Remove the ConfigMap from the Kubernetes API server to delete the corresponding virtual server from the BIG-IP.

    .. code-block:: bash

        ubuntu@k8s-master:~$ kubectl delete configmap k8vs
        configmap "k8s.vs" deleted

#. Verify the virtual server no longer exists.

    .. code-block:: bash

        root@(bigip)(cfg-sync Standalone)(Active)(/kubernetes)(tmos)# show ltm virtual
        root@(bigip)(cfg-sync Standalone)(Active)(/kubernetes)(tmos)#



Connectivity for down or replaced Services
------------------------------------------

If you need to take down a `Kubernetes Service`_  temporarily, leave the F5 Resource ConfigMap in place. This ensures continued connectivity to the BIG-IP when the Service comes back up (or when a new Service with the same name deploys).

If you take down a Service and want to remove the corresponding BIG-IP objects, delete its F5 Resource ConfigMap.


.. _k8s-config-bigip-health-monitor:

Configure a BIG-IP health monitor
`````````````````````````````````

The |kctlr-long| is not aware of node health when running in the default ``nodeport`` mode. We strongly recommend configuring BIG-IP health monitors for Kubernetes Services to help ensure that |kctlr| doesn't send traffic to unhealthy nodes.

#. Edit the Service definition.

    .. code-block:: bash

        ubuntu@k8s-master:~$ kubectl edit configmap k8s.vs

        # Please edit the object below.
        # ...


#. Define the desired health monitor in the ``backend`` section of the F5 resource.

    .. literalinclude:: /_static/config_examples/f5-resource-vs-example.configmap.yaml
        :linenos:
        :emphasize-lines: 22-26

#. Verify that the health monitor exists on the BIG-IP via the configuration utility.


