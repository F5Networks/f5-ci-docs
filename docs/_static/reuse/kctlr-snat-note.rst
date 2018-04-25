.. note::

   By default, the |kctlr| uses `BIG-IP Automap SNAT`_ for all of the virtual servers it creates.
   From :code:`k8s-bigip-ctlr` v1.5.0 forward, you can designate a specific SNAT pool in the Controller Deployment instead of using SNAT automap.

   In environments where the BIG-IP connects to the Cluster network, the self IP used as the BIG-IP VTEP serves as the SNAT pool for all origin addresses within the Cluster.
   The subnet mask you provide when you create the self IP defines the addresses available to the SNAT pool.
