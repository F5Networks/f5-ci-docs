Deploy the F5 |lwp| for Kubernetes
----------------------------------

Deploying the F5® |lwp| (LWP) in Kubernetes replaces `kube-proxy <http://kubernetes.io/docs/admin/kube-proxy/>`_.
This allows a `Kubernetes Service`_ to be annotated to enable its ClusterIP to be implemented by the |lwp|, while other services retain the basic kube-proxy behavior.

The F5 |lwp| in Kubernetes is composed of two (2) parts:

    #. a privileged service that manages the ``iptables`` rules of the host, and
    #. the proxy that processes service traffic.

The |lwp| should be deployed on every node in your Kubernetes cluster.
The LWP on the same node as the client handles requests and load-balances to the backend pod.
|lwp| will create a virtual server for every `Kubernetes Service`_ in the cluster that has the F5 annotation configured (see :ref:`Create a Virtual Server <add-lwp-kubernetes-services>`).

.. _install-lwp-kubernetes:

Install |lwp|
`````````````

Add a |lwp| Instance to Every Node
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Every node in the cluster need to run an instance of LWP.
This example will create a Kubernetes `DaemonSet <http://kubernetes.io/docs/admin/daemons/>`_ to ensure one |lwp| runs per node, and a Kubernetes `ConfigMap`_ to provide the same configuration file to each. 

#. Specify the |lwp| :ref:`global <global-config-parameters>` and :ref:`orchestration <orchestration-config-parameters>` configurations in a `ConfigMap`_.

    .. note::

        The ``orchestration.kubernetes.config-file`` property in the ConfigMap points to a volume mounted by the |lwp| DaemonSet spec you'll set up in the next step.


    .. literalinclude:: /static/f5-lwp/example-lwp-configmap.yaml
       :language: yaml
       :emphasize-lines: 12-15

    :download:`example-lwp-configmap.yaml </static/f5-lwp/example-lwp-configmap.yaml>`


#. Create a Kubernetes `DaemonSet <http://kubernetes.io/docs/admin/daemons/>`_ for the |lwp|.

    .. note::

        * As with all other Kubernetes configurations, this file can be JSON or YAML.
        * In the example DaemonSet shown here, we

            a. use the ConfigMap (set up in the previous step) to configure the |lwp|; AND

            b. mount a volume that provides the :file:`service-ports.json` config file at the path provided in the ConfigMap.


    .. literalinclude:: /static/f5-lwp/example-lwp-daemonset.yaml
       :language: yaml

    :download:`example-lwp-daemonset.yaml </static/f5-lwp/example-lwp-daemonset.yaml>`


Replace kube-proxy with f5-kube-proxy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The kube-proxy on every node in the cluster needs to support handoff to LWP.  

    .. rubric:: Replace ``kube-proxy`` with ``f5-kube-proxy`` in the **container section** of the static pod manifest file, and add the proxy-plugin volume mount.

    .. literalinclude:: /static/f5-lwp/example-kube-proxy-manifest.yaml
       :language: yaml
       :emphasize-lines: 10,27-29,40-42

    :download:`example-kube-proxy-manifest.yaml </static/f5-lwp/example-kube-proxy-manifest.yaml>`



Create a Virtual Server with |lwp|
``````````````````````````````````

.. _add-lwp-kubernetes-services:

Enable the |lwp| for Kubernetes Service(s)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

|lwp| will take over the virtual IP for any `Kubernetes Service`_ that has been enabled with the lwp annotation. A virtual server will be created in each LWP according to the annotation's value.

* The ``lwp.f5.com/config.portname`` annotation enables LWP for port named ``portname`` of the Service
* The ``lwp.f5.com/config`` annotation enables LWP for all ports for the Service, except the ports that also have a matching named port annotation.

The value for these LWP annotations provides the virtual server configuration, similar to the :ref:`Virtual Server section <lwp-configs-virtual-server>` of the LWP config file. Endpoints and destination details should not be included, as they are dynamically assigned by Kubernetes.

.. note
    If the configuration is not correct, LWP will reject traffic. The error message can be seen in the LWP logs

To annotate an existing service:

    .. code-block:: bash

        kubectl annotate service my-service \
          lwp.f5.com/config.http='{"ip-protocol":"http","load-balancing-mode":"round-robin"}'


    .. rubric:: The example below shows the F5 annotation string incorporated into a sample Service definition.

    .. literalinclude:: /static/f5-lwp/example-service-lwp.yaml

    :download:`example-service-lwp.yaml </static/f5-lwp/example-service-lwp.yaml>`


.. toctree::
    :hidden:

    self
