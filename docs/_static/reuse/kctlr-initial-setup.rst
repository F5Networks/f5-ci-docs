.. important::

   You should create all |kctlr| resources in the ``kube-system`` `namespace`_ unless otherwise specified.

#. :ref:`Add your BIG-IP device to the OpenShift Cluster <bigip-openshift-setup>`.

#. `Create a new partition`_ on your BIG-IP system.

   .. note::
   
      - The |kctlr| can not manage objects in the ``/Common`` partition.
      - **[Optional]** The Controller can decorate the IP addresses it configures on the BIG-IP with a `Route Domain`_ identifier.
        You may want to use route domains if you have many applications using the same IP address space that need isolation from one another.
        After you create the partition on your BIG-IP system, you can 1) create a route domain and 2) assign the route domain as the partition's default. See `create and set a non-zero default Route Domain for a partition`_ for setup instructions.

#. :ref:`Store your BIG-IP login credentials in a Secret <secret-bigip-login>`.

#. If you need to pull the ``k8s-bigip-ctlr`` image from a private Docker registry, `store your Docker login credentials as a Secret`_.
