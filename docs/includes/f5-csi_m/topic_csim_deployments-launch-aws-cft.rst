Launch the Cloud Formation Stack in AWS
---------------------------------------

#. Log in to your AWS account.
#. Go to `AWS CloudFormation <https://console.aws.amazon.com/cloudformation>`_.
#. Click :guilabel:`Create New Stack`.
#. Upload the :download:`CloudFormation template </static/f5-csi_m/f5-csim-cloudformation.json>`.
#. Click :guilabel:`Next`.
#. Enter the required :guilabel:`Parameters`.

    .. list-table:: CFT Configuration Parameters
        :header-rows: 1

        * - Field
          - Description
        * - ``AdminLocation``
          - | This is a CIDR subnet that will limit access to your stack.
            | Only IPs in this subnet can get to the BIG-IP, Mesos, and
            | Marathon administrative interface.
            | The default setting, "0.0.0.0/0",  allows access from any host.
            | You can restrict access to just your external ip
            | (e.g., 63.149.112.92/32). [#]_
        * - ``BIGIPRegKey``
          - | Enter the registration key for your BIG-IP.
        * - ``KeyName``
          - | Select the AWS SSH keypair you wish to use.
        * - ``OAuthEnabled``
          - | Use the default setting.
        * - ``SlaveInstanceCount``
          - | Use the default setting.

#. Click :guilabel:`Next`.
#. :guilabel:`Options`: Enter tags and/or edit Advanced configurations; or, just click :guilabel:`Next`.
#. :guilabel:`Review`: Review the information provided, then check the Identity and Access Management "I acknowledge.."  box.
#. Click :guilabel:`Create`.

.. [#] There are several ways to find your external IP address (**NOTE**: this is not necessarily  the IP address of your local host). For example, on Linux, issue the command ``curl https://api.ipify.org`` and your external IP address will be displayed.


View your stack
```````````````

#. Click the :guilabel:`Refresh` button to view the stack list. The status of your stack will initially be displayed as "CREATE_IN_PROGRESS". If you wish to view the creation events, click on the :guilabel:`Events` tab.
#. Once the stack is created, you will have a BIG-IP running alongside the MesoSphere DC/OS environment. These are listed under the :guilabel:`Resources` tab.
#. The :guilabel:`Outputs` tab contains the necessary information for accessing the stack resources. These allow you to access your BIG-IP, the Marathon UI, and Splunk.

    .. list-table:: CFT Outputs
        :header-rows: 1

        * - Output
          - Description
        * - ``BIGIPAdminUI``
          - | The IP address for the BIG-IP configuration utility
            | (aka, the UI).
        * - ``BIGIPAdminPassword``
          - | The password for the 'admin' user on the BIG-IP.
        * - ``MarathonUI``
          - | The URL for the Marathon UI.
        * - ``SplunkReadySSH``
          - | The ssh command to log into the Splunk-ready instance.
        * - ``SplunkReadyPrivateIP``
          - | If you install Splunk on the 'Splunk-ready instance' deployed
            | as part of the CloudFormation stack,
            | substitute this value for ``[SPLUNK_IP]``.

.. note::

    * The first time you access the BIG-IP configuration utility, you may see the "Configuration Utility restarting..." message. This message should resolve after about 5 minutes. *If it does not resolve*, please contact  `F5 support <https://f5.com/support>`_.
    * A partition called "mesos" was created on the BIG-IP for use with this demo. **All LTM objects originating in Mesos will be created in this partition.**

