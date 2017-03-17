.. _containers-home:

.. index::
    :pair: introduction, design

Introduction to F5 Container Integrations
=========================================

F5's Container Integrations provide the ability to dynamically allocate L4-L7 services in container orchestration environments. The BIG-IP Container Connectors ("CCs") introduce BIG-IP services for North-South traffic, while the |asp| provides services for East-West traffic.

Container Connectors
--------------------

F5's Container Connectors ('CCs') understand the container orchestration environment ('COE'). The CCs provide PaaS-native integrations for F5 BIG-IP devices and the |asp| ('ASP').

=======================     ===================================================
Container Connector         Description
=======================     ===================================================
marathon-bigip-ctlr         Configures a BIG-IP to expose applications in an
                            `Apache Mesos`_ cluster as virtual servers on
                            BIG-IP, serving North-South traffic.
-----------------------     ---------------------------------------------------
marathon-asp-ctlr           Provisions and configures ASPs in a
                            `Marathon`_ cluster to serve East-West
                            traffic.
-----------------------     ---------------------------------------------------
k8s-bigip-ctlr              Configures a BIG-IP to expose applications in a
                            `Kubernetes`_ cluster as virtual servers on BIG-IP
                            to serve North-South traffic.
-----------------------     ---------------------------------------------------
f5-kube-proxy               Configures ASPs in a `Kubernetes`_ cluster,
                            serving East-West traffic; replaces the
                            standard ``kube-proxy``
=======================     ===================================================

---------------------------------

.. image:: /_static/media/container_connectors_north-south.png
    :scale: 50 %
    :alt: North-South architecture

---------------------------------

.. image:: /_static/media/container_connectors_east-west.png
    :scale: 50 %
    :alt: East-West architecture



Design
------

Each CC is uniquely suited to its specific container orchestration environment and purpose, utilizing the architecture and language appropriate for the environment. Application Developers interact with the platform's API; the container connectors watch the API for certain events, then act accordingly.

---------------------------------

.. image:: /_static/media/container_connector-framework.png
    :scale: 50 %
    :alt: F5 Container Connector framework

---------------------------------

For example, when you create an App in Marathon with the :ref:`F5 application labels <app-labels>` applied, the |mctlr-long| uses the information defined in the labels to create objects on the BIG-IP for that App. If you create an App in Marathon with the "asp: enable" label applied, the |aspm-long| launches an |asp| instance for the App.

---------------------------------

.. image:: /_static/media/mesos_flow.png
    :scale: 50 %
    :alt: Marathon Container Connector flow

---------------------------------

The Container Connector is stateless: the inputs are the container orchestration environment's config, the BIG-IP or ASP config, and its own config (provided by the container orchestration environment). This means an instance of a Container Connector can be readily discarded. Migrating a CC is as easy as destroying it in one place and spinning up a new one somewhere else. Wherever a Container Connector runs, it always watches the API and attempts to bring the BIG-IP, or ASP, up to date with the most recent applicable configurations.


Product Documentation
---------------------

See the product documentation for more information about each component.

.. toctree::
    :caption: Product Documentation

    F5 Application Service Proxy (ASP) <http://clouddocs.f5.com/products/asp/latest>
    f5-kube-proxy <http://clouddocs.f5.com/products/connectors/f5-kube-proxy/latest>
    k8s-bigip-ctlr <http://clouddocs.f5.com/products/connectors/k8s-bigip-ctlr/latest/>
    marathon-asp-ctlr <http://clouddocs.f5.com/products/connectors/marathon-asp-ctlr/latest/>
    marathon-bigip-ctlr <http://clouddocs.f5.com/products/connectors/marathon-bigip-ctlr/latest/>




.. include:: master_toc.rst
