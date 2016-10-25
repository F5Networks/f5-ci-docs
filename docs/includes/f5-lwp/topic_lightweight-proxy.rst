.. _lightweight_proxy:

Lightweight Proxy
=================

Overview
--------

F5® |lwp| |tm| is an application delivery controller (ADC) that can be deployed dynamically in containerized environments. The |lwp| proxies services for distributed applications and, by way of built in stats collection, provides visualization into distributed applications' environment and health. It also provides load balancing for client requests and connections across an application's server pool (East-West traffic).

.. _lwp_architecture:

Architecture
````````````

|lwp| comprises four (4) basic modules: config, proxy, routing, and statistics.

.. figure:: /static/f5-lwp/lightweight-proxy_architecture.png
    :alt: Lightweight Proxy Architecture

    |lwp| Architecture

The |lwp| comes with four (4) built-in middleware functions, which run in the routing layer, and a statistics module, which records transaction based stats that can be exported to an analytics provider (such as `Splunk`_). |lwp| also has built-in helpers for `Express middleware`_, which make it easy to :ref:`customize <customize-lwp-express-middleware>` to suit the needs of your environment.

.. figure:: /static/f5-lwp/lightweight-proxy_basic-stack.png
    :alt: Lightweight Proxy Basic Stack

    |lwp| Basic Stack

.. todo:: edit diagrams a bit for display formatting


Use Case
````````

|lwp| provides load balancing services for East-West data center traffic (in other words, traffic flowing between data passing between microservices). It deploys quickly and scales easily to keep pace with a microservices architecture.

Deployments
```````````

F5's |lwp| can be deployed in Mesos with Marathon, or in Kubernetes. Please see the deployment guide for your environment for further information.

* :ref:`Mesos + Marathon <#>`
* :ref:`Kubernetes <deploy-lwp-kubernetes>`

Prerequisites
-------------

- The official F5 ``lightweight-proxy`` image pulled from the `F5 Docker registry`_.
- A functional `Kubernetes`_ or `Marathon`_ orchestration environment.
- Understanding of `Node.js`_ and `Express`_.


Caveats
-------

Configuration
-------------

You can configure the F5 |lwp| with a valid JSON config file. |lwp| can run in different orchestration environments, each of which has its own specific set of configuration options.

