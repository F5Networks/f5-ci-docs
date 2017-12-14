Troubleshoot Your OpenShift Deployment
======================================

.. toctree::
   :maxdepth: 1

How to get help
---------------

If the issue you're experiencing isn't covered here, try one of the following options:

- `Contact F5 Support`_ (valid support contract required).
- `Report a bug <https://github.com/F5Networks/k8s-bigip-ctlr/issues>`_ in the k8s-bigip-ctlr GitHub repo.
- `Ask a question <https://f5cloudsolutions.slack.com>`_ in the #cc-kubernetes channel in the F5 Cloud Solutions Slack team.


General OpenShift troubleshooting
---------------------------------

The following troubleshooting doc(s) may help with OpenShift-specific issues.

- `OpenShift: Troubleshooting OpenShift SDN <https://docs.openshift.org/1.5/admin_guide/sdn_troubleshooting.html>`_

.. _k8s-bigip-ctlr troubleshoot openshift:

BIG-IP Controller troubleshooting
---------------------------------

.. tip::

   You can use `oc`_ commands to check the |kctlr| configurations using the command line.

   .. code-block:: console

      oc get pod -o yaml                \\ Returns the Pod's YAML settings
      oc describe pod myBigIpCtlr       \\ Returns an information dump about the Pod you can use to troubleshoot specific issues


.. _controller verify openshift:

I just deployed the Controller; how do I verify that it's running?
``````````````````````````````````````````````````````````````````

#. Find the name of the k8s-bigip-ctlr Pod.

   .. code-block:: console

      oc get pod
      NAME                             READY     STATUS    RESTARTS   AGE
      k8s-bigip-ctlr-687734628-7fdds   1/1       Running   0          15d

#. Check the status of the Pod.

   .. code-block:: console

      oc get pod k8s-bigip-ctlr-687734628-7fdds -o yaml

   .. _troubleshoot openshift view-logs:

#. View the Controller logs.

   .. code-block:: console
      :caption: View the logs

      oc logs k8s-bigip-ctlr-687734628-7fdds

   .. code-block:: console
      :caption: Follow the logs

      oc logs -f k8s-bigip-ctlr-687734628-7fdds


   .. code-block:: console
      :caption: View logs for a container that isn't responding

      oc logs --previous k8s-bigip-ctlr-687734628-7fdds


How do I set the log level?
```````````````````````````

To change the log level for the |kctlr|:

#. Annotate the :ref:`Deployment <kctlr-configure-openshift>` for the |kctlr|.

   .. code-block:: console

      oc annotate k8s-bigip-ctlr.yaml "--log-level=DEBUG"

#. Verify the Deployment updated successfully.

   .. code-block:: console

      oc describe deployment k8s-bigip-ctlr -o wide

-----------------------------------------

.. _bigip-config warning openshift:

.. include:: /_static/reuse/bigip-conf-overwrite.rst

-----------------------------------------

Why didn't the BIG-IP Controller create any objects on my BIG-IP?
`````````````````````````````````````````````````````````````````

Here are a few basic things to check:

.. _json troubleshoot openshift:

.. include:: /_static/reuse/controller-json-troubleshoot.rst

.. _schema troubleshoot openshift:

.. include:: /_static/reuse/schema-troubleshoot.rst


.. _bigip-partition troubleshoot openshift:

.. include:: /_static/reuse/bigip-partition-troubleshoot.rst

-----------------------------------------

.. _ingress troubleshoot openshift:

.. todo:: Why didn't the |kctlr| create the pools/rules for my Ingress on the BIG-IP system?


.. _iapp traffic group openshift:

Why did I see a traffic group error when I deployed my iApp?
````````````````````````````````````````````````````````````

When deploying an iApp with the |kctlr-long| and OpenShift, the iApp may create a virtual IP in the wrong traffic group. If this occurs, you will see an error message like that below.

