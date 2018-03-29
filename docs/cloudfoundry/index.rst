.. _cf-home:

F5 Container Integration - Cloud Foundry
========================================

This document provides general information regarding the F5 Integration for Cloud Foundry.
For deployment and usage instructions, please refer to the guides below.

.. toctree::
   :caption: BIG-IP Controller Guides
   :maxdepth: 1

   cfctlr-app-install
   cf-per-route-virtuals
   cf-bigip-ctlr reference documentation <http://clouddocs.f5.com/products/connectors/cf-bigip-ctlr/latest>

.. _cf-overview:

Overview
--------

The |cf-long| (``cf-bigip-ctlr``) lets you use an F5 BIG-IP device(s) as an Application Delivery Controller (ADC) serving North-South traffic in `Cloud Foundry`_ or `Pivotal Cloud Foundry`_ (PCF). See the :ref:`connector compatibility` table for compatibility information.


The |cfctlr| is a Docker container-based application that runs on a Cloud Foundry `Diego cell`_. It uses a two-tier architecture:

- One virtual server handles all ingress traffic for the cloud (tier 1);
- this "ingress" virtual server uses URI routing and L7 forwarding policies to send traffic to the appropriate virtual server for each Route (tier 2).

For each Cloud Foundry Route, the |cfctlr| creates a set of forwarding policy rules, a virtual server, pool, and pool members.

.. figure:: /_static/media/cf_architecture.png
   :scale: 80
   :alt: A diagram showing how the BIG-IP Controller for Cloud Foundry sends traffic through the BIG-IP system. All traffic goes first to a single virtual server, which uses L7 policies to send requests on to the correct virtual server for each Route.

By default, the |cfctlr| creates a single HTTP virtual server in tier 1, which handles traffic on port 80. You can create an HTTPS virtual server (which uses port 443) by specifying a BIG-IP SSL profile in the Application manifest when you :ref:`deploy-cf-ctlr`.

The |cfctlr| creates an L4 (TCP) virtual server for each TCP route.

.. _cf-prereqs:

General Prerequisites
`````````````````````

The F5 Container Connector for Cloud Foundry's documentation set assumes that you:

- already have a functional PCF or Cloud Foundry cloud;
- are familiar with the `Cloud Foundry CLI`_ and API;
- already have a BIG-IP :term:`device` licensed and provisioned for your requirements; and
- are familiar with BIG-IP LTM concepts and ``tmsh`` commands.

Installation
------------

You can :ref:`deploy the F5 BIG-IP Controller for Cloud Foundry <deploy-cf-ctlr>` using an `Application Manifest`_. The Application Manifest tells Cloud Foundry and the |cfctlr| :

- how to deploy the |cfctlr| into the Cloud Foundry environment,
- how to log in to the BIG-IP device,
- how to set up the BIG-IP device when you launch the |cfctlr| for the first time, and
- how to access orchestration information from the environment.

Upgrade
-------

To upgrade to a newer version of the |cf-long|, take the steps below.

#. Update the App manifest with the settings for any new features you want to use.

#. .. include:: /_static/reuse/push-cfctlr-app.rst

Apply BIG-IP Services to Cloud Foundry Routes
---------------------------------------------

You can use the |cfctlr| to apply existing BIG-IP services -- health monitors, policies, profiles, and SSL profiles -- to the virtual server(s) and pools for HTTP routes. (These configurations do not apply to TCP routes.) Likewise, you can select any BIG-IP load balancing mode for both HTTP and TCP pools.

The Cloud Foundry :ref:`Application Manifest <create-application-manifest>` file provides the means of identifying the BIG-IP policies, profiles, etc., you want to apply. Some policy and profile configurations only apply to L7 (HTTP) virtual servers. See the `cf-bigip-ctlr configuration parameters`_ table for more information.

.. tip:: See :ref:`cf-apply-policies-profiles` for an example using "x-forwarded-for" and "x-forwarded-proto" headers.

.. _cf-key-concepts:

The |cfctlr| runs in :code:`global` mode by default, meaning a single set of configurations apply to all of the pools/pool members created for Cloud Foundry Routes and Applications.

If you need a greater degree of control over the configurations for Routes associated with specific Apps, you can run the |cfctlr| in :code:`broker_mode` as a Cloud Foundry `Service Broker`_. See :ref:`cfctlr per-route vs` for instructions.

.. _cf bigip ha:

BIG-IP High Availability and Multi-tenancy
``````````````````````````````````````````

If you're using a BIG-IP device pair or cluster, you can use automatic configuration sync to back up your configurations across all devices. Be sure to use a BIG-IP floating IP address as the external address (:code:`bigip.external_addr`) in your Application Manifest. It is possible to run multiple |cfctlr| instances -- each of which would manage a separate BIG-IP device -- provided you have not registered the Controller as a Service Broker. If you go this route, disable auto config sync.

You can use the |cf-long| to manage all of your Cloud Foundry Routes in one BIG-IP partition. You can :ref:`create per-Route virtual servers <cfctlr per-route vs>` -- from different Service Plans -- to achieve isolation within that partition.

.. seealso::

   For information about high availability and App redundancy, see the PCF documentation:

   - `High Availability in Cloud Foundry <https://docs.pivotal.io/pivotalcf/1-9/concepts/high-availability.html>`_
   - `Scaling an Application using cf scale <https://docs.pivotal.io/pivotalcf/1-9/devguide/deploy-apps/cf-scale.html>`_


Key Cloud Foundry Concepts
--------------------------

.. _cf-gorouter-nats:

Routes, NATS, and Routing API
`````````````````````````````

In Cloud Foundry, the `Gorouter`_ component routes all incoming L7 traffic. The `TCP Router`_ component routes all incoming L4 traffic. Similarly, the |cfctlr| uses Cloud Foundry's routing tables to direct traffic to the correct virtual machine(s) for a requested application. The |cfctlr| watches the `NATS bus`_ and `Routing API`_ for route updates; when the Controller discovers changes, it configures the BIG-IP device(s) accordingly.

When you deploy a new application with a mapped HTTP route in Cloud Foundry, the |cfctlr| automatically creates a BIG-IP VIP, pool, pool members, and traffic policy rule for the route. When you deploy a new application with a mapped TCP route in Cloud Foundry, the |cfctlr| automatically creates a BIG-IP virtual server, pool, and pool members for the route.

.. seealso::

   The Pivotal Cloud Foundry documentation provides instructions for `adding an external load balancer <https://docs.pivotal.io/pivotalcf/1-7/opsguide/custom-load-balancer.html>`_ to your Cloud Foundry deployment.

   See Cloud Foundry's `Routes and Domains documentation`_ for more information about how Gorouter creates and maps routes for applications.

.. _BIG-IP Local Traffic policy: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/local-traffic-policies-getting-started-12-1-0/1.html
.. _Gorouter: https://docs.cloudfoundry.org/concepts/architecture/router.html
.. _TCP Router: https://docs.cloudfoundry.org/adminguide/enabling-tcp-routing.html
.. _Routing API: https://github.com/cloudfoundry-incubator/routing-api
.. _Routes and Domains documentation: https://docs.cloudfoundry.org/devguide/deploy-apps/routes-domains.html

