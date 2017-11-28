.. _k8s-add-secret:

Secure sensitive information with Secrets
=========================================

In Kubernetes and OpenShift, a `Secret`_ allows you to securely store and consume sensitive data in your cluster.

.. tip::

   - Be sure to create your Secret in the same `Namespace`_ as the resource that needs to access it.
   - If using OpenShift, substitute :code:`kubectl` with :code:`oc` when following the examples provided.

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

If you need to pull images from a private Docker registry, follow the instructions provided in the Kubernetes documentation:

- `Pull an image from a private registry <https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/>`_
- `Creating a Secret with a Docker config <https://kubernetes.io/docs/concepts/containers/images/#creating-a-secret-with-a-docker-config>`_

.. _secret-bigip-login:

Secure your BIG-IP credentials
------------------------------

Create a generic Secret containing your BIG-IP login information.

.. code-block:: bash

   kubectl create secret generic bigip-login --namespace kube-system --from-literal=username=admin --from-literal=password=admin
   secret "bigip-login" created

.. _secret verify:

Verify that a Secret exists
---------------------------

If using standard Kubernetes, see the `Kubernetes Secrets documentation <https://kubernetes.io/docs/concepts/configuration/secret/#creating-your-own-secrets>`_.

If using OpenShift, see the `OpenShift Secrets documentation <https://docs.openshift.org/1.4/dev_guide/secrets.html>`_.
