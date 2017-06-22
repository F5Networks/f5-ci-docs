.. _kctlr-deploy-iapps:

Deploy iApps with |kctlr-long|
==============================

.. sidebar:: Docs test matrix

   We tested this documentation with:

   - ``kubernetes-v1.4.8_coreos.0``
   - |kctlr| ``v1.0.0``

The |kctlr| can deploy any iApp on a BIG-IP device via a set of `iApp configuration parameters </products/connectors/k8s-bigip-ctlr/latest/index.html#iApp>`_. The iApp must exist on your BIG-IP before |kctlr| attempts to deploy it. The steps presented here apply to any built-in or custom iApp.

If you prefer not to use iApps, you can also :ref:`manage BIG-IP objects directly <kctlr-manage-bigip-objects>` with |kctlr|.

Define the F5 Resource
----------------------

.. _f5-resource-iapp-blob:

The example F5 resource JSON blob shown below defines the ``f5.http`` iApp. The ``iappVariables`` configuration parameters correspond to fields in the `iApp template <https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/bigip_iapps_developer_11_0_0/2.html#unique_1762445433>`_ 's presentation section. You can create iApp variables for any built-in or custom iApp.

.. todo:: add link to iApp variable 'How-to'

.. seealso::

   The  `k8s-bigip-ctlr product documentation </products/connectors/k8s-bigip-ctlr/latest/index.html>`_ for detailed information about iApp resources.


.. literalinclude:: /_static/config_examples/f5-resource-vs-iApp-example.json
   :caption: Example F5 iApp Resource definition
   :linenos:
   :emphasize-lines: 8-30


:fonticon:`fa fa-download` :download:`Download f5-resource-vs-iApp-example.json </_static/config_examples/f5-resource-vs-iApp-example.json>`


Deploy the iApp
---------------

#. Create a ConfigMap with the encoded data.

   .. literalinclude:: /_static/config_examples/f5-resource-vs-iApp-example.configmap.yaml
      :caption: Example ConfigMap with F5 virtual server resource
      :linenos:

   :fonticon:`fa fa-download` :download:`f5-resource-vs-iApp-example.configmap.yaml </_static/config_examples/f5-resource-vs-iApp-example.configmap.yaml>`

#. Upload the ConfigMap to Kubernetes.

   .. code-block:: bash

      user@k8s-master:~$ kubectl create -f f5-resource-vs-example.configmap.yaml --namespace=<service-namespace>
      configmap "" created

#. Verify creation of the iApp, and its related objects, on the BIG-IP. This is most easily done via the configuration utility:

   - Log in to the BIG-IP configuration utility.
   - Go to :menuselection:`iApps --> Application Services`.
   - Verify that a new item prefixed with the name of your Kubernetes Service appears in the list, in the correct partition.


Delete iApp objects
-------------------

#. Remove the ConfigMap from the Kubernetes API server to delete the corresponding objects from the BIG-IP.

   .. code-block:: bash

      user@k8s-master:~$ kubectl delete configmap k8s.f5http
      configmap "k8s.f5http" deleted

#. Verify the iApp and its related objects no longer exist on the BIG-IP.

   - Log in to the BIG-IP configuration utility.
   - Go to :menuselection:`iApps --> Application Services`.
   - Verify that the item prefixed with the name of your Kubernetes Service no longer appears in the list for your partition.




