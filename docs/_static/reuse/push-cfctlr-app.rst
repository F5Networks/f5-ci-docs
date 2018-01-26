Deploy the ``cf-bigip-ctlr`` App using the :command:`cf push` command.

Be sure to use the ``-o`` flag to specify the Docker image and version you want to use.

.. code-block:: console

   cf push cf-bigip-ctlr -o f5networks/cf-bigip-ctlr:1.1.0 -f manifest.yaml
