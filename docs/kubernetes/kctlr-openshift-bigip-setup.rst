Use BIG-IP in an OpenShift Cluster
==================================

.. table:: Docs test matrix

    +-----------------------------------------------------------+
    | BIG-IP v12.1.1                                            |
    +-----------------------------------------------------------+
    | OpenShift Origin v1.3.2                                   |
    +-----------------------------------------------------------+

Summary
-------

Steps required to set up BIG-IP and |kctlr| for use in an `OpenShift`_ cluster:

#. :ref:`Create a host subnet <>` in your OpenShift cluster.
#. :ref:`Create a VXLAN tunnel <>` on the BIG-IP.
#. :ref:`Assign an overlay address <>` from the subnet to a `selfIP address`_ on the BIG-IP.
#. `Create an OpenShift user account`_ for the |kctlr| with permission to manage the following:

    - nodes
    - endpoints
    - services
    - configmaps

.. note::

    We assigned the existing <foo>/<bar> user and group permissions to the |kctlr|.


Create a new OpenShift HostSubnet
----------------------------------

Define a HostSubnet using valid JSON or YAML.

.. important::

    - You must define "subnet" as a range within OpenShift Origin's overlay network. [#ossdn]_
    - You must include the "annotation" section shown in the example below.


.. literalinclude:: /_static/config_examples/f5-kctlr-openshift-hostsubnet.yaml
    :linenos:
    :emphasize-lines: 5-15


Create a VXLAN on the BIG-IP
----------------------------

#. Create a new VXLAN profile on the BIG-IP using multi-point flooding.

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

#. Create a VXLAN using the new ``vxlan-mp`` profile.

    .. code-block:: bash

        admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$ create net \\
        tunnels tunnel vxlan5000 key 0 profile vxlan-mp local-address 172.16.1.28

    - The ``hostIP`` address defined in the OpenShift HostSubnet is the ``local-address`` (the VTEP).
    - The ``key`` must be set to ``0`` to give the BIG-IP access to all OpenShift subnets.

#. Verify creation of the VXLAN tunnel.

    .. code-block:: bash
        :emphasize-lines: 1, 13, 14

        curl -u USER:PASSWORD -X GET https://10.190.25.80/mgmt/tm/net/tunnels/tunnel/
        { ...
          {
            "kind": "tm:net:tunnels:tunnel:tunnelstate",
            "name": "vxlan5000",
            "partition": "Common",
            "fullPath": "/Common/vxlan5000",
            "generation": 480042,
            "selfLink": "https://localhost/mgmt/tm/net/tunnels/tunnel/~Common~vxlan5000?ver=12.1.0",
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


Assign an OpenShift overlay address to the BIG-IP
-------------------------------------------------

#. Create a `selfIP address`_ on the BIG-IP. Use an address in the range you defined in the :ref:`HostSubnet` ``subnet`` field.

    .. code-block:: bash

        admin@BIG-IP(cfg-sync Standalone)(Active)(/Common)(tmos)$ create net self \\
        10.131.0.10/16 allow-service all vlan vxlan5000

#. Verify creation of the selfIP.

    .. code-block:: bash

        curl -u admin:admin -k -X GET https://10.190.25.80/mgmt/tm/net/self
        { ...
          {
            "kind": "tm:net:self:selfstate",
            "name": "10.131.0.10/16",
            "partition": "Common",
            "fullPath": "/Common/10.131.0.10/16",
            "generation": 480055,
            "selfLink": "https://localhost/mgmt/tm/net/self/~Common~10.131.0.10~16?ver=12.1.0",
            "address": "10.131.0.10/16",
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

        The default traffic group is used if you don't specify a traffic group when creating the selfIP.

.. [#ossdn] https://docs.openshift.org/latest/architecture/additional_concepts/sdn.html#sdn-design-on-masters












.. _OpenShift: https://www.openshift.org/
.. _Create an OpenShift user account: https://docs.openshift.org/1.2/admin_guide/manage_users.html
.. _VXLAN profile:
.. _selfIP address: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/tmos-routing-administration-12-1-1/5.html
