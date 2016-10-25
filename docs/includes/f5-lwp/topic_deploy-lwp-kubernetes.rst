Deploy the F5 |lwp| from Kubernetes
-----------------------------------

The F5® |lwp| (LWP) was designed to be an alternative to `kube-proxy <http://kubernetes.io/docs/admin/kube-proxy/>`_. Like ``kube-proxy``, the F5® |lwp| can be deployed in a Kubernetes cluster to handle a `Kubernetes Service`_ within the cluster. The |lwp| can provide enhanced processing capabilities -- Via its :ref:`built-in middleware <built-in-middleware>` and ability to incorporate :ref:`Express or third-party middleware <customize-lwp-express-middleware>` -- or it can handle services in exactly the same way as ``kube-proxy``, depending on your needs.

The F5 |lwp| in Kubernetes is composed of two (2) parts:

    #. a privileged service that manages the ``iptables`` rules of the host, and
    #. the proxy that processes service traffic.

The |lwp| should be deployed on every node in your Kubernetes cluster. The |lwp| on the same node as the client handles requests and load-balances to the backend pod. |lwp| will create a virtual server for every `Kubernetes Service`_ in the cluster that has the F5 annotation (see :ref:`Add the |lwp| to your Service(s) <add-lwp-kubernetes-services>`) configured.

.. _install-lwp-kubernetes:

Install |lwp|
`````````````

Add a |lwp| Instance to Every Node
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First, create a Kubernetes `DaemonSet <http://kubernetes.io/docs/admin/daemons/>`_ for the |lwp|. This adds a |lwp| instance to every node in the cluster.

#. Specify the |lwp| :ref:`global <global-config-parameters>` and :ref:`orchestration <orchestration-config-parameters>` configurations in a `ConfigMap`_.

    .. note::

        The ``orchestration.kubernetes.config-file`` property in the ConfigMap points to a volume mounted by the |lwp| DaemonSet spec you'll set up in the next step.


    .. literalinclude:: /static/f5-lwp/example-flowpoint-configmap.yaml
       :language: yaml
       :emphasize-lines: 12-15

    :download:`example-flowpoint-configmap.yaml </static/f5-lwp/example-flowpoint-configmap.yaml>`


#. Create a Kubernetes `DaemonSet <http://kubernetes.io/docs/admin/daemons/>`_ for the |lwp|.

    .. note::

        * As with all other Kubernetes configurations, this file can be JSON or YAML.
        * In the example DaemonSet shown here, we

            a. use the ConfigMap (set up in the previous step) to configure the |lwp|; AND

            b. mount a volume that provides the :file:`service-ports.json` config file at the path provided in the ConfigMap.


    .. literalinclude:: /static/f5-lwp/example-flowpoint-daemonset.yaml
       :language: yaml

    :download:`example-flowpoint-daemonset.yaml </static/f5-lwp/example-flowpoint-daemonset.yaml>`


Edit the Pod Manifest
~~~~~~~~~~~~~~~~~~~~~

Next, replace the ``kube-proxy`` instance with ``f5-kube-proxy`` on every node in your Kubernetes cluster.

* Replace ``kube-proxy`` with ``f5-kube-proxy`` in the **container section** of the static pod manifest file.

    .. literalinclude:: /static/f5-lwp/example-kube-proxy-manifest.yaml
       :language: yaml
       :emphasize-lines: 10

    :download:`example-kube-proxy-manifest.yaml </static/f5-lwp/example-kube-proxy-manifest.yaml>`



Create a Virtual Server with |lwp|
``````````````````````````````````

.. _add-lwp-kubernetes-services:

Enable the |lwp| for Kubernetes Service(s)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To activate the |lwp| for your `Kubernetes Service`_, thereby creating a virtual server for that service, edit the service's definition file.

.. important:: You'll need to repeat this step for every Service you want to proxy.


* Add the ``lwp.f5.com/config`` ``annotation`` blob to the Service definition file.

    .. note::

        * The ``lwp.f5.com/config`` object uses a set of configuration parameters similar to those used for a :ref:`virtual server <virtualserver-config-parameters>`.
        * If you enable the |lwp| without providing any configuration parameters, the services provided by |lwp| will be identical to the stock services provided by ``kube-proxy``.


    .. code-block:: yaml
        :emphasize-lines: 2-9

        annotations:
          flowpoint.f5.com: |-
            {
              "ip-protocol": "http",
              "load-balancing-mode": "round-robin",
              "flags" : {
                "x-forwarded-for": false,
                "x-served-by": true
              }
            }

    .. rubric:: The example below shows the F5 annotation string incorporated into a sample Service definition.

    .. literalinclude:: /static/f5-lwp/example-service-flowpoint.yaml

    :download:`example-service-flowpoint.yaml </static/f5-lwp/example-service-flowpoint.yaml>`


.. toctree::
    :hidden:

    self
