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


.. _F5 Analytics App: https://splunkbase.splunk.com/app/3161/
