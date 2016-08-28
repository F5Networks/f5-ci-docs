.. _usage-guide:

Usage Guide: F5 Container Integration in a Mesos/Marathon Environment
=====================================================================

This guide describes how to set up a reference F5® Container Integration in an environment with Mesos and Marathon. This guide is intended to help users understand the components and services that F5 provides.

You do not need a pre-existing Mesos and Marathon environment. This guide will help you set one up in Amazon Web Services (AWS) using a cloud formation template (CFT). **If you do have an existing environment that you would like to use, you can skip step three below.**

This usage guide also describes how to configure the analytics providers (BIG-IP® and the F5 Lightweight Proxy) to send data to a Splunk instance. Additionally, instructions are provided for installing several F5 Splunk apps on the Splunk instance to process and display the data. If you do not already have an instance, Splunk offers a 60-day evaluation program at https://www.splunk.com/en_us/download/splunk-enterprise.html.

Prerequisites
-------------

* A `Mesos <http://mesos.apache.org/gettingstarted/>`_ `Marathon <https://mesosphere.github.io/marathon/docs/>`_ environment with containerization enabled. See `Running Docker Containers on Marathon <https://mesosphere.github.io/marathon/docs/native-docker.html>`_ for configuration instructions.
* Access to the F5 Integration for Mesos Environments beta site. This is where all components are available for download.
* An Amazon AWS account that can incur small charges, -OR-
* An existing Mesos+Marathon environment.
* A BIG-IP registration key (Good, Better, or Best license); a VE lab license that can be used in AWS can be provided by your F5 sales rep.
* Internet access (required for AWS and to pull images from Docker).
* `Docker <https://docs.docker.com/engine/getstarted/>`_ installed and at least one running container.


Compatibility
-------------

The components used in this guide have been tested with the following environments and versions:

======================= =======
Mesos                   0.28.1
----------------------- -------
Marathon                1.1.1
----------------------- -------
Docker                  1.7.1
----------------------- -------
Splunk                  6.4.2
----------------------- -------
F5 Analytics Splunk App 0.9.5
----------------------- -------
F5 BIG-IP               12.0
======================= =======

F5 Container Integration Setup
------------------------------

Set up Mesos and Marathon
`````````````````````````

In this section, we guide you through the installation of a new Mesos and Marathon environment in AWS.

.. important::

    **This demo uses an AWS CloudFormation template (CFT) that incurs charges while the stack is running.** Delete the stack when you have completed the demo to ensure that you will not continue to be charged.

#. Accept the EULA for BIG-IP VE in Amazon.

    * Go to the BIG-IP VE Amazon Marketplace page for `F5 BIG-IP Virtual Edition Good (BYOL) <http://aws.amazon.com/marketplace/pp?sku=dzweylwc4hxloqophyoi3oihr>`_.
     * Select your region from the drop-down menu.
     * Click on the :guilabel:`Continue` button.
     * Click on :guilabel:`Accept Software Terms`.

     .. warning::

        If you do not complete this step before launching the CloudFormation template, your stack creation will fail.


#. Download the CloudFormation template:

    :download:`f5-ci-beta.cloudformation.json <docs/_static/f5-ci-beta.cloudformation.json>`

