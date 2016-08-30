.. _home:

F5 Container Integrations Documentation
=======================================

This documentation set supports the projects that comprise the F5® Container Services Integration. This product suite enables the use of BIG-IP® in containerized environments.

Release |release|
-----------------

This release introduces the following:
* f5-marathon-lb: enables use of BIG-IP as an edge load balancer in a Mesos+Marathon environment (North-South traffic).
* lightweight-proxy and lwp-controller: provide load balancing inside a Mesos cluster (East-West traffic).


Content Overview
----------------
* The Usage Guide provides instructions for setting up a fully functional Mesos+Marathon environment with the F5 Container Services Integration.

* The F5 Mesos Integration guide provides insight into how and why the f5-marathon-lb tool is used in Marathon to integrate BIG-IP.

* The LWP / LWP Controller Guide provides insight into how and why the F5 lightweight proxy and lwp-controller provide loadbalancing within Marathon.

* Each of the project READMEs contains detailed information and instructions for installation and configuration.

Contents:
---------

.. toctree::
    :titlesonly:

    Usage Guide <usage-marathon-poc.rst>
    f5-mesos-integration.rst
    f5-marathon-lb README <f5mlb/README>
    lightweight-proxy README <f5lwp/README>
    lwp-controller README <f5lwpc/README>
    releases_and_versioning.rst


