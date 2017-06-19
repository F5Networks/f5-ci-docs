.. table:: Task Summary
   :align: left

   =======  ===================================================================
   Step     Task
   =======  ===================================================================
   1.       Create a Kubernetes `Ingress Resource`_.
   2.       Add the the desired `F5 virtual server annotations`_ to
            the Ingress resource.
   3.       `POST the Ingress Resource to the Kubernetes API server`_ or

            run :code:`kubectl create ingress -f <filename.yaml>`
   =======  ===================================================================

\

.. _POST the Ingress Resource to the Kubernetes API server: https://kubernetes.io/docs/api-reference/v1.6/#create-138
