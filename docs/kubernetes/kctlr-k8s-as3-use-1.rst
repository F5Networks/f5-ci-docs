:product: Container Ingress Services :type: concept

.. _kctlr-k8s-as3-use-1:

Container Ingress Services and AS3 Extensions - Use case 1
==========================================================

This use case demonstrates how Container Ingress Services (CIS) uses Application Services 3 (AS3) Extenstion declarations to:

- Expose an HTTP or HTTPs service within Kubernetes Pods.
- Configure the BIG-IP system to load balance across the Pods.


Prerequisites
`````````````
To complete this use case, ensure you have:

- A functioning Kubernetes cluster.
- A BIG-IP system running software version 12.1.x or higher.
- AS3 Extension version 3.10 or higher installed on BIG-IP.
- A BIG-IP system user account with the Administrator role.

I. Deploy a labeled kuberenetes service
```````````````````````````````````````
CIS can use service discovery to dynamically create load balancing pools on the BIG-IP system. CIS does this by mapping pool members to Kubernetes Pod labels. 

.. rubric:: **Services and Tags**

.. image:: /_static/media/cis_as3_service.png
   :scale: 70%

The first step will be to deploy a labeled Kubernetes Service. Add these labels to your Kubernetes Service. 

.. code-block:: YAML

   labels:
       cis.f5.com/as3-tenant: <tenant name>
       cis.f5.com/as3-app: <application name>
       cis.f5.com/as3-pool: <pool_name>

   For example:

.. code-block:: YAML

   labels:
       cis.f5.com/as3-tenant: AS3
       cis.f5.com/as3-app: A1SSL
       cis.f5.com/as3-pool: secure_ssl_pool

Example https://github.com/mdditt2000/kubernetes/blob/dev/cis-1-9/deployment/f5-hello-world-service.yaml

II. Deploying a ConfigMap with AS3
``````````````````````````````````
Deploying a application called A1 for http. Example of the declaration https://github.com/mdditt2000/kubernetes/blob/dev/cis-1-9/A1/f5-as3-configmap.yaml

**Note:** This is the first application to be deployed by kub. This example will deploy a simple http application on BIG-IP
```
[kube@k8s-1-13-master A1]$ kubectl create -f f5-as3-configmap.yaml
configmap/f5-as3-declaration created
```
### AS3 with HTTPs application
Deploy a second appliction called A2 for https. Example of the declaration https://github.com/mdditt2000/kubernetes/blob/dev/cis-1-9/A2/f5-as3-configmap.yaml
```
[kube@k8s-1-13-master A2]$ kubectl get cm
NAME                 DATA   AGE
f5-as3-declaration   1      24m
```
Note the declaration is already created. To deploy a new service simple apply declaration A1 + A2. AS3 running on BIP-IP will detect and implment the changes
```
[kube@k8s-1-13-master A2]$ kubectl apply -f f5-as3-configmap.yaml
Warning: kubectl apply should be used on resource created by either kubectl create --save-config or kubectl apply
configmap/f5-as3-declaration configured
```


AS3 Examples
````````````
- :fonticon:`fa fa-download` :download:`f5-as3-template-example.yaml </kubernetes/config_examples/f5-as3-template-example.yaml>`
- :fonticon:`fa fa-download` :download:`f5-as3-declaration-example.yaml </kubernetes/config_examples/f5-as3-declaration-example.yaml>`
