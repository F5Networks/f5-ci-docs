.. _lightweight_proxy:

Lightweight Proxy
=================

Overview
--------

.. lwp-overview-body-start

F5® |lwp| |tm| is an application delivery controller (ADC) that is well suited to be deployed dynamically in containerized environments.
The |lwp| has built in load balancing and telemetry for L4 and L7 services.
It is small enough that one can be deployed for every application or service.
It is multi-tenant so it can also be deployed for several services at once.
These features make it ideal for distributed applications and East-West traffic, where it can provide load balancing for dynamic applications' server pools, while providing visibility into those distributed applications' environment and health.

.. lwp-overview-body-end

.. _lwp_architecture:

Architecture
------------

.. lwp-architecture-body-start

The |lwp| comprises four (4) basic components: config, proxy, routing, and telemetry.

* Config

    The config component manages the configuration for the LWP.
    It merges the configuration inputs from static and dynamic sources and normalizes the configuration for the other components.

* Proxy

    The proxy module manages the virtual server configuration; it creates a proxy in the routing infrastructure for each virtual server.

* Routing

    The routing infrastructure is the core of the |lwp|, providing the framework for creating traffic services.
    It invokes the middleware functions and uses the feedback to determine how to handle data events and the transaction lifecycle.
    The routing infrastructure provides a consistent interface for statistics and logging, which are handled by the telemetry module.

* Telemetry

    The telemetry module sends transaction events and statistics -- for both HTTP and TCP transactions -- to an analytics provider (such as `Splunk`_).


.. lwp-architecture-body-end

Use Case
--------

The |lwp| provides load balancing services for East-West data center traffic (in other words, traffic flowing between data passing between microservices). It deploys quickly and scales easily to keep pace with a microservices architecture.

Prerequisites
-------------

.. lwp-prereqs-body-start

- The official F5 ``lightweight-proxy`` image; contact your F5 Sales rep or go to `F5 DevCentral <https://devcentral.f5.com/welcome-to-the-f5-beta-program>`_ to join the Early Access program.
- A functional `Kubernetes`_ or `Marathon`_ orchestration environment.

Caveats
```````

None.

.. lwp-prereqs-body-end


Installation
------------

.. lwp-install-body-start

The |lwp| is dynamically deployed based on a set of pre-defined :ref:`configurations <lwp-configuration>`.
In Marathon, deployment is handled by the |lwpc| for Mesos+Marathon, while in Kubernetes it's done by the ``f5-kube-proxy``.
In either environment, when a service calls for the creation of a |lwp| instance, the instance is automatically configured according to the preset definitions.

Please see the Deployment guide for your environment to learn more about configuring and running the |lwp|.

* F5 |csi_m| :ref:`Lightweight Proxy Deployment Guide <lwpc-deploy-guide>`
* F5 |csi_k| :ref:`Lightweight Proxy Deployment Guide <csik-lwp-deployment>`

.. lwp-install-body-end


.. _lwp-features:

Features
--------

.. features-body

The F5® |lwp| |tm| is a Node.js application that provides a :term:`middleware` framework for handling proxied traffic.

The included features -- :ref:`connection manager <lwp-connection-manager>`, :ref:`load balancer <lwp-load-balancer>`, and :ref:`forwarder <lwp-forwarder>` -- are all :term:`built-in middleware` functions.


.. _built-in-middleware:

Built-in Middleware
```````````````````

Header Manipulator
~~~~~~~~~~~~~~~~~~

The header manipulation module allows you to add, remove, or modify HTTP headers on the ``http.ClientRequest`` and ``http.serverResponse`` objects. The module uses the Node.js header manipulation API (``setHeader``, ``getHeader``, ``removeHeader``). |lwp| has the same semantics for adding headers as the Node.js ``setHeader`` method.

    * Sets a single header value for implicit headers.
    * If header already exists, its value will be replaced.
    * Use an array of values if you need to send header with multiple values.

The following ``flags`` configuration parameters affect this built-in middleware. See `Flags <lwp-configs-virtual-server-flags>` for more information.

    * ``x-forwarded-for``
    * ``x-serverd-by``


.. versionadded:: v0.1.0

.. _lwp-load-balancer:

Load Balancer
~~~~~~~~~~~~~

The load balancer module queries the orchestration environment for the current list of servers and implements a load balancing algorithm to choose a back-end server. This modules provides round-robin load balancing and collection of load balancing-related statistics.

.. todo:: list the applicable config parameters for load balancer module

.. versionadded:: v0.1.0

.. _lwp-connection-manager:

Connection Manager
~~~~~~~~~~~~~~~~~~

The connection manager module tracks and manages server connections. It maintains a mapping of client-to-server connections; conducts lookups for client-to-server and server-to-client connections; reuses existing connections when found and creates new ones when needed; and manages the connection lifetime. Server connections are closed when the client closes the  connection or when the inactivity timeout fires.

.. todo:: list the applicable config parameters for connection manager module

.. versionadded:: v0.1.0

.. _lwp-forwarder:

