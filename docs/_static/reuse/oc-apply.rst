When uploading resources that don't reside in the default or current Project, specify the correct Project using the :code:`--namespace` (or :code:`-n`) flag.

.. code-block:: console
   :caption: openshift cli

   oc apply -f <filename.yaml> [--namespace=<resource-project>]
