.. _kctlr-configuration:

Configure the |kctlr-long|
==========================

When you launch the |kctlr-long|, you must provide the required configuration parameters shown in the table below.
Define these configuration parameters in the ``args`` section of the `Kubernetes Deployment`_.

Required configuration parameters
---------------------------------

=====================   ===================================================
Parameter               Description
=====================   ===================================================
bigip-username          Username for BIG-IP account with permission to
                        manage objects in the specified partition;
                        can be an env variable
                        (e.g., "``$(BIGIP_USERNAME)"``)
---------------------   ---------------------------------------------------
bigip-password          Password for BIG-IP account; can be an env variable
                        (e.g., ``"$(BIGIP_PASSWORD)"``)
---------------------   ---------------------------------------------------
bigip-url               BIG-IP Hostname/IP address
---------------------   ---------------------------------------------------
bigip-partition         The BIG-IP partition |kctlr| manages
---------------------   ---------------------------------------------------
kubeconfig              Path to the `kubeconfig`_ file
---------------------   ---------------------------------------------------
namespace               Kubernetes namespace to watch
=====================   ===================================================


.. literalinclude:: /_static/config_examples/f5-k8s-bigip-ctlr_image-secret.yaml
    :caption: Example Deployment definition
    :emphasize-lines: 29-35


Required configuration parameters for OpenShift clusters
--------------------------------------------------------

In addition to the required parameters noted above, you'll need to define the following parameters when using |kctlr-long| in an OpenShift cluster.

=====================   ===================================================
Parameter               Description
=====================   ===================================================
pool-member-type        Defines the BIG-IP pool member type.
                        This must be ``cluster`` if you're using OpenShift.
---------------------   ---------------------------------------------------
openshift-sdn-name      TMOS path to the BIG-IP VXLAN tunnel providing
                        access to the Openshift SDN and Pod network;
                        include the partition and vxlan name.

                        Example: ``/Common/openshift_vxlan`` [#tunnel]_
=====================   ===================================================


.. [#tunnel] The VXLAN tunnel does not need to reside in the same partition managed by the |kctlr-long|.

.. literalinclude:: /_static/config_examples/f5-k8s-bigip-ctlr_openshift-sdn.yaml
    :caption: Example Deployment definition
    :emphasize-lines: 29-38


Required configuration parameters for F5 resources
--------------------------------------------------

The ``frontend`` section of an F5 resource must contain the parameters listed in the tables below.

virtualServer
`````````````

=====================   ===================================================
Parameter               Description
=====================   ===================================================
partition               The BIG-IP partition in which you want to create
                        a virtualServer
---------------------   ---------------------------------------------------
mode                    Proxy mode (http or tcp)
---------------------   ---------------------------------------------------
balance                 Load balancing mode
---------------------   ---------------------------------------------------
virtualAddress          JSON object; allocates a virtual address for the
                        virtualServer
---------------------   ---------------------------------------------------
- bindAddr              part of the virtualAddress JSON object; defines the
                        virtual IP address to assign to the virtualServer
---------------------   ---------------------------------------------------
- port                  part of the virtualAddress JSON object; defines the
                        port to assign to the virtualServer
=====================   ===================================================

iApps
`````

=====================   ===================================================
Parameter               Description
=====================   ===================================================
partition               The BIG-IP partition in which you want to create
                        a virtualServer
---------------------   ---------------------------------------------------
iapp                    BIG-IP iApp template you want to deploy;
                        *must already exist on the BIG-IP*
---------------------   ---------------------------------------------------
iappPoolMemberTable     Defines the name and layout of the pool-member
                        table in the iApp. [#pmtable]_
---------------------   ---------------------------------------------------
iappOptions             key-value object; used to provide information
                        about the iApp
                        (see :ref:`iApp example <f5-resource-iapp-blob>`)
=====================   ===================================================

.. [#pmtable] See `iApps Pool Member Table </products/connectors/k8s-bigip-ctlr/latest/index.html#iapps-pool-member-table>`_ for more information.

See Also
--------

See the `k8s-bigip-ctlr product documentation </products/connectors/k8s-bigip-ctlr/latest/index.html>`_ for the full list of available configuration parameters.

.. _kubeconfig: https://kubernetes.io/docs/user-guide/kubeconfig-file/
