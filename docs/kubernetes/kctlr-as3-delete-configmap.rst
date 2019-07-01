:product: Container Ingress Services
:type: concept

.. _kctlr-as3-delete-configmap:

Deleting Container Ingress Service (CIS) AS3 configmaps
=======================================================

You can use this procedure to delete CIS AS3 configmaps, and also remove the associated configuration objects from your BIG-IP system.

.. important::

   This procedure requires you to restart the :code:`k8s-bigip-ctlr`, and may briefly impact traffic processing.

.. note::

   The bold lines in the examples below should be modified based on your currently deployed ConfigMap. To help you understand how to modify the lines, view the example deployment at the bottom of the page.

#. Log in to the command line of Kubernetes Master Node.

#. To remove the associated configuration objects from the BIG-IP system, create a blank ConfigMap.

   .. note::

      To help you understand how to create a blank ConfigMap based on a deployment, review the examples at the bottom of the page.

   For example:

   .. parsed-literal::

      kind: ConfigMap
      apiVersion: v1
      metadata:
        **name: f5-as3-declaration**
        **namespace: k8s**
        labels:
          f5type: virtual-server
          as3: "true"
      data:
        template: |
          {
              "class": "AS3",
              "declaration": {
              "class": "ADC",
              "schemaVersion": "3.10.0",
              **"id":"1847a369-5a25-4d1b-8cad-5740988d4423",**
              **"label":"Sample AS3 Template",**
              "remark": "Remove AS3 declaration",
              **"stark": {**
                "class": "Tenant"
              }
            }
          }

#. Deploy the blank ConfigMap.

   .. parsed-literal::

      kubectl apply -f **f5-as3-declaration-blank.yaml** 
   
#. Delete the configmap from your Kubernetes configuration.

   .. parsed-literal::

      kubectl delete configmap **f5-as3-declaration.yaml**
     
#. Stop the :code:`k8s-bigip-ctlr`.

   .. parsed-literal::

      kubectl delete deployment **f5-k8s-bigip-ctlr-deployment**

#. Start the :code:`k8s-bigip-ctlr`.

   .. parsed-literal::

      kubectl apply -f **f5-k8s-bigip-controller.yaml** 

Example deployment and blank configmap
``````````````````````````````````````
- :fonticon:`fa fa-download` :download:`f5-as3-deployment-example.yaml </kubernetes/config_examples/f5-as3-deployment-example.yaml>`
- :fonticon:`fa fa-download` :download:`f5-as3-blank-example.yaml </kubernetes/config_examples/f5-as3-blank-example.yaml>`
