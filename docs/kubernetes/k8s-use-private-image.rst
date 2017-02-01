.. _k8s-use-private-image:

Use an image from a private repository
--------------------------------------

Add a Kubernetes Image Secret
`````````````````````````````

#. Create a `Kubernetes Secret`_ to the cluster. The secret provides the  credentials the `Docker`_ daemon needs to be able to download the required images. Be sure to create the secret in the appropriate `namespace <https://kubernetes.io/docs/user-guide/namespaces/>`_ (for example, ``kube-system``.

    .. literalinclude:: /_static/config_examples/f5-k8s-image-secret.yaml
        :linenos:


    :download:`f5-k8s-image-secret.yaml </_static/config_examples/f5-k8s-image-secret.yaml>`

#. Upload the secret to the Kubernetes API server.

    .. code-block:: bash

        $ kubectl create -f f5-k8s-image-secret.yaml

#. Call the secret in the service definition.

    .. literalinclude:: /_static/config_examples/f5-k8s-controller-image-secret.yaml
        :linenos:



