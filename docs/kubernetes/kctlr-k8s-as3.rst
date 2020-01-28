:product: Container Ingress Services
:type: concept

.. _kctlr-k8s-as3:

CIS and AS3 Extension integration
=================================

You can use Container Ingress Services (CIS) and Application Services 3 (AS3) Extensions as a BIG-IP orchestration platform.

Prerequisites
-------------

To use AS3 Extensions with CIS, ensure you meet the following requirements:

- The BIG-IP system is running software version 12.1.x or higher.
- The BIG-IP sytem has AS3 Extension version 3.10 or higher installed.
- A BIG-IP system user account with the Administrator role.

Limitations
-----------

CIS has the following AS3 Extension limitations:

- AS3 pool class declarations support only one load balancing pool.
- CIS supports only one AS3 ConfigMap instance.
- AS3 does not support moving BIG-IP nodes to new partitions.

Declaritive API
---------------

AS3 Extensions use a declarative API, meaning AS3 Extension declarations describe the desired configuration state of a BIG-IP system. When using AS3 Extenstions, CIS sends declaration files using a single Rest API call. 

CIS service discovery
---------------------

CIS can dynamically discover, and update the BIG-IP system's load balancing pool members using Service Discovery. CIS maps each pool definition in the AS3 template to a Kubernetes Service resource using Labels. To create this mapping, add the following labels to your Kubernetes Service:

+---------------------------------+-------------------------------------------------------------------+
| Label                           | Description                                                       |
+=================================+===================================================================+
| app: <string>                   | | This label associates the service with the deployment.          |
|                                 | | *Important: This label must be included, and resolve in DNS.*   |            
+---------------------------------+-------------------------------------------------------------------+
| cis.f5.com/as3-tenant: <string> | | The name of the **partition** in your AS3 declaration.          |
|                                 | | *Important: The string must not use a hyphen (-) character.*    |
+---------------------------------+-------------------------------------------------------------------+
| cis.f5.com/as3-app: <string>    | The name of the **class** in your AS3 declaration.                |
+---------------------------------+-------------------------------------------------------------------+
| cis.f5.com/as3-pool: <string>   | The name of the **pool** in your AS3 Declaration.                 |
+---------------------------------+-------------------------------------------------------------------+

.. important::

   Multiple Kubernetes Service resources tagged with same set of labels will cause a CIS error, and service discovery failure.

.. rubric:: **Service label overview**

.. image:: /_static/media/k8s_service_labels.png
   :scale: 70%

Click image for larger view.

.. rubric:: **Example Deployment**

.. code-block:: yaml

  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: f5-hello-world
    namespace: kube-system
  spec:
    replicas: 2
    selector:
      matchLabels:
        app: f5-hello-world
    template:
      metadata:
        labels:
          app: f5-hello-world
      spec:
        containers:
        - env:
          - name: service_name
            value: f5-hello-world
          image: f5devcentral/f5-hello-world:latest
          imagePullPolicy: Always
          name: f5-hello-world
          ports:
          - containerPort: 80
            protocol: TCP

.. rubric:: **Example Service**

.. code-block:: yaml

  apiVersion: v1
  kind: Service
  metadata:
    name: f5-hello-world
    namespace: kube-system
    labels:
      app: f5-hello-world
      cis.f5.com/as3-tenant: AS3
      cis.f5.com/as3-app: f5-hello-world
      cis.f5.com/as3-pool: web_pool
  spec:
    ports:
    - name: f5-hello-world
      port: 80
      protocol: TCP
      targetPort: 80
    type: NodePort
    selector:
      app: f5-hello-world


Enabling AS3 orchestration
--------------------------

You can use these steps to enable AS3 for BIG-IP orchestration:

1. Include the **--agent=as3** option in your Deployment's argument section. For example:
  
   **Note:** In this example, `k8s-bigip-ctlr`_ will create partition **myParition_AS3** to store LTM objects such as pools, and virtual servers. FDB, and Static ARP entries are stored in **myPartition**. These partitions should not be managed manually.

.. code-block:: YAML
   :emphasize-lines: 7

   args: [
         "--bigip-username=$(BIGIP_USERNAME)",
         "--bigip-password=$(BIGIP_PASSWORD)",
         "--bigip-url=10.10.10.10",
         "--bigip-partition=myPartition",
         "--pool-member-type=cluster",
         "--agent=as3"
         ]

2. Start the Controller: 

.. parsed-literal::

   kubectl apply -f f5-k8s-bigip-ctlr.yaml


