.. important::

   You should create all |kctlr| resources in the ``kube-system`` `namespace`_ unless otherwise specified.

#. :ref:`Add your BIG-IP device to the OpenShift Cluster <bigip-openshift-setup>`.

#. `Create a new partition`_ on your BIG-IP system.

   .. important:: The |kctlr| can not manage objects in the ``/Common`` partition.

#. :ref:`Store your BIG-IP login credentials in a Secret <secret-bigip-login>`.

#. If you need to pull the k8s-bigip-ctlr image from a private Docker registry, `store your Docker login credentials as a Secret`_.