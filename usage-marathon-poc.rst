Usage Guide: F5 Container Integration in a Mesos/Marathon Environment
=====================================================================

This guide describes how to set up a reference F5 Container Integration in an
environment with Mesos and Marathon. We suggest that you start by following
these steps to understand the components and services that we provide.

You do not need a pre-existing Mesos and Marathon environment. This guide
will help you set one up in AWS using a cloud formation template (CFT). If you
do have an existing environment that you would like to use, you can skip step
three below.

This usage guide will also describe how to configure the analytics providers
(e.g. Big-IP and the Lightweight Proxy) to send data to a Splunk instance.
Additionally, to make full use of the data sent, instructions are provided on
how to install several F5 Splunk apps on the Splunk instance in order to
process and display the data.   If you do not have an available instance,
Splunk offers a 60-day evaluation program at
https://www.splunk.com/en_us/download/splunk-enterprise.html.


Introduction
============

The components in this usage guide have been tested on these environments and
versions:

| Mesos: 0.28.1
| Marathon: 1.1.1
| Docker: 1.7.1
| Splunk: 6.4.2
| F5 Analytics Splunk App: 0.9.5
|

Step 1: Installing and Configure Splunk to receive data
-------------------------------------------------------

The instructions listed in this section assume you are going to install a fresh
version of Splunk Enterprise.  If you are running a pre-existing version
of Splunk, you can start at step two and may have to modify the subsequent
instructions slightly.

1. Download the free trial of `Splunk Enterprise
<https://www.splunk.com/en_us/download/splunk-enterprise.html>`_.

2. Follow the `Install Splunk Enterprise
<http://docs.splunk.com/Documentation/Splunk/6.4.2/SearchTutorial/InstallSplunk>`_
guide to install and start splunk for the first time.

3. Access the Splunk GUI at http://<your_splunk_ip_address>:8000.

 * Username: admin
 * Password - changeme

4. You will be prompted to change the default password.  You will now be at
the main dashboard page of the Splunk GUI.  To get to this page at any time,
click on the "splunk>" logo which always appears in the upper left corner of
any page.

5. Under the menu bar "Settings", select "Data inputs".  A list of available
data inputs will appear. Find the "HTTP Event Collector" input and select "Add
new" on the far righthand side.

6. Give the collector a name.  All other fields can be left at their defaults.

7. Click "Next", then "Review", and finally "Submit".

8. Record the Token Value that Splunk created for your HTTP Event Collector.
The analytics providers will need to know this value.

9. Return to the list of available data inputs (step 5)  and click on "HTTP
Event Collector" (do not click on "Add new" this time).

10. In the upper right corner of the page, click on "Global Settings" and
then click on the "Enabled" button, then click on "Save".  Note: the
remaining settings will have the event collector listening on port 8088 and
require HTTPS.

11. Enable your firewall to allow port 8088 to be passed to Splunk.  If you are
running in AWS, this will be configured as part of your security group.

Step 2: Install the F5 Splunk Apps
----------------------------------

Step 1 above enables your Splunk instance to receive data sent from the
analytics providers.  F5 provides several Splunk apps to help visualize the
data.  To install these apps, you need to perform the following steps:

1. Install the Sankey App

 * In the upper left corner of the Splunk GUI, click on the "Apps" dropdown
and then click on "Find More Apps". (Note: if you are on the main dashboard
page, you will have to first click on the gear next to the side bar header
named "Apps".)

 * Use the search bar to search for "Sankey". Click "Install" and enter your
Splunk credentials (not the local user name for the Splunk instance).

 * You will need to accept the license agreement before you can then proceed to
click on the "Login and Install" button.

 * When the installation is completed, you will be asked to restart splunk.
 Go ahead and click the "Restart Splunk" button and then login again when the
 login prompt appears.

2. Install the F5 Networks Analytics App

 * Download the file f5-networks-analytics-new_095.tgz from beta.f5.com to
 your local drive. This app allows you to visualize the Big-IP data that is
 sent to Splunk

 * In the upper left corner of the Splunk GUI, click on the "Apps"
 dropdown and then click on "Manage Apps".

 * Click on the "Install app from file" button.

 * Click on "Choose File" and browse to the location of the downloaded file.

 * After selecting the F5 app, click on "Upload".

