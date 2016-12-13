Deployment Test Cases
---------------------

Once you have launched your Cloud Formation Stack, installed Splunk, and installed the |csi_m|, you can send test traffic to your apps. We've created a few sample apps, but feel free to test out traffic on your own.


Deploy the frontend-service as a North-South Service
````````````````````````````````````````````````````

The CSI demo provides a secure front-end web server that communicates with several backend services. When the server is launched, f5-marathon-lb is notified and takes action accordingly. It creates a virtual server in the **mesos** partition on the BIG-IP (if one is not already configured); creates a pool on the virtual server; and assigns the web server to the pool.

To install the **front-end** web server application:

.. note:: Highlighted lines must be configured with data from the AWS CloudFormation outputs.

.. code-block:: text
    :linenos:
    :emphasize-lines: 2, 23

    curl -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' \
    [AWS_OUTPUT:DnsAddress]/service/marathon/v2/apps -d '
    {
      "container": {
        "docker": {
          "portMappings": [
            {
              "protocol": "tcp",
              "containerPort": 80,
              "hostPort": 0
            }
          ],
          "privileged": false,
          "image": "f5networks/f5-ci-beta:microservice-demo-v0.14",
          "network": "BRIDGE",
          "forcePullImage": true
        },
        "type": "DOCKER",
        "volumes": []
      },
      "mem": 128,
      "labels": {
        "F5_0_BIND_ADDR": "[AWS_OUTPUTS:BIGIPExternalPrivateIP]",
        "F5_0_PORT": "443",
        "F5_0_SSL_PROFILE": "Common/clientssl",
        "F5_PARTITION": "mesos",
        "F5_0_MODE": "tcp"
      },
      "cpus": 0.25,
      "uris": [
        "file:///etc/dockercfg.tgz"
      ],
      "instances": 1,
      "upgradeStrategy": {
        "maximumOverCapacity": 1,
        "minimumHealthCapacity": 1
      },
      "healthChecks": [
        {
          "portIndex": 0,
          "protocol": "HTTP",
          "timeoutSeconds": 20,
          "intervalSeconds": 20,
          "ignoreHttp1xx": false,
          "gracePeriodSeconds": 300,
          "maxConsecutiveFailures": 3,
          "path": "/healthcheck"
        }
      ],
      "id": "frontend-server"
    }'


Once the application has deployed, the virtual server, pool, pool member, and health monitor will appear in the **mesos** partition on the BIG-IP.

You can now access the web server at the URL provided in [AWS_OUTPUTS:FrontendExample]. At this point, any actions requiring access to the back-end services would fail because we haven't created them yet, but you can see several tabs there (like **Example**, **Browse**, and **Watch**).

Scale up the frontend-service
`````````````````````````````

You can scale the number of web servers up or down via the Marathon UI.

To scale the number of web services to two:

#. Click on :guilabel:`frontend-server` in the :guilabel:`Applications` panel.
#. Click :guilabel:`Scale Application`.
#. Enter "2" in the instances window.
#. Click :guilabel:`SCale Application`.

Once the status of the second instance changes to "Started", check the **mesos** partition on the BIG-IP. The ``f5-marathon-lb`` app has added another pool member on the virtual server for the second instance.


Launch a service with an iApp
`````````````````````````````

Next, we'll install the ``f5.http`` iApp to launch an insecure version of the web service, on the standard HTTP port 80.

