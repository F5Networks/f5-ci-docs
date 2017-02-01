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
namespace               Kubernetes namespace to watch; defaults to
                        "kube-system"
=====================   ===================================================


.. literalinclude:: /_static/config_examples/f5-k8s-bigip-ctlr_image-secret.yaml
    :caption: Example Deployment definition
    :lines: 1-35
    :emphasize-lines: 29-35


See Also
--------

Additional |kctlr| :ref:`configuration parameters <tbd>` define the BIG-IP objects that |kctlr| manages. See the |kctlr| :ref:`product documentation <tbd>` for more information.

.. _kubeconfig: https://kubernetes.io/docs/user-guide/kubeconfig-file/
