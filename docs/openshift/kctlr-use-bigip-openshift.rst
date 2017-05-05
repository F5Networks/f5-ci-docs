.. _bigip-openshift-setup:

Set up BIG-IP and |kctlr| for use in an OpenShift Cluster
=========================================================

.. sidebar:: Docs test matrix

   We tested this documentation with:

   - BIG-IP v12.1.1
   - OpenShift Origin v1.3.2

Summary
-------

Steps required to set up a BIG-IP device and |kctlr| for use in an `OpenShift`_ cluster:

#. :ref:`Create a host subnet <k8s-openshift-hostsubnet>` in your OpenShift cluster.
#. :ref:`Create a VXLAN tunnel <k8s-openshift-vxlan-setup>` on the BIG-IP device.
#. :ref:`Assign an overlay address <k8s-openshift-assign-ip>` from the subnet to a BIG-IP `Self IP address`_.
#. `Create an OpenShift user account`_ for the |kctlr| with permission to manage the following:

    - nodes
    - endpoints
    - services
    - configmaps
    - namespaces

.. note::

   In our lab, we used the namespace 'management-infra' and the ``serviceAccountName`` 'management-admin'.


.. _k8s-openshift-hostsubnet:

Create a new OpenShift HostSubnet
----------------------------------

Define a HostSubnet using valid JSON or YAML.

.. code-block:: bash

   user@openshift:~$ oc create -f f5-kctlr-openshift-hostsubnet.yaml


.. important::

   - You must define 'subnet' as a range within OpenShift Origin's overlay network. The default network is 10.128.0.0/14. [#ossdn]_
   - You must include the "annotation" section shown in the example below.

.. literalinclude:: /_static/config_examples/f5-kctlr-openshift-hostsubnet.yaml
   :linenos:
   :emphasize-lines: 5-15

:download:`Download the example </_static/config_examples/f5-kctlr-openshift-hostsubnet.yaml>`

.. _k8s-openshift-vxlan-setup:

Create a BIG-IP VXLAN
---------------------

#. Create a new VXLAN profile on the BIG-IP device using multi-point flooding.

   .. code-block:: bash

      admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$ create net \\
      tunnels vxlan vxlan-mp flooding-type multipoint

#. Verify creation of the profile.

   .. code-block:: bash
      :emphasize-lines: 1, 13

      curl -u USER:PASSWORD -X GET https://10.190.25.80/mgmt/tm/net/tunnels/vxlan/vxlan-mp
      {
          "kind": "tm:net:tunnels:vxlan:vxlanstate",
          "name": "vxlan-mp",
          "fullPath": "vxlan-mp",
          "generation": 480034,
          "selfLink": "https://localhost/mgmt/tm/net/tunnels/vxlan/vxlan-mp?ver=12.1.0",
          "defaultsFrom": "/Common/vxlan",
          "defaultsFromReference": {
              "link": "https://localhost/mgmt/tm/net/tunnels/vxlan/~Common~vxlan?ver=12.1.0"
          },
          "encapsulationType": "vxlan",
          "floodingType": "multipoint",
          "port": 4789
      }

#. Create a BIG-IP VXLAN using the new ``vxlan-mp`` profile.

   .. code-block:: bash

      admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$ create net \\
      tunnels tunnel openshift_vxlan key 0 profile vxlan-mp local-address 172.16.1.28

   - The ``hostIP`` address defined in the OpenShift HostSubnet is the ``local-address`` (the VTEP).
   - The ``key`` must be ``0`` if you want to give the BIG-IP access to all OpenShift subnets.

#. Verify creation of the VXLAN tunnel.

   .. code-block:: bash
      :emphasize-lines: 1, 13, 14

      curl -u USER:PASSWORD -X GET https://10.190.25.80/mgmt/tm/net/tunnels/tunnel/
      { ...
        {
          "kind": "tm:net:tunnels:tunnel:tunnelstate",
          "name": "openshift_vxlan",
          "partition": "Common",
          "fullPath": "/Common/openshift_vxlan",
          "generation": 480042,
          "selfLink": "https://localhost/mgmt/tm/net/tunnels/tunnel/~Common~openshift_vxlan?ver=12.1.0",
          "autoLasthop": "default",
          "idleTimeout": 300,
          "ifIndex": 160,
          "key": 0,
          "localAddress": "172.16.1.28",
          "mode": "bidirectional",
          "mtu": 0,
          "profile": "/Common/vxlan-mp",
          "profileReference": {
              "link": "https://localhost/mgmt/tm/net/tunnels/vxlan/~Common~vxlan-mp?ver=12.1.0"
        }
       ...
      }

.. _k8s-openshift-assign-ip:

Assign an OpenShift overlay address to the BIG-IP device
--------------------------------------------------------

#. Create a `Self IP address`_ on the BIG-IP device.
   Use an address in the range you defined in the :ref:`HostSubnet <k8s-openshift-hostsubnet>` ``subnet`` field.

   .. code-block:: bash

      admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$ create net self \\
      10.131.0.10/14 allow-service all vlan vxlan5000

#. Verify creation of the Self IP.

   .. code-block:: bash

      curl -u admin:admin -k -X GET https://10.190.25.80/mgmt/tm/net/self
      { ...
        {
          "kind": "tm:net:self:selfstate",
          "name": "10.131.0.10/14",
          "partition": "Common",
          "fullPath": "/Common/10.131.0.10/14",
          "generation": 480055,
          "selfLink": "https://localhost/mgmt/tm/net/self/~Common~10.131.0.10~16?ver=12.1.0",
          "address": "10.131.0.10/14",
          "addressSource": "from-user",
          "floating": "disabled",
          "inheritedTrafficGroup": "false",
          "trafficGroup": "/Common/traffic-group-local-only",
          "trafficGroupReference": {
              "link": "https://localhost/mgmt/tm/cm/traffic-group/~Common~traffic-group-local-only?ver=12.1.0"
        },
      ...
      }

   .. note::

      If you don't specify a traffic group when creating the selfIP, it will use the default traffic group.

.. [#ossdn] https://docs.openshift.org/latest/architecture/additional_concepts/sdn.html#sdn-design-on-masters


Next Steps
----------

- :ref:`Install the F5 Kubernetes BIG-IP Controller <install-kctlr>`
- :ref:`Configure the F5 Kubernetes BIG-IP Controller for OpenShift <kctlr-configure-openshift>`

.. _OpenShift: https://www.openshift.org/
.. _Create an OpenShift user account: https://docs.openshift.org/1.2/admin_guide/manage_users.html
.. _VXLAN profile:
.. _Self IP address: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/tmos-routing-administration-12-1-1/5.html