#. Install the front-end web server application:

    .. note:: Remember to substitute the highlighted values with the correct data from the AWS CloudFormation outputs.

    .. code-block:: text
        :linenos:
        :emphasize-lines: 2, 27

        curl -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' \
        [AWS_OUTPUT:DnsAddress]/service/marathon/v2/apps -d '
        {
          "container": {
            "docker": {
              "portMappings": [
                {
                  "protocol": "tcp",
                  "containerPort": 80,
                  "hostPort": 0
                }
              ],
              "privileged": false,
              "image": "f5networks/f5-ci-beta:microservice-demo-v0.14",
              "network": "BRIDGE",
              "forcePullImage": true
            },
            "type": "DOCKER",
            "volumes": []
          },
          "mem": 128,
          "labels": {
            "F5_PARTITION": "mesos",
            "F5_0_IAPP_VARIABLE_pool__pool_to_use": "/#create_new#",
            "F5_0_IAPP_OPTION_description": "iApp for insecure (HTTP) frontend-server",
            "F5_0_IAPP_VARIABLE_monitor__monitor": "/#create_new#",
            "F5_0_IAPP_VARIABLE_pool__addr": "[AWS_OUTPUTS:BIGIPExternalPrivateIP]",
            "F5_0_IAPP_TEMPLATE": "/Common/f5.http",
            "F5_0_IAPP_VARIABLE_monitor__response": "none",
            "F5_0_IAPP_VARIABLE_net__server_mode": "lan",
            "F5_0_IAPP_POOL_MEMBER_TABLE_NAME": "pool__members",
            "F5_0_IAPP_VARIABLE_net__client_mode": "wan",
            "F5_0_IAPP_VARIABLE_monitor__uri": "/healthcheck",
            "F5_0_IAPP_VARIABLE_pool__port": "80"
          },
          "cpus": 0.25,
          "uris": [
            "file:///etc/dockercfg.tgz"
          ],
          "instances": 2,
          "upgradeStrategy": {
            "maximumOverCapacity": 1,
            "minimumHealthCapacity": 1
          },
          "env": {
            "INSECURE": "1"
          },
          "healthChecks": [
            {
              "portIndex": 0,
              "protocol": "HTTP",
              "timeoutSeconds": 20,
              "intervalSeconds": 20,
              "ignoreHttp1xx": false,
              "gracePeriodSeconds": 300,
              "maxConsecutiveFailures": 3,
              "path": "/healthcheck"
            }
          ],
          "id": "frontend-server-insecure"
        }'


When the script has completed, there will be two instances of the insecure web service deployed. You can verify this through the Marathon UI or by pointing your browser to ``[AWS_OUTPUT:FrontendExampleInsecure]``.

Deploy an example East-West service
```````````````````````````````````

The front-end web service makes uses of several backend services.  We will spin up one such service to show how easy it is to insert the lightweight proxy to front and load balance the service.

#. To install the **example** backend service:

    .. note:: Remember to substitute the highlighted values with the correct data from AWS.

    .. code-block:: text
        :linenos:
        :emphasize-lines: 2

        curl -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' \
        [AWS_OUTPUT:DnsAddress]/service/marathon/v2/apps -d '
        {
          "container": {
            "docker": {
              "portMappings": [
                {
                  "servicePort": 11099,
                  "protocol": "tcp",
                  "containerPort": 80,
                  "hostPort": 0
                }
              ],
              "privileged": false,
              "image": "f5networks/f5-ci-beta:microservice-demo-v0.14",
              "network": "BRIDGE",
              "forcePullImage": true
            },
            "type": "DOCKER",
            "volumes": []
          },
          "mem": 128,
          "labels": {
            "lwp": "enable"
          },
          "cpus": 0.25,
          "uris": [
            "file:///etc/dockercfg.tgz"
          ],
          "instances": 1,
          "upgradeStrategy": {
            "maximumOverCapacity": 1,
            "minimumHealthCapacity": 1
          },
          "id": "example"
        }'

The |lwpc| will notice an application is being spun up that it needs to control; it then adds the |lwp| in front of the application. We will not be load balancing, as there is only one service at present, but you can confirm that the service is accessible.

Click on the :guilabel:`example` tab in the main panel of the Front End Example at [AWS_OUTPUTS:FrontendExample]. The ID of the backend service will be displayed on the web page. You can confirm this is the same ID reported in the Marathon UI for the **Example** service.

Scale the Example service up
````````````````````````````

You can follow the steps provided in :ref:`Scale up the frontend-service` to run additional instances of the Example service using the Marathon UI. When you click on the :guilabel:`Example` tab after adding instances, the returned ID value will be balanced among the running instances.

Deploy complex microservices topology
`````````````````````````````````````

The front-end web service can communicate with various additional backend services. You can spin these services up using the ``curl`` command for the Example app, with any of the following ``id`` and ``servicePort`` fields substituted for "example" and "11099".


+-------------------+-----------------+
| ID                | Port            |
+===================+=================+
| auth-svc          | 11001           |
+-------------------+-----------------+
| list-manager-svc  | 11002           |
+-------------------+-----------------+
| title-detail-svc  | 11003           |
+-------------------+-----------------+
| trending-svc      | 11004           |
+-------------------+-----------------+
| activity-svc      | 11005           |
+-------------------+-----------------+
| suggestions-svc   | 11006           |
+-------------------+-----------------+
| drm-svc           | 11007           |
+-------------------+-----------------+


