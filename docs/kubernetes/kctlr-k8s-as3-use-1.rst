:product: Container Ingress Services :type: concept

.. _kctlr-k8s-as3-use-1:

Container Ingress Services and AS3 Extensions - Use case 1
==========================================================

This use case demonstrates how you can use Container Ingress Services (CIS) and Application Services 3 (AS3) Extenstion declarations to:

- Expose an HTTP or HTTPs Kubernetes Service with labels.
- Use the labels for Service Discovery.
- Configure the BIG-IP system to load balance across PODs.

Prerequisites
`````````````
To complete this use case, ensure you have:

- A functioning Kubernetes cluster.
- A BIG-IP system running software version 12.1.x or higher.
- AS3 Extension version 3.10 or higher installed on BIG-IP.
- A BIG-IP system user account with the Administrator role.

I. Deploy a labeled Kuberenetes Service
```````````````````````````````````````
The first step will be to deploy a labeled Kubernetes Service. This example creates a Kubernetes Service named f5-hello-world-web. The Services uses labels to identify the application as f5-hellow-world-web, the Tenent (partition) on BIG-IP as AS3, and a pool name on BIG-IP as web_pool:

.. note::

   When you deploy an AS3 ConfigMap, CIS will perform Service Discovery, and map new BIG-IP pool members to Kubernetes Pods using these labels. 

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

Create the Kubernetes Service using kubectl apply.

.. parsed-literal::

   kubectl apply -f <service name>.yaml -n <name space>

For example:

.. parsed-literal::

   kubectl apply -f f5-hello-world-web-service.yaml -n k8s


II. Create a Deployment
```````````````````````
A Kubernetes Pod represent one or more containers that you create using a Kubernetes Deployment. The following example creates a new application using named f5-hellow-world-web, using the f5-hello-world container. The deployment uses the f5-hellow-world-web label to identify the application. 

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

   kubectl apply -f f5-hello-world-service.yaml -n k8s

Example https://raw.githubusercontent.com/mdditt2000/kubernetes/dev/cis-1-9/deployment/f5-hello-world-deployment.yaml



III. Create an AS3 ConfigMap
````````````````````````````
AS3 ConfigMaps represent the BIG-IP system configuration used to load balance across the PODs. CIS will use Service discovery to create a load balancing pool with all of the application's PODs as members.  This example will create a simple HTTP application the the BIG-IP system.

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

   kubectl create -f f5-as3-configmap.yaml -n k8s
