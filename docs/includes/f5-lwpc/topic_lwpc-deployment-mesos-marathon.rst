.. _lwpc-deployment-mesos:

|lwpc| Deployment Guide for Mesos
=================================




Discovery and Visibility
````````````````````````

The |lwpc| monitors applications from the Marathon scheduler. They maintain an address for each task in the pool configuration of the LWP that manages traffic for that application. A Mesos application that needs to access another application load balanced by the LWP connects to the LWP instance for the application to which it requires access. The address of the LWP instance is discoverable via a Mesos DNS SRV query. The SRV query provides the IP address, port and protocol of the LWP.

By convention, the DNS name of a LWP for an application is “lwp-<application name>.<domain name>”. So, for example, if an application is named “app1” and the domain is “marathon.mesos”, the DNS name of the LWP for that application will be “lwp-app1.marathon.mesos”.

By default, lwp-controller starts one LWP instance per application. The default behavior can be overridden using labels, as described in the LWP Controller Project README (:ref:`Override Controller Configuration`).

The LWP collects traffic statistics for the applications that it is load balancing, which can be sent to an analytics application. The location and type of the analytics application can be configured on the LWP controller via the ``LWP_DEFAULT_STATS_URL`` option.