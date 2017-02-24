Introduction to Container Connectors
====================================

F5's Container Solutions


Design
------

Each CC is uniquely suited to its specific container orchestration environment and purpose, utilizing the architecture and language appropriate for the environment. Generally, each contains the following core elements:

- Frontend: communicates with the container orchestration environment over HTTP REST; interprets the COE applications and containers into the declarative config.
- Declarative config: JSON config; represents the BIG-IP or ASP objects the connector manages; shared between the frontend and the backend.
- Backend: communicates with the BIG-IP or ASP control plane; enacts the declarative config by creating, updating, or deleting objects in the BIG-IP or ASP.



Container Connectors
--------------------

F5's Container Connectors ('CCs') understand the container orchestration environment ('COE'). The CCs provide PaaS-native integrations for F5 BIG-IP devices and the |asp| ('ASP').

=======================     ===================================================
Container Connector         Description
=======================     ===================================================
marathon-bigip-ctlr         Configures a BIG-IP to expose applications in a
                            `Marathon`_ cluster as virtual servers on
                            BIG-IP to serve North-South traffic.
-----------------------     ---------------------------------------------------
marathon-asp-ctlr           Provisions and configures ASPs in a
                            `Marathon`_ cluster to serve East-West
                            traffic.
-----------------------     ---------------------------------------------------
k8s-bigip-ctlr              Configures a BIG-IP to expose applications in a
                            `Kubernetes`_ cluster as virtual servers on BIG-IP
                            to serve North-South traffic.
-----------------------     ---------------------------------------------------
f5-kube-proxy               Configures ASPs in a `Kubernetes`_ cluster to
                            serve East-West traffic.
=======================     ===================================================
