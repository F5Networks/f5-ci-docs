When uploading resources that don't reside in the default namespace, specify the correct namespace using the :code:`--namespace` (or :code:`-n`) flag.

.. code-block:: console

   kubectl apply -f <filename.yaml> [--namespace=<resource-namespace>]
