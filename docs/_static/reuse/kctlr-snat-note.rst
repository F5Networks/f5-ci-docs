.. note::

   By default, the |kctlr| uses `BIG-IP SNAT`_ automap for all virtual servers it creates.
   You can override this setting in your :ref:`Route <create os route>` or :ref:`F5 Resource ConfigMap <kctlr-create-vs>` definitions (requires :code:`k8s-bigip-ctlr` v1.5.0 or later and f5-schema v0.1.8 or later).

   When you use SNAT automap, the self IP address that serves as the VTEP on the BIG-IP also functions as a SNAT pool. The subnet mask you provide when creating the self IP defines the addresses available in the SNAT pool.
