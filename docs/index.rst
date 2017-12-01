.. _containers-home:

.. index::
   single: F5 Container Integration; overview


Introduction to F5 Container Integrations
=========================================

F5's Container Integrations make it possible to dynamically allocate BIG-IP L4-L7 services in container orchestration environments. The Container Connectors ('CCs') understand the container orchestration environment ('COE'), thereby providing PaaS-native integrations for F5 BIG-IP devices.

=======================     ===================================================
Container Connector         Description
=======================     ===================================================
`cf-bigip-ctlr`_            Integrates BIG-IP as an
                            Application Delivery Controller (ADC) in
                            `Pivotal Cloud Foundry`_, serving North-South
                            traffic.
-----------------------     ---------------------------------------------------
`k8s-bigip-ctlr`_           Configures a BIG-IP device to expose applications
                            in `Kubernetes`_ and `Red Hat OpenShift`_ clusters
                            as virtual servers, serving North-South traffic.
-----------------------     ---------------------------------------------------
`marathon-bigip-ctlr`_      Configures a BIG-IP device to expose applications
                            in an `Apache Mesos`_ `Marathon`_ cluster as
                            virtual servers, serving North-South traffic.
=======================     ===================================================

\

.. image:: /_static/media/container_connectors_north-south.png
   :scale: 50 %
   :alt: North-South architecture:


Design
------

Each CC is uniquely suited to its specific container orchestration environment and purpose, utilizing the architecture and language appropriate for the environment. Application Developers interact with the platform's API; the container connectors watch the API for certain events, then act accordingly.

.. image:: /_static/media/container_connector-framework.png
   :scale: 50 %
   :alt: F5 Container Connector framework

For example, when you create an App in Marathon with the :ref:`F5 application labels <app-labels>` applied, the |mctlr-long| uses the information defined in the labels to create objects on the BIG-IP device for that App.

.. image:: /_static/media/mesos_flow.png
   :scale: 50 %
   :alt: Marathon Container Connector flow

---------------------------------

The Container Connector is stateless. The inputs are:

- the container orchestration environment's config,
- the BIG-IP device config, and
- the CC config (provided via the appropriate means for the container orchestration environment).

This means an instance of a Container Connector can be readily discarded. Migrating a CC is as easy as destroying it in one place and spinning up a new one somewhere else. Wherever a Container Connector runs, it always watches the API and attempts to bring the BIG-IP up-to-date with the latest applicable configurations.


---------------------------------

Site Contents
-------------

.. include:: master_toc.rst
