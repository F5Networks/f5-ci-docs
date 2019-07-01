:product: Container Ingress Services
:type: concept

.. _kctlr-as3-delete-configmap:

Deleting Container Ingress Service (CIS) AS3 configmaps
=======================================================

You can use this procedure to delete CIS AS3 configmaps, and also remove the associated configuration objects from your BIG-IP system. 

.. important::

   This procedure requires you to restart the :code:`k8s-bigip-ctlr`, and may briefly impact traffic processing.

.. note::

   Modify the bold lines in the examples below based on your ConfigMap. 

#. Log in to the command line of Kubernetes Master Node.

#. To remove the associated configuration objects from the BIG-IP system, create a blank ConfigMap.

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

      kubectl apply -f **f5-as3-declaration-blank.yaml** -n **k8s**
   
#. Delete the configmap from your Kubernetes configuration.

   .. parsed-literal::

      kubectl delete configmap **f5-as3-declaration.yaml** -n **k8s**
     
#. Stop the :code:`k8s-bigip-ctlr`.

   .. parsed-literal::

      kubectl delete deployment **f5-k8s-bigip-ctlr-deployment** -n **k8s**

#. Start the :code:`k8s-bigip-ctlr`.

   .. parsed-literal::

      kubectl apply -f **f5-k8s-bigip-controller.yaml**  -n **k8s**

Example deployment and blank configmap
``````````````````````````````````````
- :fonticon:`fa fa-download` :download:`f5-as3-deployment-example.yaml </kubernetes/config_examples/f5-as3-deployment-example.yaml>`
- :fonticon:`fa fa-download` :download:`f5-as3-blank-example.yaml </kubernetes/config_examples/f5-as3-blank-example.yaml>`
