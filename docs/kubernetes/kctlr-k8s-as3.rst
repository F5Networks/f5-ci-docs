:product: Container Ingress Services
:type: concept

.. _kctlr-k8s-as3-int:

Container Ingress Services and AS3 Extension integration
========================================================

You can use Container Ingress Services (CIS) to expose services to external traffic using Application Services 3 (AS3) Extension declarations.

Prerequisites
`````````````
To use AS3 declarations with CIS, ensure you meet the following requirements:

- The BIG-IP system is running software version 12.1.x or higher.
- The BIG-IP sytem has AS3 Extension version 3.10 or higher installed.
- A BIG-IP system user account with the Administrator role.

Limitations
```````````
CIS has the following AS3 Extension limitations:

- AS3 pool class declarations support only one load balancing pool.
- CIS supports only one AS3 ConfigMap instance.
- AS3 does not support moving BIG-IP nodes to new partitions.
- Static ARP entries remain after deleting an AS3 ConfigMap.

CIS service discovery
`````````````````````

CIS can dynamically discover and update load balancing pool members using service discovery. CIS maps each pool definition in the AS3 template to a Kubernetes Service resource using a label. To create this mapping, add the following labels to your Kubernetes Service:

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

.. _kctlr-k8s-as3-discovery:

Service discovery and controller mode
`````````````````````````````````````
CIS service discovery adds IP address and service port information to AS3 declarations differently, depending on the controller mode.

+----------------------------------------------------------------------------------------------------------------------------------------+
| Controller mode  | Configuration update                                                                                                |
+==================+=====================================================================================================================+
| Cluster IP       |  - Add the Kubernetes :code:`Service endpoint IP Addresses` to the :code:`ServiceAddresses` section.                |
|                  |  - Use the Kubernetes :code:`Service endpoint service ports` to replace entries in the :code:`ServicePort` section. |
+------------------+---------------------------------------------------------------------------------------------------------------------+
| Node Port        | - Add the Kubernetes :code:`cluster node IP addresses` to the :code:`ServerAddresses` section.                      |
|                  | - Use the Kubernetes :code:`cluster NodePort ports` to replace entries in the :code:`ServicePort` section.          | 
|                  | Ensure you expose Kubernetes services as type :code:`Nodeport`.                                                     |
+------------------+---------------------------------------------------------------------------------------------------------------------+

.. _kctlr-k8s-as3-processing:

AS3 declaration processing 
``````````````````````````

To process an AS3 declaration using CIS, set the :code:`f5type` label to :code:`virtual-server` and the :code:`as3` label to the :code:`true`. 

.. note::
  Ensure the value of the as3 label is a string value true, not the boolean True.

Exampe AS3 declaration configured for CIS processing:

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


AS3 declaration processing involves these four steps:

1. You submit the AS3 template inside the configMap resource and deploy it in Kubernetes. 

2. After the AS3 configMap becomes available for processing, CIS performs service discovery as described in the Service Discovery section.

3. After Service discovery completes, CIS modifies the AS3 template to append discovered endpoints. CIS only modify these two values in the AS3 template:

   - :code:`serverAddresses` array. If this array is not empty, CIS treats will not overwrite the entries. 

   - :code:`servicePort` value.

4. CIS posts the generated AS3 declaration to the BIG-IP system and begins processing traffic.

.. _kctlr-k8s-as3-params:

Parameters
``````````
+-----------------+---------+----------+-------------------+-------------------------------------------+-----------------+
| Parameter       | Type    | Required | Default           | Description                               | Allowed Values  |
+=================+=========+==========+===================+===========================================+=================+
| as3-validation  | Boolean | Optional | True              | Tells CIS whether or not to               | "true", "false" |
|                 |         |          |                   | perform AS3 validation.                   |                 |
+-----------------+---------+----------+-------------------+-------------------------------------------+-----------------+
| insecure        | Boolean | Optional | False             | Tells CIS whether or not to               | "true", "false" |
|                 |         |          |                   | allow communication with BIG-IP using     |                 |
|                 |         |          |                   | invalid SSL certificates.                 |                 |
|                 |         |          |                   | For more info, refer to the next section; |                 |
|                 |         |          |                   | CIS and SSL certificate validation.       |                 |
+-----------------+---------+----------+-------------------+-------------------------------------------+-----------------+

.. _kctlr-k8s-as3-ssl:

CIS and SSL certificate validation
``````````````````````````````````
CIS validates SSL certificates using the root CA certifictes bundled with the base Debian/Redhat image. Because of this, CIS will fail to validate a BIG-IP system's self-signed SSL certificate, and log an error message similar to the following in the AS3 log file:

.. code-block:: bash

  [ERROR] [as3_log] REST call error: Post https://10.10.10.100/mgmt/shared/appsvcs/declare: x509: cannot validate certificate for 10.10.10.100

To avoid this issues, include the ``insecure=true`` parameter in your configuration when executing a Kubernetes deployment.

.. _kctlr-k8s-as3-resource:

AS3 Resources
`````````````
- See the `F5 AS3 User Guide`_ to get started using F5 AS3 Extension declarations.
- See the `F5 AS3 Reference Guide`_ for an overview and list of F5 AS3 Extension declarations.

.. _kctlr-k8s-as3-example:

AS3 Examples
````````````
- :fonticon:`fa fa-download` :download:`f5-as3-template-example.yaml </kubernetes/config_examples/f5-as3-template-example.yaml>`
- :fonticon:`fa fa-download` :download:`f5-as3-declaration-example.yaml </kubernetes/config_examples/f5-as3-declaration-example.yaml>`

