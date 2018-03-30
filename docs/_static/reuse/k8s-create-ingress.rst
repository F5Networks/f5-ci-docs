.. table:: Task Summary
   :align: left

   =======  ===================================================================
   Step     Task
   =======  ===================================================================
   1.       Create a Kubernetes `Ingress resource`_.
   2.       Annotate the Ingress resource with the desired
            `F5 virtual server properties`_.
   3.       `POST the Ingress resource to the Kubernetes API server`_ or

            run :code:`kubectl create -f <filename.yaml>`
   =======  ===================================================================

\

.. _POST the Ingress resource to the Kubernetes API server: https://kubernetes.io/docs/api-reference/v1.6/#create-138
