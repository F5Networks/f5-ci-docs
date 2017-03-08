.. _kctlr-manage-bigip-objects:

Manage BIG-IP objects with |kctlr-long|
=======================================

The |kctlr-long| watches the Kubernetes API for :ref:`F5 resources <k8s-f5-resources>` and creates/modifies BIG-IP objects accordingly.

F5 resources contain the `configuration parameters <tbd>`_ |kctlr| should apply to the BIG-IP objects.

.. _f5-resource-blob:

.. rubric:: Example:

The example F5 resource JSON blob shown below tells  |kctlr| to create one (1) virtual server - with one (1) health monitor and one (1) pool - in the kubernetes partition on the BIG-IP.

.. literalinclude:: /_static/config_examples/f5-resource-vs-example.json
    :caption: Example F5 Resource definition

.. tip::

    You can also :ref:`deploy iApps with the k8s-bigip-ctlr <kctlr-deploy-iapps>`.

.. _kctlr-create-vs:

Create a virtual server for a Kubernetes Service
````````````````````````````````````````````````

.. note::

    All BIG-IP objects created by |kctlr| will be prefaced with ``[namespace]_[configmap-name]``. For example, ``default_k8s.vs``.

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

        root@(host-172)(cfg-sync Standalone)(Active)(/kubernetes)(tmos)# show ltm virtual
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
```````````````````````

Use ``kubectl edit`` to open the ConfigMap in your default text editor.

    .. code-block:: bash

        ubuntu@k8s-master:~$ kubectl edit configmap k8s.vs

        # Please edit the object below. Lines beginning with a '#' will be ignored,
        # and an empty file will abort the edit. If an error occurs while saving this file will be
        # reopened with the relevant failures.
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


.. note:: Kubernetes disregards any breaking or syntactically-incorrect changes.


Delete a virtual server
```````````````````````

#. Remove the ConfigMap from the Kubernetes API server to delete the corresponding virtual server from the BIG-IP.

    .. code-block:: bash

        ubuntu@k8s-master:~$ kubectl delete configmap k8vs
        configmap "k8s.vs" deleted

#. Verify the virtual server no longer exists.

    .. code-block:: bash

        root@(host-172)(cfg-sync Standalone)(Active)(/kubernetes)(tmos)# show ltm virtual
        root@(host-172)(cfg-sync Standalone)(Active)(/kubernetes)(tmos)#



Taking down or replacing Services
`````````````````````````````````

If you need to take down a `Kubernetes Service`_  temporarily, leave the F5 Resource ConfigMap in place. This ensures continued connectivity to the BIG-IP when the Service comes back up (or when a new Service with the same name deploys).

If you take down a Service and want to remove the corresponding BIG-IP objects, delete its F5 Resource ConfigMap.


