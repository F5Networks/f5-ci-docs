:product: BIG-IP Controller for Kubernetes
:type: concept

.. _kctlr-k8s-as3-use:

BIG-IP Controller and AS3 Extension integration
===============================================

You can use the |kctlr| to expose services to external traffic using Application Services 3 (AS3) Extension declarations.

Prerequisites
`````````````
To use AS3 declarations with BIG-IP Controller, ensure you meet the following requirements:

- The BIG-IP system is running software version 12.1.x or higher.
- The BIG-IP sytem has AS3 Extension version 3.10.3 or higher installed.
- A BIG-IP system user account with the Administrator role.

Limitations
```````````
The |kctlr| has the following AS3 Extension limitations:

- AS3 pool class declarations support only one load balancing pool.
- The BIG-IP Contoller supports only one AS3 ConfigMap instance.
- AS3 does not support moving BIG-IP nodes to new partitions.
- Static ARP entries remain after deleting an AS3 ConfigMap.

Parameters
``````````
+-----------------+---------+----------+-------------------+-----------------------------------------+-----------------+
| Parameter       | Type    | Required | Default           | Description                             | Allowed Values  |
+=================+=========+==========+===================+=========================================+=================+
| as3-validation  | Boolean | Optional | True              | Tells the controller whether or not to  |                 |
|                 |         |          |                   | perform AS3 validation.                 | "true", "false" |  
+-----------------+---------+----------+-------------------+-----------------------------------------+-----------------+
| insecure        | Boolean | Optional | False             | Tells the contrroler whether or not to  |                 |
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