.. _kctlr-k8s-as3-discovery:

Service discovery and controller mode
-------------------------------------

CIS service discovery adds IP address and service port information to AS3 declarations differently, depending on the controller mode.

+------------------+---------------------------------------------------------------------------------------------------------------------+
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
--------------------------

To process an AS3 declaration using CIS, set the :code:`f5type` label to :code:`virtual-server` and the :code:`as3` label to the :code:`true`. 

.. note::
  CIS uses :code:`gojsonschema` to validate AS3 data. If the data structure does not conform with the schema, an error will be logged. Also, ensure the the AS3 label value is the string :code:`true`, and not the boolean :code:`True`.

.. rubric:: **Example AS3 ConfigMap**

.. code-block:: yaml

  kind: ConfigMap
  apiVersion: v1
  metadata:
    name: as3-template
    namespace: kube-system
    labels:
      f5type: virtual-server
      as3: "true"
  data:
    template: |
      { 
            <YOUR AS3 DECLARATION>
      }


AS3 declaration processing involves these four steps:

1. Submit the AS3 template inside a configMap, and deploy it in Kubernetes. 

2. After the AS3 configMap becomes available for processing, CIS performs service discovery as described in the Service Discovery section.

3. After Service discovery completes, CIS modifies the AS3 template, and appends the discovered endpoints. CIS only modify these two values in the AS3 template:

   - :code:`serverAddresses` array. If this array is not empty, CIS treats will not overwrite the entries. 

   - :code:`servicePort` value.

4. CIS posts the generated AS3 declaration to the BIG-IP system to begin processing traffic.

.. rubric:: **CIS and AS3 deployment workflow**

.. image:: /_static/media/container_ingress_services.png

.. _kctlr-k8s-as3-params:

Parameters
----------
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

.. _kctlr-k8s-use-cases:

Application use case
--------------------

You can use the HTTP application use case to better understand how CIS, and AS3 integrate.

- :ref:`HTTP application <kctlr-k8s-as3-use-1>`

.. _kctlr-k8s-delete-map:

Deleting CIS configmaps
-----------------------

Because CIS and AS3 use a Declarative API, the BIG-IP system configuration is not removed after you delete a configmap. To remove the BIG-IP system configuration objects created by an AS3 declaration, you must deploy a blank configmap, and restart the controller. Refer to `Deleting CIS AS3 configmaps <kctlr-as3-delete-configmap.html>`_.

.. _kctlr-k8s-as3-ssl:

SSL certificate validation
--------------------------

CIS validates SSL certificates using the root CA certifictes bundled with the base Debian/Redhat image. Because of this, CIS will fail to validate a BIG-IP system's self-signed SSL certificate, and log an error message similar to the following in the AS3 log file:

.. code-block:: bash

   [ERROR] [as3_log] REST call error: Post https://10.10.10.100/mgmt/shared/appsvcs/declare: x509: cannot validate certificate for 10.10.10.100

To avoid this issue, you can perform one of the following:

- Bypass certificate validation by including the ``--insecure=true`` option in your configuration when executing a Kubernetes deployment.
- Establish trust with the BIG-IP system by `Updating the CIS trusted certificate store <kctlr-as3-cert-trust.html>`_. 

.. _kctlr-k8s-as3-partition:

Administrative partitions 
-------------------------

CIS requires a unique administrative partition on the BIG-IP system to manage the ARP entries of discovered services. Ensure that you set the ``--bigip-partition=<name>`` parameter to a unique value when executing a Kubernetes deployment.

.. important::
  This unique BIG-IP partition does not allow the use of the AS3 ``Tenant`` class.

.. _kctlr-k8s-tenants:

AS3 tenants
-----------

AS3 tenants are BIG-IP administrative partitions used to group configurations that support specific AS3 applications. An AS3 application may support a network-based business application or system. AS3 tenants may also include resources shared by applications in other tenants.


.. _kctlr-k8s-as3-resource:

AS3 Resources
-------------

- See the `F5 AS3 User Guide`_ to get started using F5 AS3 Extension declarations.
- See the `F5 AS3 Reference Guide`_ for an overview and list of F5 AS3 Extension declarations.

.. _kctlr-k8s-as3-example:

AS3 Examples
------------
- :fonticon:`fa fa-download` :download:`f5-as3-template-example.yaml </kubernetes/config_examples/f5-as3-template-example.yaml>`
- :fonticon:`fa fa-download` :download:`f5-as3-declaration-example.yaml </kubernetes/config_examples/f5-as3-declaration-example.yaml>`