3. Install the F5 Lightweight Proxy Analytics App

 * Download the file f5-lightweight-proxy-analytics.tgz from beta.f5.com to
 your local drive. This app allows you to visualize the Lightweight Proxy
 data that is sent to Splunk.

 * Click on the "Install app from file" button.

 * Click on "Choose File" and browse to the location of the downloaded file.

 * After selecting the F5 Lightweight Proxy app, click on "Upload".

 * Click on the "splunk>" logo in the upper left corner to verify all three
 apps have been installed.  They should show up on the lefthand side of the
 main panel.

 * To have the F5 Lightweight Proxy app be the default display panel, click
 "Choose a home dashboard" and then select the "F5 Networks Lightweight
 Proxy" followed by the "Save" button.

Step 3: Set up Mesos and Marathon
---------------------------------

If you do not have an environment running Mesos and Marathon, or if you would
rather exercise these instructions in a new test environment, follow these
instructions.

These instructions require you to execute an AWS CloudFormation template, which
will incur a cost while the stack is running. Deleting the stack that is
produced will delete all associated resources: you should do this once you are
satisfied with the completion of these steps.

As a participant in the Container Integration beta program, you were granted
access to an AWS CloudFormation template called f5-ci.beta.cloudformation.json.
Download this CloudFormation template and start it in your account.

Parameters:

*KeyName*: You must select an SSH keypair that is configured in AWS. You'll
need this to log in to the VMs that are started.

*AdminLocation*: This is a CIDR subnet that is configured to limit access to
the stack that is produced. Only IPs in this subnet can get to the BIG-IP,
Mesos, or Marathon administrative interface. The default is "0.0.0.0/0" which
allows access from any host. You may want to restrict access to just your
external ip (e.g. 63.149.112.92/32).  There are several ways to find your
external IP address (this may not necessarily be the IP address of your
local host).  For instance, on Linux, you can issue the command "curl
https://api.ipify.org" and it will display your external IP address.

*BIGIPRegKey*: Use the evaluation registration key that was provided to you
as a member of the beta program.

All other inputs leave at their default.

Outputs:

Once the stack is set up, you will have a BigIP running along side the
MesoSphere DC/OS environment.  The CFT outputs will provide the necessary
information for accessing these resources

*BIGIPAdminUI*: Navigate to this URL in a browser and log in with the username
"admin" and the password from the *BIGIPAdminPassword* output. A special
partition named 'mesos' should have been created just for the demo.

*MarathonUI*: Navigate to this URL in a browser and confirm that you see a
Marathon user interface, with no applications running.

Step 4: Deploy f5-marathon-lb (CSI)
-----------------------------------

**f5-marathon-lb** is a component of the Container Service Integrator (CSI). It
is packaged in a container and it runs in the Marathon environment. It will
connect to Marathon as well as the BIG-IP. It watches changes in Marathon
and configures new elements like virtual servers and pool members on BIG-IP
in response.

