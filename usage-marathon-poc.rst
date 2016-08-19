Usage Guide: F5 Container Integration in a Mesos/Marathon Environment
=====================================================================

This guide describes how to set up a reference F5 Container Integration in an
environment with Mesos and Marathon. We suggest that you start by following
these steps to understand the components and services that we provide.

You do not need a Mesos and Marathon environment. If you do not have one, the
first few steps will help you set one up. If you do have an existing
environment that you would like to use, you can skip these steps.
(**TODO: Fill in which steps can be skipped.**)

This usage guide will also describe how to configure the analytics providers
(e.g. Big-IP and the Lightweight Proxy) to send data to a Splunk instance.
Additionally, to make full use of the data sent, instructions are provided on
how to install several F5 Splunk apps on the Splunk instance in order to
process and display the data.   If you do not have an available instance,
Splunk offers a 60-day evaluation program at
https://www.splunk.com/en_us/download/splunk-enterprise.html.


Introduction
============

**NOTE: Assuming another doc has provided the high-level architecture**

The components in this usage guide have been tested on these environments and
versions:

| Mesos: 0.27.1
| Marathon: 0.15.3
| Docker: 1.9.1
| Splunk: 6.4.2
| F5 Analytics Splunk App: 0.9.5
| F5 Lightweight Proxy Splunk App: 0.1.0
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
access to an AWS CloudFormation template called **TODO**. Download
this CloudFormation template and start it in your account.

Inputs:

KeyName: You must select an SSH keypair that is configured in AWS. You'll
need this to log in to the VMs that are started.

AdminLocation: This is a CIDR subnet that is configured to limit access to
the stack that is produced. Only IPs in this subnet can get to the BIG-IP,
Mesos, or Marathon administrative interface. The default is "0.0.0.0/0" which
allows access from any host.

BIGIPRegKey: Use the evaluation registration key that was provided to you
as a member of the beta program.

**TODO: Any EULAs for Mesosphere? Hopefully getting rid of that**

All other inputs leave at their default.

Once the stack is set up, check the stack outputs:

BIGIPAdminUI: Navigate to this URL in a browser and log in with the username
"admin" and the password from the *BIGIPAdminPassword* output.

MarathonUI: Navigate to this URL in a browser and confirm that you see
a Marathon user interface, with no applications running.

Step 4: Deploy f5-marathon-lb (CSI)
-----------------------------------

**f5-marathon-lb** is a component of the Container Service Integrator (CSI). It
is packaged in a container and it runs in the Marathon environment. It will
connect to Marathon as well as the BIG-IP. It watches changes in Marathon
and configures new elements like virtual servers and pool members on BIG-IP
in response. For detailed information, see **TODO**. For now,
we'll set up a few simple configurations.

Go to the Marathon UI, click on "Create", and fill out the options in the UI
like the following:

**TODO**

Click "Create" and then observe that the application is created in Marathon.
You may see the application show as "Staged" while Marathon and Mesos schedule
the application task, download the container, and start it. You will see it
show as "Started" once it has started.

Click on the application *f5-marathon-lb* and you will see a page showing the
tasks (there is only 1 task for f5-marathon-lb). Click on the task and you can
see more details. There will be a row saying "Mesos details: link"; click on
this link to see Mesos details. Then, click on "Sandbox" to see the container
sandbox that it is running in. Click on "stdout" and "stderr" to see the logs
from the *f5-marathon-lb*. It should say:

**TODO: Example of a happy f5-marathon-lb**

Deployment Test Cases
=====================

Deploy the frontend-service as a North-South Service
----------------------------------------------------

coming soon!

Scale the frontend-service up
-----------------------------

coming soon!

Reconfigure the frontend-service to use the f5.http iApp
--------------------------------------------------------

coming soon!

Configure the lwp-controller (CSI)
----------------------------------

coming soon!

Deploy an example East-West Service
-----------------------------------

coming soon!

Scale the example service up
----------------------------

coming soon!

Deploy complex microservices topology
-------------------------------------

coming soon!

Inject, diagnose, and address errors
------------------------------------

coming soon!