The |lwp| is designed to implement virtual servers dynamically for services in a container environment, providing the flexibility to handle apps/services in the manner the orchestration environment defines. [#]_ You can also simply provide a static config file if you want to run the |lwp| for a static service.

The |lwp| config file must contain the following sections:

-  :ref:`Global <#>`: global configurations that are not specific to an orchestration environment.
-  :ref:`Orchestration <#>`: contains parameters that allow you to specify your orchestration environment
-  :ref:`Virtual servers <#>`: contains parameters that specify list(s) of virtual server objects representing service endpoints.
-  :ref:`Stats <#>`: contains parameters for statistics gathering and reporting.

.. [#] See the :ref:`Deployment Guides <lwp-deployment-guides>` for details regarding specific orchestration environments.

.. _lwp-configuration-parameters:

Configuration Parameters
````````````````````````

.. include:: /includes/f5-lwp/ref_config-parameters-global.rst


.. include:: /includes/f5-lwp/ref_config-parameters-orchestration.rst

.. include:: /includes/f5-lwp/ref_config-parameters-virtual-server.rst

.. include:: /includes/f5-lwp/ref_config-parameters-stats.rst

.. rubric:: See :ref:`Statistics and Data Aggregation <lwp-statistics>`.

.. include:: /includes/f5-lwp/ref_lwp-config-example.rst


.. _lwp-features:

Features
--------

F5 |lwp| is a Node.js application that provides a :term:`middleware` framework for handling proxied traffic.

The included :ref:`connection manager`, :ref:`load balancer`, and :ref:`forwarder` features are all :term:`built-in middleware` functions.

|lwp| provides helper functions that make it easy to run other `Express middleware <https://expressjs.com/en/guide/using-middleware.html>`_ within our middleware framework. You can also use  `third-party middleware <https://expressjs.com/en/guide/using-middleware.html#middleware.third-party>`_ to add functionality. See the Express documentation for more information.

.. _built-in-middleware:

Built-in Middleware
```````````````````

Header Manipulator
^^^^^^^^^^^^^^^^^^
The header manipulation module allows you to add, remove, or modify HTTP headers on the ``http.ClientRequest`` and ``http.serverResponse`` objects. The module uses the Node.js header manipulation API (``setHeader``, ``getHeader``, ``removeHeader``). |lwp| has the same semantics for adding headers as the Node.js ``setHeader`` method.

    * Sets a single header value for implicit headers.
    * If header already exists, its value will be replaced.
    * Use an array of values if you need to send header with multiple values.


.. todo:: list the applicable config parameters for header manipulation module

.. versionadded:: v0.1.1

Load Balancer
^^^^^^^^^^^^^

The load balancer module queries the orchestration environment for the current list of
servers and implements a load balancing algorithm to choose a back-end server. This modules provides round-robin load balancing and collection of load balancing-related statistics.

.. todo:: list the applicable config parameters for load balancer module

.. versionadded:: v0.1.1

Connection Manager
^^^^^^^^^^^^^^^^^^

The connection manager module tracks and manages server connections. It maintains a mapping of client-to-server connections; conducts lookups for client-to-server and server-to-client connections; reuses existing connections when found and creates new ones when needed; and manages the connection lifetime. Server connections are closed when the client closes the  connection or when the inactivity timeout fires.

.. todo:: list the applicable config parameters for connection manager module

.. versionadded:: v0.1.1


Forwarder
^^^^^^^^^

The forwarder module forwards data back and forth between client and server connections.

For HTTP and TCP connections, the forwarder provides proxy functionality between the client and server and collects statistics.

.. include:: /includes/f5-lwp/ref_table-forwarder-stats-collection.rst


.. todo:: list the applicable config parameters for forwarder

.. versionadded:: v0.1.1

.. _lwp-statistics:

Statistics and Data Aggregator
``````````````````````````````

The statistics and data aggregator module allows Node.js programs to capture various metrics and send them to a number of
different backend systems.

.. versionadded:: v0.1.1
    Supported systems in this version are `Splunk <https://www.splunk.com/>`_ (default) and Leo.


Global Stats
^^^^^^^^^^^^

The global stats config parameters serve as the default for all other metrics that don't require configuration.

-  splunk source: lwp.transaction
-  splunk sourcetype: f5:lwp.stats:json
-  Frequency: periodic (controlled by ``LWP_CONFIG`` environment variable)

.. include:: /includes/f5-lwp/ref_table-lwp-global-stats.rst


TCP Transaction Stats
^^^^^^^^^^^^^^^^^^^^^

-  splunk source: lwp.transaction
-  splunk sourcetype: f5:lwp.stats:json
-  Frequency: per connection

.. include:: /includes/f5-lwp/ref_table-lwp-tcp-stats.rst


HTTP Transaction Stats
^^^^^^^^^^^^^^^^^^^^^^

-  splunk source: lwp.transaction
-  splunk sourcetype: f5:lwp.stats:json
-  Frequency: per request

.. include:: /includes/f5-lwp/ref_table-lwp-http-stats.rst

Usage
-----

.. _run-lwp-manually:

Run |lwp| Manually
``````````````````
Use either of the options below to start an |lwp| instance locally from the command line of the client for which you wish to proxy.


* Start |lwp| from the command line using a config file:

    .. code-block:: bash

        $ lwp_proxy --config-file=/<path_to_config_file>/config.json

-- OR --

* Start |lwp| from the command line using an environment variable:

    .. code-block:: bash

        $ LWP_CONFIG='{ "virtual-servers": { ... } }' lwp_proxy


.. tip::

    Using the environment variable makes it easier to start |lwp| in a containerized environment.

    For example, the following command can be used to start |lwp| with Docker.

    .. code-block:: bash

        $ docker run -e LWP_CONFIG='{ "virtual-servers": { ... } }' -p 8080:8080 -d f5/lwp-proxy

.. _customize-lwp-express-middleware:

Customize |lwp| with Express Middleware
```````````````````````````````````````

You can add to the built-in functionality provided by F5's |lwp| with `Express middleware`_. We've built in helpers that make running Express or third-party middleware at the Router level of the |lwp| framework easy. [#]_ See the `Express <https://expressjs.com/>`_  documentation for installation, usage, and composition instructions.

We recommend checking out the documentation for `third-party middleware <https://expressjs.com/en/guide/using-middleware.html#middleware.third-party>`_, which contains instructions for installing and loading Express-compatible third-party middleware functions.

.. [#] Described in the :ref:`Architecture <lwp_architecture>` overview.


Further Reading
---------------

.. seealso::

    * :ref:`|lwp| Deployment Guides <lwp-deployment-guides>`
    * :ref:`|lwpc| for Marathon <lwpc-m_home>`
    * :ref:`F5 |csc| for Apache Mesos/Marathon <csc-m_home>`
    * :ref:`F5 |csc| for Kubernetes <csc-k_home>`


.. toctree::
    :hidden:

    self