.. topic:: Examples:

    .. code-block:: text
        :linenos:

        curl -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' \
        [AWS_OUTPUT:DnsAddress]/service/marathon/v2/apps -d '
        {
          "container": {
            "docker": {
              "portMappings": [
                {
                  "servicePort": 11001,
                  "protocol": "tcp",
                  "containerPort": 80,
                  "hostPort": 0
                }
              ],
              "privileged": false,
              "image": "f5networks/f5-ci-beta:microservice-demo-v0.14",
              "network": "BRIDGE",
              "forcePullImage": true
            },
            "type": "DOCKER",
            "volumes": []
          },
          "mem": 128,
          "labels": {
            "lwp": "enable"
          },
          "cpus": 0.25,
          "uris": [
            "file:///etc/dockercfg.tgz"
          ],
          "instances": 2,
          "upgradeStrategy": {
            "maximumOverCapacity": 1,
            "minimumHealthCapacity": 1
          },
          "id": "auth-svc"
        }'


   .. code-block:: text
        :linenos:

        curl -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' \
        [AWS_OUTPUT:DnsAddress]/service/marathon/v2/apps -d '
        {
          "container": {
            "docker": {
              "portMappings": [
                {
                  "servicePort": 11002,
                  "protocol": "tcp",
                  "containerPort": 80,
                  "hostPort": 0
                }
              ],
              "privileged": false,
              "image": "f5networks/f5-ci-beta:microservice-demo-v0.14",
              "network": "BRIDGE",
              "forcePullImage": true
            },
            "type": "DOCKER",
            "volumes": []
          },
          "mem": 128,
          "labels": {
            "lwp": "enable"
          },
          "cpus": 0.25,
          "uris": [
            "file:///etc/dockercfg.tgz"
          ],
          "instances": 2,
          "upgradeStrategy": {
            "maximumOverCapacity": 1,
            "minimumHealthCapacity": 1
          },
          "id": "list-manager-svc"
        }'


At this point, you have a fully functioning environment and should be able to click on any of the tabs in the front-end web service in your browser.


Inject, diagnose, and address errors
````````````````````````````````````

Analytics are collected for both the North-South traffic (reported by the BIG-IP) and the East-West traffic to the individual apps (reported by the lightweight proxies). The traffic exercise below demonstrates how to inject, diagnose, and address errors with your Marathon applications.

.. tip::

    * Click on the :guilabel:`repeat` button in the front-end web service,  then on one of the other tabs, to continuously send requests to the server.
    * The **F5 Networks** app in Splunk displays panels for North-South traffic.
    * The **F5 Lightweight Proxy** app in Splunk displays panels for East-West traffic.


.. rubric:: Traffic Exercise:

#. View the **F5 Lightweight Proxy** app in Splunk.
#. Change the time range to a realtime 5-minute window. If the environment is properly set up, you should only see 2xx responses in the :guilabel:`Virtual Server Requests` panel.
#. To inject some errors into the East-West traffic, change the URL of the front-end web service from **[AWS_OUTPUTS:FrontendExample]** to **[AWS_OUTPUTS:FrontendExample]?forceFailures=true**.
#. Then, turn on the repeat option for the Example requests.
#. To speed up the degradation, use the Marathon UI to scale the Example services to one instance.
#. To make the analytics more interesting, access the front-end web service in a different browser and repeat a different application (Browse or Watch).
#. HTTP errors will start to occur in the Example app. The rate of errors will start to increase after a few minutes. At around 5 minutes, the service will no longer successfully respond to requests.
#. As you look at the panels, you will notice that 5xx errors will start to show up in the :guilabel:`Virtual Server Requests` panel. This lets you know that something is going wrong in the back-end applications, but you can't tell which application is the one having trouble.
#. If you click on the 5xx line, you'll see a drill-down panel that shows which applications are reporting the 5xx errors. As you would expect, all the errors are coming from the Example application.
#. Since it looks like the Example application has a catastrophic error condition, you can try to fix it by going to the Marathon UI and restarting the instance. Go ahead and restart the instance, then observe the Splunk panels. You should see 5xx errors immediately drop to zero.


Conclusion
----------

This concludes the F5 |csi_m| deployment guide. Thank you for participating in F5's Beta program! Please send any questions and/or feedback to us at beta@f5.com.

.. important:: Remember, **AWS will continue to charge you until you delete your stack**.


.. ref:`F5 Lightweight Proxy Getting Started Guide <lwp-getting-started-guide>`
.. ref:`F5 Lightweight Proxy Controller for Mesos+Marathon: Getting Started Guide <lwpc-getting-started-guide>`

