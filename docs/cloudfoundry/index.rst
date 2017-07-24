.. _cf-home:

F5 Cloud Foundry Container Integration :fonticon:`fa fa-wrench`
===============================================================
.. _cf-overview:

Overview
--------

.. include:: /_static/reuse/beta-announcement-cf.rst

The F5 Container Integration for `Cloud Foundry`_  consists of the `F5 BIG-IP Controller for Cloud Foundry </products/connectors/cf-bigip-ctlr/latest>`_.

The |cf-long| configures BIG-IP Local Traffic Manager (LTM) objects for Cloud Foundry applications, serving North-South traffic.

You can use the |cf-long| with `Cloud Foundry`_ or `Pivotal Cloud Foundry`_ (PCF).

.. _cf-prereqs:

General Prerequisites
---------------------

The F5 Integration for Cloud Foundry's documentation set assumes that you:

- already have a functional Cloud Foundry or Pivotal Cloud Foundry deployment;
- are familiar with the `Cloud Foundry CLI`_ and API;
- already have a BIG-IP :term:`device` licensed and provisioned for your requirements; and
- are familiar with BIG-IP LTM concepts and ``tmsh`` commands.


|cf-long|
---------

The |cf-long| is a Docker container-based application that runs on a Cloud Foundry `Diego cell`_.

You can :ref:`deploy the F5 BIG-IP Controller for Cloud Foundry <deploy-cf-ctlr>` using an `Application Manifest`_.
The Application Manifest tells the |cf-long|

- how to log in to the BIG-IP device, and
- how to set up the BIG-IP device when you launch the |cfctlr| for the first time.

Once the |cf-long| is running, it

- creates a BIG-IP virtual server, which serves as the entry point for traffic into the cloud;
- creates a `BIG-IP Local Traffic policy`_ (maximum of two - one each for http and https) with rules for each route it finds in Cloud Foundry;
- creates a pool for each route, with members for each application instance;
- associates each application's traffic policy rule with its pool.

.. attention::

   The |cf-long| can create a maximum of two (2) virtual servers for Cloud Foundry: one (1) for HTTP and one (1) for HTTPS.
   The |cf-long| creates an HTTP virtual server by default.


.. _cf-key-concepts:

Key Cloud Foundry Concepts
--------------------------

|cf-long| configurations are "global", meaning a single set of configurations apply to all of the pools/pools members created for Cloud Foundry Apps.
The Cloud Foundry :ref:`Application Manifest <create-application-manifest>` file is the means via which you can identify the BIG-IP policies, profiles, etc., you want to apply.

.. _cf-gorouter-nats:

Gorouter and NATS
`````````````````

In Cloud Foundry, the `Gorouter`_ component routes all incoming traffic.
Similarly, the |cf-long| uses Cloud Foundry's routing tables to direct traffic to the correct Diego cell virtual machine(s) for a requested application.
The |cf-long| watches the `NATS bus`_ for route updates; when it discovers changes, it configures the BIG-IP device(s) accordingly.

When you deploy a new application in Cloud Foundry, the |cf-long| automatically creates a BIG-IP pool, pool members, and traffic policy rule for the new route.

.. seealso::

   The Pivotal Cloud Foundry documentation provides instructions for `adding an external load balancer <https://docs.pivotal.io/pivotalcf/1-7/opsguide/custom-load-balancer.html>`_ to your Cloud Foundry deployment.

   See Cloud Foundry's `Routes and Domains documentation`_ for more information about how Gorouter creates and maps routes for applications.

.. _cf-health-monitors:

BIG-IP Local Traffic Manager Services
-------------------------------------

You can apply existing BIG-IP health monitors, policies, and SSL profiles to the virtual server(s) and pools the |cf-long| creates.
Likewise, you can select any load balancing mode that exists on the BIG-IP device.
Define the |cfctlr| `configuration parameters </products/connectors/cf-bigip-ctlr/latest/index.html#configuration-parameters>`_ in your :ref:`Application Manifest <create-application-manifest>`.

.. tip::

   You can enable "x-forwarded-for" and "x-forwarded-proto" profiles for the BIG-IP virtual server(s).
   Just create the profiles on the BIG-IP, then add them to the Application Manifest before launching the |cfctlr|.


.. Related
   -------

.. image /_static/media/tbd
   :scale: 50 %
   :alt: F5 Container Solution for CloudFoundry

.. _BIG-IP Local Traffic policy: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/local-traffic-policies-getting-started-12-1-0/1.html
.. _Gorouter: https://docs.cloudfoundry.org/concepts/architecture/router.html
.. _Routes and Domains documentation: https://docs.cloudfoundry.org/devguide/deploy-apps/routes-domains.html

