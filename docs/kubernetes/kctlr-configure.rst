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
                        manage objects in the ``bigip-partition``;
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
namespace               Kubernetes namespace to watch [#fnnamespace]_
=====================   ===================================================

.. [#fnnamespace] As of |kctlr| `v1.1.0 </products/connectors/k8s-bigip-ctlr/v1.1.0>`_ ``namespace`` is not required.

.. todo:: add link to multiple namespaces doc when it's added

.. literalinclude:: /_static/config_examples/f5-k8s-bigip-ctlr_image-secret.yaml
   :caption: Example Deployment definition
   :linenos:
   :emphasize-lines: 32-35, 43


Required configuration parameters for F5 resources
--------------------------------------------------

The ``frontend`` section of an F5 resource should contain the parameters listed in the tables below.

.. tip::

   - You can set the ``virtualAddress.bindAddr`` parameter :ref:`using an IPAM system <kctlr-ipam>`.
   - If you want to :ref:`create pools without virtual servers <kctlr-pool-only>`, you can leave out the ``virtualServer`` section altogether.

virtualServer
`````````````

=====================   ===================================================
Parameter               Description
=====================   ===================================================
partition               The `BIG-IP partition`_ in which you want to create
                        a virtual server
---------------------   ---------------------------------------------------
mode                    Proxy mode (http or tcp)
---------------------   ---------------------------------------------------
balance                 Load balancing mode
---------------------   ---------------------------------------------------
virtualAddress          JSON object; allocates a virtual address for the
                        virtualServer. [#fn1]_

- bindAddr              The IP address you want to assign to the virtual
                        server. [#fn1]_
- port                  The port you want to assign to the virtual server.
                        [#fn2]_
=====================   ===================================================


.. [#fn1] Not required when creating :ref:`unattached pools <kctlr-pool-only>`.
.. [#fn2] Required when the virtualAddress object is present; not required if you're creating :ref:`unattached pools <kctlr-pool-only>` and you omit the virtualAddress object.

iApps
`````

=====================   ===================================================
Parameter               Description
=====================   ===================================================
partition               The `BIG-IP partition`_ in which you want to create
                        a virtual server
---------------------   ---------------------------------------------------
iapp                    The BIG-IP iApp template you want to deploy;
                        *must already exist on the BIG-IP device*
---------------------   ---------------------------------------------------
iappPoolMemberTable     The name and layout of the pool-member
                        table in the iApp. [#pmtable]_
---------------------   ---------------------------------------------------
iappOptions             key-value object that provides information
                        about the iApp
                        (see :ref:`iApp example <f5-resource-iapp-blob>`)
=====================   ===================================================

.. [#pmtable] See `iApps Pool Member Table </products/connectors/k8s-bigip-ctlr/latest/index.html#iapps-pool-member-table>`_ for more information.

See Also
--------

See the `k8s-bigip-ctlr product documentation </products/connectors/k8s-bigip-ctlr/latest/index.html>`_ for the full list of available configuration parameters.

.. _kubeconfig: https://kubernetes.io/docs/user-guide/kubeconfig-file/
