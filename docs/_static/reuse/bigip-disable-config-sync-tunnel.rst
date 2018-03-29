.. code-block:: console
   :caption: Disable config sync for tunnels and save the config

   tmsh modify sys db iptunnel.configsync value disable
   tmsh save sys config

When you `disable config sync for tunnels`_, the BIG-IP does not sync information from tunnels across devices.
This means you can manually sync configurations across your devices without wiping out or breaking the VIPs associated with the OpenShift subnets on either device.

.. pull-quote::

   **For example:**

   - BIG-IP_01 has VIPs configured on subnet :code:`openshift-vxlanA`.
   - BIG-IP_02 has VIPs configured on subnet :code:`openshift-vxlanB`.

   **If you don't disable config sync for tunnels**, the following actions will occur when you manually sync configurations from BIG-IP_01 to BIG-IP_02:

   - the VIPs from BIG-IP_01 will sync to BIG-IP_02;
   - the VIPs on BIG-IP_02 get deleted, because they don't exist on BIG-IP_01;
   - all traffic to VIPs from BIG-IP_01 will fail because :code:`openshift-vxlanA` doesn't exist on BIG-IP_02;
   - all traffic to VIPs from :code:`openshift-vxlanB` will fail because the VIPs no longer exist.

