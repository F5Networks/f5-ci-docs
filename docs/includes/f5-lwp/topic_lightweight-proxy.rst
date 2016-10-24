Lightweight Proxy
=================

Overview
--------

F5® |lwp| |tm| is a lightweight Proxy application delivery controller (ADC) that can be deployed dynamically in containerized environments. |lwp| proxies services for distributed applications and, by way of built in stats collection, provides visualization into distributed applications' environment and health. It also provides load balancing for client requests and connections across an application's server pool.

.. _fp_architecture:
Architecture
````````````

|lwp| comprises four (4) basic modules: config, proxy, routing, and statistics.

.. figure:: /_static/flowpoint_architecture.png
    :alt: Lightweight Proxy Architecture

    |lwp| Architecture

|lwp| comes with four (4) built-in middleware functions, which run in the Routing layer, and a statistics module, which records transaction based stats that can be exported to an analytics provider (such as `Splunk`_). |lwp| also has built-in helpers for `Express middleware`_, which make it easy to :ref:`customize <customize-fp-express-middleware>` to suit the needs of your environment.

.. figure:: /_static/flowpoint_basic-stack.png
    :alt: Lightweight Proxy Basic Stack

    |lwp| Basic Stack

.. todo:: edit diagrams a bit for display formatting


Use Case
--------

|lwp| provides load balancing services for East-West data center traffic (in other words, traffic flowing between data passing between microservices). It deploys quickly with apps and scales easily to keep pace with a microservices architecture.

Prerequisites
-------------

- The official F5 ``lightweight-proxy`` image pulled from the `F5 Docker registry`_.
- A functional `Kubernetes`_ or `Marathon`_ orchestration environment.
- Understanding of `Node.js`_ and `Express`_.


Caveats
-------

None.

Configuration
-------------

All |lwp| configuration is done via a valid JSON config file. |lwp| can run in different orchestration environments, each of which has its own set of configuration options.

For more information, check out the F5 |csi| (CSI) documentation for the environment you're using.

    * :ref:`Apache Mesos / Marathon CSI <#>`
    * :ref:`Kubernetes CSI <#>`

|lwp| is designed to deploy dynamically alongside apps as they spin up. In order to do so, you'll need to use a JSON config file to tell your orchestration environment where to find the |lwp| container image and set the desired virtual server and stats parameters.

The |lwp| config file must contain the following sections:

-  :ref:`Global <global-config-parameters>`: global configurations that are not specific to an orchestration environment.
-  :ref:`Orchestration <orchestration-config-parameters>`: contains parameters that allow you to specify your orchestration environment
-  :ref:`Virtual servers <virtualserver-config-parameters`: contains parameters that specify list(s) of virtual server objects representing service endpoints.
-  :ref:`Stats <stats-config-parameters>`: contains parameters for statistics gathering and reporting.


Configuration Parameters
````````````````````````
.. _global-config-parameters:
.. include:: /includes/ref_config-parameters-global.rst

.. _orchestration-config-parameters:
.. include:: /includes/ref_config-parameters-orchestration.rst

.. _virtualserver-config-parameters:
.. include:: /includes/ref_config-parameters-virtual-server.rst

.. _stats-config-parameters:
.. include:: /includes/ref_config-parameters-stats.rst


Deployments
-----------

coming soon!

Usage
-----

|lwp| has four (4) middleware functions built-in:

    * :ref:`Head Manipulation Module <fp_header-manipulation>` (HTTP only)
    * :ref:`Load Balancer <fp_load-balancer>`
    * :ref:`Connection Manager <fp_connection-manager>`
    * :ref:`Forwarder <fp_forwarder>`

.. _fp_header-manipulation:

Header Manipulation Module
``````````````````````````

The header manipulation module allows you to add, remove, or modify HTTP headers on the ``http.ClientRequest`` and ``http.serverResponse`` objects. The module uses the Node.js header manipulation API (``setHeader``, ``getHeader``, ``removeHeader``). |lwp| has the same semantics for adding headers as the Node.js ``setHeader`` method.

    * Sets a single header value for implicit headers.
    * If header already exists, its value will be replaced.
    * Use an array of values if you need to send header with multiple values.

Options
~~~~~~~

.. list-table:: Header Manipulation Config Parameters
    :header-rows: 1

    * - Section
      - Field(s)
      - Required
    * - Global
      - ``console-log-level``
      - No
    * - Orchestration
      - | ``marathon``  and related config parameters
        | ``kubernetes`` and related config parameters
      - | No
        | No
    * - Virtual Server
      - | ``destination``
        | ``service-name``
        | ``ip-protocol``
        | ``flags``
        | ``flags.x-forwarded-for``
        | ``flags.x-served-by``
      - | Yes
        | Yes
        | Yes
        | Yes
        | Yes
    * - Stats
      - All
      - No


.. _fp_load-balancer:

Load Balancer Module
````````````````````

The load balancer module queries the orchestration environment for the current list of
servers and implements a load balancing algorithm to choose a back-end server. This modules provides round-robin load balancing and collection of load balancing-related statistics.

Options
~~~~~~~



.. _fp_connection-manager:

Connection Manager
``````````````````

The connection manager module tracks and manages server connections. It maintains a mapping of client-to-server connections; conducts lookups for client-to-server and server-to-client connections; reuses existing connections when found and creates new ones when needed; and manages the connection lifetime. Server connections are closed when the client closes the  connection or when the inactivity timeout fires.

Options
~~~~~~~



.. _fp_forwarder:

Forwarder
`````````

The forwarder module forwards data back and forth between client and server connections.

For HTTP and TCP connections, the forwarder provides proxy functionality between the client and server and collects statistics.

.. table:: Forwarder Stats Collection

Connection Type     Per Transaction/Connection      Across Transaction/Connection
===============     ===========================     =============================
HTTP                client address                  request counts
                    server address                  response counts
                    method                          method counts
                    status code                     status code counts
                    URL                             error counts
                    server RTT
                    latency
---------------     ---------------------------     -----------------------------
TCP                 client address                  total connections
                    server address                  current connections
                    bytes read                      total closed
                    bytes written                   error counts
                    server RTT
                    latency
===============     ===========================     =============================


Options
~~~~~~~

HTTP            TCP
====            ====

 max connection limit

.. _customize-fp-express-middleware:

Customize |lwp| with Express Middleware
``````````````````````````````````````

You can add to the built-in functionality provided by |lwp| with `Express middleware`_. We've built in helpers that make it easy to run Express middleware at the Router level of the |lwp| framework. [#]_ See the `Express <https://expressjs.com/>`_  documentation for installation, usage, and composition instructions.

We recommend checking out the documentation for `Third-party middleware <https://expressjs.com/en/guide/using-middleware.html#middleware.third-party>`_, which contains instructions for installing and loading third-party middleware functions.

.. [#] Described in the :ref:`Architecture <fp_architecture>` overview.

Further Reading
---------------

