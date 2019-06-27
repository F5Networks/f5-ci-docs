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
The first step will be to deploy a labeled Kubernetes Service. The following example labels identify this POD as f5-hello-world-web, the Tenent (partition) on BIG-IP as AS3, and the pool on BIG-IP as web_pool:

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

Deploy the Service using kubectl apply.

   .. parsed-literal::

      kubectl apply -f <service name>.yaml -n <name space>

   For example:

   .. parsed-literal::

      kubectl apply -f f5-hello-world-web-service.yaml -n k8s


II. Create a Deployment
```````````````````````
Kubernetes Pod represent one or more containers that you create using a Kubernetes Deployment. To link specific Services with Deployments, ensure the same app labels are applied to each.

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

.. parsed-literal::

   kubectl apply -f <service name>.yaml -n <name space>

For example:

.. parsed-literal::

   kubectl apply -f f5-hello-world-service.yaml -n k8s

Example https://raw.githubusercontent.com/mdditt2000/kubernetes/dev/cis-1-9/deployment/f5-hello-world-deployment.yaml

III. Create an AS3 ConfigMap
````````````````````````````
AS3 ConfigMaps represent the BIG-IP system configuration used to load balance across the PODs. Service discovery will create a load balancing pool of PODs based on labels.

This example will deploy a simple http application on BIG-IP

Example https://github.com/mdditt2000/kubernetes/blob/dev/cis-1-9/A1/f5-as3-configmap.yaml

.. parsed-literal::

   kubectl create -f <configMap name>.yaml -n <name space>

For example:

.. parsed-literal::

   kubectl create -f f5-as3-configmap.yaml -n k8s

AS3 Examples
````````````
- :fonticon:`fa fa-download` :download:`f5-as3-template-example.yaml </kubernetes/config_examples/f5-as3-template-example.yaml>`
- :fonticon:`fa fa-download` :download:`f5-as3-declaration-example.yaml </kubernetes/config_examples/f5-as3-declaration-example.yaml>`
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
---
