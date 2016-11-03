F5 |lwpc|
=========

Overview
--------

The F5® |lwpc| |tm| (LWPC) provides internal load balancing and service discovery in a Mesos cluster. It watches Marathon's event stream for changes in applications and automatically starts, stops, and/or reconfigures the F5 |lwp| |tm| (LWP) app as needed. The |lwp|, in turn, watches Marathon to automatically load balance across an application's tasks as the application is scaled.

Use Case
````````

The F5 |lwpc| dynamically deploys the F5 |lwp|. Together, they provide responsive and scalable load balancing services for East-West data center traffic (in other words, traffic flowing between apps/microservices).

Prerequisites
`````````````

In order to use the |lwpc|, you will need the following:

- An existing, functional `Mesos`_ `Marathon`_ deployment.
- The official F5 ``lwp-controller`` image pulled from the `F5 Docker registry`_.
- Internet access (required for pulling the image from Docker).

Caveats
```````
None

Install the |lwpc|
------------------

The |lwpc| can be installed as a `Marathon App`_ via the `Marathon REST API <https://mesosphere.github.io/marathon/docs/generated/api.html>`_ or the `Marathon UI <https://mesosphere.github.io/marathon/docs/marathon-ui.html>`_. Both options use the same set of :ref:`configuration parameters <cscm_configuration-parameters>`, formatted as a valid JSON blob.

Install via a JSON config file
``````````````````````````````

* Create a JSON file containing the correct configurations for your environment.

    .. literalinclude:: /static/f5-lwpc/f5-lwp-controller.json
        :emphasize-lines: 2, 9, 17-29

    :download:`f5-lwp-controller.json </static/f5-lwpc/f5-lwp-controller.json>`


Launch the |lwpc| App via the Marathon REST API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Send a POST request to the Marathon server that references your JSON config file.

    .. code-block:: bash

        $ curl -X POST -H "Content-Type: application/json" http://<marathon-ip-addr>:8080/v2/apps -d @f5-lwp-controller.json

Launch the |lwpc| via the Marathon UI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. Click the :guilabel:`Create Application` button.
#. Toggle the :guilabel:`JSON Mode` switch.
#. Paste in your JSON blob.
#. Click :guilabel:`Create Application`.


Configure the |lwpc|
--------------------

The F5® |lwpc| can be configured, using the parameters below, with valid JSON. The service configuration details are stored in Marathon application labels.

.. important::

    The configurations you set for the |lwpc| controller app will apply to each instance of the |lwp| it launches. If you want to override these settings for specific apps, use the label in the "Override Label" column of the table.

.. _lwpc_configuration-parameters:

.. include:: /includes/f5-lwpc/ref_lwpc-table-configuration-parameters.rst


Usage
-----

Deploy an App and Activate the |lwp| with the Default Configurations
````````````````````````````````````````````````````````````````````

The example below demonstrates how to deploy the F5 |lwp| when launching a new app in Marathon. All you need to do to insert the lightweight proxy to front and load balance the service is include the label ``"lwp": "enable"`` in the service definition.

    .. code-block:: json

          "labels": {
            "lwp": "enable"
          },

The |lwpc| will notice that an application is being spun up that it needs to control and will create an instance of the |lwp| in front of the application using the default configurations.

    .. literalinclude:: /static/f5-lwpc/lwpc_example_app_defaults.json
        :emphasize-lines: 23-24



Deploy an App and Activate the |lwp| with Custom Configurations
```````````````````````````````````````````````````````````````

The example below demonstrates how to deploy the F5 |lwp| when launching a new app in Marathon and override the |lwpc|'s default configurations.

The |lwpc| will notice that an application is being spun up that it needs to control and will create an instance of the |lwp| in front of the application using the custom configurations specified in the JSON.

    .. literalinclude:: /static/f5-lwpc/lwpc_example_app_custom.json
        :emphasize-lines: 23-29


Further Reading
---------------

.. seealso::

    * :ref:`Configure the Lightweight Proxy <lwp-configuration-guide>`