Forwarder
~~~~~~~~~

The forwarder module forwards data back and forth between client and server connections.

For HTTP and TCP connections, the forwarder provides proxy functionality between the client and server and collects statistics.

.. include:: /includes/f5-lwp/ref_table-forwarder-stats-collection.rst


.. todo:: list the applicable config parameters for forwarder

.. versionadded:: v0.1.0

.. _lwp-telemetry:

Telemetry
`````````

The telemetry module allows LWP and its middleware to capture and aggregate various metrics and send them to a backend system for reporting and analysis or locally to an internal log.

.. versionadded:: v0.1.0
    Supported systems in this version are `Splunk <https://www.splunk.com/>`_ (default).


Global Stats
~~~~~~~~~~~~

The global stats configuration parameters serve as the default for all other metrics that don't require configuration.

-  splunk source: lwp.global
-  splunk sourcetype: f5:lwp.stats:json
-  Frequency: periodic (controlled by ``LWP_CONFIG`` environment variable)

.. include:: /includes/f5-lwp/ref_table-lwp-global-stats.rst


TCP Transaction Stats
~~~~~~~~~~~~~~~~~~~~~

-  splunk source: lwp.tcp.transaction
-  splunk sourcetype: f5:lwp.stats:json
-  Frequency: per connection

.. include:: /includes/f5-lwp/ref_table-lwp-tcp-stats.rst


HTTP Transaction Stats
~~~~~~~~~~~~~~~~~~~~~~

-  splunk source: lwp.http.transaction
-  splunk sourcetype: f5:lwp.stats:json
-  Frequency: per request

.. include:: /includes/f5-lwp/ref_table-lwp-http-stats.rst


.. _customize-lwp-express-middleware:

Customize |lwp| with Express Middleware
```````````````````````````````````````

We've built in helpers that make running `Express middleware <https://expressjs.com/en/guide/using-middleware.html>`_ at the Router level of the |lwp| framework easy. See the Express documentation for more information and configuration instructions.
Using `third-party middleware <https://expressjs.com/en/guide/using-middleware.html#middleware.third-party>`_ to supplement the |lwp|'s built-in functionality  will be supported in a future release.

.. features-body-end

.. _lwp-configuration-section:

Configuration
-------------

.. lwp-configuration-body-start

The F5® |lwp| |tm| implements virtual servers dynamically for services in a container environment, providing the flexibility to handle apps/services in the manner the orchestration environment defines. [#]_ You can also simply provide a static config file if you want to run the |lwp| for static services.

Configure the |lwp| using valid JSON. The available configuration options fall into four (4) categories:

-  :ref:`Global <lwp-global-config>`: configurations that are not specific to an orchestration environment.
-  :ref:`Orchestration <lwp-orchestration-config>`: environment-specific configuration parameters.
-  :ref:`Virtual servers <lwp-virtual-server-config>`: these parameters specify list(s) of virtual server objects representing service endpoints. Part or all of this section is provided by the orchestration environment.
-  :ref:`Telemetry <lwp-stats-config>`: these parameters pertain to statistics gathering and reporting.

.. [#] See the :ref:`Deployment Guides <lwp-deployment-guides>` for details regarding specific orchestration environments.

.. _lwp-config-params:

Configuration Parameters
````````````````````````
.. _lwp-global-config:

.. include:: /includes/f5-lwp/ref_config-parameters-global.rst

.. _lwp-orchestration-config:

.. include:: /includes/f5-lwp/ref_config-parameters-orchestration.rst

.. _lwp-virtual-server-config:

.. include:: /includes/f5-lwp/ref_config-parameters-virtual-server.rst

.. _lwp-stats-config:

.. include:: /includes/f5-lwp/ref_config-parameters-stats.rst

.. seealso:: See :ref:`Telemetry <lwp-telemetry>` for more information regarding stats collection and analysis.

.. include:: /includes/f5-lwp/ref_lwp-config-example.rst

.. lwp-configuration-body-end


Usage
-----

.. usage-body

The F5® |lwp| |tm| can run in Mesos+Marathon or Kubernetes. Environment-specific deployment instructions are provided in the F5 |csi_k| and |csi_m| user guides.

Kubernetes
``````````

The |lwp| deploys in Kubernetes via a custom implementation of ``kube-proxy``. See the |csi_k| :ref:`LWP Deployment Guide <csik-lwp-deployment>` for instructions.

Mesos+Marathon
``````````````

The |lwp| deploys in Mesos+Marathon via an application called the |lwpc|. Once you deploy the |lwpc|, it launches instances of the |lwp| automatically for Marathon Apps with the appropriate labels configured. See the |lwpc| :ref:`Deployment Guide <lwpc-deploy-guide>` for instructions.


Further Reading
---------------

.. seealso::

    * |lwp|  :ref:`Deployment Guides <lwp-deployment-guides>`
    * :ref:`F5 CSI for Mesos+Marathon <csim-home>`
    * :ref:`F5 CSI for Kubernetes <csik-home>`


.. toctree::
    :hidden:




.. usage-body-end
