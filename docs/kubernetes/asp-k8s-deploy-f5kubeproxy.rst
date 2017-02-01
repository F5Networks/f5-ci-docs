Deploy the |aspk| App
=====================

.. table:: Docs test matrix

    +-----------------------------------------------------------+
    | kubernetes v1.3.7                                         |
    +-----------------------------------------------------------+
    | coreos-stable-1185.3.0                                    |
    +-----------------------------------------------------------+
    | asp v1.0.0                                                |
    +-----------------------------------------------------------+
    | f5-kube-proxy f5-v1.3.7                                   |
    +-----------------------------------------------------------+


Summary
-------

The |aspk| is a container-based application that runs in a `Pod`_ on each `Node`_ in a Kubernetes `Cluster`_. It takes the place of the standard ``kube-proxy`` component.

.. important::

    Master and Worker nodes have distinct pod manifests. See the CoreOS documentation regarding `setting up kube-proxy on the master <https://coreos.com/kubernetes/docs/latest/deploy-master.html#set-up-the-kube-proxy-pod>`_ and `setting up kube-proxy on the workers <https://coreos.com/kubernetes/docs/latest/deploy-workers.html#set-up-the-kube-proxy-pod>`_ for more information.


.. _k8s-pod-manifest:

Set up |aspk| on each node
--------------------------

.. tip::

    The `kube-proxy`_ manifest lives in the path ``/etc/kubernetes/manifests/kube-proxy.yaml``.

        .. code-block:: bash
            :caption: SSH to a node and edit the kube-proxy manifest

            user@k8s-master:~$ ssh core@172.16.1.21
            Last login: Fri Feb 17 18:33:35 UTC 2017 from 172.16.1.20 on pts/0
            CoreOS alpha (1185.3.0)
            Update Strategy: No Reboots
            core@k8s-worker-0 ~ $ sudo su
            k8s-worker-0 core \# vim /etc/kubernetes/manifests/kube-proxy.yaml


#. Edit the `kube-proxy`_ manifest on each node to match the :ref:`manifest examples <k8s-pod-manifest-example>`.

    The key additions/changes are:

    .. code-block:: bash
        :caption: Change the command to ``/proxy``.

        spec:
          containers:
            command: /proxy

    .. code-block:: bash
        :caption: Replace the image with the ``f5-kube-proxy`` image.

        spec:
          containers:
            image: f5networks/f5-kube-proxy:f5-v1.3.7

    .. code-block:: bash
        :caption: Add a new ``mountPath`` to the ``volumeMounts`` section.

        spec:
          containers:
            volumeMounts:
              ...
              - mountPath: /var/run/kubernetes/proxy-plugin
                name: plugin-config
                readOnly: false

    .. code-block:: bash
        :caption: Add ``plugin-config`` to the ``volumes`` section.

        spec:
          volumes:
            ...
            - name: plugin-config
              hostPath:
                path: /var/run/kubernetes/proxy-plugin



.. _k8s-pod-manifest-example:

Examples
--------

.. literalinclude:: /_static/config_examples/f5-kube-proxy-manifest-master.yaml
    :caption: kube-proxy manifest on MASTER node
    :linenos:
    :emphasize-lines: 10, 21-22, 27-29

:download:`f5-kube-proxy-manifest-master.yaml </_static/config_examples/f5-kube-proxy-manifest-master.yaml>`

.. literalinclude:: /_static/config_examples/f5-kube-proxy-manifest-worker.yaml
    :caption: kube-proxy manifest on WORKER node
    :linenos:
    :emphasize-lines: 10, 28-29, 40-42

:download:`f5-kube-proxy-manifest-worker.yaml </_static/config_examples/f5-kube-proxy-manifest-worker.yaml>`
