:product: Container Ingress Services :type: concept

.. _kctlr-k8s-as3-use-1:

Container Ingress Services and AS3 Extension - HTTP use case
=============================================================

This use case demonstrates how you can use Container Ingress Services (CIS) and Application Services 3 (AS3) Extenstion declarations to:

- Deploy a simple HTTP application (Container). 
- Expose the application using a Kubernetes Service.
- Configure the BIG-IP system to load balance across the application (PODs).

.. rubric:: **CIS & AS3 HTTP application**

.. image:: /_static/media/cis_http_as3_service.png
   :scale: 70%

           
           
Prerequisites
`````````````
To complete this use case, ensure you have:

- A functioning Kubernetes cluster.
- A BIG-IP system running software version 12.1.x or higher.
- AS3 Extension version 3.10 or higher installed on BIG-IP.
- A BIG-IP system user account with the Administrator role.

.. important::
   If your BIG-IP system is using a self-signed certificate (the default configuration), include the `--insecure=true` option in your :code:`k8s-bigip-ctlr` deployment. Also, to allow the BIG-IP system to reach containers directly, set the :code:`--pool-member-type=` option to :code:`cluster`.  Your :code:`k8s-bigip-ctlr` deployment should resemble:

.. code-block:: YAML

   args: [
      "--bigip-username=$(BIGIP_USERNAME)",
      "--bigip-password=$(BIGIP_PASSWORD)",
      "--bigip-url=10.10.10.100",
      "--bigip-partition=AS3",
      "--namespace=kube-system",
      "--pool-member-type=cluster",
      "--flannel-name=fl-vxlan",
      "--insecure=true"
         ]

I. Deploy the application 
`````````````````````````
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

II. Expose the application
``````````````````````````
Kubernetes Services expose applications to external clients. This example creates a new Kubernetes Service named :code:`f5-hello-world-web`. The Service uses labels to identify the application as :code:`f5-hello-world-web`, the Tenent (BIG-IP partition) as :code:`AS3,` and the BIG-IP pool as :code:`web_pool`:

.. note::

   Labels are simple key value pairs used to group a set of configuration objects. In this example, Kubernets creates a Service, and CIS creates pool members by selecting PODS with the f5-hellow-world-web Label. 

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

III. Configure the BIG-IP system
````````````````````````````````
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
