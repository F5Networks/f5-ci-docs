.. _k8s-add-secret:

Secure sensitive information with Kubernetes Secrets
====================================================

A Kubernetes `Secret`_ allows you to securely store and consume sensitive data in your Kubernetes cluster.

.. _k8s-tls-cert:

Add a TLS certificate and key
-----------------------------

#. Encode your certificate and key with base64.
#. Add the encoded certificate and key to the Data field of the Secret as "<myCert>.crt" and "<myKey>.key".

   .. code-block:: yaml

      data:
        tls.crt: <base64-encoded_cert>
        tls.key: <base64-encoded_key>

.. seealso::

   See the Kubernetes documentation: `Distribute Credentials Securely Using Secrets <https://kubernetes.io/docs/tasks/inject-data-application/distribute-credentials-secure/>`_.

.. _k8s-secret-docker-config:

Pull an image from a private Docker registry
--------------------------------------------

The Kubernetes documentation covers this topic well:

- `Pull an image from a private registry <https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/>`_
-  `Creating a Secret with a Docker config <https://kubernetes.io/docs/concepts/containers/images/#creating-a-secret-with-a-docker-config>`_

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

