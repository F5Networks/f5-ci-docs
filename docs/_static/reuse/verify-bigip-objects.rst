You can use the BIG-IP configuration utility or a TMOS shell to verify creation/modification/deletion of BIG-IP objects.

.. rubric:: Configuration Utility

- Go to :menuselection:`Local Traffic --> Virtual Servers`.
- Select the correct partition from the :guilabel:`Partition` drop-down menu.

.. rubric:: TMOS Management Console

.. parsed-literal::

   admin@(bigip)(cfg-sync Standalone)(Active)(/Common) cd **my-partition**
   admin@(bigip)(cfg-sync Standalone)(Active)(/my-partition) **tmsh**
   admin@(bigip)(cfg-sync Standalone)(Active)(/my-partition)(tmos)$ **show ltm virtual**
   ------------------------------------------------------------------
   Ltm::Virtual Server: **default_myApp.vs_173.16.2.2_80**
   ------------------------------------------------------------------
   Status
     Availability     : available
     State            : enabled
     Reason           : The virtual server is available
     CMP              : enabled
     CMP Mode         : all-cpus
     Destination      : 173.16.2.2:80
   ...
   Ltm::Virtual Server: **default_myApp.vs_173.16.2.2_443**
   ------------------------------------------------------------------
   Status
     Availability     : available
     State            : enabled
     Reason           : The virtual server is available
     CMP              : enabled
     CMP Mode         : all-cpus
     Destination      : 173.16.2.2:443
   ...
