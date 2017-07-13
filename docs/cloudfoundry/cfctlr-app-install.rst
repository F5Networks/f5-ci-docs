.. _deploy-cf-ctlr:

Deploy the Cloud Foundry BIG-IP Controller :fonticon:`fa fa-wrench`
===================================================================

.. sidebar: Docs test matrix
   We tested this documentation with:
   -
   - :code:`cf-bigip-ctlr` v1.0.0

This document describes the steps required to deploy the |cf-long| in `Cloud Foundry`_ or `Pivotal Cloud Foundry`_ using an `Application Manifest`_.

.. include:: /_static/reuse/beta-announcement-cf.rst

.. _cf-deployment-prereqs:

Before you begin
----------------

- `Enable Docker in Cloud Foundry`_ :fonticon:`fa fa-external-link`.
- `Create a User in Cloud Foundry`_ :fonticon:`fa fa-external-link` with `"routing.routes.read" permission`_.
- `Add the BIG-IP device to Cloud Foundry`_ :fonticon:`fa fa-external-link` as a custom load balancer.

.. _create-application-manifest:

Create an Application Manifest
------------------------------

Create a new Application Manifest file defining the |cf-long| `configuration parameters </products/connectors/cf-bigip-ctlr/latest/index.html#configuration-parameters>`_ you want to apply for your cloud.

The :code:`bigip` section of the example |cfctlr| manifest below does the following:

- provides the IP address and user account credentials for the BIG-IP device;
- defines the existing BIG-IP partition in which |cfctlr| should create objects;
- sets the load balancing method for the virtual server to round-robin;
- sets the interval at which the |cfctlr| attempts to verify BIG-IP settings;
- assigns an external IP address to the virtual server;
- assigns an existing BIG-IP traffic policy (:code:`/Common/bigip-traffic`) to the virtual server; and
- assigns an existing BIG-IP health monitor (:code:`/Common/tcp_half_open`) to the virtual server.

.. literalinclude:: /_static/config_examples/manifest.yaml
   :linenos:
   :caption: Example App Manifest for cf-bigip-ctlr

:fonticon:`fa fa-download` :download:`manifest.yaml </_static/config_examples/manifest.yaml>`


.. tip::

   If you want to use "x-forwarded-for" and "x-forwarded-proto" headers, add a BIG-IP traffic policy for each before you launch the |cfctlr| app.
   Add the :code:`policies` configuration parameter to the Application Manifest to assign the policies to the virtual server(s).


Push the |cfctlr| App to Cloud Foundry
--------------------------------------

Use the `Cloud Foundry CLI`_ :command:`cf push` command to deploy the |cfctlr| App.

.. code-block:: console

   cf push -o https://hub.docker.com/r/f5networks/cf-bigip-ctlr/ -f manifest.yaml

Verify Creation of BIG-IP Objects
---------------------------------

Policies
````````

The |cf-long| turns Cloud Foundry route tables into BIG-IP Local Traffic policies.
You should see a new policy on your BIG-IP device (there will be two if you're using https), with a rule for each route in your Cloud Foundry deployment.

#. Log in to the BIG-IP configuration utility at the management IP address (for example, :code:`https://10.190.25.228/xui`).
#. Choose the "cf" partition from the :guilabel:`Partition` dropdown menu.
#. Go to :menuselection:`Local Traffic --> Policies` to view a list of all policies in the partition.

Pools
`````

The |cf-long| also creates a pool and pool members for every route in your Cloud Foundry deployment.

You can use the BIG-IP configuration utility to verify that the pools and pool members exist.

#. Log in to the BIG-IP configuration utility at the management IP address (for example, :code:`https://10.190.25.228/xui`).
#. Choose the "cf" partition from the :guilabel:`Partition` dropdown menu.
#. Go to :menuselection:`Local Traffic --> Pools` to view a list of all pools in the partition.


.. _Enable Docker in Cloud Foundry: https://docs.cloudfoundry.org/adminguide/docker.html#run-monitor
.. _Create a User in Cloud Foundry: https://docs.cloudfoundry.org/adminguide/uaa-user-management.html
.. _"routing.routes.read" permission: https://docs.cloudfoundry.org/concepts/architecture/uaa.html#routing-scopes
.. _Add the BIG-IP device to Cloud Foundry: https://docs.pivotal.io/pivotalcf/1-7/opsguide/custom-load-balancer.html
