F5 |lwpc|
=========

Overview
--------

.. lwpc-overview-body-start

The F5® |lwpc| |tm| (LWPC) deploys the :ref:`Lightweight Proxy <lwp-home>` in a Mesos+Marathon cluster. It watches Marathon's event stream for changes in applications and automatically starts, stops, and/or reconfigures the F5 |lwp| |tm| (|lwp|) app as needed. The |lwp|, in turn, watches Marathon to automatically load balance across an application's tasks as the application is scaled.

.. lwpc-overview-body-end

Use Case
--------

Together, F5 |lwpc| and |lwp| provide responsive and scalable load balancing services for East-West data center traffic (in other words, traffic flowing between apps/microservices).

Prerequisites
-------------

.. lwpc-prereqs-body-start

- An existing, functional `Mesos`_ `Marathon`_ deployment.
- The official F5 ``lwp-controller`` and ``light-weight-proxy`` images; contact your F5 Sales rep or go to `F5 DevCentral <https://devcentral.f5.com/welcome-to-the-f5-beta-program>`_ to join the Early Access program.
- Internet access (required to pull images from Docker).

.. lwpc-prereqs-body-end

Caveats
```````

None.


.. _lwpc-install-section:

.. lwpc-install-section-start

Install the |lwpc|
------------------

.. lwpc-install-body-start

The |lwpc| is a `Marathon Application <https://mesosphere.github.io/marathon/docs/application-basics.html>`_, defined using valid JSON.
You can install the App via either the `Marathon REST API <https://mesosphere.github.io/marathon/docs/generated/api.html>`_ or the `Marathon UI <https://mesosphere.github.io/marathon/docs/marathon-ui.html>`_.

The default configurations that will be used to deploy the |lwp| should be defined in the ``env`` section of the Application service definition.
To override these settings, include the appropriate |lwpc| configuration parameters in the service definition when deploying or updating an App in Marathon.

.. seealso::

    * |lwpc| :ref:`configuration parameters <lwpc-configuration>`
    * |lwp| :ref:`configuration parameters <lwp-configuration>`

.. lwpc-install-body-intro-end


Launch the |lwpc| App via the Marathon REST API
```````````````````````````````````````````````

.. launch-lwpc-REST-body-start

#. Create a JSON file containing the correct configurations for your environment.

    .. literalinclude:: /static/f5-lwpc/f5-lwp-controller.json
        :language: json
        :emphasize-lines: 2, 9, 17-29
        :linenos:
        :name: f5-lwp-controller-json

    :download:`f5-lwp-controller.json </static/f5-lwpc/f5-lwp-controller.json>`

#. Send a POST request that references your JSON config file to the Marathon server.

    .. code-block:: bash

        $ curl -X POST -H "Content-Type: application/json" http://<marathon-url>:8080/v2/apps -d @f5-lwp-controller.json

.. launch-lwpc-REST-body-end

Launch the |lwpc| via the Marathon UI
`````````````````````````````````````

.. launch-lwpc-UI-body-start

#. Click the :guilabel:`Create Application` button.
#. Complete the :guilabel:`Docker Container Settings` section:

    ===================   ============================
    Field                 Setting
    ===================   ============================
    Image                 <f5-lwp-controller-image>
    Network               Bridge
    Force Pull Image      user defined
    Privileges            unchecked
    ===================   ============================

#. Provide the |lwpc| :ref:`configurations <lwpc_configuration-parameters>` in the :guilabel:`Labels` section.

#. Click :guilabel:`Create Application`.

.. launch-lwpc-UI-body-end

.. lwpc-install-body-end

.. lwpc-install-section-end

.. _lwpc-configuration-section:

Configure the |lwpc|
--------------------

.. lwpc-configuration-body-start

The F5® |lwpc| can be configured with valid JSON using the parameters below. The service configuration details are stored in Marathon application labels.

.. important::

    The configurations you set for the |lwpc| controller app will apply to each instance of the |lwp| it launches. If you want to override these settings for specific apps, use the label in the "Override Label" column of the table.

