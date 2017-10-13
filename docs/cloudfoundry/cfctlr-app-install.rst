.. _deploy-cf-ctlr:

Deploy the BIG-IP Controller for Cloud Foundry
==============================================

Complete the steps provided below to deploy the |cf-long| in `Cloud Foundry`_ or `Pivotal Cloud Foundry`_ using an `Application Manifest`_.

.. _cf-deployment-prereqs:

Before you begin
----------------

- `Enable Docker in Cloud Foundry`_ :fonticon:`fa fa-external-link`.
- `Create a read-only Admin user in Cloud Foundry`_ :fonticon:`fa fa-external-link` (needs "routing.routes.read" and "routing.router_groups.read" permissions).
- `Add the BIG-IP device to Cloud Foundry`_ :fonticon:`fa fa-external-link` as a custom load balancer.

.. _create-application-manifest:

Create an application manifest
------------------------------

Create a new Application Manifest file defining the |cfctlr| `configuration parameters </products/connectors/cf-bigip-ctlr/latest/index.html#configuration-parameters>`_ you want to apply for your cloud.

The :code:`bigip` section of the example |cfctlr| manifest below does the following:

- provides the IP address and user account credentials for the BIG-IP device;
- defines the existing BIG-IP partition in which |cfctlr| should create objects;
- sets the load balancing method desired for all pools created by the |cfctlr|;
- sets the interval at which the |cfctlr| attempts to verify BIG-IP settings; and
- assigns an external IP address to the virtual server.

.. note::

   - To support L7 (HTTP) routing, you must include the :code:`nats` section in the Controller manifest.
   - To support L4 (TCP) routing, you must define the following sections:

      * :code:`routing_api` (REQUIRED)
      * :code:`oauth`  (REQUIRED)
      * :code:`route_mode`  (OPTIONAL)

   See the |cfctlr| `configuration parameters </products/connectors/cf-bigip-ctlr/v1.0/#configuration-parameters>`_ table for more information.

.. literalinclude:: /_static/config_examples/manifest.yaml
   :linenos:
   :caption: Example App Manifest for cf-bigip-ctlr

:fonticon:`fa fa-download` :download:`manifest.yaml </_static/config_examples/manifest.yaml>`


.. tip::

   If you want to use the "x-forwarded-for" and "x-forwarded-proto" headers, take the steps below **before** you launch the |cfctlr| app:

   #. Add a BIG-IP profile with "x-forwarded-for" enabled.
   #. Add a BIG-IP traffic policy to set the "x-forwarded-proto" header.
   #. Add these objects to the Application Manifest using the :code:`profiles` and :code:`policies` configuration parameters, respectively.

Push the |cfctlr| app to Cloud Foundry
--------------------------------------

Use the `Cloud Foundry CLI`_ :command:`cf push` command to deploy the |cfctlr| App.

.. code-block:: console

   cf push -o f5networks/cf-bigip-ctlr -f manifest.yaml

Verify creation of BIG-IP objects
---------------------------------

Virtual Servers
```````````````

The |cf-long| creates and manages BIG-IP virtual servers. You should see one (1) virtual server per TCP route configured in your Cloud Foundry
deployment. You should also have at least one (1) virtual server handling unencrypted HTTP traffic on port 80. If the configuration manifest contains an SSL profile, the Controller creates another L7 virtual server on port 443.

#. Log in to the BIG-IP configuration utility at the management IP address (for example, :code:`https://10.90.25.228/xui`).
#. Choose the configured partition ("cf" in our examples) from the :guilabel:`Partition` dropdown menu.
#. Go to :menuselection:`Local Traffic --> Virtual Servers` to view the virtual server(s) created in the partition.

Policies
````````

The |cf-long| turns Cloud Foundry route tables into BIG-IP Local Traffic policies.
You should see a new policy on your BIG-IP device, with a rule for each route in your Cloud Foundry deployment.

#. Log in to the BIG-IP configuration utility at the management IP address (for example, :code:`https://10.190.25.228/xui`).
#. Choose the configured partition ("cf" in our examples) from the :guilabel:`Partition` dropdown menu.
#. Go to :menuselection:`Local Traffic --> Policies` to view a list of all policies in the partition.

Pools
`````

The |cf-long| also creates a pool and pool members for every route in your Cloud Foundry deployment.

You can use the BIG-IP configuration utility to verify that the pools and pool members exist.

#. Log in to the BIG-IP configuration utility at the management IP address (for example, :code:`https://10.190.25.228/xui`).
#. Choose the configured partition ("cf" in our examples) from the :guilabel:`Partition` dropdown menu.
#. Go to :menuselection:`Local Traffic --> Pools` to view a list of all pools in the partition.


.. _Enable Docker in Cloud Foundry: https://docs.cloudfoundry.org/adminguide/docker.html#enable
.. _Create a read-only Admin user in Cloud Foundry: https://docs.cloudfoundry.org/concepts/roles.html
.. _Add the BIG-IP device to Cloud Foundry: https://docs.pivotal.io/pivotalcf/1-7/opsguide/custom-load-balancer.html
