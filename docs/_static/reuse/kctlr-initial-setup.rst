.. important::

   You should create all |kctlr| resources in the ``kube-system`` `namespace`_ unless otherwise specified.

#. :ref:`Add your BIG-IP device to the OpenShift Cluster <bigip-openshift-setup>`.

#. `Create a new partition`_ on your BIG-IP system.

   .. note:: 
   
      Optional: The controller can properly decorate an IP address configured on the BIG-IP with a Route Domain identifier. Route domains are BIG-IP configuration objects that isolate network traffic on the network. This is useful if there are multiple applications utilizing the same IP address space, which require isolation from one another. After creating the partition on your BIG-IP system, you can create a route domain and designate that route domain to be the default for the partition. To enable the controller to utilize route domains you can follow the instructions to `create and set non-zero default Route Domain for a partition<https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/tmos-implementations-13-0-0/4.html#guid-e73e1052-8e05-4913-bba3-99f29d26bc56>`. 

   .. important:: The |kctlr| can not manage objects in the ``/Common`` partition.

#. :ref:`Store your BIG-IP login credentials in a Secret <secret-bigip-login>`.

#. If you need to pull the ``k8s-bigip-ctlr`` image from a private Docker registry, `store your Docker login credentials as a Secret`_.
