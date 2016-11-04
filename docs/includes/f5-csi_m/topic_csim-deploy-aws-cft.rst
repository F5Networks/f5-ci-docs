.. _csim-deploy-aws-cft-getting-started:

Overview
--------

Upon completing this guide, you will have an Amazon Web Services (AWS) Cloud Formation (CF) stack running the following:

    * BIG-IP® Virtual Edition (VE),
    * a Mesos / Marathon cluster with several running applications,
    * a Splunk instance that can receive and analyze data from BIG-IP and the F5 |lwp| |tm|.

Prerequisites
`````````````

- The F5 |csi_m-long| package, avilable at `downloads.f5.com <#>`_
- An AWS account that can incur charges. While we attempt to utilize free services wherever possible, there will be a charge to run this stack in AWS.
- An SSH keypair configured in AWS and on any machine from which you want to access the VMs in your CF stack.
- A BIG-IP registration key (Good, Better, or Best license); a VE lab license that can be used in AWS can be provided by an F5 sales rep.
- Internet access; this is required for AWS to access the F5 Docker images.
- A `Splunk`_ user account (required for installing Apps in your Splunk instance).

Caveats
```````

- **This guide uses an AWS CloudFormation template (CFT) that incurs charges while the stack is running.** Delete the stack when you have completed the demo to ensure that you will not continue to be charged.

Getting Started
```````````````

First, you'll need to accept our EULA for BIG-IP VE in Amazon.

#. Go to the BIG-IP VE Amazon Marketplace page for `F5 BIG-IP Virtual Edition Good (BYOL) <http://aws.amazon.com/marketplace/pp?sku=dzweylwc4hxloqophyoi3oihr>`_.
#. Select your region from the drop-down menu.
#. Click on the :guilabel:`Continue` button.
#. Click on :guilabel:`Accept Software Terms`.

.. warning::

   If you do not complete this step before launching the CloudFormation template, your stack creation will fail.

Next, download our CloudFormation template:

:download:`f5-csim-cloudformation.json </static/f5-csi_m/f5-csim-cloudformation.json>`

