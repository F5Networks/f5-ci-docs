.. _home:

F5 Container Integrations Documentation
=======================================

This documentation set supports the projects that comprise the F5® Container Services Integration. This product suite enables the use of BIG-IP® in containerized environments.

Release |version|
-----------------

This release introduces the following:

* **f5-marathon-lb** |f5mlb_version|: enables use of BIG-IP as an edge load balancer in a Mesos+Marathon environment (North-South traffic).
* **lightweight-proxy** |lwp_version| and **lwp-controller** |lwpc_version|: provide load balancing inside a Mesos cluster (East-West traffic).


Content Overview
----------------
* The Usage Guide provides instructions for setting up a fully functional Mesos+Marathon environment with the F5 Container Services Integration via Amazon AWS.

* The F5 Mesos Integration guide provides high-level information, as well as instructions for deploying the F5 Container Integration in your own Mesos environment.

* Each of the projects' home pages contains detailed information and instructions for installation and configuration.


Contents:
---------

.. toctree::
    :maxdepth: 2

    usage-marathon-poc.rst
    f5-marathon-lb/index.rst
    lightweight-proxy/index.rst
    lwp-controller/index.rst

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


