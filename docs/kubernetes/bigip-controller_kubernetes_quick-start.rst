.. _k8s-controller-quickstart:

Deploy the |csi_k|
==================

.. toctree::
     :caption: Contents
     :maxdepth: 4

Objectives
----------

The purpose of this tutorial is to walk through the tasks necessary to deploy the |csi_k|.

- Create a `Kubernetes Deployment`_ for the |csi|.
- Create objects on the BIG-IP.
- Delete objects from the BIG-IP.
- Delete the |csi| Deployment.

Requirements
------------

- `BIG-IP`_ (hardware or VE) 12.1+
- `Kubernetes`_ 1.3.7+

Before you begin
----------------

To complete this tutorial, you need:

- a licensed BIG-IP;
- admin access to the BIG-IP --OR-- a user account with permission to configure objects in a specific :term:`partition` on the BIG-IP;
- a running Kubernetes Cluster;
- `kubectl <https://kubernetes.io/docs/user-guide/kubectl-overview/>`_ (the Kubernetes CLI) configured to communicate with your cluster.

.. important::

    If you do not already have a BIG-IP :term:`partition` dedicated for use by the |csi_k|, `create one now <https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/tmos-implementations-12-1-0/29.html>`_.


Create a |csi_k| Deployment
---------------------------

#. Store your BIG-IP credentials in a `Kubernetes Secret`_.

    .. code-block:: bash

        $ kubectl create secret generic bigip-credentials --from-literal=username=<yourusername> --from-literal=password=<yourpassword>

#. Verify the secret was created correctly.

        .. note:: The values are base64 encoded and will differ from the example shown here.

        .. code-block:: bash

          $ kubectl get secret bigip-credentials -o yaml

#. Define the Deployment in a new YAML file.

    .. literalinclude:: /_static/config_examples/f5-k8s-controller-quickstart.yaml
        :linenos:
        :emphasize-lines: 14-34

    .. tip::

        Customize your Deployment by adding any of the :ref:`configuration parameters <tbd>` to the ``args`` section.

#. Upload the Deployment to Kubernetes with ``kubectl``.

    .. code-block:: bash

        $ kubectl create -f f5-k8s-controller-quickstart.yaml
        deployment "f5-k8s-controller" created

#. Verify the Deployment launched the |csi_k| as a `Pod`_.

    .. code-block:: bash

        $ kubectl get pods -l app=f5-k8s-controller --namespace kube-system
        NAME                                   READY     STATUS         RESTARTS   AGE
        f5-k8s-controller-3184671219-s1ldo     0/1       Running        0          34s


.. _k8s-create-bigip-objects:

Create Objects on the BIG-IP
----------------------------

#. Create a ``virtualServer`` :ref:`F5 resource <tbd>`.

    - Define the :ref:`front-end <tbd>` and :ref:`back-end <tbd>` :ref:`properties <tbd>` for the virtual server as a JSON blob.

        .. literalinclude:: /_static/config_examples/f5-resource-vs-example.json
            :linenos:

    - Create a Kubernetes ConfigMap.

        This identifies the resource to Kubernetes, encodes the data so it is readable by BIG-IP, and defines the virtual server object using the JSON blob.

        .. literalinclude:: /_static/config_examples/f5-resource-vs-example.configmap.yaml
            :linenos:
            :emphasize-lines: 7, 9, 10

#. Upload the ConfigMap to Kubernetes using ``kubectl``.

    .. code-block:: bash

        $ kubectl create -f f5-resource-vs-example.configmap.yaml


#. Verify creation of the virtual server object in your partition on the BIG-IP.

    .. code-block:: bash

        $ tmsh list /ltm virtual /my-bigip-partition/*


Delete objects from the BIG-IP
------------------------------

#. Remove the ConfigMap from the Kubernetes API server.

    .. code-block:: bash

        $ kubectl delete configmap example-vs-resource

#. Verify the virtual server object is no longer in your partition on the BIG-IP.

    .. code-block:: bash

        $ tmsh list /ltm virtual /my-bigip-partition/*

Delete the |csi_k| Deployment
-----------------------------

#. Kill the application and delete the deployment using ``kubectl``.

    .. code-block:: bash

        $ kubectl delete deployment f5-k8s-controller
        deployment "f5-k8s-controller" deleted

#. Verify that the ``f5-k8s-controller`` pod was deleted.

    .. code-block:: bash

        $ kubectl get pods -l app=f5-k8s-controller --namespace kube-system
        NAME                                   READY     STATUS         RESTARTS   AGE


.. _Pod: https://kubernetes.io/docs/user-guide/pods/
