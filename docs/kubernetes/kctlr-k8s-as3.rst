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
.. note::

  AS3 and CIS can dynamically discover and update load balancing pool members using service discovery. When using CIS to process AS3 configMaps, CIS performs service discovery. 

Each pool definition in an AS3 template should map to a kubernetes Service resource. To establish mapping, add the following labels to your kubernetes service:

.. code-block:: yaml

  cis.f5.com/as3-tenant: <tenant_name>
  cis.f5.com/as3-app: <application_name>
  cis.f5.com/as3-pool: <pool_name>

.. important::

  Multiple Service resources tagged with same set of labels will cause a CIS service discovery to fail.

CIS service discovery updates AS3 template configurations based on the controller mode.

+------------------------------------------------------------------------------------------------------------------------+
| Controller mode  | Configuration update                                                                                |
+==================+=====================================================================================================+
| Cluster IP       |  - Add the Kubernetes Service endpoint IP Addresses to the ServiceAddresses section.                |
|                  |  - Use the Kubernetes Service endpoint service ports to replace entries in the ServicePort section. |
+------------------+-----------------------------------------------------------------------------------------------------+
| Node Port        | - Add the Kubernetes cluster node IP addresses to the ServerAddresses section.                      |
|                  | - Use the Kubernetes cluster NodePort ports to replace entries in the ServicePort section.          | 
|                  |  Ensure you expose Kubernetes services as type Nodeport.                                               |
+------------------+-----------------------------------------------------------------------------------------------------+

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

Example AS3 ConfigMap
`````````````````````
- :fonticon:`fa fa-download` :download:`f5-as3-service-example.yaml </kubernetes/config_examples/f5-as3-service-example.yaml>`

