#. If you want to use BIG-IP High Availability (HA), `set up two or more F5 BIG-IPs in a Device Service Cluster (DSC)`_.
#. `Create a new partition`_ on your BIG-IP system.

   .. note::
   
      - The |kctlr| can not manage objects in the ``/Common`` partition.
      - **[Optional]** The Controller can decorate the IP addresses it configures on the BIG-IP with a `Route Domain`_ identifier.
        You may want to use route domains if you have many applications using the same IP address space that need isolation from one another.
        After you create the partition on your BIG-IP system, you can 1) create a route domain and 2) assign the route domain as the partition's default. See `create and set a non-zero default Route Domain for a partition`_ for setup instructions.
      - **[Optional]** If you're using a BIG-IP HA pair or cluster, sync your changes across the group.

#. :ref:`Store your BIG-IP login credentials in a Secret <secret-bigip-login>`.
#. If you need to pull the ``k8s-bigip-ctlr`` image from a private Docker registry, `store your Docker login credentials as a Secret`_.

