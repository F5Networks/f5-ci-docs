Frequently Asked Questions (FAQ)
================================


**What is Container Ingress Services?**

Container Ingress Services (CIS) is an F5 open-source solution being offered to support Ingress control (BIG-IP) app services in leading containerized and PaaS environments. 

Container Ingress Services enables app self-service selection and service automation for DevOps’ containerized applications deployments. The CIS integrates with the native container environment management/orchestration system, such as Kubernetes and Red Hat OpenShift platform as a service (PaaS). The CIS consists of three components: 

- The ``bigip-controller-<environment>``: Integrates the BIG-IP control plane into the specific container environment 
- F5 BIG-IP Controller for Kubernetes 
- F5 BIG-IP Controller for OpenShift 



|



**What is the latest version of Container Ingress Services?**

At this time, Container Ingress Services uses the following file versions in documentation and for download at Docker Hub, GitHub, and RedHat. 
- BIG-IP Controller for Kubernetes v1.15
- BIG-IP Controller for Red Hat OpenShift v3.x, v4.x 


|


**What platforms has it been validated on?** 

Container Ingress Services has been validated on:

- K8S v1.15 
- BIG-IP 14.X, BIG-IP 13.X, BIG-IP 12.X with OSCP 
- BIG-IP 14.X, BIG-IP 13.X, BIG-IP 12.X with K8S


|


**What are some limitations I should be aware of in CIS 1.12?**

- Master Node label must set to ``node-role.kubernetes.io/master=true`` when operating on K8S version 1.13.4 or OSCP version 4.1 and above in nodeport mode. If not set, BIG-IP treats master node as any other pool member.
- CIS considers ``secure-serverssl`` annotation as ``true`` irrespective of the configuration.



|


**What is F5’s positioning with regards to Container Ingress Services?**

- Dynamic application services integration for containerized environments that enable app delivery by enabling self-service selection of app services in orchestration for DevOps and automates spin up and down based on event discovery. 
- Improve user experience and productivity through integration with existing native app deployment workflows and new URL Rewrite paths. 
- Integrate control plane connectors for BIG-IP into the container environment management and orchestration systems. CIS supports Kubernetes and Red Hat OpenShift.

.. NOTE:: Red Hat OpenShift PaaS uses Kubernetes container for management and orchestration though OpenShift has a slightly different additional command line utility and graphical User Interface (UI). You can use the BIG-IP Controller for Kubernetes for both Kubernetes and Red Hat OpenShift environments.

- Container Ingress Services allows BIG-IP to enable Ingress control services, including HTTP routing, URI routing, and API versioning into the container environment. In addition, Ingress services include load balancing, scaling, security services, and programmability. 
- Simplify Container Ingress Services deployment using pre-configured Kubernetes Helm Charts and provide flexible deployment with pre-existing configs.



|


**What is the customer value proposition for Container Ingress Services?**

Container Ingress Services delivers F5 inline integration for app performance and security services orchestration and management by native integrations with container environments. CIS enables self-service selection within orchestration management for container applications, and automated discovery and services insertion based on app events. In addition, CIS easily creates appropriate service configurations of the inline BIG-IP for Ingress control within container environments for performance, security, and management of container app traffic. Finally, CIS simplifies deployment in Helm Charts with pre-configured Kubernetes resources, and enables flexible deployment of OpenShift Routes with pre-existing configurations. 


|


**Who are the Target Customers?**

Network architects, Network operations, AppDev, DevOps & System Infrastructure. Container Ingress Services provides the ability to expose BIG-IP services to NetOps, Network Architects’ customers, the application owners, and system infrastructure teams through their container management/orchestration system for self-service and standardization. Many times, NetOps aren’t able to keep up with the many container app service IT requests from AppDev/System teams for DevOps process. NetOps needs to provide through integration self-service and automation of app services within the container orchestration UI. 



|


**What are Container Ingress Services use cases?**

- **Dynamic app services for container environments**: The BIG-IPs can have application level objects (VIPs, Pools, Pool Members) provisioned and managed from within the container orchestration environment, enabling auto-scaling of pool members up or down depending on app services demand. 
- **Auto-scaling and security in cloud and on premesis container environments**: Self-service selection within the orchestration UI or automated app performance and security services based on event discovery for on premesis and across cloud container applications. 
- **Advanced container app protection** Container Ingress Services integrated to BIG-IP and the container environment provides simplified and centralized app and network protection. Integrate with vulnerability assessment for patching and gain attack insights from F5 and data stream export to Prometheus, Splunk or SIEM/Analytics solution. 
- **Streamline app migration and scale multiple app versions simultaneously**: Blue/Green deployments for multiple app versions in Red Hat OpenShift PaaS for production at the same time for scaling and moving to newer applications. It provides A/B testing traffic management of two or more app versions in Red Hat OpenShift for development and testing at the same time. 



|


**What is Ingress and how is it different that ingress?**

Ingress with a capital “I” refers to HTTP Routing or a collection of rules to reach the cluster services. In addition, ingress, many times with a lower-case “i”, refers to inbound connections, app load balancing, and security services.


|
