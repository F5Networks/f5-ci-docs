:product: BIG-IP Controller for Kubernetes
:type: concept

.. _kctlr-as3-use:

F5 Container Ingress Services and AS3 Extension declarations
============================================================

You can use the |kctlr| to expose services to external traffic using Application Services 3 (AS3) Extension declarations.

Version support
```````````````
- BIG-IP version 12.1.x is compatible with AS3 Extenstion versions 3.1.0 or later.
- BIG-IP version 13.0.x is compatible with all AS3 Extension versions after v3.1.0.  

Limitations
```````````
The F5 BIG-IP Controller has the following AS3 Extension limitations:

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
- :fonticon:`fa fa-download` :download:`example-as3-service.yaml </_static/config_examples/example-as3-service.yaml>`