.. code-block:: console

   Configuration error: Unable to to create virtual address (/openshift/127.0.0.2) as part of application
   (/os/default_os.http.app/default_os.http) because it matches the self ip (/Common/selfip.external)
   which uses a conflicting traffic group (/Common/traffic-group-local-only)

If you've seen this error, you can override or change the default traffic-group as follows:

- Set the specific traffic group you need in the ``iappOptions`` section of the virtual server F5 Resource definition.
- **Preferred** Set the desired traffic group as the default for the partition you want the |kctlr| to manage. This option doesn't require Kubernetes/OpenShift to know about BIG-IP traffic groups.

  .. code-block:: javascript

     "trafficGroup": "/Common/traffic-group-local-only"

-----------------------------------------

.. _networking troubleshoot openshift:

Network troubleshooting
-----------------------

How do I verify connectivity between the BIG-IP VTEP and the OSE Node?
``````````````````````````````````````````````````````````````````````

#. Ping the Node's VTEP IP address.

   Use the ``-s`` flag to set the MTU of the packets to allow for VxLAN encapsulation. ::

     ping -s 1600 <OSE_Node_IP>

#. :ref:`View the logs <troubleshoot openshift view-logs>` for the k8s-bigip-ctlr.

   .. tip:: Use the ``-f`` option to follow the logs.

#. In a TMOS shell, output the REST requests from the BIG-IP logs.

   - Do a ``tcpdump`` of the underlay network. ::

       tcpdump -i <name-of-BIG-IP-VXLAN-tunnel>

     \

     .. code-block:: console
        :caption: Example showing two-way communication on port 4789 between the BIG-IP VTEP IP and the OSE node VTEP IPs.

        root@localhost:Active:Standalone] config # tcpdump -i ocpvlan
        08:08:06.933951 IP 10.214.1.102.58472 > 10.214.1.23.4789: VXLAN, flags [I] (0x08), vni 0
        IP 10.130.0.27.http > 10.128.2.10.37542: Flags [.], ack 9, win 219, options [nop,nop,TS val 573988389 ecr 3961177660], length 0 in slot1/tmm1 lis=_wcard_tunnel_/Common/ose-tunnel
        08:08:06.934310 IP 10.214.1.23.28277 > 10.214.1.102.4789: VXLAN, flags [I] (0x08), vni 0
        IP 10.128.2.10.37542 > 10.130.0.27.http: Flags [.], ack 923, win 251, options [nop,nop,TS val 3961177661 ecr 573988389], length 0 out slot1/tmm0 lis=_wcard_tunnel_/Common/ose-tunnel

   - Do a ``tcpdump`` of the overlay network. ::

       tcpdump -i <name-of-BIG-IP-VXLAN-tunnel>

     \

     .. code-block:: console
        :caption: Example showing traffic on the overlay network; at minimum, you should see BIG-IP health monitors for the Pod IP addresses.

        root@localhost:Active:Standalone] config # tcpdump -i ose-tunnel
        08:09:51.911667 IP 10.128.2.10.38036 > 10.130.0.27.http: Flags [.], ack 1, win 229, options [nop,nop,TS val 3961282640 ecr 574093366], length 0 out slot1/tmm0 lis=
        08:09:51.911672 IP 10.128.2.10.38036 > 10.130.0.27.http: Flags [P.], seq 1:8, ack 1, win 229, options [nop,nop,TS val 3961282640 ecr 574093366], length 7 out slot1/tmm0 lis=
        08:09:51.913161 IP 10.130.0.27.http > 10.128.2.10.38036: Flags [.], ack 8, win 219, options [nop,nop,TS val 574093369 ecr 3961282640], length 0 in slot1/tmm0 lis=
        08:09:51.913265 IP 10.130.0.27.http > 10.128.2.10.38036: Flags [P.], seq 1:922, ack 8, win 219, options [nop,nop,TS val 574093369 ecr 3961282640], length 921 in slot1/tmm0 lis=

