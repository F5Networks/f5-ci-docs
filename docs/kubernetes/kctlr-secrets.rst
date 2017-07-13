.. _k8s-add-secret:

Secure sensitive information with Kubernetes Secrets
====================================================

A Kubernetes `Secret`_ allows you to securely store and consume sensitive data in your Kubernetes cluster.

.. _secret-bigip-login:

Secure your BIG-IP credentials
------------------------------

#. Create a generic Kubernetes `Secret`_ to secure your BIG-IP login information.

   .. code-block:: bash
      :caption: Create a secret for your BIG-IP login credentials

      user@k8s-master:~$ kubectl create secret generic bigip-login --namespace kube-system --from-literal=username=admin --from-literal=password=admin
      secret "bigip-login" created

#. Verify the Secret exists

   .. code-block:: bash
      :caption: BIG-IP credentials

      user@k8s-master:~$ kubectl get secret bigip-login --namespace kube-system -o yaml
      apiVersion: v1
      data:
        password: YWRtaW4=
        username: YWRtaW4=
      kind: Secret
      metadata:
        creationTimestamp: 2017-02-06T19:18:34Z
        name: bigip-login
        namespace: kube-system
        resourceVersion: "8586"
        selfLink: /api/v1/namespaces/kube-system/secrets/bigip-login
        uid: 0d950bbc-eca1-11e6-92a8-fa163e4f44e9
      type: Opaque

.. _k8s-secret-docker-config:

Pull an image from a private docker registry
--------------------------------------------

1. Create a `docker-registry secret`_ for your :file:`.docker/config.json` file.

   - Use base64 to encode the contents of your /.docker/config.json:

     .. code-block:: bash

         base64 < ~/.docker/config.json

   - Copy the long string of characters ending in "==" into the Secret definition as the ``.dockerconfigjson`` value.

     .. note:: An abridged ``.dockerconfigjson`` value (indicated by ``[...]``) appears in the example below.

     .. literalinclude:: /_static/config_examples/f5-k8s-image-secret.yaml
        :emphasize-lines: 8

2. Verify the Secret exists.

   .. code-block:: bash
      :caption: docker-registry
      :emphasize-lines: 4, 9, 13

      user@k8s-master:~$ kubectl get secret f5-docker-images --namespace=kube-system -o yaml
      apiVersion: v1
      data:
        .dockerconfigjson: ewoJImF1dG[...]NqcGpPVVJVUzNSQlZuUXlaSGM9IgoJCX0KCX0KfQ==
      kind: Secret
      metadata:
        creationTimestamp: 2017-02-08T17:43:17Z
        name: f5-docker-images
        namespace: kube-system
        resourceVersion: "316698"
        selfLink: /api/v1/namespaces/kube-system/secrets/f5-docker-images
        uid: 12fb584f-ee26-11e6-92a8-fa163e4f44e9
      type: kubernetes.io/dockerconfigjson


#. Add the Secret to the :ref:`Deployment <create-k8s-deployment>` or :ref:`Pod manifest <k8s-pod-manifest>` definition as the ``imagePullSecrets`` value.

   .. rubric:: Example

   .. literalinclude:: /_static/config_examples/f5-k8s-bigip-ctlr_image-secret.yaml
      :caption: ``k8s-bigip-ctlr`` Deployment
      :emphasize-lines: 43-44


.. _docker-registry secret: https://kubernetes.io/docs/concepts/containers/images/#creating-a-secret-with-a-docker-config
