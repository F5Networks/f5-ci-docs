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

|lwp| comprises four (4) basic components: config, proxy, routing, and telemetry.

Config
``````

The config component manages the configuration for the LWP.
It merges the configuration inputs from static and dynamic sources, and normalizes the configuration for the other components.

Proxy Module
````````````

The proxy module manages the virtual server configuration and creates a proxy in the routing infrastructure for each virtual server.

Routing
```````

The routing infrastructure is the core of LWP that provides the framework to create traffic services.
It is a middelware framework that invokes the middleware functions, and use the feedback to determine how to handle data events and the transaction lifecycle.
The routing infrastructure also provides a consistent interface for statistics and logging that will be handled by the telemetry module.

The LWP comes with a small number of built-in middleware functions.
It also has built-in helpers for `Express middleware`_, which make it easy to :ref:`customize <customize-lwp-express-middleware>` to suit the needs of your environment.

Telemetry Module
````````````````

The telemetry module manages statistics and real-time events.
It provides a modular interface to send those details where they need to go.


The |lwp| comes with a telemetry module which sends transaction events and statistics for both HTTP and TCP transactions to an analytics provider (such as `Splunk`_).

.. lwp-architecture-body-end

Use Case
--------

|lwp| provides load balancing services for East-West data center traffic (in other words, traffic flowing between data passing between microservices). It deploys quickly and scales easily to keep pace with a microservices architecture.

Prerequisites
-------------

.. lwp-prereqs-body-start

- The official F5 ``lightweight-proxy`` image pulled from the `F5 Docker registry`_.
- A functional `Kubernetes`_ or `Marathon`_ orchestration environment.


Caveats
-------

- None.

.. lwp-prereqs-body-end


Installation
------------

.. lwp-install-body-start

F5's |lwp| can be installed in Mesos+Marathon or in Kubernetes. Please see the guides below for environment-specific installation instructions.

* F5 |lwpc| for Mesos+Marathon :ref:`Getting Started Guide <lwpc-getting-started-guide>`
* F5 |csi_k| :ref:`LWP Deployment Guide <csik-lwp-deployment>`

.. lwp-install-body-end

Configuration
-------------

.. lwp-configuration-body-start

You can configure the F5 |lwp| with a valid JSON config file. |lwp| can run in different orchestration environments, each of which has its own specific set of configuration options.

The |lwp| is designed to implement virtual servers dynamically for services in a container environment, providing the flexibility to handle apps/services in the manner the orchestration environment defines. [#]_ You can also simply provide a static config file if you want to run the |lwp| for static services.

The |lwp| config file contains the following sections:

-  :ref:`Global <lwp-global-config>`: global configurations that are not specific to an orchestration environment.
-  :ref:`Orchestration <lwp-orchestration-config>`: contains parameters that allow you to specify your orchestration environment.
-  :ref:`Virtual servers <lwp-virtual-server-config>`: contains parameters that specify list(s) of virtual server objects representing service endpoints. Part or all of this section is provided by the orchestration environment.
-  :ref:`Telemetry <lwp-stats-config>`: contains parameters for statistics gathering and reporting.

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

.. rubric:: See :ref:`Telemetry <lwp-telemetry>`.

.. include:: /includes/f5-lwp/ref_lwp-config-example.rst

.. lwp-configuration-body-end

.. _lwp-features:

Features
--------

.. features-body

F5 |lwp| is a Node.js application that provides a :term:`middleware` framework for handling proxied traffic.

The included :ref:`connection manager <lwp-connection-manager>`, :ref:`load balancer <lwp-load-balancer>`, and :ref:`forwarder <lwp-forwarder>` features are all :term:`built-in middleware` functions.

|lwp| provides helper functions that make it easy to run other `Express middleware <https://expressjs.com/en/guide/using-middleware.html>`_ within our middleware framework. You can also use  `third-party middleware <https://expressjs.com/en/guide/using-middleware.html#middleware.third-party>`_ to add functionality. See the Express documentation for more information.

.. _built-in-middleware:

