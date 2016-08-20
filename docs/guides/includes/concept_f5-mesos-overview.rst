Overview
--------

Apache Mesos with Marathon provides load balancing using `Mesos-DNS <http://mesosphere.github.io/mesos-dns/>`_. It uses DNS to allow applications running within a Mesos cluster to find each other. Mesos-DNS uses polling to create DNS records that can result in stale records and slow failover times. A lack of service-based health checks can result in traffic being sent to a failed application. In addition, it can be difficult for applications and users to access services and apps from outside the Mesos cluster environment.

F5's Container Service Integration provides an alternative to Mesos-DNS; it enables the use of BIG-IP as an edge load balancer and provides a lightweight proxy service for internal load balancing and service discovery.

The F5 Container Service Integration provides the following services:

- load balancing for external users and applications;
- internal service discovery and load balancing;
- health checks;
- TLS and SSL offload (with BIG-IP for edge load balancing);
- advanced persistence profiles;
- dynamic pool member discovery and updates;
- application visibility via stats collection and per-transaction metrics.
