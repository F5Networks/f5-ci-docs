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
to send data to a Splunk instance. If you have a Splunk instance available,
instructions are provided to send data to that instance. If you do not,
Splunk offers an evaluation program **TODO: details**


Introduction
============

**NOTE: Assuming another doc has provided the high-level architecture**

The components in this usage guide have been tested on these environments and versions:

Mesos:
Marathon:
Docker:

Step 1: Set up Mesos and Marathon
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

Step 2: Deploy f5-marathon-lb (CSI)
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

