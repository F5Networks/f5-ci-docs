AS3 Override
============

AS3 override functionality allows you to alter the existing Big-IP configuration using AS3 with a user-defined config map without affecting the existing Kubernetes resources. The administrator can modify the existing BIG-IP configuration incrementally without having to overwrite/delete the existing one.

Use AS3 override when you want to manually create a virtual server in a controlled and managed partition and add metadata so that ``f5-cccl`` will not create a new virtual server. In order to do this you will need to add a new argument to the deployment file. Run the following command to enable AS3 override functionality:

``--override-as3-declaration=<namespace>/<user_defined_configmap_name>``

For example:

.. image:: /_static/media/as3-override.png
   :scale: 60%

If this argument is not provided the default value for ``--override-as3-declaration`` is null.


Example
```````
This example shows how to change the virtual server address with AS3 override functionality. In the below screenshot, you can see a virtual server ``ingress_172_16_3_23_80`` and the destination IP ``172.16.3.23``

.. image:: /_static/media/as3-override-virtual-server-address.png
   :scale: 60%

   
In order to change the configuration in BIG-IP, you need to create a user-defined config map and provide the altered value. In the metadata section of the user-defined config map you will need to provide the following:

- name: name of the user defined config map
- namespace: namespace of the deployment
- template: This section should be of the same hierarchy as of AS3


.. code-block:: yaml

    kind: ConfigMap
    apiVersion: v1
    metadata:
     name: <configmap_name>
     namespace: <namespace>
    data:
     template: |
        {
            "declaration": {
                "<partition_name>": {
                    "<application_name>": {
                        "<component_name>": {
                            "": [
                                "<altered_value>"
                            ]
                        }
                    }
                }
            }
        }

Below is the user-defined config map to change the virtual server IP address:

.. code-block:: yaml

    kind: ConfigMap
    apiVersion: v1
    metadata:
     name: example-vs
     namespace: default
    data:
     template: |
        {
            "declaration": {
                "test_AS3": {
                    "Shared": {
                        "ingress_172_16_3_23_80": {
                            "virtualAddresses": [
                                "172.16.3.111"
                            ]
                        }
                    }
                }
            }
        }


Create the config map by running the command ``#kubectl create configmap <config_map_name>``.

.. important::

   - CIS will not listen to any events on override config map.
   - When override config map is deployed before CIS, all the resources will get overridden automatically.
   - When override config map is deployed post CIS with existing resources, the resources get overridden when at least one existing resource gets modified or new resource gets added


There are three other ways to create ConfigMaps using the `kubectl create configmap command.

1. Use the contents of an entire directory:

``#kubectl create configmap my-config --from-file=./my/dir/path/``

2. Use the contents of a file or specific set of files:

``#kubectl create configmap my-config --from-file=./my/file_name.json``

3. Use literal key-value pairs defined on the command line:

``#kubectl create configmap my-config --from-literal=key1=value1 --from-literal=key2=value2``

.. note::

   - You can get more information about this command using ``kubectl create configmap --help``
   - You can also create a user defined config map using the specification from a json file.
   - When override config map is deployed post CIS with existing resources, the resources get overridden when at least one existing resource gets modified or new resource gets added


After the config map is applied the changes are reflected in the BIG-IP which can be seen in the screen shot below.


.. image:: /_static/media/as3-override-result.png
   :scale: 60%