To install the **f5-marathon-lb** application, use the following curl command
(or similar program), substituting the appropriate values from the AWS CFT
**Parameter** and **Output** variables::

    curl -X POST -H 'Content-Type: application/json' -H 'Accept: application/json' \
    [AWS_OUTPUT:DnsAddress]/service/marathon/v2/apps -d '
    {
      "container": {
        "docker": {
          "portMappings": [
            {}
          ],
          "privileged": false,
          "image": "[AWS_PARAMETER:DockerRepo]:f5-marathon-lb-v0.1.0",
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
        "[AWS_OUTPUTS:BIGIPExternalPrivateIP]",
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


After issuing the command, you should be able to observe the creation of
the application in the Marathon UI. You may see the application shown as
"Staged" while Marathon schedules the application task, downloads the
container, and starts it. You will see it show as "Started" once the process
has completed.

Click on the application *f5-marathon-lb* and you will see a page showing the
tasks (there is only 1 task for f5-marathon-lb). Click on the task and you can
see more details. There will be a row saying "Mesos details: link"; click on
this link to see Mesos details. Then, click on "Sandbox" to see the container
sandbox that it is running in. Click on "stdout" and "stderr" to see the logs
for the *f5-marathon-lb* instance.

Step 4: Deploy lwp-controller (CSI)
-----------------------------------

**lwp-controller** is a component of the Container Service Integrator (CSI). It
is packaged in a container and it runs in the Marathon environment. It will
be configured to listen to Marathon events related to the management of
applications. If an application is spun up or down that it is responsible for
controlling, it will insert (or remove) the light-weight-proxy in front of
the application, providing east-west management of that particular application.

To install the **lwp-controller** application, use the following curl command
(or similar program), substituting the appropriate values from the AWS CFT
Parameter and Output
variables::

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

After issuing the command, you should be able to observe the creation of
the application in the Marathon UI.

Step 5: Deploy F5 Analytics IApp
---------------------------------
To enable the sending of stats from within the Big-IP, you need to
download and then install an IApp template file from F5.

 * Download the file **f5.analytics.tmpl** from beta.f5.com to your local drive.

 * From the BigIP GUI, select the **Import** from **IApps/Templates** and
 upload the file.

 * In the GUI, select **Create** from **IApps/Application Services** page and
 choose the **f5.analytics** template.

 * Fill in the following fields (unspecified fields should be left at their
 defaults) before clicking on the finished button:
   * Name - user defined
   * Module HSL Streams - No
   * Local System Logging (syslog) - No
   * System SNMP Alerts - No
   * iHealth Snapshot Information - No
   * Your Facility Name - [user defined]
   * Default Tenant - [user defined]
   * Alternative Device Group - [user defined]
   * IP Address or Hostname - [SPLUNK_IP]
   * Port - 8088
   * Protocol - HTTPS
   * API Key - [SPLUNK_TOKEN]
   * Push Interval - 20
   * Mapping Table (1) - **Type**=App Name **From**=Virtual Name **Regex**=(.*)_d **Action**=Map
   * Mapping Table (2) - **Type**=Tenant Name **From**=Partition **Regex**=(.*) **Action**=Map

Deployment Test Cases
=====================

Deploy the frontend-service as a North-South Service
----------------------------------------------------
The CSI demo provides a secure front-end web server that communicates with
several backend services.  The previously installed f5-marathon-lb will be
notified when the web server is launched and take action.  It will configure
the Big-IP to install a virtual server on the **mesos** partition if one is
not already configured. It will then ass the server to the pool associated
with the virtual server.

To install the **front-end** web server application, use the following curl
command (or similar program), substituting the appropriate values from the
AWS CFT Parameter and Output variables::

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
      "id": "/frontend-server"
    }

Once the application has been deployed, you will notice that the Big-IP is
configured with a virtual server and one pool member for the front-end web
service in the **mesos** partition.  It will also have a health monitor
configured.

At this point you will be able to access the web server but any actions
requiring access to the back-end services fronted by the web server will fail
because we have not created them.  To access the server, point your browser at
[AWS_OUTPUTS:FrontendExample].  You will see several tabs with labels such as
**Example**, **Browse**, and **Watch**.

Scale the frontend-service up
-----------------------------
At this point you have one web service running fronted by a Big-IP virtual
server.  You can scale up or down the number of web servers by using the
marathon UI (you obtain the URL from [DOCKER_OUTPUTS:MarathonUI]).

To scale the number of web services to two, click on **frontend-server** in
the Applications panel.  A **Scale Application** button will appear that will
allow you to choose the number of instances desired.

You should notice that the f5-lb-marathon app will adjust the pool members of
 the Big-IP virtual server to match the value you entered.

Reconfigure the frontend-service to use the f5.http iApp
--------------------------------------------------------
The **f5-lb-marathon** app also offers the flexibility of installing
arbitrary iapps. We will use this option to install another insecure version
of the web service running on the standard HTTP port 80.  We will use the
pre-packaged iapp **f5.http**.

To install the **front-end** web server application, use the following curl
command (or similar program), substituting the appropriate values from the
AWS CFT Parameter and Output variables::

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
      "id": "/frontend-server-insecure"
    }

When the script has completed, there will be two instances of the insecure
web service deployed.  You can verify this through the marathon UI or by
pointing your browser to [AWS_OUTPUTS:FrontendExampleInsecure].

Deploy an example East-West Service
-----------------------------------
The front-end web service makes uses of several backend services.  We will
spin up one such service so show how easy it is to insert the lightweight
proxy to front and load balance the service.

To install the **example** backend service, use the following curl
command (or similar program), substituting the appropriate values from the
AWS CFT Parameter and Output variables::

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
      "instances": 2,
      "upgradeStrategy": {
        "maximumOverCapacity": 1,
        "minimumHealthCapacity": 1
      },
      "id": "example"
    }

