:product: Container Connectors
:type: tutorial

.. _send-stats-splunk:

How to send statistics to Splunk
================================

You can send data from your BIG-IP device(s) to `Splunk`_ for analysis. This tutorial leads you through the steps required to send data from a BIG-IP device to a Splunk instance.

Before you begin
----------------

- If you don't already have a Splunk instance, `install and configure Splunk <https://docs.splunk.com/Documentation>`_.
- Install and configure the :ref:`Container Connector <containers-home>` for your orchestration environment.

  - :ref:`Deploy the cf-bigip-ctlr in Cloud Foundry <deploy-cf-ctlr>`
  - :ref:`Deploy the k8s-bigip-ctlr in Kubernetes <install-kctlr>`
  - :ref:`Install the marathon-bigip-ctlr in Marathon <install-mctlr>`

------------------------------------------

**tl/dr: Watch the installation video:**

.. raw:: html

   <iframe width="560" height="315" src="https://www.youtube.com/embed/Z6KPelL5YC4?rel=0&amp;start=113" frameborder="0" allowfullscreen></iframe>

-------------------------------------------

Set up Splunk to receive data
-----------------------------

#. Add a new :guilabel:`HTTP Event Collector`:

   * Click on the :guilabel:`Apps` gear icon.
   * Go to :menuselection:`Settings --> Data inputs`.
   * Click on :guilabel:`HTTP Event Collector`.
   * Click on :guilabel:`Global Settings`.
   * Click on :guilabel:`Enabled`.
   * Click :guilabel:`Save`.
   * Click on :guilabel:`New Token`.
   * Enter a name for the token, then click :guilabel:`Next`.
   * On the :guilabel:`Input Settings` screen, click :guilabel:`Create a new index`.
   * Name the index, then click :guilabel:`Save`.
   * Make sure the new index is the :guilabel:`Default index`.
   * Click :guilabel:`Review`, then click :guilabel:`Submit`.
   * Record the :guilabel:`Token Value` Splunk created for your HTTP Event Collector; **you'll configure the BIG-IP system with this value later**.

#. Install the `F5 Analytics App`_.

   * In the Splunk GUI, click on :menuselection:`Apps --> Find More Apps`.
   * Search for "F5 Networks".
   * Click :guilabel:`Install` and enter your splunk.com credentials (this is your actual Splunk account, not the instance login).
   * Accept the license agreement, then click the :guilabel:`Login and Install` button.
   * When the installation is complete, you can view the App, or click Done.

#. Configure your firewall to allow port 8088 to be open to Splunk.

   .. important::

      The event collector listens on port 8088 and requires HTTPS.

Send stats from a BIG-IP device to Splunk
-----------------------------------------

Use the `F5 Analytics iApp`_ template to enable stats collection on your BIG-IP device and send the data to Splunk.

.. seealso::

   The instructions provided here cover the basics of iApp deployment. See the `F5 Analytics iApp Deployment Guide`_ for additional details

Deploy the F5 Analytics iApp
````````````````````````````

Download the `F5 Analytics iApp`_ from DevCentral, then upload it to the Common partition on the BIG-IP device.

#. Select :menuselection:`IApps/Templates --> Import`.

#. Upload the iApp template (:file:`f5.analytics.tmpl`).

#. Select :menuselection:`IApps/Application Services --> Create`.

#. Choose the :file:`f5.analytics` template.

#. Fill in the following fields; unspecified fields should use the default setting.

   * Name - [user defined]
   * Template - f5.analytics
   * Module HSL Streams - ``No``
   * Local System Logging (syslog) - ``No``
   * System SNMP Alerts - ``No``
   * iHealth Snapshot Information - ``No``
   * Facility Name - [user defined]
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

.. _F5 Analytics iApp Deployment Guide: https://www.f5.com/pdf/deployment-guides/f5-analytics-dg.pdf
.. _F5 Analytics iApp: https://devcentral.f5.com/codeshare/f5-analytics-iapp
.. _F5 Analytics App: https://splunkbase.splunk.com/app/3161/
