Run |csi| + ASP with Kubernetes Guestbook
=========================================

.. toctree::
     :caption: Contents
     :maxdepth: 4

Objectives
----------

The purpose of this guide is to demonstrate the functionality of the F5 |csi_k| and |asp|, using the `Kubernetes Guestbook`_ example app. The Guestbook is a simple, multi-tier web app; the front-end is built in Go and the backend uses Redis for data storage.

The |csi| provide access to the Go front-end app for clients outside of the `Kubernetes cluster`_. The |asp| directs traffic between the Redis master and slaves on the backend.

- Download and set up the Kubernetes Guestbook app.
- Deploy the Guestbook Datastore.
- ??

Requirements
------------

- `BIG-IP`_ (hardware or VE) 12.1+
- `Kubernetes`_ 1.3.7+

Before you begin
----------------

To complete this demo, you need:

- a Kubernetes cluster running the :ref:`BIG-IP Connector for Kubernetes <k8s-controller-quickstart>` and :ref:`Application Services Proxy <asp-k8s-quickstart>`;
- a licensed BIG-IP with a dedicated :term:`partition` for your `Kubernetes cluster`_;


.. [#gitclient] This is required to clone the Kubernetes repo from GitHub. As an alternative, you can download and unzip the source file archive for your preferred `Kubernetes release <https://github.com/kubernetes/kubernetes/releases>`_.

Download and set up the Kubernetes Guestbook app
------------------------------------------------

#. Download the Kubernetes source archive and ``cd`` to the ``guestbook-go`` example.

    .. code-block:: bash

        $ wget https://github.com/kubernetes/kubernetes/archive/v1.5.2.tar.gz
        $ tar -xvf v1.5.2.tar.gz
        $ cd kubernetes-1.5.2/examples/guestbook

#. Edit the Guestbook Service definition in :file:`guestbook-service.json` to use ``"type": "NodePort"``.

    .. literalinclude:: /_static/config_examples/demo-k8s-guestbook-service.json
        :emphasize-lines: 20

    :download:`demo-k8s-guestbook-service.json </_static/config_examples/demo-k8s-guestbook-service.json>`


Deploy the Guestbook Datastore service with the |asp|
-----------------------------------------------------

#. Deploy the Guestbook application in your Kubernetes cluster.

    .. code-block:: bash

        $ kubectl create -f examples/guestbook-go/
        replicationcontroller "guestbook" created
        service "guestbook" created
        replicationcontroller "redis-master" created
        service "redis-master" created
        replicationcontroller "redis-slave" created
        service "redis-slave" created


#. Annotate the Redis slave service with the |asp| configurations.

    .. note:: Be sure to set the ``ip-protocol`` to ``tcp``.

    .. code-block:: bash

        $ kubectl annotate service redis-slave lwp.f5.com/config='{"ip-protocol":"tcp","load-balancing-mode":"round-robin"}'
        service "redis-slave" annotated


Deploy the Guestbook front-end with the |csi_k|
-----------------------------------------------

#. :ref:`Create a virtual server <k8s-create-bigip-objects>` on your BIG-IP for the Guestbook.

    .. important::

        The highlighted lines in the example below must be a valid IP address and port that are available on your BIG-IP.

    .. literalinclude:: /_static/config_examples/demo-k8s-guestbook-f5_configmap.yaml
        :emphasize-lines: 22-23

    :download:`demo-k8s-guestbook-f5_configmap.yaml </_static/config_examples/demo-k8s-guestbook-f5_configmap.yaml>`

    .. code-block:: bash

        $ kubectl create -f demo-k8s-guestbook-f5_configmap.yaml

#. Verify that the |csi_k| is running.

    .. code-block:: bash

        $ kubectl get pod -l name f5-k8s-controller --namespace kube-system
        NAME                                   READY     STATUS    RESTARTS   AGE
        f5-k8s-controller-1659257167-ftfx9     1/1       Running   0          1m


#. Verify that the new :ref:`F5 resource <tbd>` was created on the `BIG-IP`_:

    .. code-block:: bash
        :caption: via kubectl logs

        $ kubectl logs f5-k8s-controller-1659257167-ftfx9 --namespace kube-system --tail 10
        2016/11/08 00:30:12 [INFO] [2016-11-08 00:30:12,869 marathon_lb INFO] Generating config for BIG-IP from Kubernetes state
        2016/11/08 00:30:12 [INFO] Wrote 1 Virtual Server configs to file /tmp/f5-k8s-controller.config.1.json

    .. code-block:: bash
        :caption: via tmsh

        $ tmsh list /ltm virtual /<your_partition>/*





.. _Kubernetes Guestbook: https://github.com/kubernetes/kubernetes/tree/master/examples/guestbook-go

