F5 Marathon Container Integration
=================================

Overview
--------

The F5 `Marathon`_ Container Integration consists of the `F5 Marathon BIG-IP Controller </products/connectors/marathon-bigip-ctlr/latest>`_, the `F5 Application Service Proxy </products/asp/latest>`_ (ASP), and the `F5 Marathon ASP Controller </products/connectors/marathon-asp-ctlr/latest>`_.

The |mctlr-long| configures a BIG-IP to expose applications in a `Mesos cluster`_ as BIG-IP virtual servers, serving North-South traffic.

The |asp| provides load balancing and telemetry for containerized applications, serving East-West traffic. The |aspm-long| deploys ASP instances 'on-demand' for Marathon Applications.

.. image:: /_static/media/mesos_solution.png
    :scale: 50 %
    :alt: F5 Container Solution for Marathon


General Prerequisites
---------------------

This documentation set assumes that you:

- already have a `Mesos cluster`_ running;
- are familiar with the `Marathon Web Interface`_ ;
- are comfortable using `HTTP methods`_ to make REST API calls;
- already have a BIG-IP :term:`device` licensed and provisioned for your requirements; [#bigipcaveat]_ and
- are familiar with BIG-IP Local Traffic Manager (LTM) concepts and ``tmsh`` commands. [#bigipcaveat]_

.. [#bigipcaveat] Not required for the |asp| .

|asp|
-----

The |asp| (ASP) provides container-to-container load balancing, traffic visibility, and inline programmability for applications. Its light form factor allows for rapid deployment in datacenters and across cloud services. The ASP integrates with container environment management and orchestration systems and enables application delivery service automation.

|aspm-long|
-----------

The |aspm-long| -- |aspm| -- deploys the |asp|. Like the |mctlr-long|, the |aspm-long| watches the Marathon API for Apps defined with a specific set of labels. When it finds an Application configured with the ``asp: enable`` label, it launches an instance of the |asp| to front the App and creates a virtual server on the |asp| instance. The |aspm-long| maintains an address in the |asp| pool configuration for each of an Application's tasks.

The |aspm-long| App definition contains a set of default `configuration parameters <tbd>`_. These configurations -- set in the "env" (or, "Environment", in the Web UI) section of the |aspm| :ref:`App definition <install-asp-marathon>` -- apply to each ASP instance the |aspm| launches.
The |aspm-long| also has a set of "override" labels. [#overridelabel]_ When you add these labels to the definition for an Application you want the ASP to proxy, they take precedence over the default |aspm| settings.

By default, the |aspm| starts one (1) |asp| instance per application. You can override this setting using the ``ASP_COUNT_PER_APP`` :ref:`F5 application label <app-labels>`.

The |asp| collects traffic statistics for the Applications it load balances; these stats are either logged locally or sent to an external analytics application. You can set the location and type of the analytics application using the ``ASP_DEFAULT_STATS_URL`` label.

.. seealso:: :ref:`Export ASP Stats to an analytics provider <tbd>`


.. [#overridelabel] See the |aspm| `configuration parameters <tbd>`_ table.


|mctlr-long|
------------

The |mctlr-long| is a container-based `Marathon Application`_ -- |mctlr|. You can :ref:`launch <install-mctlr>` the |mctlr-long| in Marathon via the `Marathon REST API`_ or the `Marathon Web Interface`_.

The |mctlr| watches the Marathon API for special "F5 Application Labels" that tell it:

    a) what Application we want it to manage, and
    b) how we want to configure the BIG-IP for that specific Application.


You can :ref:`manage BIG-IP objects <mctlr-manage-bigip-objects>` directly, or :ref:`deploy iApps <mctlr-deploy-iapps>`, with the |mctlr-long|.

Key Mesos/Marathon Concepts
---------------------------

.. _app-labels:

Application Labels
``````````````````

In Marathon, you can `associate labels with Application tasks`_ for tracking/reporting purposes. We've developed a set of custom "F5 Application Labels" as a way notify the |mctlr-long| and |aspm-long| that they have work to do.

When the |mctlr-long| discovers Applications with new or updated F5 Application Labels, it dynamically creates virtual servers, pools, pool members, and HTTP health monitors for each of the Application's tasks.

When the |aspm-long| discovers Applicaitons configured with the ``"asp": "enable"`` label, it launches an ASP instance for that app. The ASP configurations are also defined with F5 Application Labels.

See the |mctlr| `product documentation </products/connectors/marathon-bigip-ctlr/latest/>`_ for the full list of F5 Application Labels.

.. tip::

    You can :download:`download the code example </_static/config_examples/f5-marathon-bigip-ctlr-example_pm_hc.json>` used in the next few sections and modify it to suit your needs.



Mesos DNS and ASP Discovery
```````````````````````````

Each |asp| instance is discoverable via a Mesos DNS SRV query, which returns its IP address, port, and protocol.
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
For Applications proxied by the |mctlr-long|, these port mappings make it possible for the BIG-IP to route external traffic to `service ports`_ inside the Mesos cluster. You can define multiple port mappings for a Marathon Application.

.. important::

    Mesos commonly restricts binding to ports in a specific range. Consult the Mesos `ports resource`_ to see what ports are available in your cluster before defining service ports and/or port mappings for your applications.

    Incorrect port mappings may result in deployment failures. See :ref:`Troubleshooting your Marathon deployments <troubleshoot-marathon>` for more information.

Most F5 Application Labels let you specify an index into the port mapping array, beginning at ``0``. These parameters include ``{n}`` in the label key; simply replace ``{n}`` with the port index to which you want the setting to apply.

.. rubric:: For example:

The code sample below defines an Application with three (3) port indices.

.. literalinclude:: /_static/config_examples/f5-marathon-bigip-ctlr-example_pm_hc.json
    :caption: Service definition with multiple ports
    :lines: 1-24
    :linenos:
    :emphasize-lines: 13-15, 16-18, 19-21


In the ``labels`` section, we specify that we want to create HTTP virtual servers on the BIG-IP for port indices ``0`` and ``1``.
In this example, ``0`` refers to the first mapping defined above (``"containerPort": "8088"``) and ``1`` refers to the second (``"containerPort": "8188"``).

.. literalinclude:: /_static/config_examples/f5-marathon-bigip-ctlr-example_pm_hc.json
    :caption: |mctlr| labels defining BIG-IP objects for two (2) port indices
    :lines: 25-33
    :lineno-start: 25

.. [#dockerbridge] See the `Docker Networking <https://docs.docker.com/engine/userguide/networking/>`_ documentation for more information.

.. _health-checks:

Marathon Health Checks
``````````````````````

The |mctlr-long| provides compatibilty with existing Marathon `Health Checks`_. For ports configured with Marathon health checks, the |mctlr|:

    * creates corresponding health monitors on the BIG-IP;
    * checks the specified port's health status *before* adding it to a pool on the BIG-IP. [#setuphealthchecks]_

.. rubric:: To continue our example:

Here, we create health checks for each of the port indices defined for our Application.

.. literalinclude:: /_static/config_examples/f5-marathon-bigip-ctlr-example_pm_hc.json
    :caption: Defining health checks for multiple ports
    :lines: 33-61
    :lineno-start: 33


.. [#setuphealthchecks] When the ``F5_CC_USE_HEALTHCHECK`` configuration parameter is set to "True".



Related
-------

.. toctree::
    :glob:

    mctlr*
    asp*

- `|mctlr| </products/connectors/marathon-bigip-ctlr/latest/>`_
- `|aspm| </products/connectors/marathon-asp-ctlr/latest/>`_
- `asp </products/asp/latest>`_

.. _Marathon Application: https://docs.mesosphere.com/1.8/overview/concepts/#marathon-application
.. _Marathon REST API: https://mesosphere.github.io/marathon/api-console/index.html
.. _Mesos cluster: https://docs.mesosphere.com/1.8/overview/concepts/#dcos-cluster
.. _Marathon Web Interface: https://mesosphere.github.io/marathon/docs/marathon-ui.html
.. _HTTP methods: http://restfulapi.net/http-methods/
.. _associate labels with Application tasks: https://dcos.io/docs/1.7/usage/tutorials/task-labels/
.. _port mappings: https://mesosphere.github.io/marathon/docs/ports.html
.. _Health Checks: https://mesosphere.github.io/marathon/docs/health-checks.html
.. _Marathon documentation: https://mesosphere.github.io/marathon/docs/
.. _ports resource: http://mesos.apache.org/documentation/latest/attributes-resources/
.. _service ports: https://mesosphere.github.io/marathon/docs/ports.html