Built-in Middleware
```````````````````

Header Manipulator
~~~~~~~~~~~~~~~~~~

The header manipulation module allows you to add, remove, or modify HTTP headers on the ``http.ClientRequest`` and ``http.serverResponse`` objects. The module uses the Node.js header manipulation API (``setHeader``, ``getHeader``, ``removeHeader``). |lwp| has the same semantics for adding headers as the Node.js ``setHeader`` method.

    * Sets a single header value for implicit headers.
    * If header already exists, its value will be replaced.
    * Use an array of values if you need to send header with multiple values.

The following flags config parameters affect this built-in middleware. See `Flags <lwp-configs-virtual-server-flags>`.

    * ``x-forwarded-for``
    * ``x-serverd-by``


.. versionadded:: v0.1.1

.. _lwp-load-balancer:

Load Balancer
~~~~~~~~~~~~~

The load balancer module queries the orchestration environment for the current list of
servers and implements a load balancing algorithm to choose a back-end server. This modules provides round-robin load balancing and collection of load balancing-related statistics.

.. todo:: list the applicable config parameters for load balancer module

.. versionadded:: v0.1.1

.. _lwp-connection-manager:

Connection Manager
~~~~~~~~~~~~~~~~~~

The connection manager module tracks and manages server connections. It maintains a mapping of client-to-server connections; conducts lookups for client-to-server and server-to-client connections; reuses existing connections when found and creates new ones when needed; and manages the connection lifetime. Server connections are closed when the client closes the  connection or when the inactivity timeout fires.

.. todo:: list the applicable config parameters for connection manager module

.. versionadded:: v0.1.1

.. _lwp-forwarder:

Forwarder
~~~~~~~~~

The forwarder module forwards data back and forth between client and server connections.

For HTTP and TCP connections, the forwarder provides proxy functionality between the client and server and collects statistics.

.. include:: /includes/f5-lwp/ref_table-forwarder-stats-collection.rst


.. todo:: list the applicable config parameters for forwarder

.. versionadded:: v0.1.1

.. _lwp-telemetry:

Telemetry
`````````

The telemetry module allows LWP and its middleware to capture and aggregate various metrics and send them to a backend system for reporting and analysis.

.. versionadded:: v0.1.1
    Supported systems in this version are `Splunk <https://www.splunk.com/>`_ (default).


Global Stats
~~~~~~~~~~~~

The global stats config parameters serve as the default for all other metrics that don't require configuration.

-  splunk source: lwp.transaction
-  splunk sourcetype: f5:lwp.stats:json
-  Frequency: periodic (controlled by ``LWP_CONFIG`` environment variable)

.. include:: /includes/f5-lwp/ref_table-lwp-global-stats.rst


TCP Transaction Stats
~~~~~~~~~~~~~~~~~~~~~

-  splunk source: lwp.transaction
-  splunk sourcetype: f5:lwp.stats:json
-  Frequency: per connection

.. include:: /includes/f5-lwp/ref_table-lwp-tcp-stats.rst


HTTP Transaction Stats
~~~~~~~~~~~~~~~~~~~~~~

-  splunk source: lwp.transaction
-  splunk sourcetype: f5:lwp.stats:json
-  Frequency: per request

.. include:: /includes/f5-lwp/ref_table-lwp-http-stats.rst

.. features-body-end

Usage
-----

.. usage-body

The F5® |lwp| can run in Mesos+Marathon or Kubernetes. Environment-specific deployment instructions are provided in the F5 |csi_k| and |csi_m| user guides.

Create a Virtual Server via the |lwp| in Kubernetes
```````````````````````````````````````````````````

The |lwp| deploys in Kubernetes via a custom implementation of ``kube-proxy``. See the |csi_k| :ref:`LWP Deployment Guide <csik-lwp-deployment>` for instructions.

Create a Virtual Server via the |lwpc| for Mesos+Marathon
`````````````````````````````````````````````````````````

The F5® |lwpc| for Mesos+Marathon deploys the |lwp| dynamically. See the |lwpc| :ref:`User Guide <lwpc-user-guide>` for deployment instructions.


.. _run-lwp-manually:

Run |lwp| Manually
``````````````````

Use either of the options below to start an |lwp| instance locally from the command line of the client for which you wish to proxy.


* Start |lwp| from the command line using a config file:

    .. code-block:: bash

        lwp_proxy --config-file=/<path_to_config_file>/config.json

-- OR --

* Start |lwp| from the command line using an environment variable:

    .. code-block:: bash

        LWP_CONFIG='{ "virtual-servers": { ... } }' lwp_proxy


.. tip::

    Using the environment variable makes it easier to start |lwp| in a containerized environment.

    For example, the following command can be used to start |lwp| with Docker.

    .. code-block:: bash

        $ docker run -e LWP_CONFIG='{ "virtual-servers": { ... } }' -p 8080:8080 -d f5/lwp-proxy

.. _customize-lwp-express-middleware:

Customize |lwp| with Express Middleware
```````````````````````````````````````

You can add to the built-in functionality provided by F5's |lwp| with `Express middleware`_. We've built in helpers that make running Express or third-party middleware at the Router level of the |lwp| framework easy.

.. todo:: Adding user provided middleware is not yet supported, and interfaces may change. 

.. [#] Described in the :ref:`Architecture <lwp_architecture>` overview.


.. usage-body-end

Further Reading
---------------

.. seealso::

    * :ref:`|lwp| Deployment Guides <lwp-deployment-guides>`
    * :ref:`|lwpc| for Marathon <lwpc-m_home>`
    * :ref:`F5 |csi| for Apache Mesos_Marathon <csi-m_home>`
    * :ref:`F5 |csi| for Kubernetes <csi-k_home>`


.. toctree::
    :hidden:

    self