#. Launch the CFT in AWS:

    * Log in to your AWS account.
    * Go to CloudFormation (https://console.aws.amazon.com/cloudformation)
    * Click :guilabel:`Create New Stack`.
    * Upload the CloudFormation template.
    * Click :guilabel:`Next`.
    * Enter the required :guilabel:`Parameters`:

        - AdminLocation: This is a CIDR subnet that will limit access to your stack.

            * Only IPs in this subnet can get to the BIG-IP, Mesos, and Marathon administrative interface.
            * The default, "0.0.0.0/0",  allows access from any host.
            * You may want to restrict access to just your external ip (e.g., 63.149.112.92/32). There are several ways to find your external IP address (note: this is not necessarily  the IP address of your local host). For example, on Linux, issue the command ``curl https://api.ipify.org`` and your external IP address will be displayed.

        - BIGIPRegKey: Use the evaluation registration key that was provided to you by your F5 sales rep.
        - KeyName: You must select an SSH keypair that is configured in AWS; this will be used to log in to the VMs that are started by the template.
        - OAuthEnabled: Use the default setting.
        - SlaveInstanceCount: Use the default setting.
    * Click :guilabel:`Next`.
    * :guilabel:`Options`: Enter tags and/or edit Advanced configurations; or, just click :guilabel:`Next`.
    * :guilabel:`Review`: Review the information provided, then check the Identity and Access Management "I acknowledge.."  box.
    * Click :guilabel:`Create`.

#. View your stack.

    * Click the refresh button to view the stack list. The status of your stack will initially be displayed as "CREATE_IN_PROGRESS". If you wish to view the creation events, click on the :guilabel:`Events` tab.
    * Once the stack is created, you will have a BIG-IP running alongside the MesoSphere DC/OS environment. These are listed under the :guilabel:`Resources` tab.
    * The :guilabel:`Outputs` tab contains the necessary information for accessing the stack resources. The following Outputs allow you to access your BIG-IP and the Marathon UI.

        - **BIGIPAdminUI**: the IP address for the BIG-IP configuration utility (aka, the UI).
        - **BIGIPAdminPassword**: the password for the 'admin' user on the BIG-IP.
        - **MarathonUI**: the URL for the Marathon UI.
        - **SplunkReadySSH**: the ssh command to log into an instance ready for Splunk installation.

.. note::

    * The first time you access the BIG-IP configuration utility, you may see the "Configuration Utility restarting..." message. This message should resolve after about 5 minutes. *If it does not resolve*, please contact your F5 Beta rep.
    * A partition called "mesos" was created on the BIG-IP for use with this demo. All LTM objects originating in Mesos will be created in this partition.

Install and Configure Splunk
````````````````````````````

.. tip:: If you already have a Splunk instance set up, skip to step 3.

You'll need to install Splunk somewhere that data from the web applications will be able to reach it (read: probably not on your local machine). If you created the cloud stack in the previous step, it has an Amazon Linux instance that is ready for Splunk installation (see the **SplunkReadySSH** cloud output).

#. Download the free trial of `Splunk Enterprise <https://www.splunk.com/en_us/download/splunk-enterprise.html>`_ to your EC2 instance.

    .. code-block:: bash

        wget -O splunk-6.4.3-b03109c2bad4-Linux-x86_64.tgz 'https://www.splunk.com/bin/splunk/DownloadActivityServlet?architecture=x86_64&platform=linux&version=6.4.3&product=splunk&filename=splunk-6.4.3-b03109c2bad4-Linux-x86_64.tgz&wget=true'

#. Follow the `Install Splunk Enterprise <http://docs.splunk.com/Documentation/Splunk/6.4.2/Installation/InstallonLinux>`_ guide to install and start Splunk for the first time.

    .. note::

        You may need ``chmod`` or ``chown`` the directory in which Splunk (``/opt/splunk``) is installed to complete the startup.

#. Log in to the Splunk GUI, at the URL provided, using the following credentials:

    * Username: admin
    * Password: changeme

    .. note:: Change the default password when prompted.

#. Add a new :guilabel:`HTTP Event Collector`:

    * Click on the gear icon next to :guilabel:`Apps`.
    * Go to :menuselection:`Settings --> Data inputs`.
    * For :guilabel:`HTTP Event Collector`, select :guilabel:`Add new`.
    * Enter a name for the collector; all other fields can use the default values.
    * Click :guilabel:`Next`, then :guilabel:`Review`, then :guilabel:`Submit`.
    * Record the :guilabel:`Token Value` Splunk created for your HTTP Event Collector; **the analytics providers will need this value**.

#. Enable the :guilabel:`HTTP Event Collector`:

    * Go to :menuselection:`Settings --> Data inputs`.
    * Click on :guilabel:`HTTP Event Collector`, then on :guilabel:`Global Settings`.
    * Click on :guilabel:`Enabled`.
    * Click :guilabel:`Save`.

    .. important::

        The event collector listens on port 8088 and requires HTTPS.

#. Configure your firewall to allow port 8088 to be open to Splunk.

    .. note:: If you are using the provided cloud stack, this has already been done.


Install the F5 Splunk Apps
``````````````````````````

In the previous step, you configured your Splunk instance to receive data from the analytics providers. Now, you will configure Splunk apps that provide data visualization: Sankey; F5's Network Analytics; and F5's Lightweight Proxy Analytics.

#. Install the Sankey App:

     * In the Splunk GUI, click on :menuselection:`Apps --> Find More Apps`.
     * Search for "Sankey".
     * Click "Install" and enter your splunk.com credentials (this is your actual Splunk account, not the instance login).
     * Accept the license agreement, then click the :guilabel:`Login and Install` button.
     * Restart Splunk when prompted, then log back in.

#. Install the F5 Networks Analytics App:

     * Download the file :file:`f5-networks-analytics-new_095.tgz` from beta.f5.com to your local drive.
     * In the Splunk GUI, click on :menuselection:`Apps --> Manage Apps`.
     * Click :guilabel:`Install app from file`.
     * Click :guilabel:`Choose File` and select :file:`f5-networks-analytics-new_095.tgz`.
     * Click :guilabel:`Upload`.

#. Install the F5 Lightweight Proxy Analytics App:

     * Download :file:`f5-lightweight-proxy-analytics-v0.1.0.tgz` from beta.f5.com to your local drive.
     * Click :guilabel:`Install app from file`.
     * Click :guilabel:`Choose File` and select :file:`f5-lightweight-proxy-analytics-v0.1.0.tgz`.
     * Click :guilabel:`Upload`.

#. Verify installation:

     * Click the :guilabel:`splunk>` logo to view the main panel. The installed apps should be displayed on the left side of the panel.

#. **Optional**: Set the F5 Lightweight Proxy app as the default display panel:

    * Click :guilabel:`Choose a home dashboard`.
    * Click :guilabel:`F5 Networks Lightweight Proxy`.
    * Click :guilabel:`Save`.


Deploy f5-marathon-lb (CSI)
```````````````````````````

The **f5-marathon-lb** component of the F5 Container Service Integration (CSI) is packaged in a container and runs in the Marathon environment. This component connects Marathon to the BIG-IP. It watches changes in Marathon and configures new objects, like virtual servers and pool members, on the BIG-IP accordingly.

#. Install **f5-marathon-lb**:

    .. note::

        * We use a ``curl`` command here; you may substitute the command of your choice (e.g., ``wget``).
        * You will need to substitute the appropriate values from your AWS stack for the AWS_OUTPUTs shown in the sample JSON blob.

    .. code-block:: text
        :linenos:
        :emphasize-lines: 2, 10, 21, 25, 29

        curl -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' \
        [AWS_OUTPUT:DnsAddress]/service/marathon/v2/apps -d '
        {
          "container": {
            "docker": {
              "portMappings": [
                {}
              ],
              "privileged": false,
              "image": "f5networks/f5-ci-beta:f5-marathon-lb-v0.1.0",
              "network": "BRIDGE",
              "forcePullImage": true
            },
            "type": "DOCKER",
            "volumes": []
          },
          "mem": 64,
          "args": [
            "sse",
            "--marathon",
            "[AWS_OUTPUTS:InternalMarathonURL]",
            "--partition",
            "mesos",
            "--hostname",
            "[AWS_OUTPUTS:BIGIPAdminPrivateIP]",
            "--username",
            "admin",
            "--password",
            "[AWS_OUTPUTS:BIGIPAdminPassword]"
          ],
          "cpus": 0.5,
          "uris": [
            "file:///etc/dockercfg.tgz"
          ],
          "instances": 1,
          "id": "/f5-csi/f5-marathon-lb"
        }'

    The ``curl`` command will return a JSON blob like that shown below:

    .. code-block:: json

        {
            "id": "/f5-csi/f5-marathon-lb",
            "cmd": null,
            "args": ["sse", "--marathon",
                "http://internal-csi-beta2-Internal-1JTBFE9E6UIRN-483548438.us-west-2.elb.amazonaws.com/service/marathon",
                "--partition", "mesos", "--hostname", "10.0.9.79", "--username", "admin", "--password", "i-f9de536d"
            ],
            "user": null,
            "env": {},
            "instances": 1,
            "cpus": 0.5,
            "mem": 64,
            "disk": 0,
            "executor": "",
            "constraints": [],
            "uris": ["file:///etc/dockercfg.tgz"],
            "fetch": [{
                "uri": "file:///etc/dockercfg.tgz",
                "extract": true,
                "executable": false,
                "cache": false
            }],
            "storeUrls": [],
            "ports": [0],
            "portDefinitions": [{
                "port": 0,
                "protocol": "tcp",
                "labels": {}
            }],
            "requirePorts": false,
            "backoffSeconds": 1,
            "backoffFactor": 1.15,
            "maxLaunchDelaySeconds": 3600,
            "container": {
                "type": "DOCKER",
                "volumes": [],
                "docker": {
                    "image": "f5networks/f5-ci-beta:f5-marathon-lb-v0.1.0",
                    "network": "BRIDGE",
                    "portMappings": [{
                        "containerPort": 0,
                        "hostPort": 0,
                        "servicePort": 0,
                        "protocol": "tcp",
                        "labels": {}
                    }],
                    "privileged": false,
                    "parameters": [],
                    "forcePullImage": true
                }
            },
            "healthChecks": [],
            "readinessChecks": [],
            "dependencies": [],
            "upgradeStrategy": {
                "minimumHealthCapacity": 1,
                "maximumOverCapacity": 1
            },
            "labels": {},
            "acceptedResourceRoles": null,
            "ipAddress": null,
            "version": "2016-08-25T20:26:49.257Z",
            "residency": null,
            "tasksStaged": 0,
            "tasksRunning": 0,
            "tasksHealthy": 0,
            "tasksUnhealthy": 0,
            "deployments": [{
                "id": "f1718cbb-4ad3-4abb-aacd-25fdb6e51041"
            }],
            "tasks": []
        }


#. Go to your Marathon UI and watch the app creation.

    The application's status may be "Waiting", "Delayed", or "Deploying" while Marathon schedules the application task, downloads the container, and starts it. It will change to "Running" once the process is complete.

#. Click on the application called *f5-marathon-lb*.

    * Click on the available task to view more details.
    * Click on :guilabel:`Mesos details: link` to see more Mesos details.
    * Click on :guilabel:`Sandbox` to see the container sandbox that the *f5-marathon-lb* instance is running in.
    * Click on :guilabel:`stdout` and :guilabel:`stderr` to see the logs for the *f5-marathon-lb* instance.

Deploy lwp-controller (CSI)
```````````````````````````

The **lwp-controller** component of the CSI is packaged in a container and runs in the Marathon environment. It listens to Marathon events related to the management of applications. If an application that it controls is spun up or down, the lwp-controller will insert or remove the light-weight-proxy in front of the application, providing east-west management of that particular app.

#. Install **lwp-controller**:

    .. note::

        * We use a ``curl`` command here; you may substitute the command of your choice (e.g., ``wget``).
        * You will need to substitute the appropriate Splunk values from :ref:`Install and Configure Splunk` in the JSON blob.

    .. code-block:: text
        :linenos:
        :emphasize-lines: 2, 24, 26

        curl -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' \
        [AWS_OUTPUT:DnsAddress]/service/marathon/v2/apps -d '
        {
          "container": {
            "docker": {
              "portMappings": [],
              "privileged": false,
              "image": "f5networks/f5-ci-beta:lwp-controller-v0.1.0",
              "network": "BRIDGE",
              "forcePullImage": true
            },
            "type": "DOCKER",
            "volumes": []
          },
          "mem": 128,
          "cpus": 1,
          "uris": [
            "file:///etc/dockercfg.tgz"
          ],
          "instances": 1,
          "env": {
            "LWP_DEFAULT_LOG_LEVEL": "info",
            "LWP_DEFAULT_CONTAINER": "f5networks/f5-ci-beta:light-weight-proxy-v0.1.0",
            "LWP_DEFAULT_STATS_TOKEN": "[SPLUNK_TOKEN]",
            "LWP_DEFAULT_STATS_BACKEND": "splunk",
            "LWP_DEFAULT_STATS_URL": "https://[SPLUNK_IP]:8088",
            "LWP_ENABLE_LABEL": "lwp",
            "LWP_DEFAULT_URIS": "file:///etc/dockercfg.tgz",
            "LWP_DEFAULT_MEM": "128",
            "LWP_DEFAULT_STATS_FLUSH_INTERVAL": "10000",
            "LWP_DEFAULT_CPU": "1",
            "MARATHON_URL": "http://marathon.mesos:8080",
            "LWP_DEFAULT_FORCE_PULL": "True"
          },
          "upgradeStrategy": {
            "maximumOverCapacity": 1,
            "minimumHealthCapacity": 1
          },
          "id": "/f5-csi/lwp-controller"
        }'

    The ``curl`` command will return a JSON blob like the one shown below.

    .. code-block:: json
        :linenos:

        {
            "id": "/f5-csi/lwp-controller",
            "cmd": null,
            "args": null,
            "user": null,
            "env": {
                "LWP_DEFAULT_CONTAINER": "f5networks/f5-ci-beta:light-weight-proxy-v0.1.0",
                "MARATHON_URL": "http://marathon.mesos:8080",
                "LWP_DEFAULT_CPU": "1",
                "LWP_DEFAULT_STATS_FLUSH_INTERVAL": "10000",
                "LWP_DEFAULT_FORCE_PULL": "True",
                "LWP_DEFAULT_MEM": "128",
                "LWP_DEFAULT_LOG_LEVEL": "info",
                "LWP_ENABLE_LABEL": "lwp",
                "LWP_DEFAULT_STATS_TOKEN": "C6F63B3A-366F-4A3F-8025-4F32031C5D0B",
                "LWP_DEFAULT_STATS_BACKEND": "splunk",
                "LWP_DEFAULT_URIS": "file:///etc/dockercfg.tgz",
                "LWP_DEFAULT_STATS_URL": "https://192.168.88.146:8088"
            },
            "instances": 1,
            "cpus": 1,
            "mem": 128,
            "disk": 0,
            "executor": "",
            "constraints": [],
            "uris": ["file:///etc/dockercfg.tgz"],
            "fetch": [{
                "uri": "file:///etc/dockercfg.tgz",
                "extract": true,
                "executable": false,
                "cache": false
            }],
            "storeUrls": [],
            "ports": [],
            "portDefinitions": [],
            "requirePorts": false,
            "backoffSeconds": 1,
            "backoffFactor": 1.15,
            "maxLaunchDelaySeconds": 3600,
            "container": {
                "type": "DOCKER",
                "volumes": [],
                "docker": {
                    "image": "f5networks/f5-ci-beta:lwp-controller-v0.1.0",
                    "network": "BRIDGE",
                    "portMappings": [],
                    "privileged": false,
                    "parameters": [],
                    "forcePullImage": true
                }
            },
            "healthChecks": [],
            "readinessChecks": [],
            "dependencies": [],
            "upgradeStrategy": {
                "minimumHealthCapacity": 1,
                "maximumOverCapacity": 1
            },
            "labels": {},
            "acceptedResourceRoles": null,
            "ipAddress": null,
            "version": "2016-08-25T20:53:05.063Z",
            "residency": null,
            "tasksStaged": 0,
            "tasksRunning": 0,
            "tasksHealthy": 0,
            "tasksUnhealthy": 0,
            "deployments": [{
                "id": "f7276efa-eaf6-468f-b5dc-09bf872e71f6"
            }],
            "tasks": []
        }

#. Go to your Marathon UI and watch the app creation.

#. Click on the application called *lwp-controller* to view its details.

Deploy F5 Analytics iApp
````````````````````````

Use an F5 iApps® template file to enable stats collection on your BIG-IP and send the data to Splunk.

#. Download :file:`f5.analytics.tmpl` from beta.f5.com.

#. Log in to the BIG-IP configuration utility.

#. Select :menuselection:`IApps/Templates --> Import`.

#. Upload the iApp template (:file:`f5.analytics.tmpl`).

#. Select :menuselection:`IApps/Application Services --> Create`.

#. Choose the :file:`f5.analytics` template.

#. Fill in the following fields; unspecified fields should use the default setting:

    * Name - [user defined]
    * Module HSL Streams - ``No``
    * Local System Logging (syslog) - ``No``
    * System SNMP Alerts - ``No``
    * iHealth Snapshot Information - ``No``
    * Your Facility Name - [user defined]
    * Default Tenant - [user defined]
    * Alternative Device Group - [user defined]
    * IP Address or Hostname - [SPLUNK_IP]
    * Port - ``8088``
    * Protocol - ``HTTPS``
    * API Key - [SPLUNK_TOKEN]
    * Push Interval - ``20``
    * Mapping Table: 1 - ``Type=[App Name] From=[Virtual Name] Regex= (.*)_\d  Action=Map``
    * Mapping Table: 2 - ``Type=[Tenant Name] From=[Partition] Regex=(.*) Action=Map``

#. Click :guilabel:`Finished`.


Deployment Test Cases
---------------------

Deploy the frontend-service as a North-South Service
````````````````````````````````````````````````````

The CSI demo provides a secure front-end web server that communicates with several backend services. When the server is launched, f5-marathon-lb is notified and takes action accordingly. It creates a virtual server in the **mesos** partition on the BIG-IP (if one is not already configured); creates a pool on the virtual server; and assigns the web server to the pool.

To install the **front-end** web server application:

    .. note:: Highlighted lines need to be configured with data from the AWS CFT.

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


Once the application has deployed, the virtual server, pool, and pool member will appear in the **mesos** partition on the BIG-IP. A health monitor is also configured on the BIG-IP.

You can now access the web server at the URL provided in [AWS_OUTPUTS:FrontendExample]. At this point, any actions requiring access to the back-end services would fail because we haven't created them yet, but you can see several tabs there (like **Example**, **Browse**, and **Watch**).

Scale up the frontend-service
`````````````````````````````

You can scale the number of web servers up or down via the Marathon UI.

To scale the number of web services to two:

#. Click on :guilabel:`frontend-server` in the :guilabel:`Applications` panel.
#. Click :guilabel:`Scale Application`.
#. Enter "2" in the instances window.
#. Click :guilabel:`SCale Application`.

Once the status of the second instance changes to "Started", check the **mesos** partition on the BIG-IP. The f5-lb-marathon app has added another pool member on the virtual server for the second instance.


Launch a service with an iApp
`````````````````````````````

The **f5-lb-marathon** app also supports the installation of arbitrary iApps. Next, we'll install the :file:`f5.http` iApp to launch an insecure version of the web service, running on the standard HTTP port 80.

#. Install the front-end web server application:

    .. note:: Remember to substitute the highlighted values with the correct data from AWS.

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


When the script has completed, there will be two instances of the insecure web service deployed. You can verify this through the Marathon UI or by pointing your browser to [AWS_OUTPUTS:FrontendExampleInsecure].

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

The **lwp-controller** will notice an application is being spun up that it needs to control; it will then add the lightweight proxy in front of the application. We will not be load balancing, as there is only one service at present, but you can confirm that the service is accessible. Click on the :guilabel:`example` tab in the main panel of the Front End Example at [AWS_OUTPUTS:FrontendExample]. The ID of the backend service will be displayed on the web page. You can confirm this is the same ID reported in the Marathon UI for the **Example** service.

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
        }


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
        }


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

This concludes the F5 Container Service Integration usage guide. Remember, **AWS will continue to charge you until you delete your stack**.

Thank you for participating in F5's Beta program! Please send any questions and/or feedback to us at <enter-email-here>.

.. todo:: enter email address

