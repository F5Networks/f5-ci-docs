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

.. table:: Task table

   =======  ===================================================================
   Step     Task
   =======  ===================================================================
   1.       :ref:`define per-route vs settings`

            :ref:`cf-routes-apply-policies-profiles` (OPTIONAL)

            :ref:`cf-route-health-monitors` (OPTIONAL)

   2.       :ref:`push cf-bigip-ctlr per-route`

   3.       :ref:`register cf-ctlr service broker`

   4.       :ref:`service broker bind`

   5.       :ref:`manage-bigip-objects-cf-routes`
   =======  ===================================================================


.. _define per-route vs settings:

Define the Virtual Server Settings in the Application Manifest
--------------------------------------------------------------

Define the desired BIG-IP virtual server settings as a `Service Plan`_ in the |cfctlr| Application Manifest. You can add the Service Plan section to the Application Manifest for an existing |cfctlr| instance, or when deploying the Controller for the first time.

You can use as many Service Plans as you need to define the BIG-IP services your Apps require. When you :ref:`register cf-ctlr service broker`, the :code:`f5servicebroker` Service discovers Service Plan(s) associated with the |cfctlr| automatically.

.. warning::

   Cloud Foundry supports **one Route Service Binding** per Route. While you can define multiple Service Plans in a single |cfctlr| Application Manifest, you cannot apply multiple plans to the same Application.

#. :ref:`Deploy <deploy-cf-ctlr>` or update the |cfctlr| Application with the following settings:

   - Set :code:`broker_mode` to :code:`true`.
   - Provide a :code:`tier2_ip_range` in CIDR format.
   - Include the :code:`SERVICE_BROKER_CONFIG` section. Use the `cf-bigip-ctlr Service Broker config parameters`_ to define the desired virtual server settings.

   \

   .. tip::

      You can also :ref:`cf-routes-apply-policies-profiles` and/or :ref:`cf-route-health-monitors` in the Service Plan.

   \

   .. literalinclude:: /cloudfoundry/config_examples/manifest.yaml
      :linenos:
      :caption: Example App Manifest for cf-bigip-ctlr Service Broker

   :fonticon:`fa fa-download` :download:`Download the example manifest </cloudfoundry/config_examples/manifest.yaml>`

#. To add a Service Plan for a Controller that's already registered as a `Service Broker`_:

   - Edit the :code:`cf-cigip-ctlr` Application Manifest.
   - Add the desired Service Plan.
   - `Restart the App`_ to make the new settings take effect.

.. sidebar:: :fonticon:`fa fa-question-circle-o` Did you know?

   F5 provides examples of custom local traffic policies in its BIG-IP documentation.

   View the `PreventSpoofOfXFF policy`_ referenced in the example :fonticon:`fa fa-external`.

.. _cf-routes-apply-policies-profiles:

Apply BIG-IP policies and profiles
``````````````````````````````````

Include any of the following BIG-IP objects in the Service Plan to attach them to the Route's virtual server:

- policies (`BIG-IP Application Security Manager`_, L7 forwarding, compression, etc.),
- profiles (tcp optimizations, x-forwarded-for, OneConnect, etc.),
- pool settings (including **health monitors** and **load balancing algorithm**), and
- server ssl profiles.

.. warning::

   The |cfctlr| cannot create or manage policies or profiles on the BIG-IP system. All of the BIG-IP objects that you want to apply to the virtual server -- With the exception of health monitors -- must already exist on the BIG-IP device.

.. _cf-route-health-monitors:

Add BIG-IP Health Monitors
``````````````````````````

You can create a new health monitor in the Service Plan, use an existing BIG-IP health monitor, or both:

.. literalinclude:: /cloudfoundry/config_examples/manifest.yaml
   :linenos:
   :lines: 69-90
   :emphasize-lines: 14-22
   :caption: Example health monitor configuration for cf-bigip-ctlr Service Broker

:fonticon:`fa fa-download` :download:`Download the example manifest </cloudfoundry/config_examples/manifest.yaml>`

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
   - the username and password provided in the :code:`bigip.status` section of the Application Manifest (lets the Cloud Controller authenticate to the |cfctlr| Service Broker API;
   - the Route created in the previous step.

   .. code-block:: console

      cf create-service-broker cfbigip-sb someUser somePass https://sbtest.example.com

#. `Enable Service Access`_ for the :code:`f5servicebroker` Service.

   .. code-block:: console

      cf enable-service-access f5servicebroker

#. `Create a Service instance`_ for your users.

   .. tip:: The plan name you provide here -- "sbtest" in the example below -- must match the name of a plan defined in your :code:`cf-bigip-ctlr` Application Manifest.

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


.. _manage-bigip-objects-cf-routes:

Edit or Remove BIG-IP Objects for Cloud Foundry Routes
------------------------------------------------------

.. note::

   - If you remove all bound Routes before you delete the associated Service Plan, the Controller cleans up the BIG-IP objects and removes the Plan from the data group before restarting.

   - If you remove a Plan without unbinding the associated Routes, the Controller logs will show a diff of the data group vs any incoming Plans. It will remove all BIG-IP objects associated with the deleted plan. If you try to unbind a Route *after* removing its associated Plan, the Controller takes no action on the BIG-IP.

   - Altering Plans that are already in effect may cause interruptions in traffic, depending on what settings have changed.

Edit or Remove a Service Plan
`````````````````````````````

When you remove a Service Plan from the Application Manifest, the Controller removes all of the BIG-IP objects associated with the Plan. This is the case regardless of whether any Routes are still bound to the Service when you delete the plan.


#. To edit or remove a Service Plan for a Controller that's already registered as a `Service Broker`_:

   - Edit the Application Manifest to edit or remove the desired Service Plan.
   - `Restart the App`_ to make the new settings take effect.

.. _service broker unbind:

Stop using the f5servicebroker Service
``````````````````````````````````````

If you no longer want to use the F5 Service Broker for an App, unbind the Service from the Route.

.. code-block:: console

   cf unbind-route-service example.com myAppSbTest --hostname myApp

What's Next
-----------

- :ref:`cf-verify BIG-IP objects`
- View the `cf-bigip-ctlr reference documentation`_


.. _Register a Broker: https://docs.cloudfoundry.org/services/managing-service-brokers.html#register-broker
.. _Map a Route: http://cli.cloudfoundry.org/en-US/cf/map-route.html
.. _Enable Service access: http://cli.cloudfoundry.org/en-US/cf/enable-service-access.html
.. _Create a Service instance: http://cli.cloudfoundry.org/en-US/cf/create-service.html
.. _PreventSpoofOfXFF policy: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/bigip-local-traffic-policies-getting-started-13-1-0/4.html
.. _Restart the App: http://cli.cloudfoundry.org/en-US/cf/restart.html
.. _bind a Route to the Service: http://cli.cloudfoundry.org/en-US/cf/bind-route-service.html
.. _Service Plan: https://docs.cloudfoundry.org/devguide/services/
