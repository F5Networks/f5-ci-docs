:product: Container Ingress Services :type: concept

.. _kctlr-k8s-as3-use-1:

Container Ingress Services and AS3 Extension - HTTP use case
=============================================================

This use case demonstrates how you can use Container Ingress Services (CIS) and Application Services 3 (AS3) Extenstion declarations to:

- Expose an HTTP Kubernetes Service.
- Deploy a simple HTTP application 
- Configure the BIG-IP system to load balance across the application (PODs).

.. rubric:: **HTTP application**

.. image:: /_static/media/cis_as3_service.png
   :scale: 70%

Prerequisites
`````````````
To complete this use case, ensure you have:

- A functioning Kubernetes cluster.
- A BIG-IP system running software version 12.1.x or higher.
- AS3 Extension version 3.10 or higher installed on BIG-IP.
- A BIG-IP system user account with the Administrator role.

I. Create a Kuberenetes Service
```````````````````````````````
Kubernetes Services expose applications to external clients. This example creates a new Kubernetes Service named :code:`f5-hello-world-web`. The Service uses labels to identify the application as :code:`f5-hello-world-web`, the Tenent (BIG-IP partition) as :code:`AS3,` and the BIG-IP pool as :code:`web_pool`:

.. note::

   If you need additional detail on labels, refer to . 

.. code-block:: YAML

   apiVersion: v1
   kind: Service
   metadata:
     name: f5-hello-world-web
      namespace: kube-system
      labels:
       app: f5-hello-world-web
       cis.f5.com/as3-tenant: AS3
       cis.f5.com/as3-app: A1
       cis.f5.com/as3-pool: web_pool
   spec:
     ports:
     - name: f5-hello-world-web
       port: 8080
       protocol: TCP
       targetPort: 8080
     type: NodePort
     selector:
       app: f5-hello-world-web

- :fonticon:`fa fa-download` :download:`f5-hello-world-web-service.yaml </kubernetes/config_examples/f5-hello-world-web-service.yaml>`

Create the Kubernetes Service using kubectl apply:

.. parsed-literal::

   kubectl apply -f <service name>.yaml -n <name space>

For example:

.. parsed-literal::

   kubectl apply -f f5-hello-world-web-service.yaml 


II. Create a Deployment
```````````````````````
Kubernetes Deployments are used to create Kubernetes PODs, or applications distributed across multiple hosts. The following example creates a new application named :code:`f5-hellow-world-web`, using the f5-hello-world Docker container. The deployment uses the :code:`f5-hellow-world-web` label to identify the application. 

.. code-block:: YAML

   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: f5-hello-world-web
     namespace: kube-system
   spec:
     replicas: 2
     selector:
       matchLabels:
         app: f5-hello-world-web
     template:
       metadata:
         labels:
           app: f5-hello-world-web
       spec:
         containers:
         - env:
           - name: service_name
             value: f5-hello-world-web
             image: f5devcentral/f5-hello-world:latest
           imagePullPolicy: Always
           name: f5-hello-world-web
           ports:
           - containerPort: 8080
             protocol: TCP

- :fonticon:`fa fa-download` :download:`f5-hello-world-web-deployment.yaml </kubernetes/config_examples/f5-hello-world-web-deployment.yaml>`

Create the Deployment using kubectl apply:

.. parsed-literal::

   kubectl apply -f <service name>.yaml -n <name space>

For example:

.. parsed-literal::

   kubectl apply -f f5-hello-world-service.yaml 

III. Create an AS3 ConfigMap
````````````````````````````
AS3 ConfigMaps create the BIG-IP system configuration used to load balance across the PODs. This example creates a ConfigMap named :code:`f5-as3-declaration`. CIS uses the AS3 ConfigMap to create a virtual server, and use Service Discovery, a load balancing pool named :code:`web_pool` using POD members as endpoints. The new configuration is created in the AS3 Tenant (BIG-IP partition) :code:`AS3`.

.. code-block:: YAML

   kind: ConfigMap
   apiVersion: v1
   metadata:
     name: f5-as3-declaration
     namespace: kube-system
     labels:
       f5type: virtual-server
       as3: "true"
   data:
     template: |
       {
           "class": "AS3",
           "declaration": {
               "class": "ADC",
               "schemaVersion": "3.10.0",
               "id": "urn:uuid:33045210-3ab8-4636-9b2a-c98d22ab915d",
               "label": "http",
               "remark": "A1 example",
               "AS3": {
                   "class": "Tenant",
                   "A1": {
                       "class": "Application",
                       "template": "http",
                       "serviceMain": {
                           "class": "Service_HTTP",
                           "virtualAddresses": [
                               "10.192.75.101"
                           ],
                           "pool": "web_pool"
                       },
                       "web_pool": {
                           "class": "Pool",
                           "monitors": [
                               "http"
                           ],
                           "members": [
                               {
                                   "servicePort": 8080,
                                   "serverAddresses": []
                               }
                           ]
                       }
                   }
               }
           }
       }

- :fonticon:`fa fa-download` :download:`f5-hello-world-as3-configmap.yaml </kubernetes/config_examples/f5-hello-world-as3-configmap.yaml>`

Deploy the ConfigMap using kubectl apply:

.. parsed-literal::

   kubectl create -f <configMap name>.yaml -n <name space>

For example:

.. parsed-literal::

   kubectl create -f f5-hello-world-as3-configmap.yaml
