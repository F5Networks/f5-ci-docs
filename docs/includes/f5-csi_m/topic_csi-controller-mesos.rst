F5 |csi_m|
==========

Overview
--------

The F5® |csi| (CSI) makes L4-L7 services available to users deploying miscroservices-based applications in a containerized infrastructure. [#]_ The |csi_m-long| allows you to configure load balancing on a BIG-IP®  using the `Mesos`_ `Marathon`_ orchestration platform.

Architecture
````````````

The |csi_m| is a Docker container that can run as an app in `Marathon`_. Once installed, it watches for the creation/destruction of `Marathon Apps`_ with the  ``f5-marathon-lb`` labels applied. When it finds a properly-configured App, the CSI  automatically updates the configuration of the BIG-IP as follows:

    - matches Marathon apps to a specified BIG-IP partition;
    - creates a virtual server and pool in the specified partition on the BIG-IP;
    - creates a pool member for each `task`_ and adds the member to the default pool.
    - creates a health monitor on the BIG-IP for each pool member if the application has a Marathon Health Monitor configured.


.. [#] See `Using Docker Container Technology with F5 Products and Services <https://f5.com/resources/white-papers/using-docker-container-technology-with-f5-products-and-services>`_.

Use Case
````````

The F5 |csi_m| makes it possible to manage BIG-IP Local Traffic Manager™ (LTM®) services for North-South traffic (i.e., traffic in and out of the data center) via the Marathon API or GUI. It can be used in conjunction with the F5 :ref:`Lightweight Proxy <lwp-home>`, which provides services for East-West traffic (i.e., traffic between services/apps in the data center).

Prerequisites
`````````````

In order to use the |csi_m-long|, you will need the following:

- Licensed, operational BIG-IP (hardware or Virtual Edition).
- Knowledge of BIG-IP `system configuration`_ and `local traffic management`_.
- Administrator access to both the BIG-IP and Marathon. [*]_
- An existing, functional `Mesos`_ `Marathon`_ deployment.
- BIG-IP partitions that correspond to the Marathon apps.
- The official F5 ``f5-marathon-lb`` image, pulled from the `F5 Docker registry`_.

.. [*] Admin access to the BIG-IP is only required to create the partitions the CSI will manage. Users with permission to configure objects in the partition can do so via the CSI.

Caveats
```````

- |csi_m| can not manage the "Common" partition on the BIG-IP.
- You must create the partition you wish to manage from Marathon on the BIG-IP *before* configuring the CSI.

.. csim-install-section-start

.. _csim-installation-section:

Install the |csi_m|
-------------------

The |csi_m| can be installed as a `Marathon App`_ via the `Marathon REST API <https://mesosphere.github.io/marathon/docs/generated/api.html>`_, the `Marathon UI <https://mesosphere.github.io/marathon/docs/marathon-ui.html>`_, or the command line. All options use the same set of :ref:`configuration parameters <csim_configuration-parameters>`.


Install via a JSON config file
``````````````````````````````

* Create a JSON configuration file with the correct ``env`` parameters for your BIG-IP :term:`device` and Marathon.

    .. rubric:: Example:

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
            "F5_CSI_USE_SSE": "true",
            "MARATHON_URL": "<marathon_url>:8080",
            "F5_CSI_PARTITIONS": "<bigip_partition_for_mesos_apps>",
            "F5_CSI_BIGIP_HOSTNAME": "<bigip_admin_console>",
            "F5_CSI_BIGIP_USERNAME": "<bigip_username>",
            "F5_CSI_BIGIP_PASSWORD": "<bigip_password>"
          }
        }


Launch the |csi_m| App via the Marathon REST API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Send a POST request to the Marathon server that references your JSON config file.

    .. code-block:: bash

        $ curl -X POST -H "Content-Type: application/json" http://<marathon_url>:8080/v2/apps -d @f5-marathon-lb.json


Launch the |csi_m| via the Marathon UI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. Click the :guilabel:`Create Application` button.
#. Complete the :guilabel:`Docker Container Settings` section:

    =================   =========================
    Field               Setting
    -----------------   -------------------------
    Image               f5-marathon-lb-container
    Network             Bridge
    Force Pull Image    user defined
    Privileges          user defined
    Container Port      80
    Host Port           0
    Service Port        user defined
    Protocol            user defined
    =================   =========================

#. Complete the :guilabel:`Environment variables` section as appropriate for your environment.
#. Click :guilabel:`Create Application`.


Verify Installation
```````````````````

Once you have completed the installation, you can view the new app in the Marathon UI, under :menuselection:`Applications --> Running`.

You can also query the Marathon REST interface for a list of all running apps. [#]_


.. [#] http://mesosphere.github.io/marathon/docs/rest-api.html#get-v2-apps

.. csim-install-section-end

.. csim-config-section-start

.. _csim_configuration-section:

Configuration
-------------

The F5 |csi_m| can be configured with valid JSON by setting the parameters below as environment variables. The service configuration details are stored in Marathon application labels.

.. _csim_configuration-parameters:

Configuration Parameters
````````````````````````

.. include:: /includes/f5-csi_m/ref_csim-table-configuration-params.rst

.. csim-config-section-end

.. csim-usage-section-start

Usage
-----

Manage Applications with |csi_m|
````````````````````````````````

The |csi_m| identifies and configures applications via Marathon Application labels.

.. tip::

    Some labels are specified *per service port*. These are denoted with the ``{n}`` parameter in the label key; ``{n}`` corresponds to the service port index, beginning at ``0``.


.. literalinclude:: /includes/f5-csi_m/ref_csim-table-application-labels.rst


Deploy Applications with |csi_m| and iApps
``````````````````````````````````````````

F5's `iApps® <https://devcentral.f5.com/iapps>`_ is a user-customizable framework for deploying applications that enables you to templatize sets of functionality on your BIG-IP. You can use |csi_m| to instantiate and manage an iApp® Application Service. The iApp template and variables are defined via Marathon application labels specific to the iApp you are deploying.

