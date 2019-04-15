.. index::
   single: Cloud Foundry; Deploy BIG-IP Controller
   single: Cloud Foundry; Application manifest
   single: Cloud Foundry; Global Configuration

.. _deploy-cf-ctlr:

Deploy the BIG-IP Controller for Cloud Foundry
==============================================

Complete the steps provided below to deploy the |cf-long| using the default global configuration mode.

.. note::

   If you need to configure BIG-IP objects for individual Routes, you'll need to register the |cfctlr| as a `Service Broker`_. See :ref:`cfctlr per-route vs` for more information.


.. table:: Task Summary

   =======  ===================================================================
   Step     Task
   =======  ===================================================================
   1.       :ref:`Complete the setup prerequisites <cf-deployment-prereqs>`

   2.       :ref:`create-application-manifest`

            :ref:`cf-health-monitors` (OPTIONAL)

            :ref:`cf-apply-policies-profiles` (OPTIONAL)

   3.       :ref:`push cf-bigip-ctlr global`

   4.       :ref:`cf-verify BIG-IP objects`
   =======  ===================================================================

.. _cf-deployment-prereqs:

Before you begin
----------------

#. `Enable Docker in Cloud Foundry`_ :fonticon:`fa fa-external-link`.
#. `Create a read-only Admin user in Cloud Foundry`_ :fonticon:`fa fa-external-link`

   - In :code:`global` mode, this user needs "routing.routes.read" and "routing.router_groups.read" permissions.
   - In :code:`service_broker` mode, the user needs "routing.routes.read", "routing.router_groups.read", and "cloud_controller.read" permissions.

#. `Add the BIG-IP device to Cloud Foundry`_ :fonticon:`fa fa-external-link` as a custom load balancer.

.. _create-application-manifest:

Create an application manifest
------------------------------

Create a new Application Manifest file containing your desired `cf-bigip-ctlr configuration parameters`_.

Include the following in the :code:`env.BIGIP_CTLR_CFG.bigip` section of the manifest:

- the IP address and user account credentials for the BIG-IP device;

  .. include:: /_static/reuse/bigip-permissions-ctlr.rst

- the BIG-IP partition you want the |cfctlr| to manage (must already exist on the BIG-IP device);
- the load balancing method desired for all pools created by the |cfctlr|;
- the poll interval at which the |cfctlr| should attempt to verify BIG-IP settings;
- the external IP address you want to assign to the virtual server (should be an existing BIG-IP Self IP address); and
- a username and password the Cloud Controller can use to interact with the |cfctlr| API.

To support L7 (HTTP) routing, include the :code:`nats` section shown in the example manifest.

To support L4 (TCP) routing, define the following sections:

* :code:`routing_api` (REQUIRED)
* :code:`oauth`  (REQUIRED)
* :code:`route_mode`  (OPTIONAL)

See the `cf-bigip-ctlr configuration parameters`_ table for more information.

.. literalinclude:: /cloudfoundry/config_examples/manifest.yaml
   :linenos:
   :caption: Example App Manifest for cf-bigip-ctlr
   :lines: 1-42

:fonticon:`fa fa-download` :download:`manifest.yaml </cloudfoundry/config_examples/manifest.yaml>`


.. _cf-health-monitors:

Add BIG-IP Health Monitors
``````````````````````````

In the global :code:`bigip` configuration section, you can attach health monitors that already exist on the BIG-IP device. The example below attaches the existing BIG-IP health monitor called "http.get", which resides in the :code:`/Common` partition.

.. code-block:: yaml
   :caption: Excerpt from example manifest with health monitor defined
   :emphasize-lines: 11

   BIGIP_CTLR_CFG: |
             bigip:
               url: https://bigip.example.com
               user: myBigipUsername
               pass: myBigipPassword
               partition:
                 - cf
               balance: round-robin
               verify_interval: 30
               external_addr: 192.168.1.1
               health-monitors:
               - /Common/http.get

.. tip:: You can create new health monitors and/or attach existing BIG-IP health monitors for `per-Route virtual servers <define per-route vs settings>`.

.. _cf-apply-policies-profiles:

Apply BIG-IP policies and profiles
``````````````````````````````````

You can apply existing BIG-IP policies and profiles to the virtual server(s) created for your Cloud Foundry Routes.
For example: to use the "x-forwarded-for" and "x-forwarded-proto" headers, take the steps below.

#. `Create a BIG-IP local traffic profile`_ with "x-forwarded-for" enabled.
#. `Create a BIG-IP local traffic policy`_ to set the "x-forwarded-proto" header.
#. Add the profile and policy to the Application Manifest. This will associate the objects with the virtual server when the Controller creates it on the BIG-IP system.

   .. code-block:: yaml
      :caption: Excerpt from example manifest with policy and profile defined
      :emphasize-lines: 11-14

      BIGIP_CTLR_CFG: |
                bigip:
                  url: https://bigip.example.com
                  user: myBigipUsername
                  pass: myBigipPassword
                  partition:
                    - cf
                  balance: round-robin
                  verify_interval: 30
                  external_addr: 192.168.1.1
                  profiles:
                  - /Common/x-forwarded-for
                  policies:
                  - /Common/x-forwarded-proto

.. _push cf-bigip-ctlr global:

Push the |cfctlr| app to Cloud Foundry
--------------------------------------

.. include:: /_static/reuse/push-cfctlr-app.rst


.. _cf-verify BIG-IP objects:

Verify object creation on the BIG-IP system
-------------------------------------------

.. important:: The objects created on the BIG-IP system will vary depending on how you set up your Application Manifest.

At minimum, you should see one HTTP virtual server accepting traffic on port 80. If you included an SSL profile in your Manifest, you should also see an HTTPS virtual server accepting traffic on port 443. If you're using TCP Routes, you should see one virtual server for each Route.

#. Log in to the BIG-IP configuration utility at the management IP address (for example, :code:`https://10.90.25.228/xui`).
#. Choose the configured partition (for example, "cf") from the :guilabel:`Partition` dropdown menu.

   #. Go to :menuselection:`Local Traffic --> Virtual Servers` to view the list of virtual server(s) in the partition.
   #. Go to :menuselection:`Local Traffic --> Policies` to view a list of all policies in the partition.
   #. Go to :menuselection:`Local Traffic --> Pools` to view a list of all pools in the partition.


What's Next
-----------

- Learn about :ref:`creating per-Route virtual servers <cfctlr per-route vs>`
- View the `cf-bigip-ctlr reference documentation`_

.. _Enable Docker in Cloud Foundry: https://docs.cloudfoundry.org/adminguide/docker.html#enable
.. _Create a read-only Admin user in Cloud Foundry: https://docs.cloudfoundry.org/concepts/roles.html
.. _Add the BIG-IP device to Cloud Foundry: https://docs.pivotal.io/pivotalcf/2-4/customizing/f5-lb.html
.. _Create a BIG-IP local traffic profile: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/ltm-profiles-reference-13-1-0/1.html
.. _Create a BIG-IP local traffic policy: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/bigip-local-traffic-policies-getting-started-13-1-0/1.html
