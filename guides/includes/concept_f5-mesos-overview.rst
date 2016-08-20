Overview
--------

Apache Mesos with Marathon is configured by default to provide load balancing using `Mesos-DNS <http://mesosphere.github.io/mesos-dns/>`_. It uses DNS to allow applications running within a Mesos cluster to find each other.

Using Mesos-DNS has uses polling to create it's DNS records which can result in stale records and slow failover times. A lack of service-based health checks which can result in traffic being sent to a failed application.

An additional issue is the ability to applications and users to be able to access applications and services from outside of the Mesos cluster environment.

F5's Container Service Integration provides a Mesos environments with the ability to use a BIG-IP as an edge load balancer. Internal load balancing and service discovery is also possible through our lightweight proxy service.

Using a combination of BIG-IP and the lightweight proxy, F5 Container Service Integration provides:

- Load Balancing for external users and applications
- Internal service discovery and load balancing
- Health Checks
- TLS and SSL offload (with BIG-IP for edge load balancing)
- Advanced Persistance Profiles
- Dynamic pool member discovery and updates