.. important::

    The iApp template you wish to deploy **must** already be installed on the BIG-IP. Variable names and values are template-specific.

.. literalinclude:: /includes/f5-csi_m/ref_csim-table-application-labels-iApps.rst

.. csim-usage-section-end

Deployment Examples
-------------------

Deploy a Marathon Application via the REST API
``````````````````````````````````````````````

In the following example, we deploy an application in Marathon with the appropriate |csi_m| labels configured.

- The app (``server-app4``) has three service ports configured; only the first two are exposed via the BIG-IP (port indices 0 and 1 are configured in the ``labels`` section).
- Marathon health monitors are configured for all three service ports.

.. note:: All IP addresses shown are for demonstration purposes only.

#. Deploy the application in Marathon via the REST API.

    .. code-block:: shell

        curl -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' \
        http://<marathon_url>:8080/v2/apps -d @sample-marathon-application.json

    .. literalinclude:: /static/f5-csi_m/sample-marathon-application.json
        :caption: sample-marathon-application.json

    :download:`sample-marathon-application.json </static/f5-csi_m/sample-marathon-application.json>`


#. For our Marathon application, |csi_m| configures virtual servers, pools, and health monitors on the BIG-IP.

    .. note::

        - If a Marathon health monitor exists for a service port, |csi_m| creates a corresponding health monitor for it on the BIG-IP.
        - If the ``--health-check`` option is set, |csi_m| checks the Marathon health status for the service port before adding it to the backend pool.

    .. code-block:: shell
        :caption: BIG-IP configurations

        user@(my-bigip)(Active)(/my-marathon-app)(tmos)# show ltm
        ltm monitor http server-app4_10.128.10.240_8080 {
            adaptive disabled
            defaults-from /Common/http
            destination *:*
            interval 20
            ip-dscp 0
            partition mesos
            send "GET /\r\n"
            time-until-up 0
            timeout 61
        }
        ltm monitor http server-app4_10.128.10.242_8090 {
            adaptive disabled
            defaults-from /Common/http
            destination *:*
            interval 20
            ip-dscp 0
            partition mesos
            send "GET /\r\n"
            time-until-up 0
            timeout 61
        }
        ltm node 10.141.141.10 {
            address 10.141.141.10
            partition mesos
            session monitor-enabled
            state up
        }
        ltm persistence global-settings { }
        ltm pool server-app4_10.128.10.240_8080 {
            members {
                10.141.141.10:31383 {
                    address 10.141.141.10
                    session monitor-enabled
                    state up
                }
                10.141.141.10:31775 {
                    address 10.141.141.10
                    session monitor-enabled
                    state up
                }
            }
            monitor server-app4_10.128.10.240_8080
            partition mesos
        }
        ltm pool server-app4_10.128.10.242_8090 {
            members {
                10.141.141.10:31384 {
                    address 10.141.141.10
                    session monitor-enabled
                    state up
                }
                10.141.141.10:31776 {
                    address 10.141.141.10
                    session monitor-enabled
                    state up
                }
            }
            monitor server-app4_10.128.10.242_8090
            partition mesos
        }
        ltm virtual server-app4_10.128.10.240_8080 {
            destination 10.128.10.240:webcache
            ip-protocol tcp
            mask 255.255.255.255
            partition mesos
            pool server-app4_10.128.10.240_8080
            profiles {
                /Common/http { }
                /Common/tcp { }
            }
            source 0.0.0.0/0
            source-address-translation {
                type automap
            }
            vs-index 153
        }
        ltm virtual server-app4_10.128.10.242_8090 {
            destination 10.128.10.242:8090
            ip-protocol tcp
            mask 255.255.255.255
            partition mesos
            pool server-app4_10.128.10.242_8090
            profiles {
                /Common/http { }
                /Common/tcp { }
            }
            source 0.0.0.0/0
            source-address-translation {
                type automap
            }
            vs-index 154
        }


Deploy an iApps Application via the REST API
````````````````````````````````````````````

In the following example, we deploy the "f5.http" iApp® on the BIG-IP as a Marathon Application, via the Marathon REST API. [#]_

.. note::

    Only the the ``IAPP`` labels and the ``F5_PARTITION`` label are needed to deploy using an iApp template. For example, the ``F5_0_BIND_ADDR`` and ``F5_0_PORT`` parameters are accounted for by iApp variables (``pool__addr`` and ``pool__port``, respectively).

#. Deploy the iApp in Marathon via the REST API.

    .. code-block:: shell

        curl -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' \
        http://<marathon_url>:8080/v2/apps -d @sample-iapp-marathon.json

    .. literalinclude:: /static/f5-csi_m/sample-iapp-marathon.json
        :caption: sample-marathon-application.json

    :download:`sample-marathon-application.json </static/f5-csi_m/sample-iapp-marathon.json>`


#. To verify creation of the iApp, log into the BIG-IP config utility. Be sure to look in the correct partition!

    * Go to :menuselection:`iApps --> Application Services` to view the list of Application Services.
    * Click on ``f5.http`` to view all of the objects configured as part of the iApp deployment.




.. [#] The iApp template is available for download from https://downloads.f5.com/.


Further Reading
---------------


.. seealso::

    * x
    * y
    * z

.. toctree::
    :hidden:
