Overview
--------

Apache Mesos with Marathon provides load balancing using `Mesos-DNS <http://mesosphere.github.io/mesos-dns/>`_. Mesos-DNS creates DNS records, and applications poll Mesos-DNS to find each other. Because the DNS updates and polling happen periodically, the records can be stale and have slow failover times. The polling rate is outside of admin control in Mesos, so it's not possible to scale it to handle the rate of app bringup/failure. A lack of service-based health checks can result in traffic being sent to a failed application. It can also be difficult for applications and users to access services and apps from outside the Mesos cluster environment.

F5's Container Service Integration (CSI) provides an alternative to Mesos-DNS that enables the use of BIG-IP in Mesos. BIG-IP can be used as an edge load balancer to allow a greater degree of control than that provided by Mesos-DNS/. The CSI also provides a lightweight proxy service for internal load balancing and service discovery.

The F5 Container Service Integration provides the following services:

- load balancing for external users and applications;
- internal service discovery and load balancing;
- health checks;
- TLS and SSL offload (with BIG-IP for edge load balancing);
- advanced persistence profiles;
- dynamic pool member discovery and updates;
- application visibility via stats collection and per-transaction metrics;
- iApps to manage customizations, advanced policy and iRules.
