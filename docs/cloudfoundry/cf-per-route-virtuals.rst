.. index::
   single: Cloud Foundry; BIG-IP Controller; deploy
   single: Cloud Foundry; BIG-IP Controller; Application manifest
   single: Cloud Foundry; BIG-IP Controller; Service Broker
   single: Cloud Foundry; BIG-IP Controller; per-Route configuration

.. _cfctlr per-route vs:

Deploy the BIG-IP Controller for Cloud Foundry with per-Route Virtual Servers
=============================================================================

.. include:: /_static/reuse/cf-version-added-1_1.rst

Follow the instructions provided here to run the |cf-long| in :code:`broker_mode`. In :code:`broker_mode`, the |cfctlr| acts as a `Service Broker`_ to let you deploy per-Route BIG-IP virtual servers.

.. _define per-route vs settings:

Define the Virtual Server Settings in a Service Plan
----------------------------------------------------

#. Create an Application Manifest for the |cfctlr|.

#. Include the :code:`bigip.status` and :code:`SERVICE_BROKER_CONFIG` sections of the Application Manifest shown in the example below.

   .. note::

      The Service Plan, in the :code:`SERVICE_BROKER_CONFIG` section, contains the settings you want to apply to the BIG-IP virtual server. The :code:`f5servicebroker` Service discovers the Service Plan(s) automatically.

      Cloud Foundry supports **one Route Service Binding** per Route. While you can define multiple Service Plans, each must apply to a separate Application.

.. sidebar:: :fonticon:`fa fa-question-circle-o` Did you know?

   F5 provides examples of custom local traffic policies in its BIG-IP documentation.

   View the `PreventSpoofOfXFF policy`_ referenced in the example :fonticon:`fa fa-external`.

You can attach any of the following BIG-IP objects to a per-Route virtual server:

- policies (`BIG-IP Application Security Manager`_, L7 forwarding, compression, etc.),
- profiles (tcp optimizations, x-forwarded-for, OneConnect, etc.),
- pool settings (including **health monitors** and **load balancing algorithm**), and
- server ssl profiles.

The |cfctlr| cannot create or manage BIG-IP policies or profiles. With the exception of health monitors, all of the BIG-IP objects that you want to apply to the virtual server must already exist on the BIG-IP device.

You can create a new health monitor in the Service Plan, use an existing BIG-IP health monitor, or both (shown in the example below).

.. literalinclude:: /cloudfoundry/config_examples/manifest.yaml
   :linenos:
   :caption: Example App Manifest for cf-bigip-ctlr Service Broker

:fonticon:`fa fa-download` :download:`Download the example manifest </cloudfoundry/config_examples/manifest.yaml>`

.. _add-remove service plans:

Add/Remove Service Plans
````````````````````````

You can use as many Service Plans as you need to define the BIG-IP services your Apps require. If you want to add or remove a Service Plan for a Controller that's already registered as a Service Broker:

#. Edit the Application Manifest to add or remove the desired Service Plan.
#. `Restart the App`_ to make the new settings take effect.

When you remove a Service Plan from the Application Manifest, the Controller removes all of the BIG-IP objects associated with the Plan. This is the case regardless of whether any Routes are still bound to the Service when you delete the plan.

.. note::

   - If you remove all bound Routes before you delete the Plan, the Controller will clean up the BIG-IP objects and remove the Plan from the data group before the restart occurs.

   - If you remove the Plan without unbinding the Routes, the Controller logs will show a diff of the data group vs any incoming Plans. It will remove all BIG-IP objects associated with the deleted plan. If you try to unbind a Route *after* removing its associated Plan, the Controller takes no action on the BIG-IP.

   - Altering Plans that are already in effect may cause interruptions in traffic, depending on what settings have changed.

.. _push cf-bigip-ctlr per-route:

Push the |cfctlr| app to Cloud Foundry
--------------------------------------

.. include:: /_static/reuse/push-cfctlr-app.rst

.. _register cf-ctlr service broker:

Register the BIG-IP Controller as a Service Broker
--------------------------------------------------

.. attention::

   The tasks in this section require a Cloud Foundry user account with administrator permissions.

#. `Map a Route`_ for the |cfctlr|.

   .. hint:: Mapping a new Route creates a unique endpoint to use for calls to the Service Broker. This allows you to differentiate between calls to the Controller (such as Cloud Foundry health checks) and calls to the Service Broker API.

   .. code-block:: console

      cf map-route cf-bigip-ctlr example.com --hostname sbtest

#. Register the Controller as a Service Broker.

   Follow the instructions provided in `Register a Broker`_ :fonticon:`fa fa-external` as appropriate for your environment.
   You'll need to provide the following information:

   - a name for the Service Broker;
   - the username and password provided in the :code:`bigip.status` section of the Application Manifest; this will be used to authenticate to the |cfctlr| Service Broker API;
   - the Route created in the previous step.

   .. code-block:: console

      cf create-service-broker cfbigip-sb someUser somePass https://sbtest.example.com

#. `Enable Service Access`_ for the :code:`f5servicebroker` Service.

   .. code-block:: console

      cf enable-service-access f5servicebroker

#. `Create a Service instance`_ for your users.

   .. tip:: Provide a Plan name that matches a Plan defined in your Application Manifest.

   .. code-block:: console

      cf create-service f5servicebroker sbtest myAppSbTest

#. Verify availability of the Service in the Cloud Foundry Marketplace.

   .. code-block:: console

      cf marketplace -s f5servicebroker

.. _service broker bind:

Bind the f5servicebroker Service to a Route
-------------------------------------------

Once an administrator has completed the section above, developers can use the :code:`f5servicebroker` Service for their Apps. To do so, bind the :code:`f5servicebroker` Service to the App's Route.

.. important:: Cloud Foundry supports **one Route Service Binding per Route**.

.. code-block:: console

   cf bind-route-service example.com myAppSbTest --hostname myApp

When you `bind a Route to the Service`_, the |cfctlr| creates a virtual server, pool(s), and pool member(s) on the BIG-IP device with the requested policy(ies) and profile(s) attached.

.. _service broker unbind:

Unbind the f5servicebroker Service
----------------------------------

If you no longer want to use the F5 Service Broker for an App, unbind the Service from the Route.

.. code-block:: console

   cf unbind-route-service example.com myAppSbTest --hostname myApp

What's Next
-----------

- :ref:`verify BIG-IP objects`
- View the `cf-bigip-ctlr reference documentation`_


.. _Register a Broker: https://docs.cloudfoundry.org/services/managing-service-brokers.html#register-broker
.. _Map a Route: http://cli.cloudfoundry.org/en-US/cf/map-route.html
.. _Enable Service access: http://cli.cloudfoundry.org/en-US/cf/enable-service-access.html
.. _Create a Service instance: http://cli.cloudfoundry.org/en-US/cf/create-service.html
.. _PreventSpoofOfXFF policy: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/bigip-local-traffic-policies-getting-started-13-1-0/4.html
.. _Restart the App: http://cli.cloudfoundry.org/en-US/cf/restart.html
.. _bind a Route to the Service: http://cli.cloudfoundry.org/en-US/cf/bind-route-service.html
