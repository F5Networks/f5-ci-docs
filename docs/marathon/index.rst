F5 Marathon Container Integration
=================================

Overview
--------

The F5 `Marathon`_ Container Integration consists of the `F5 Marathon BIG-IP Controller </products/connectors/marathon-bigip-ctlr/latest>`_, the `F5 Application Services Proxy </products/asp/latest>`_ (ASP), and the `F5 Marathon ASP Controller </products/connectors/marathon-asp-ctlr/latest>`_.

The |mctlr-long| configures BIG-IP Local Traffic Manager (LTM) objects for Applications in a `Mesos cluster`_, serving North-South traffic.

The |asp| provides load balancing and telemetry for containerized applications, serving East-West traffic. The |aspm-long| deploys ASP instances 'on-demand' for Marathon Applications.

.. image:: /_static/media/mesos_solution.png
   :scale: 50 %
   :alt: F5 Container Solution for Marathon


General Prerequisites
---------------------

The F5 Mesos/Marathon Integration's documentation set assumes that you:

- already have a `Mesos cluster`_ running;
- are familiar with the `Marathon Web Interface`_ ;
- are comfortable using `HTTP methods`_ to make REST API calls;
- already have a BIG-IP :term:`device` licensed and provisioned for your requirements; [#bigipcaveat]_ and
- are familiar with BIG-IP Local Traffic Manager (LTM) concepts and ``tmsh`` commands. [#bigipcaveat]_

.. [#bigipcaveat] Not required for the |asp| and ASP controllers (|aspk|, |aspm|).

|asp|
-----

The |asp| (ASP) provides container-to-container load balancing, traffic visibility, and inline programmability for applications.
Its light form factor allows for rapid deployment in datacenters and across cloud services.
The ASP integrates with container environment management and orchestration systems and enables application delivery service automation.

.. seealso:: `ASP product documentation </products/asp/latest/index.html>`_


|aspm-long|
-----------

The |aspm-long| -- |aspm| -- deploys the |asp|.
Like the |mctlr-long|, the |aspm-long| watches the Marathon API for Apps defined with a specific set of labels.
When it finds an Application configured with the ``f5-asp: enable`` label, it launches an instance of the |asp| to front the App and creates a virtual server on the |asp| instance.
The |aspm-long| maintains an address in the |asp| pool configuration for each of an Application's tasks.

The |aspm-long| App definition contains a set of default `Marathon ASP configuration labels </products/connectors/marathon-asp-ctlr/latest/index.html#configuration-parameters>`_.
These configurations -- set in the "env" (or, "Environment", in the Web UI) section of the |aspm| :ref:`App definition <install-asp-marathon>` -- apply to each ASP instance the |aspm| launches.
The |aspm-long| also has a set of "override" labels. [#overridelabel]_
When you add these labels to the definition for an Application you want the ASP to proxy, they take precedence over the default |aspm| settings.


By default, the |aspm| starts one (1) |asp| instance per application.
You can override this setting using the ``ASP_COUNT_PER_APP`` :ref:`F5 application label <app-labels>`.

The |asp| collects traffic statistics for the Applications it load balances; these stats are either logged locally or sent to an external analytics application.
You can set the location and type of the analytics application using the ``ASP_DEFAULT_STATS_URL`` label.

.. todo:: add "Export ASP Stats to an analytics provider"

.. [#overridelabel] See the `Marathon ASP configuration labels </products/connectors/marathon-asp-ctlr/latest/index.html#configuration-parameters>`_ table.

|mctlr-long|
------------

The |mctlr-long| is a container-based `Marathon Application`_ -- |mctlr|.
You can :ref:`launch <install-mctlr>` the |mctlr-long| in Marathon via the `Marathon REST API`_ or the `Marathon Web Interface`_.

The |mctlr| watches the Marathon API for special "F5 Application Labels" that tell it:

* what Marathon Application we want it to manage, and
* what BIG-IP LTM objects we want to create for that specific Application.

When the |mctlr-long| discovers new or updated Marathon Applications with the F5 Application Labels, it dynamically applies the desired settings to the BIG-IP device.

.. important::

   The |mctlr-long| cannot manage objects in the ``/Common``  `BIG-IP partition`_.


You can use the |mctlr-long| to:

- :ref:`create BIG-IP LTM virtual servers <mctlr-create-vs>`
- :ref:`assign IP addresses to BIG-IP LTM virtual servers using IPAM <mctlr-ipam>`
- :ref:`create unattached BIG-IP LTM pools <mctlr-pool-only>` (pools without virtual servers)
- :ref:`deploy iApps <mctlr-deploy-iapps>`


Key Apache Mesos/Marathon Concepts
----------------------------------

.. _app-labels:

Application Labels
``````````````````

In Marathon, you can `associate labels with Application tasks`_ for tracking/reporting purposes.
We've developed a set of custom "F5 Application Labels" as a way notify the |mctlr-long| and |aspm-long| that they have work to do.

When the |mctlr-long| discovers Applications with new or updated F5 Application Labels, it dynamically creates BIG-IP virtual servers, pools, pool members, and HTTP :ref:`health monitors <health-checks>` for each of the Application's tasks.

When the |aspm-long| discovers Applications configured with the ``"f5-asp": "enable"`` label, it launches an ASP instance for that app.
F5 Application Labels define the ASP configurations.

See the |mctlr| `product documentation </products/connectors/marathon-bigip-ctlr/latest/>`_ for the full list of F5 Application Labels.

.. tip::

   You can download the code example used in the following sections and modify it to suit your environment.

   :fonticon:`fa fa-download` :download:`f5-marathon-bigip-ctlr-example_pm_hc.json </_static/config_examples/f5-marathon-bigip-ctlr-example_pm_hc.json>`



iApps Application Labels
~~~~~~~~~~~~~~~~~~~~~~~~

You can use the |mctlr-long| to deploy BIG-IP iApps using a special set of customizable iApps Application Labels. The iApp you want to deploy must already exist on the BIG-IP device (can be in the ``/Common`` partition).

A few of the key iApp Application Labels depend on the iApp you want to deploy, as well as your environment and needs.
See :ref:`Required iApp Application Labels <marathon-required-iapp-labels>` and the `marathon-bigip-ctlr product documentation </products/connectors/marathon-bigip-ctlr/latest/>`_ for more information.


Apache Mesos DNS and ASP Discovery
``````````````````````````````````

Each |asp| instance is discoverable via an Apache Mesos DNS SRV query, which returns its IP address, port, and protocol.
By convention, the DNS name of an |asp| instance for an Application is “<ASP_ENABLE_LABLE>-<application name>.<domain name>”.

For example:

- ``ASP_ENABLE_LABEL``: ASP +
- Application name: “app1” +
- Domain name: “marathon.mesos” =
- ASP DNS name: “ASP-app1.marathon.mesos”

.. _port-mappings:

Port Mapping
````````````

In Marathon, container-based applications using Docker BRIDGE mode must have `port mappings`_ configured. [#dockerbridge]_
For Applications proxied by the |mctlr-long|, these port mappings make it possible for the BIG-IP device to route external traffic to `service ports`_ inside the Apache Mesos cluster.
You can define multiple port mappings for a Marathon Application.

.. important::

   Apache Mesos commonly restricts binding to ports in a specific range.
   Consult the Apache Mesos `ports resource`_ to see what ports are available in your cluster before defining service ports and/or port mappings for your applications.

   Incorrect port mappings may result in deployment failures.
   See :ref:`Troubleshooting your Marathon deployments <troubleshoot-marathon>` for more information.

Most F5 Application Labels let you specify an index into the port mapping array, beginning at ``0``.
These parameters include ``{n}`` in the label key; simply replace ``{n}`` with the port index to which you want the setting to apply.

.. rubric:: For example:

The code sample below defines an Application with three (3) port indices.

.. literalinclude:: /_static/config_examples/f5-marathon-bigip-ctlr-example_pm_hc.json
   :caption: Service definition with multiple ports
   :lines: 1-25
   :linenos:
   :emphasize-lines: 13-23


In the ``labels`` section, we specify that we want to create HTTP virtual servers on the BIG-IP device for port indices ``0`` and ``1``.
In this example, ``0`` refers to the first mapping defined above (``"containerPort": "8088"``) and ``1`` refers to the second (``"containerPort": "8188"``).

.. literalinclude:: /_static/config_examples/f5-marathon-bigip-ctlr-example_pm_hc.json
   :caption: |mctlr| labels defining BIG-IP objects for two (2) port indices
   :lines: 26-40
   :lineno-start: 26

.. [#dockerbridge] See the `Docker Networking <https://docs.docker.com/engine/userguide/networking/>`_ documentation for more information.

.. _health-checks:

Marathon Health Checks
``````````````````````

The |mctlr-long| provides compatibilty with existing Marathon `Health Checks`_.
For ports configured with Marathon health checks, the |mctlr|:

* creates corresponding BIG-IP health monitors;
* checks the specified port's health status *before* adding it to a BIG-IP pool. [#setuphealthchecks]_

.. rubric:: To continue our example:

Here, we create health checks for each of the port indices defined for our Application.

.. literalinclude:: /_static/config_examples/f5-marathon-bigip-ctlr-example_pm_hc.json
   :caption: Defining health checks for multiple ports
   :lines: 41-66
   :lineno-start: 41


.. [#setuphealthchecks] Occurs when ``F5_CC_USE_HEALTHCHECK``'s value is "True".


Related
-------

.. toctree::
   :glob:

   mctlr*
   asp*
   marathon-bigip-ctlr docs <http://clouddocs.f5.com/products/connectors/marathon-bigip-ctlr/latest/>
   marathon-asp-ctlr docs <http://clouddocs.f5.com/products/connectors/marathon-asp-ctlr/latest/>
   F5 Application Services Proxy docs <http://clouddocs.f5.com/products/asp/latest>

.. _Marathon Application: https://docs.mesosphere.com/1.8/overview/concepts/#marathon-application
.. _Marathon REST API: https://mesosphere.github.io/marathon/api-console/index.html
.. _Mesos cluster: https://docs.mesosphere.com/1.8/overview/concepts/#dcos-cluster
.. _HTTP methods: http://restfulapi.net/http-methods/
.. _associate labels with Application tasks: https://dcos.io/docs/1.7/usage/tutorials/task-labels/
.. _port mappings: https://mesosphere.github.io/marathon/docs/ports.html
.. _Health Checks: https://mesosphere.github.io/marathon/docs/health-checks.html
.. _Marathon documentation: https://mesosphere.github.io/marathon/docs/
.. _ports resource: http://mesos.apache.org/documentation/latest/attributes-resources/
.. _service ports: https://mesosphere.github.io/marathon/docs/ports.html

