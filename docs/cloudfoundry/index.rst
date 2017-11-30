.. _cf-home:

F5 Container Integration - Cloud Foundry
========================================

This document provides general information regarding the F5 Integration for Cloud Foundry.
For deployment and usage instructions, please refer to the guides below.

.. toctree::
   :caption: BIG-IP Controller
   :maxdepth: 1

   Install the BIG-IP Controller in Cloud Foundry <cfctlr-app-install>
   cf-bigip-ctlr Reference <http://clouddocs.f5.com/products/connectors/cf-bigip-ctlr/latest>

.. _cf-overview:

Overview
--------

The F5 Container Integration for `Cloud Foundry`_  consists of the |cf-long| (``cf-bigip-ctlr``).
The |cfctlr| lets you use your F5 BIG-IP device as an Application Delivery Controller (ADC) in Cloud Foundry, serving North-South traffic. You can use the |cfctlr| with `Cloud Foundry`_ or `Pivotal Cloud Foundry`_ (PCF).

The |cf-long| is a Docker container-based application that runs on a Cloud Foundry `Diego cell`_.

You can :ref:`deploy the F5 BIG-IP Controller for Cloud Foundry <deploy-cf-ctlr>` using an `Application Manifest`_.
The Application Manifest tells Cloud Foundry and the |cfctlr|

- how to deploy the |cfctlr| into the Cloud Foundry environment,
- how to log in to the BIG-IP device,
- how to set up the BIG-IP device when you launch the |cfctlr| for the first time, and
- how to access orchestration information from the environment.

Once the |cf-long| is running, it

- creates BIG-IP virtual servers, which serve as the entry points for traffic into the cloud;
- creates a `BIG-IP Local Traffic policy`_ with rules for each HTTP route it finds in Cloud Foundry;
- creates a pool for each TCP and HTTP route, with members for each application instance;
- associates each application's traffic policy rule with its pool.

.. attention::

   - The |cfctlr| can create two (2) L7 virtual servers for Cloud Foundry: one (1) for HTTP and one (1) for HTTPS.
   - The |cfctlr| creates an HTTP virtual server by default.
   - The |cfctlr| creates an L4 (TCP) virtual server for each mapped route to a TCP domain.

.. _cf-prereqs:

General Prerequisites
`````````````````````

The F5 Integration for Cloud Foundry's documentation set assumes that you:

- already have a functional Cloud Foundry or Pivotal Cloud Foundry deployment;
- are familiar with the `Cloud Foundry CLI`_ and API;
- already have a BIG-IP :term:`device` licensed and provisioned for your requirements; and
- are familiar with BIG-IP LTM concepts and ``tmsh`` commands.


.. _cf-key-concepts:

Key Cloud Foundry Concepts
--------------------------

The |cfctlr| configurations are "global", meaning a single set of configurations apply to all of the pools/pool members created for Cloud Foundry Routes and Applications.
The Cloud Foundry :ref:`Application Manifest <create-application-manifest>` file is the means via which you can identify the BIG-IP policies, profiles, etc., you want to apply.

.. important::

   Some policy and profile configurations only apply to L7 (HTTP) virtual servers. See the `cf-bigip-ctlr configuration parameters`_ table for more information.

.. _cf-gorouter-nats:

Routes, NATS, and Routing API
`````````````````````````````

In Cloud Foundry, the `Gorouter`_ component routes all incoming L7 traffic. The `TCP Router`_ component routes all incoming L4 traffic.
Similarly, the |cfctlr| uses Cloud Foundry's routing tables to direct traffic to the correct virtual machine(s) for a requested application.
The |cfctlr| watches the `NATS bus`_ and `Routing API`_ for route updates; when the Controller discovers changes, it configures the BIG-IP device(s) accordingly.

When you deploy a new application with a mapped HTTP route in Cloud Foundry, the |cfctlr| automatically creates a BIG-IP pool, pool members, and traffic policy rule for the new route. When you deploy a new application with a mapped TCP route in Cloud Foundry, the |cfctlr| automatically creates a BIG-IP virtual server, pool, and pool members for the new route.

.. seealso::

   The Pivotal Cloud Foundry documentation provides instructions for `adding an external load balancer <https://docs.pivotal.io/pivotalcf/1-7/opsguide/custom-load-balancer.html>`_ to your Cloud Foundry deployment.

   See Cloud Foundry's `Routes and Domains documentation`_ for more information about how Gorouter creates and maps routes for applications.

.. _cf-health-monitors:

BIG-IP Local Traffic Manager Services
-------------------------------------

You can apply existing BIG-IP health monitors, policies, profiles, and SSL profiles to the virtual server(s) and pools the |cfctlr| creates for HTTP routes (these configurations do not apply to objects managed for TCP routes).
Likewise, you can select any BIG-IP load balancing mode (applies to both HTTP and TCP pools).
Define the `cf-bigip-ctlr configuration parameters`_ in your :ref:`Application Manifest <create-application-manifest>`.

.. tip::

   You can apply additional BIG-IP configurations to achieve greater feature parity with `Gorouter`_.
   For example, you can add 'X_FORWARDED_PROTO: HTTP' and  'X_FORWARDED_PROTO: HTTPS' headers using BIG-IP policies and profiles.

   See :ref:`Deploy the BIG-IP Controller for Cloud Foundry <create-application-manifest>` for instructions.

.. Related
   -------

.. image /_static/media/tbd
   :scale: 50 %
   :alt: F5 Container Solution for CloudFoundry

.. _BIG-IP Local Traffic policy: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/local-traffic-policies-getting-started-12-1-0/1.html
.. _Gorouter: https://docs.cloudfoundry.org/concepts/architecture/router.html
.. _TCP Router: https://docs.cloudfoundry.org/adminguide/enabling-tcp-routing.html
.. _Routing API: https://github.com/cloudfoundry-incubator/routing-api
.. _Routes and Domains documentation: https://docs.cloudfoundry.org/devguide/deploy-apps/routes-domains.html

