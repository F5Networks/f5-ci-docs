.. _csim-deployments-splunk-setup:

Set up Splunk
-------------

Install Splunk on the CF Splunk-ready Instance
``````````````````````````````````````````````

.. tip:: If you already have a Splunk instance set up, skip to the next section.

Because Splunk needs to receive data from the BIG-IP and the Mesos cluster, it must run somewhere that external traffic can reach it (i.e., if you're running it from your laptop behind a firewall, it probably won't work).

Follow the instructions in this section, and the Splunk `Installation <http://docs.splunk.com/Documentation/Splunk/6.4.2/Installation/InstallonLinux>`_ guide, to set up Splunk on the Splunk-ready Amazon Linux instance created in your cloud stack.

#. SSH into the Splunk-ready instance using the ``SplunkReadySSH`` cloud output value.

#. Download the free trial of `Splunk Enterprise <https://www.splunk.com/en_us/download/splunk-enterprise.html>`_ from the Splunk downloads site to your EC2 instance.

    .. code-block:: bash
        :caption: Example - Use wget to download Splunk

        wget -O splunk-6.4.3-b03109c2bad4-Linux-x86_64.tgz 'https://www.splunk.com/bin/splunk/DownloadActivityServlet?architecture=x86_64&platform=linux&version=6.4.3&product=splunk&filename=splunk-6.4.3-b03109c2bad4-Linux-x86_64.tgz&wget=true'

#. Follow the steps in the `Install Splunk Enterprise <http://docs.splunk.com/Documentation/Splunk/6.4.2/Installation/InstallonLinux>`_ guide to install and start Splunk for the first time.

    .. note::

        You may need to ``chmod`` or ``chown`` the directory in which Splunk (``/opt/splunk``) is installed to complete the startup.

#. Log in to the Splunk GUI.

    * URL: Use the public IP provided in the description of the Splunk-ready instance in AWS, like so: ``http://<public-splunk-ip>:8000``
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

.. important::

    The BIG-IP and Mesos nodes can send data to Splunk at the ``SplunkReadyPrivateIP`` provided in the CF Outputs.


Install Splunk Apps
```````````````````

In the previous section, you configured your Splunk instance to receive data from the analytics providers. Now, you will configure Splunk apps that provide data visualization: Sankey; F5's Network Analytics; and F5's Lightweight Proxy Analytics.

#. Install the Sankey App:

    * Download the `Sankey App <https://splunkbase.splunk.com/app/3112/>`_ from Splunkbase.
    * In the Splunk GUI, click on :menuselection:`Apps --> Manage Apps`.
    * Click :guilabel:`Install app from file`.
    * Click :guilabel:`Choose File` and select the Sankey download file.
    * Click :guilabel:`Upload`.
    * Accept the license agreement, then click the :guilabel:`Login and Install` button.
    * Restart Splunk when prompted, then log back in.

#. Install the F5 Networks Analytics App:

     * Download the file :file:`f5-networks-analytics-new_095.tgz` from `downloads.f5.com <https://downloads.f5.com/>`_ to your local drive.
     * In the Splunk GUI, click on :menuselection:`Apps --> Manage Apps`.
     * Click :guilabel:`Install app from file`.
     * Click :guilabel:`Choose File` and select :file:`f5-networks-analytics-new_095.tgz`.
     * Click :guilabel:`Upload`.

#. Install the F5 Lightweight Proxy Analytics App:

     * Download :file:`f5-lightweight-proxy-analytics-v0.1.0.tgz` from `downloads.f5.com <https://downloads.f5.com/>`_ to your local drive.
     * Click :guilabel:`Install app from file`.
     * Click :guilabel:`Choose File` and select :file:`f5-lightweight-proxy-analytics-v0.1.0.tgz`.
     * Click :guilabel:`Upload`.

#. Verify installation:

     * Click the :guilabel:`splunk>` logo to view the main panel. The installed apps should be displayed on the left side of the screen.

#. **Optional**: Set the F5 Lightweight Proxy app as the default display panel:

    * Click :guilabel:`Choose a home dashboard`.
    * Click :guilabel:`F5 Networks Lightweight Proxy`.
    * Click :guilabel:`Save`.


Deploy F5 Analytics iApp
````````````````````````

To enable stats collection on your BIG-IP and send the data to Splunk, launch the F5 analytics iApp® from your BIG-IP.

#. Download :file:`f5.analytics.tmpl` from `downloads.f5.com <https://downloads.f5.com/>`_.

#. Log in to the BIG-IP configuration utility.

#. Select :menuselection:`IApps/Templates --> Import`.

#. Upload the iApp template (:file:`f5.analytics.tmpl`).

#. Ensure you are in the Common partition (top-right), then select :menuselection:`IApps/Application Services --> Create`.

#. Choose the :file:`f5.analytics` template.

#. Fill in the fields specified in the table below; unspecified fields should use the default setting.

    .. list-table:: F5 Analytics iApp configurations
        :header-rows: 1

        * - Field
          - Entry
        * - Name
          - [user defined]
        * - Module HSL Streams
          - No
        * - Local System Logging (syslog)
          - No
        * - System SNMP Alerts
          - No
        * - iHealth Snapshot Information
          - No
        * - Your Facility Name
          - [user defined]
        * - Default Tenant
          - [user defined]
        * - Alternative Device Group
          - [user defined]
        * - IP Address or Hostname
          - [SPLUNK_IP]
        * - Port
          - ``8088``
        * - Protocol
          - ``HTTPS``
        * - API Key
          - [SPLUNK_TOKEN]
        * - Push Interval
          - 20
        * - Mapping Table: 1
          - ``Type=[App Name] From=[Virtual Name] Regex= (.*)_\d  Action=Map``
        * - Mapping Table: 2
          - ``Type=[Tenant Name] From=[Partition] Regex=(.*) Action=Map``

#. Click :guilabel:`Finished`.

