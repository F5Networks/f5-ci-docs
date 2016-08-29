.. F5 Container Integrations documentation master file, created by
   sphinx-quickstart on Wed Aug 10 13:36:59 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to F5 Container Integrations's documentation!
=====================================================

This documentation set supports the beta release of the F5® Container Service Integration. This product suite enables the use of BIG-IP® as an edge load balancer in a Mesos+Marathon environment and introduces a new lightweight proxy tool that load balances inside Marathon.


Content Overview
----------------
The Usage Guide provides instructions for setting up a fully functional Mesos+Marathon environment with the F5 Container Services Integration.

The F5 Mesos Integration guide provides insight into how and why the f5-marathon-lb tool is used in Marathon to integrate BIG-IP.

The LWP / LWP Controller Guide provides insight into how and why the F5 lightweight proxy and lwp-controller provide loadbalancing within Marathon.

Finally, each of the project READMEs contains detailed information and instructions for installation and configuration.

Contents:
---------

.. toctree::
    :titlesonly:

    Usage Guide <usage-marathon-poc.rst>
    f5-mesos-integration.rst
    f5-marathon-lb README <f5-marathon-lb/index>
    lightweight-proxy README <lightweight-proxy/index>
    lwp-controller README <lwp-controller/index>
    releases_and_versioning.rst


