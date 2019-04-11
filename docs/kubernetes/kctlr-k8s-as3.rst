:product: Container Ingress Services
:type: concept

.. _kctlr-k8s-as3-use:

Container Ingress Services and AS3 Extension integration
========================================================

You can use Container Ingress Services to expose services to external traffic using Application Services 3 (AS3) Extension declarations.

Prerequisites
`````````````
To use AS3 declarations with Container Ingress Services, ensure you meet the following requirements:

- The BIG-IP system is running software version 12.1.x or higher.
- The BIG-IP sytem has AS3 Extension version 3.10.3 or higher installed.
- A BIG-IP system user account with the Administrator role.

Limitations
```````````
The |kctlr| has the following AS3 Extension limitations:

- AS3 pool class declarations support only one load balancing pool.
- Container Ingress Services (CIS) supports only one AS3 ConfigMap instance.
- AS3 does not support moving BIG-IP nodes to new partitions.
- Static ARP entries remain after deleting an AS3 ConfigMap.

CIS service discovery
`````````````````````

Both AS3 and CIS can dynamically discover and update load balancing pool members using service discovery. However, when using CIS to process AS3 declarations, CIS performs the service discovery. When using CIS, you must map each pool definition in the AS3 template to a Kubernetes Service resource using a label. To create this mapping, add the following labels to your Kubernetes Service:

.. code-block:: yaml

  cis.f5.com/as3-tenant: <tenant_name>
  cis.f5.com/as3-app: <application_name>
  cis.f5.com/as3-pool: <pool_name>

.. important::

  Multiple Kubernetes Service resources tagged with same set of labels will cause a CIS error, and service discovery failure.

An example Kubernetes Service using labels:

.. code-block:: yaml

  kind: Service
  apiVersion: v1
  metadata:
    name: stark-blog-frontend
    labels:
      cis.f5.com/as3-tenant: "stark"
      cis.f5.com/as3-app: "blog"
      cis.f5.com/as3-pool: "web_pool"
  spec:
    selector:
      run: web-service
      ports:
      - protocol: TCP
        port: 80
        targetPort: 80

The Kubernetes deployment created by the Kubernetes Service:

.. code-block:: yaml

  kind: Service
  apiVersion: v1
  metadata:
    name: stark-blog-frontend
    labels:
      cis.f5.com/as3-tenant: "stark"
      cis.f5.com/as3-app: "blog"
      cis.f5.com/as3-pool: "web_pool"
  spec:
    selector:
      run: web-service
    ports:
      - protocol: TCP
        port: 80
        targetPort: 80
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: nginx-web-service
  spec:
    selector:
      matchLabels:
        run: web-service
    replicas: 3
    template:
      metadata:
        labels:
          run: web-service
      spec:
        containers:
          - name: nginx
            image: nginx


Service discovery and controller mode
`````````````````````````````````````
CIS service discovery adds IP address and service port information to AS3 declarations differently, depending on the controller mode.

+--------------------------------------------------------------------------------------------------------------------------------+
| Controller mode  | Configuration update                                                                                        |
+==================+=============================================================================================================+
| Cluster IP       |  - Add the Kubernetes Service endpoint IP Addresses to the :code:`ServiceAddresses` section.                |
|                  |  - Use the Kubernetes Service endpoint service ports to replace entries in the :code:`ServicePort` section. |
+------------------+-------------------------------------------------------------------------------------------------------------+
| Node Port        | - Add the Kubernetes cluster node IP addresses to the ServerAddresses section.                              |
|                  | - Use the Kubernetes cluster NodePort ports to replace entries in the ServicePort section.                  | 
|                  |  Ensure you expose Kubernetes services as type Nodeport.                                                    |
+------------------+-------------------------------------------------------------------------------------------------------------+

AS3 declaration processing 
``````````````````````````

To processes AS3 declarations using CIS, set the f5type label to virtual-server and the as3 label to the true. 

.. note::
  Ensure the value of the as3 label is a string value true, not the boolean True.

AS3 declaration processing involves these four steps:

1. Submit the AS3 template inside the configMap resource and deploy it in Kubernetes. 

.. code-block:: yaml

  kind: ConfigMap
  apiVersion: v1
  metadata:
    name: as3-template
    namespace: default
    labels:
      f5type: virtual-server
      as3: "true"
  data:
    template: |
      { 
            <YOUR AS3 DECLARATION>
      }

2. The AS3 configmap becomes available for processing, CIS performs service discovery as described in the Service Discovery section.

3. Service discovery completes, and CIS modifies the AS3 template to append discovered endpoints. CIS only modify these two values in the AS3 template:

   - serverAddresses array. If this array is not empty, CIS treats will not overwrite the entries. 

   - servicePort value

4. CIS posts the generated AS3 declaration to the BIG-IP system.

Parameters
``````````
+-----------------+---------+----------+-------------------+-----------------------------------------+-----------------+
| Parameter       | Type    | Required | Default           | Description                             | Allowed Values  |
+=================+=========+==========+===================+=========================================+=================+
| as3-validation  | Boolean | Optional | True              | Tells CIS whether or not to             |                 |
|                 |         |          |                   | perform AS3 validation.                 | "true", "false" |  
+-----------------+---------+----------+-------------------+-----------------------------------------+-----------------+
| insecure        | Boolean | Optional | False             | Tells CIS whether or not to             |                 |
|                 |         |          |                   | allow communication with BIG-IP using   |                 |
|                 |         |          |                   | invalid SSL certificates.               | "true", "false" |
+-----------------+---------+----------+-------------------+-----------------------------------------+-----------------+

AS3 Resources
`````````````
- See the `AS3 User Guide`_ to get started using F5 AS3 Extension declarations.
- See the `AS3 Reference Guide`_ for an overview and list of F5 AS3 Extension declarations.

AS3 Examples
````````````
- :fonticon:`fa fa-download` :download:`f5-as3-template-example.yaml </kubernetes/config_examples/f5-as3-template-example.yaml>`
- :fonticon:`fa fa-download` :download:`f5-as3-template-example.yaml </kubernetes/config_examples/f5-as3-declaration-example.yaml>`

