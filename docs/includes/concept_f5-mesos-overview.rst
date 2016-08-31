Overview
--------

Apache Mesos with Marathon provide a containerized platform for running containerized applications on a shared infrastructure. Applications are implemented by one or more identical tasks, which are started and stopped automatically, and often given ephemeral addresses. Included support for exposing and load-balancing these applications to clients outside of Mesos, as well to other services withing Mesos are limited.

F5's Container Service Integration (CSI) provides several options beyond the capabilities of Mesos with Marathon. It enables the use of BIG-IP® as an edge load balancer to expose services outside the Mesos cluster and provides a lightweight proxy service for internal load balancing and service discovery.

The F5 Container Service Integration provides several services, including the following.

- BIG-IP support for Marathon Applications
- TLS and SSL offload for North-South traffic
- Advanced persistence profiles for North-South traffic
- East-West load-balancing with L7 visibility
- Dynamic pool member discovery and updates
- Application visibility via stats collection and per-transaction metrics for North-South and East-West traffic
- iApps® to manage customizations, advanced policy, and iRules®
