.. _send-stats-splunk:

How to send statistics to Splunk
================================

The |asp| (ASP) and BIG-IP device(s) can send data to `Splunk`_ for analysis.
This tutorial leads you through the steps required to send data from a BIG-IP device and an ASP instance to a Splunk instance.

Before you begin
----------------

- If you don't already have a Splunk instance, `install and configure Splunk <https://docs.splunk.com/Documentation>`_.

.. rubric:: If you're sending data from a BIG-IP device to Splunk:

- Install and configure the :ref:`Container Connector <containers-home>` for your orchestration environment.

  - :ref:`Deploy the k8s-bigip-ctlr in Kubernetes <install-kctlr>`
  - :ref:`Install the marathon-bigip-ctlr App in Marathon <install-mctlr>`

.. rubric:: If you're sending data from the ASP to Splunk:

-  Install and configure the |asp| as appropriate for your orchestration environment.

   - :ref:`Install the ASP in Kubernetes <install-asp-k8s>`
   - :ref:`Install the ASP in Marathon <install-asp-marathon>`

.. seealso::

   Application Services Proxy `Telemetry Module`_


Set up Splunk to receive data
-----------------------------

#. Add a new :guilabel:`HTTP Event Collector`:

   * Click on the :guilabel:`Apps` gear icon.
   * Go to :menuselection:`Settings --> Data inputs`.
   * :guilabel:`Add new` :guilabel:`HTTP Event Collector`.
   * Enter a name for the collector; all other fields can use the default values.
   * Click :guilabel:`Next`, then :guilabel:`Review`, then :guilabel:`Submit`.
   * Record the :guilabel:`Token Value` Splunk created for your HTTP Event Collector; **you'll configure the analytics providers with this value later**.

#. Enable the :guilabel:`HTTP Event Collector`:

   * Go to :menuselection:`Settings --> Data inputs`.
   * Click on :guilabel:`HTTP Event Collector`, then on :guilabel:`Global Settings`.
   * Click on :guilabel:`Enabled`.
   * Click :guilabel:`Save`.

#. Configure your firewall to allow port 8088 to be open to Splunk.

   .. important::

      The event collector listens on port 8088 and requires HTTPS.

#. Install the `Sankey Splunk App`_:

   * In the Splunk GUI, click on :menuselection:`Apps --> Find More Apps`.
   * Search for "Sankey".
   * Click "Install" and enter your splunk.com credentials (this is your actual Splunk account, not the instance login).
   * Accept the license agreement, then click the :guilabel:`Login and Install` button.
   * Restart Splunk when prompted, then log back in.

Send stats from a BIG-IP device to Splunk
-----------------------------------------

Use an F5 iApps template to enable stats collection on your BIG-IP device and send the data to Splunk.
The `F5 Analytics iApp`_ is available for download from the F5 DevCentral codeshare.

Deploy the F5 Analytics iApp on the BIG-IP
``````````````````````````````````````````

Download the `F5 Analytics iApp`_ from DevCentral, then upload it to the BIG-IP device using the configuration utility.

#. Select :menuselection:`IApps/Templates --> Import`.

#. Upload the iApp template (:file:`f5.analytics.tmpl`).

#. Select :menuselection:`IApps/Application Services --> Create`.

#. Choose the :file:`f5.analytics` template.

#. Fill in the following fields; unspecified fields should use the default setting.

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

.. todo:: add instructions for deployment from Kubernetes and Marathon using the iApp variables


Send stats from the ASP to Splunk
---------------------------------

Kubernetes
``````````

#. Edit the `Service`_ annotation.

   .. code-block:: bash

      $ kubectl edit service <service-name>

#. Add the "stats" JSON blob.

   .. note::

      - You must escape all quotes, as shown in the example below.
      - Provide the URL and token for your Splunk instance.

   .. code-block:: text

      \"stats\": {
        \"url\": \"splunk-url\",
        \"token\": \"splunk-token\",
        \"backend\": \"splunk\"
      }

#. Verify the change to the Service annotation.

   .. code-block:: bash

      $ kubectl get service <service-name>

Marathon
````````

Add the ``ASP_DEFAULT_STATS_*`` labels to the |aspm| App.

#. In the Marathon web interface, click on the |aspm| App.

#. Click :guilabel:`Configuration`.

#. Click :guilabel:`Edit`.

#. Click :guilabel:`Labels`.

#. Add the stats labels. Provide the URL and token for your Splunk instance.

   .. code-block:: text

      "ASP_DEFAULT_STATS_URL": "splunk-url"
      "ASP_DEFAULT_STATS_TOKEN": "splunk-token"
      "ASP_DEFAULT_STATS_BACKEND": "splunk"

#. Click :guilabel:`Change and deploy configuration`.

#. View the Applications list to verify that the STATS labels appear for all ASP-proxied Apps.


.. _Sankey Splunk App: https://splunkbase.splunk.com/app/3112/
.. _F5 Analytics iApp: https://devcentral.f5.com/codeshare/f5-analytics-iapp