#. In a TMOS shell, view the VLAN statistics.

   - Underlay ::

       tmsh show net vlan <name_of_vlan_used_for_VTEP>

     \

     .. code-block:: console
        :caption: Example

        root@localhost:Active:Standalone] config # tmsh show net vlan ocpvlan
        -------------------------------------
        Net::Vlan: ocpvlan
        -------------------------------------
        Interface Name      ocpvlan
        Mac Address (True)  00:0c:29:fe:f9:4e
        MTU                 1500
        Tag                 4094
        Customer-Tag
          -----------------------
          | Net::Vlan-Member: 1.1
          -----------------------
          | Tagged    no
          | Tag-Mode  none
             -------------------------------------------------------------
             | Net::Interface
             | Name  Status   Bits   Bits   Pkts  Pkts  Drops  Errs  Media
             |                  In    Out     In   Out
             -------------------------------------------------------------
             | 1.1       up  52.8G  17.0G  14.6M  7.4M      0     0   none

   - Overlay ::

       tmsh show net vlan <name_of_VXLAN_tunnel_on_BIG-IP>

     \

     .. code-block:: console
        :caption: Example

        root@localhost:Active:Standalone] config # tmsh show net tunnels tunnel ose-tunnel
        -------------------------------------
        Net::Tunnel: ose-tunnel
        -------------------------------------
        Incoming Discard Packets            0
        Incoming Error Packets              0
        Incoming Unknown Proto Packets      0
        Outgoing Discard Packets            0
        Outgoing Error Packets              0
        HC Incoming Octets               1.8G
        HC Incoming Unicast Packets     10.2M
        HC Incoming Multicast Packets       0
        HC Incoming Broadcast Packets       5
        HC Outgoing Octets               1.8G
        HC Outgoing Unicast Packets     10.2M
        HC Outgoing Multicast Packets   91.6K
        HC Outgoing Broadcast Packets   92.7K

#. In a TMOS shell, view the MAC address entries for the OSE tunnel. This will show the mac address and IP addresses of all of the OpenShift endpoints.

   ::

      tmsh show net fdb tunnel <name_of_VXLAN_tunnel on BIG-IP>

   \

   .. code-block:: console
      :caption: Example

      root@localhost:Active:Standalone] config # tmsh show net fdb tunnel ose-tunnel
      -------------------------------------------------------------
      Net::FDB
      Tunnel      Mac Address        Member                 Dynamic
      -------------------------------------------------------------
      ose-tunnel  0a:58:0a:82:00:1b  endpoint:10.214.1.102  yes
      ose-tunnel  0a:58:0a:82:00:21  endpoint:10.214.1.102  yes
      ose-tunnel  0a:58:0a:82:00:25  endpoint:10.214.1.102  yes


#. In a TMOS shell, view the ARP entries. This will show all of the ARP entries; you should see the VTEP entries on the ocpvlan and the Pod IP addresses on ``ose-tunnel``.

   .. code-block:: console

      root@localhost:Active:Standalone] config # tmsh show net arp
      ------------------------------------------------------------------------------------------
      Net::Arp
      Name          Address       HWaddress          Vlan                Expire-in-sec  Status
      ------------------------------------------------------------------------------------------
      10.130.0.27   10.130.0.27   0a:58:0a:82:00:1b  /Common/ose-tunnel  224            resolved
      10.130.0.33   10.130.0.33   0a:58:0a:82:00:21  /Common/ose-tunnel  220            resolved
      10.130.0.37   10.130.0.37   0a:58:0a:82:00:25  /Common/ose-tunnel  222            resolved
      10.214.1.100  10.214.1.100  00:0c:29:c8:4c:dc  /Common/ocpvlan     220            resolved
      10.214.1.101  10.214.1.101  00:0c:29:8d:ac:42  /Common/ocpvlan     220            resolved
      10.214.1.102  10.214.1.102  00:0c:29:cd:ba:44  /Common/ocpvlan     220            resolved



.. _service type: https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services---service-types
.. _v1.3 features: /products/connectors/k8s-bigip-ctlr/latest/RELEASE-NOTES.html#v1-3-0
