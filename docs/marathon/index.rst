F5 Container Integration - Marathon
=====================================

This document provides general information regarding the F5 Integration for Marathon.
Please refer to the guides below for deployment and usage instructions.

.. toctree::
   :caption: BIG-IP Controller Guides
   :maxdepth: 1

   Set up DC/OS auth <mctlr-authenticate-dcos>
   Deploy the BIG-IP Controller <mctlr-app-install>
   Manage BIG-IP objects <mctlr-manage-bigip-objects>
   Deploy iApps <mctlr-deploy-iapp>
   marathon-bigip-ctlr reference documentation <http://clouddocs.f5.com/products/connectors/marathon-bigip-ctlr/latest>

Overview
--------

The |mctlr-long|  (``marathon-bigip-ctlr``) configures BIG-IP objects for Applications in a `Mesos cluster`_, serving North-South traffic.
The |mctlr| is a container-based `Marathon Application`_ that runs within the Marathon cluster. It configures the BIG-IP device as needed to handle traffic for Apps within the cluster. You can :ref:`launch <install-mctlr>` the |mctlr| in Marathon via the `Marathon REST API`_ or the `Marathon Web Interface`_ [#mgui]_.

.. image:: /_static/media/cc_solution.png
   :scale: 65%
   :alt: Solution design: The Container Connector runs as an App within the cluster; it configures the BIG-IP device as needed to handle traffic for Apps in the cluster

The |mctlr| watches the Marathon API for special "F5 Application Labels" that tell it:

* what Marathon Application we want it to manage, and
* what BIG-IP LTM objects we want to create for that specific Application.

When the |mctlr| discovers new or updated Marathon Applications with the F5 Application Labels, it dynamically applies the desired settings to the BIG-IP device.

.. image:: /_static/media/mesos_flow.png
   :scale: 65%
   :alt: Diagram demonstrating how the BIG-IP Controller picks up configurations from F5 Application labels and applies the desired config to BIG-IP devices.


.. sidebar:: :fonticon:`fa fa-exclamation-circle` Important:

   The |mctlr| cannot manage objects in the ``/Common``  `BIG-IP partition`_.

You can use the |mctlr| to:

- :ref:`create BIG-IP LTM virtual servers <mctlr-create-vs>`
- :ref:`assign IP addresses to BIG-IP LTM virtual servers using IPAM <mctlr-ipam>`
- :ref:`create unattached BIG-IP LTM pools <mctlr-pool-only>` (pools without virtual servers)
- :ref:`deploy iApps <mctlr-deploy-iapps>`

General Prerequisites
`````````````````````

The F5 Container Integration for Mesos Marathon documentation set assumes that you:

- already have a `Mesos cluster`_ running;
- are familiar with the `Marathon Web Interface`_ ;
- are comfortable using `HTTP methods`_ to make REST API calls;
- already have a BIG-IP :term:`device` licensed and provisioned for your requirements; and
- are familiar with BIG-IP Local Traffic Manager (LTM) concepts and ``tmsh`` commands.

.. [#mgui] Per the Marathon documentation, the `Marathon Web Interface`_ is no longer actively developed. Use the Marathon REST API to access the latest Marathon features.

Key Apache Mesos/Marathon Concepts
----------------------------------

.. _app-labels:

Application Labels
``````````````````

In Marathon, you can `associate labels with Application tasks`_ for tracking/reporting purposes. The custom "F5 Application Labels" notify the |mctlr| that it has work to do. When the |mctlr| discovers Applications with new or updated F5 Application Labels, it dynamically creates BIG-IP virtual servers, pools, pool members, and HTTP :ref:`health monitors <health-checks>` for each of the Application's tasks.

See the `marathon-bigip-ctlr reference documentation`_ for the full list of F5 Application Labels.

.. tip::

   You can download the code example used in the following sections and modify it to suit your environment.

   :fonticon:`fa fa-download` :download:`f5-marathon-bigip-ctlr-example_pm_hc.json </marathon/config_examples/f5-marathon-bigip-ctlr-example_pm_hc.json>`

.. _iapps labels:

iApps Application Labels
~~~~~~~~~~~~~~~~~~~~~~~~

You can use the |mctlr| to deploy BIG-IP iApps using a special set of customizable iApps Application Labels. The iApp you want to deploy must already exist on the BIG-IP device (can be in the ``/Common`` partition).

A few of the key iApp Application Labels depend on the iApp you want to deploy, as well as your environment and needs. See the `marathon-bigip-ctlr reference documentation`_ for more information about the Application labels required for iApp deployment.

.. _port-mappings:

Port Mapping
````````````

In Marathon, container-based applications using Docker BRIDGE mode must have `port mappings`_ configured. [#dockerbridge]_ For Applications proxied by the |mctlr|, these port mappings make it possible for the BIG-IP device to route external traffic to `service ports`_ inside the Apache Mesos cluster. You can define multiple port mappings for a Marathon Application.

.. sidebar:: :fonticon:`fa fa-exclamation-circle` Important:

   Apache Mesos commonly restricts binding to ports in a specific range. Consult the Apache Mesos `ports resource`_ to see what ports are available in your cluster before defining service ports and/or port mappings for your applications. Incorrect port mappings may result in deployment failures.

Most F5 Application Labels let you specify an index into the port mapping array, beginning at ``0``.
These parameters include ``{n}`` in the label key; simply replace ``{n}`` with the port index to which you want the setting to apply.

.. rubric:: For example:

The code sample below defines an Application with three (3) port indices.

.. literalinclude:: /marathon/config_examples/f5-marathon-bigip-ctlr-example_pm_hc.json
   :caption: Define an Application 3 port indices
   :lines: 1-25
   :linenos:
   :emphasize-lines: 13-23


In the ``labels`` section, we specify that we want to create HTTP virtual servers on the BIG-IP device for port indices ``0`` and ``1``.
In this example, ``0`` refers to the first mapping defined above (``"containerPort": "8088"``) and ``1`` refers to the second (``"containerPort": "8188"``).

.. literalinclude:: /marathon/config_examples/f5-marathon-bigip-ctlr-example_pm_hc.json
   :caption: |mctlr| labels defining BIG-IP objects for two (2) port indices
   :lines: 26-40
   :lineno-start: 26

.. [#dockerbridge] See the `Docker Networking <https://docs.docker.com/engine/userguide/networking/>`_ documentation for more information.

.. _health-checks:

Marathon Health Checks
``````````````````````

The |mctlr| provides compatibilty with existing Marathon `Health Checks`_. For ports configured with Marathon health checks, the |mctlr|:

* creates corresponding BIG-IP health monitors;
* checks the specified port's health status *before* adding it to a BIG-IP pool. [#setuphealthchecks]_

.. rubric:: To continue the previous example:

.. literalinclude:: /marathon/config_examples/f5-marathon-bigip-ctlr-example_pm_hc.json
   :caption: Create health checks for each of the Application's port indices
   :lines: 41-67
   :lineno-start: 41


.. [#setuphealthchecks] Occurs when ``F5_CC_USE_HEALTHCHECK``'s value is "True".

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
