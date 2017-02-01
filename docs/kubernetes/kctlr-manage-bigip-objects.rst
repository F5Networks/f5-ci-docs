.. _kctlr-manage-bigip-objects:

Manage BIG-IP objects with |kctlr-long|
=======================================

Encode the |kctlr| F5 Resource in a Kubernetes `ConfigMap`_. The |kctlr| :ref:`configuration parameters <tbd>` define the BIG-IP objects.

.. _f5-resource-blob:

The example F5 resource JSON blob shown below tells  |kctlr| to create one (1) virtual server - with one (1) health monitor and one (1) pool - in the kubernetes partition on the BIG-IP.

.. literalinclude:: /_static/config_examples/f5-resource-vs-example.json
    :caption: Example F5 Resource definition


Create a virtual server for a Kubernetes Service
````````````````````````````````````````````````

.. note::

    The below code samples show the |kctlr| proxying the `k8PetStore <https://github.com/kubernetes/kubernetes/tree/release-1.5/examples/k8petstore>`_ app, using the NodePort example.


#. Create a ConfigMap with the encoded data.

    .. tip::

        You can download the example ConfigMap file below and modify it to suit your environment.

        :download:`f5-resource-vs-example.configmap.yaml </_static/config_examples/f5-resource-vs-example.configmap.yaml>`

#. Upload the ConfigMap to Kubernetes.

    .. code-block:: bash

        ubuntu@k8s-master:~$ kubectl create -f f5-resource-vs-example.configmap.yaml --namespace=<service-namespace>
        configmap "k8petstorevs" created

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

        ubuntu@k8s-master:~$ kubectl edit configmap k8vs --namespace=k8petstore

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
          name: k8vs
          namespace: k8petstore


.. note:: Kubernetes disregards any breaking or syntactically-incorrect changes.


Delete a virtual server
```````````````````````

#. Remove the ConfigMap from the Kubernetes API server to delete the corresponding virtual server from the BIG-IP.

    .. code-block:: bash

        ubuntu@k8s-master:~$ kubectl delete configmap k8petstorevs --namespace k8petstore
        configmap "k8petstorevs" deleted

#. Verify the virtual server no longer exists.

    .. code-block:: bash

        root@(host-172)(cfg-sync Standalone)(Active)(/kubernetes)(tmos)# show ltm virtual
        root@(host-172)(cfg-sync Standalone)(Active)(/kubernetes)(tmos)#



Taking down or replacing Services
`````````````````````````````````

If you need to take down a `Kubernetes Service`_  temporarily, leave the F5 Resource ConfigMap in place. This ensures continued connectivity to the BIG-IP when the Service comes back up (or when a new Service with the same name deploys).

If you take down a Service and want to remove the corresponding BIG-IP objects, delete its F5 Resource ConfigMap.


