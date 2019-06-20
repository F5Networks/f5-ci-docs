:product: Container Ingress Services
:type: concept

.. _kctlr-as3-delete-configmap:

Deleting Container Ingress Service (CIS) AS3 configmaps
=======================================================

You can use this procedure to delete CIS AS3 configmaps, and also remove the associated configuration objects from your BIG-IP system.

.. important::

   This procedure requires you to restart the :code:`k8s-bigip-ctlr`, and may briefly impact traffic processing.

#. Log in to the command line of your container orchestration environment (COE).

#. To remove the associated configuration objects from the BIG-IP system, you must first create a blank configmap.

   .. note::

      The bold lines should be modified based on your currently deployed configmap. To help you understand how to modify the lines, view the example deployment at the bottom of the page.

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

#. Deploy the blank configmap.

   .. parsed-literal::

      kubectl apply -f <config map> -n <name space>

   For example:

   .. parsed-literal::

      kubectl apply -f as3-declaration-1.yaml -n k8s
   
#. Delete the configmap from your Kubernetes configuration.

   .. parsed-literal::

      kubectl delete configmap <configmap name> -n <name space>

   For example:

   .. parsed-literal::

      kubectl delete configmap as3-declaration-1.yaml -n k8s
     
#. Stop the :code:`k8s-bigip-ctlr`.

   .. parsed-literal::

      kubectl delete deployment <deployement name> -n <name space>

   For example:

   .. parsed-literal::

      kubectl delete deployment k8s-bigip-ctlr-deployment -n k8s

#. Start the :code:`k8s-bigip-ctlr`.

   .. parsed-literal::

      kubectl apply -f <deployment name> -n <name space> 

   For example:

   .. parsed-literal::

      kubectl apply -f k8scontroller.yaml -n <name space> 

Example deployment and blank configmap
``````````````````````````````````````
- :fonticon:`fa fa-download` :download:`f5-as3-deployment-example.yaml </kubernetes/config_examples/f5-as3-deployment-example.yaml>`
- :fonticon:`fa fa-download` :download:`f5-as3-blank-example.yaml </kubernetes/config_examples/f5-as3-blank-example.yaml>`