.. _lwpc_configuration-parameters:

.. include:: /includes/f5-lwpc/ref_lwpc-table-configuration-parameters.rst

.. lwpc-configuration-body-end

.. _lwpc-usage-section:

Usage
-----

.. lwpc-usage-body-start

The F5® |lwpc| deploys the an F5 |lwp| instance when a new Marathon app is launched, or when the configuration for an existing App is edited.
The |lwpc| monitors Marathon application services; when it finds an application service with the ``lwp: enable`` label, it launches an instance of the |lwp| to front the App and creates a virtual server on the |lwp| instance.

The |lwpc| maintains an address in the pool configuration of the |lwp| for each Application task, which manages traffic for that application.
An Application needing access to another Application that's load balanced by the |lwp| connects to the |lwp| instance for that Application.

The address of each |lwp| instance is discoverable via a Mesos DNS SRV query, which provides the IP address, port, and protocol of the |lwp| instance. By convention, the DNS name of a |lwp| for an Application is “lwp-<application name>.<domain name>”. So, for example, if an Application is named “app1” and the domain is “marathon.mesos”, the DNS name of the |lwp| for that Application will be “lwp-app1.marathon.mesos”.

By default, the |lwpc| starts **one |lwp| instance per application**. The default behavior can be overridden using labels, as described in the :ref:`configuration section <lwpc-configuration-section>`.

The |lwp| collects traffic statistics for the Applications it load balances, which can be sent to an analytics application. The location and type of the analytics application can be configured on the |lwpc| via the ``LWP_DEFAULT_STATS_URL`` parameter.

.. lwpc-usage-body-intro-end

Create a Default |lwp| Virtual Server via the Marathon REST API
```````````````````````````````````````````````````````````````

.. lwpc-create-vs-DEFAULT-body-start

#. Include the ``"lwp": "enable"`` label in the service definition for your App.

   The |lwpc| discovers that an App has the ``"lwp": "enable"`` label and creates an instance of the |lwp| in front of the application using the default :ref:`configurations <lwpc_configuration-parameters>`.

    .. literalinclude:: /static/f5-lwpc/lwpc_example_app_defaults.json
        :language: json
        :emphasize-lines: 21-23
        :linenos:
        :name: app_lwp-enabled-json

    :download:`lwpc_example_app_defaults.json </static/f5-lwpc/lwpc_example_app_defaults.json>`

#. Send a POST request to the Marathon server that references your JSON file.

    .. code-block:: bash

        $ curl -X POST -H "Content-Type: application/json" http://<marathon-url>:8080/v2/apps -d @app_lwp-enabled.json

.. lwpc-create-vs-DEFAULT-body-end

Create a Custom |lwp| Virtual Server via the Marathon REST API
``````````````````````````````````````````````````````````````

.. lwpc-create-vs-CUSTOM-body-start

#. Include the ``"lwp": "enable"`` label in the service definition for your App.

#. Include your custom configurations in the ``"labels"`` section of the service definition.

   The |lwpc| discovers that an App has the ``"lwp": "enable"`` label and creates an instance of the |lwp| in front of the application. The custom configurations specified in the labels section for ``LWP_LOG_LEVEL`` and ``LWP_VS_KEEP_ALIVE`` will override the default configurations.

    .. literalinclude:: /static/f5-lwpc/lwpc_example_app_custom.json
        :language: json
        :emphasize-lines: 21-25
        :linenos:
        :name: app_custom-lwp-enabled-json

    :download:`lwpc_example_app_custom.json </static/f5-lwpc/lwpc_example_app_custom.json>`

#. Send a POST request to the Marathon server that references your JSON file.

    .. code-block:: bash

        $ curl -X POST -H "Content-Type: application/json" http://<marathon-url>:8080/v2/apps -d @app_custom-lwp-enabled.json

.. lwpc-create-vs-CUSTOM-body-end



Further Reading
---------------

.. seealso::

    * F5 |lwp| :ref:`User Guide <lwp-user-guide>`


.. lwpc-usage-body-end


