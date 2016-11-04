REST API Deployment Examples
----------------------------

Deploy a Marathon Application via the REST API
``````````````````````````````````````````````

In the following example, we deploy an application in Marathon with the appropriate |csi_m| labels configured.

- The app (``server-app4``) has three service ports configured; only the first two are exposed via the BIG-IP (port indices 0 and 1 are configured in the ``labels`` section).
- The ``0`` entry in the ``port-mapping`` allows Mesos to auto-allocate a port; the |csi_m| then adds that auto-allocated port number to the pool on the BIG-IP.
- For variables with a number in them (for example, ``F5_{n}_SSL_PROFILE``) ``n`` is a reference to the index in the port array.
- Because Marathon health monitors are configured, corresponding health monitors are created on the BIG-IP.

.. note:: All IP addresses shown are for demonstration purposes only.

#. Deploy the application in Marathon via the REST API.

    .. code-block:: shell

        curl -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' \
        http://<marathon_url>:8080/v2/apps -d @sample-marathon-application.json

    .. literalinclude:: /static/f5-csi_m/sample-marathon-application.json
        :caption: sample-marathon-application.json

    :download:`sample-marathon-application.json </static/f5-csi_m/sample-marathon-application.json>`


#. For our Marathon application, |csi_m| configures virtual servers, pools, and health monitors on the BIG-IP.

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

    When deploying an iApp, you only need to use the ``IAPP`` and ``F5_PARTITION`` labels. The other parameters, such as ``F5_0_BIND_ADDR`` and ``F5_0_PORT``, are accounted for by iApp variables (``pool__addr`` and ``pool__port``, respectively).

#. Deploy the iApp in Marathon via the REST API.

    .. code-block:: shell

        curl -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' \
        http://<marathon_url>:8080/v2/apps -d @sample-iapp-marathon.json

    .. literalinclude:: /static/f5-csi_m/sample-iapp-marathon.json
        :caption: sample-marathon-application.json

    :download:`sample-marathon-application.json </static/f5-csi_m/sample-iapp-marathon.json>`


#. To verify creation of the iApp, log into the BIG-IP config utility. Be sure to look in the correct partition.

    * Go to :menuselection:`iApps --> Application Services` to view the list of Application Services.
    * Click on ``f5.http`` to view all of the objects configured as part of the iApp deployment.




.. [#] The iApp template is available for download from https://downloads.f5.com/.