The **lwp-controller** will notice that an application is being spun up that
it needs to control and will therefore make sure the service is fronted by
the lightweight proxy.  At this point, there is only one such service so we
won't we load balancing.  However, you can confirm that the service is now
accessible by clicking on the **example** tab in the main panel of your web
browser.  The ID of the backend service will be printed to the web page.  You
can confirm this is the same ID as was reported in the marathon UI for the
**example** service.

Scale the example service up
----------------------------
To run additional instances of the example service, simply go to the marathon
UI and increase the number of instances for it.  This is similar to the
previous exercise where we spun up an additional web service.

Now when you click on the **example** tab, you will notice that the returned
ID value will be balanced among the running instances.

Deploy complex microservices topology
-------------------------------------
The front-end web service can communicated with various additional backend
services. You can spin these services up by issuing the previous curl for the
**example** app, but replacing the **id** and **servicePort** fields using
the following table:

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

At this point you have a fully functioning environment and should be able to
click on any of the tabs presented by the front-end web service in your
browser.


Inject, diagnose, and address errors
------------------------------------

In your browser that is pointing at the front-end web server, click on the
**repeat** button and then one of the subsequent tabs to continuously send
requests to the server.

You can then view the analytics that are being collected for both the
North-South traffic (reported by the Big-IP) as well as the East-West traffic
to the individual apps (reported by the lightweight proxies).  Open a
browser and point it at your Splunk Instance (**http://[SPLUNK_IP]:8000**).
The **F5 Networks** app will display panels for the North-South traffic,
while the **F5 Lightweight Proxy** app will display panels for the
East-West traffic. Go ahead and view the F5 Lightweight Proxy app.  Change
the time range to a realtime 5-minute window. If the environment is properly
setup, you should only see 2xx responses in the **Virtual Server Requests**
panel.

To inject some errors into the East-West, change the URL of the web service
from **[AWS_OUTPUTS:FrontendExample]** to
**[AWS_OUTPUTS:FrontendExample]?forceFailures=true**.  Then turn the repeat
option on for the Example requests. To speed up the degradation, you will
want to scale the Example services to one using the Marathon UI.  To make the
analytics more interesting, you could start a second browser but repeat
either the Browse or Watch applications.

Slowly over time, HTTP errors will start to occur in the example app.  The
rate of errors will start to increase after a few minutes. At a certain
point (around 5 minutes), the service will no longer successfully respond to
requests.

As you look at the panels, you will notice that 5xx errors will start to show
up in the **Virtual Server Requests** panel.  This gives you a quick view
that something bad is starting to occur in the back-end applications, but you
cannot tell which application may be the one experiencing the trouble.  If
you click on the 5xx line, you will get a drill down panel populated which
will show you which applications are reporting the 5xx errors.  As you would
expect, all the errors are coming from the Example application.

Since it looks like the Example application has a catastrophic error
condition, you can try to fix it by going to the Marathon UI and restarting
the instance.  Go ahead and perform this step, and then observe the Splunk
panels to see if that solved anything (at least, for the next 5 minutes).

This concludes the demonstration of many of the F5 Container Integration
features.  Remember that if you started the Marathon-Mesos environment in
AWS, you will continue to be billed until you delete your stack.