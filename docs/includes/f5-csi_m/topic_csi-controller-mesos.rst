F5 |csi_m|
==========


Overview
--------

.. csim-overview-body-start

The F5® |csi| (CSI) makes L4-L7 services available to users deploying miscroservices-based applications in a containerized infrastructure. [#]_ The |csi_m-long| allows you to configure load balancing on a BIG-IP®  using the `Mesos`_ `Marathon`_ orchestration platform.

.. [#] See `Using Docker Container Technology with F5 Products and Services <https://f5.com/resources/white-papers/using-docker-container-technology-with-f5-products-and-services>`_.

.. csim-overview-body-end

Architecture
------------

.. csim-architecture-body-start

The |csi_m| is a Docker container that can run as a `Marathon Application <https://mesosphere.github.io/marathon/docs/application-basics.html>`_. Once installed, it watches for the creation/destruction of Marathon Apps with the :ref:`F5 Marathon application labels <f5-application-labels>` applied. When it finds an App configured with the F5 labels, the CSI  automatically updates the configuration of the BIG-IP as follows:

    - matches Marathon Apps to a specified BIG-IP partition;
    - creates a virtual server and pool in the specified partition on the BIG-IP for each `port-mapping <https://mesosphere.github.io/marathon/docs/ports.html>`_ ;
    - creates a pool member for each App task and adds the member to the default pool;
    - creates a health monitor on the BIG-IP for each pool member, if the application has a Marathon Health Monitor configured.

.. csim-architecture-body-end

Use Case
--------

The F5 |csi_m| makes it possible to manage BIG-IP Local Traffic Manager™ (LTM®) services for North-South traffic (i.e., traffic in and out of the data center) via the Marathon API or GUI. It can be used in conjunction with the F5 :ref:`Lightweight Proxy <lwp-home>`, which provides services for East-West traffic (i.e., traffic between services/apps in the data center).

Prerequisites
-------------

.. csim-prereqs-body-start

- Licensed, operational `BIG-IP`_ :term:`device`.
- Knowledge of BIG-IP `system configuration`_ and `local traffic management`_.
- An existing, functional `Mesos`_ `Marathon`_ deployment.
- Administrative access to both the BIG-IP and Marathon. [#]_
- A BIG-IP :term:`partition` that will only be used by the |csi_m|.
- The official F5 ``f5-marathon-lb`` image; contact your F5 Sales rep or go to `F5 DevCentral <https://devcentral.f5.com/welcome-to-the-f5-beta-program>`_ to join the Early Access program.


.. [#] Admin access to the BIG-IP is required to create the :term:`partition` the CSI will manage. CSI users only need permission to configure objects in their partition.


Caveats
```````

- |csi_m| can not manage the "Common" partition on the BIG-IP.
- You must create the partition you wish to manage from Marathon on the BIG-IP *before* configuring the CSI.

.. csim-prereqs-end



.. _csim-installation-section:

.. csim-install-section-start

Install the |csi_m|
-------------------

.. csim-install-body-start

The |csi_m| can be installed as a `Marathon Application <https://mesosphere.github.io/marathon/docs/application-basics.html>`_ via the `Marathon REST API <https://mesosphere.github.io/marathon/docs/generated/api.html>`_, the `Marathon UI <https://mesosphere.github.io/marathon/docs/marathon-ui.html>`_, or the command line. All options use the same set of :ref:`configuration parameters <csim_configuration-parameters>`.


Launch the |csi_m| App via the Marathon REST API
````````````````````````````````````````````````

#. Create a JSON configuration file with the correct ``env`` parameters for your BIG-IP :term:`device` and Marathon.

    .. rubric:: Example

    .. code-block:: json
        :caption: f5-marathon-lb.json

        {
          "id": "f5-marathon-lb",
          "cpus": 0.5,
          "mem": 64.0,
          "instances": 1,
          "container": {
            "type": "DOCKER",
            "docker": {
              "image": "<f5-marathon-lb-container>",
              "network": "BRIDGE"
            }
          },
          "env": {
            "MARATHON_URL": "<marathon_url>:8080",
            "F5_CSI_PARTITIONS": "<bigip_partition_for_mesos_apps>",
            "F5_CSI_BIGIP_HOSTNAME": "<bigip_admin_console>",
            "F5_CSI_BIGIP_USERNAME": "<bigip_username>",
            "F5_CSI_BIGIP_PASSWORD": "<bigip_password>"
          }
        }

#. Send a POST request that references your JSON config file to the Marathon server.

    .. code-block:: bash

        $ curl -X POST -H "Content-Type: application/json" http://<marathon_url>:8080/v2/apps -d @f5-marathon-lb.json


Launch the |csi_m| App via the Marathon UI
``````````````````````````````````````````

#. Click the :guilabel:`Create Application` button.
#. Complete the :guilabel:`Docker Container Settings` section:

    =================   =========================
    Field               Setting
    =================   =========================
    Image               f5-marathon-lb-container
    Network             Bridge
    Force Pull Image    user defined
    Privileges          unchecked
    =================   =========================

#. Complete the :guilabel:`Environment variables` section as appropriate for your environment.
#. Click :guilabel:`Create Application`.


Launch the |csi_m| App with Enhanced DC/OS Security Features
````````````````````````````````````````````````````````````

.. versionadded:: 0.2.0
    Support for the enhanced `cluster security features <https://docs.mesosphere.com/1.8/overview/features/#identity-access-mgmt>`_ in `Mesos DC/OS v1.8 <https://docs.mesosphere.com/1.8/overview/>`_.

DC/OS Open
^^^^^^^^^^

`DC/OS Open <https://dcos.io/>`_ uses `DC/OS oauth <https://dcos.io/docs/1.8/administration/id-and-access-mgt/#user-management>`_ to secure access. To use the |csi_m| App, assign it a user account with permission to access the desired cluster(s).

#. `Create a user account for the App <https://dcos.io/docs/1.8/administration/id-and-access-mgt/managing-authentication>`_

#. `Generate the HTTP API token <https://dcos.io/docs/1.8/administration/id-and-access-mgt/auth-api/>`_ and record it in a safe place.

#. Add the token to your |csi_m| App definition using the ``F5_CSI_DCOS_AUTH_TOKEN`` :ref:`configuration parameter <csim_configuration-parameters>`.

#. :ref:`Launch the CSI App <csim-installation-section>`.


DC/OS Enterprise
^^^^^^^^^^^^^^^^

`DC/OS Enterprise <https://docs.mesosphere.com/>`_ provides fine-grained access control via `Service Accounts <https://docs.mesosphere.com/1.8/administration/id-and-access-mgt/service-auth/>`_.

If you want to use the ``permissive`` or ``strict`` `Security Mode <https://docs.mesosphere.com/1.8/administration/installing/custom/configuration-parameters/#security>`_, you'll need to create a Service Account for the |csi_m|.
If you set Security Mode to `disabled`, creating a Service Account for the |csi_m| is optional.

#. `Create a Service Account <https://docs.mesosphere.com/1.8/administration/id-and-access-mgt/service-auth/custom-service-auth>`_ with the permissions shown below.

    ================================================   =======
    Resource                                           Action
    ================================================   =======
    ``dcos:adminrouter:service:marathon``              full
    ``dcos:service:marathon:marathon:admin:events``    read
    ``dcos:service:marathon:marathon:services:/``      read
    ================================================   =======

#. Obtain the certificate for your cluster:

    .. code-block:: bash

       $ curl -k -v https://<cluster-url>/ca/dcos-ca.crt -o dcos-ca.crt

    .. important::

        If you don't provide a server certificate, server-certificate validation will not be performed.

#. Add the service account and certificate to your App definition using the ``F5_CSI_DCOS_AUTH_CREDENTIALS`` and ``F5_CSI_MARATHON_CA_CERT`` :ref:`configuration parameters <csim_configuration-parameters>`, respectively.

    .. important::

        ``F5_CSI_DCOS_AUTH_CREDENTIALS`` is a JSON object; use of escaped quotes is required.

    .. code-block:: json
        :caption: Example JSON configuration with ``F5_CSI_DCOS_AUTH_CREDENTIALS`` and ``F5_CSI_MARATHON_CA_CERT``
        :linenos:
        :emphasize-lines: 19, 20

        {
          "id": "f5-marathon-lb",
          "cpus": 0.5,
          "mem": 64.0,
          "instances": 1,
          "container": {
            "type": "DOCKER",
            "docker": {
              "image": "<f5-marathon-lb-container>",
              "network": "BRIDGE"
            }
          },
          "env": {
            "MARATHON_URL": "<marathon_url>",
            "F5_CSI_PARTITIONS": "<bigip_partition_for_mesos_apps>",
            "F5_CSI_BIGIP_HOSTNAME": "<bigip_admin_console>",
            "F5_CSI_BIGIP_USERNAME": "<bigip_username>",
            "F5_CSI_BIGIP_PASSWORD": "<bigip_password>",
            "F5_CSI_DCOS_AUTH_CREDENTIALS": "{ \"scheme\": \"RS256\", \"uid\": \"<service_account_name>\", \"login_endpoint\": \"https://<mesos_master>/acs/api/v1/auth/login\", \"private_key\": \"<private_key>\" }",
            "F5_CSI_MARATHON_CA_CERT": "<marathon_ca_cert>"
          }

#. :ref:`Launch the CSI App <csim-installation-section>`.


Verify Installation
```````````````````

You can view the App in the Marathon UI, under :menuselection:`Applications --> Running`, or you can `query the Marathon REST interface <http://mesosphere.github.io/marathon/docs/rest-api.html#get-v2-apps>`_, to confirm that the |csi_m| is installed and running.


.. csim-install-body-end

.. csim-install-section-end



.. _csim_configuration-section:

.. csim-config-section-start

Configuration
-------------

.. csim-configuration-body-start

Use the configuration parameters, formatted as valid JSON, to configure the F5 |csi_m|.
The service configuration details are stored in Marathon as application labels.

.. _csim_configuration-parameters:

Configuration Parameters
````````````````````````

.. include:: /includes/f5-csi_m/ref_csim-table-configuration-params.rst

.. csim-configuration-body-end
.. csim-config-section-end

.. _csim-usage-section:

.. csim-usage-section-start

Usage
-----

.. csim-usage-body-start

The F5® |csi_m| runs as an App in Marathon. It watches for other Apps configured with a custom set of application labels and creates/manages objects on the BIG-IP as specified in the App configuration.

When the App deploys, the |csi_m|  does the following:

   - creates the virtual server on the BIG-IP in the specified partition,
   - assigns the virtual server to the specified `port-mapping <https://mesosphere.github.io/marathon/docs/ports.html>`_ for the App,
   - creates pool members for each of the App's tasks,
   - creates health monitors for the pool members if a Marathon health check has been configured.

.. _f5-application-labels:

F5 Application Labels
`````````````````````

The F5 application labels consist of key-value pairs that direct the |csi_m| to apply configurations to the BIG-IP. You can use the application labels to configure your App via the Marathon UI or the REST API, in a JSON config file.

.. include:: /includes/f5-csi_m/ref_csim-table-application-labels.rst

.. tip::

    * To configure virtual servers on the BIG-IP for specific ports, provide a port index in the F5 application label.

        - The labels that allow port-specific configuration include ``{n}`` in the label key.
        - The ``{n}`` refers to an index into the port mapping array, starting at 0.

    * If a service port has a Marathon health monitor, |csi_m| creates a corresponding health monitor on the BIG-IP.
    * If the ``F5_CSI_USE_HEALTHCHECK`` option is set to True, |csi_m| checks the port's health status before adding it to a pool on the BIG-IP.

Create a Virtual Server with the F5 |csi_m| via the REST API
````````````````````````````````````````````````````````````

#. Create a JSON file containing the App service definitions and F5 labels.

    .. literalinclude:: /static/f5-csi_m/sample-marathon-application.json
        :caption: sample-marathon-application.json

    :download:`sample-marathon-application.json </static/f5-csi_m/sample-marathon-application.json>`

#. Deploy the application in Marathon via the REST API using the JSON file.

    .. code-block:: shell

        curl -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' \
        http://<marathon_url>:8080/v2/apps -d @sample-marathon-application.json

In this sample application configuration, we have three (3) port indices. We created HTTP virtual servers on the BIG-IP for port 0 and port 1, and specified the IP address and port for each. Corresponding pools, pool members, and HTTP health monitors will be added automatically for each of the Application's tasks.

For a detailed breakdown of the objects created on the BIG-IP, see the :ref:`REST API Deployment Examples <REST API Deployment Examples>`.


Create a Virtual Server with the F5 |csi_m| and iApps via the REST API
``````````````````````````````````````````````````````````````````````

The |csi_m| supports the use of `iApps® <https://devcentral.f5.com/iapps>`_ to create and manage pre-defined services on the BIG-IP.

Use the custom F5 iApp application labels to define variables specific to the iApp you want to deploy. Use the labels listed in the table below to create the custom labels needed for your iApp and to provide the configuration options the iApp requires.

.. important::

    The iApp template you wish to deploy **must** already be installed on the BIG-IP. Variable names and values are template-specific.

.. include:: /includes/f5-csi_m/ref_csim-table-application-labels-iApps.rst

#. Create a JSON file containing the App service definitions and F5 iApp labels.

    .. literalinclude:: /static/f5-csi_m/sample-iapp-marathon.json
        :caption: sample-marathon-application.json

    :download:`sample-marathon-application.json </static/f5-csi_m/sample-iapp-marathon.json>`


#.  Deploy the iApp in Marathon via the REST API.

    .. code-block:: shell

        curl -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' \
        http://<marathon_url>:8080/v2/apps -d @sample-iapp-marathon.json


.. csim-usage-body-end
.. csim-usage-section-end


Further Reading
---------------

.. seealso::

    * F5 |csi_m| :ref:`User Guide <csim-user-guide>`
    * F5 |csi_m| :ref:`Quick Start Guide <csim-quick-start>`
    * F5 |csi_m| :ref:`Deployment Guide <csi-mesos-deployments>`


.. toctree::
    :hidden:
