Are you looking in the correct partition on the BIG-IP system?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you're in the ``Common`` partition, switch to the partition managed by the |kctlr| to find the objects it deployed.

* In the BIG-IP configuration utility (aka, the GUI), check the partition drop-down menu.

  .. image:: /_static/media/bigip-partition_gui.png


* In the BIG-IP Traffic Management shell (TMSH), check the name of the partition shown in the prompt.

  .. image:: /_static/media/bigip-partition_tmsh.png