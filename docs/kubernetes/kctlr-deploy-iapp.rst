:product: BIG-IP Controller for Kubernetes
:type: task

.. _kctlr-deploy-iapps:

Deploy iApps with the BIG-IP Controller
=======================================

The |kctlr| can deploy any iApp on a BIG-IP device using the `k8s-bigip-ctlr iApp configuration parameters`_. The iApp must exist on your BIG-IP before |kctlr| attempts to deploy it. The steps presented here apply to any built-in or custom iApp.

.. note::

   You can use the |kctlr| to deploy iApps in standard Kubernetes and OpenShift environments.

   If using the OpenShift CLI, substitute :command:`oc` for :command:`kubectl` in the examples provided.

If you prefer not to use iApps, you can also :ref:`manage BIG-IP objects directly <kctlr-manage-bigip-objects>` with |kctlr|.

Define the F5 Resource
----------------------

.. _f5-resource-iapp-blob:

The example F5 resource JSON blob shown below defines the ``f5.http`` iApp. The ``iappVariables`` configuration parameters correspond to fields in the `iApp template <https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/bigip-iapps-developer-11-4-0/2.html>`_ 's presentation section. You can create iApp variables for any built-in or custom iApp.

.. literalinclude:: /kubernetes/config_examples/f5-resource-vs-iApp-example.json
   :caption: Example F5 iApp Resource definition
   :linenos:
   :emphasize-lines: 9-29

:fonticon:`fa fa-download` :download:`Download f5-resource-vs-iApp-example.json </kubernetes/config_examples/f5-resource-vs-iApp-example.json>`

.. todo:: add link to iApp variable 'How-to'

.. seealso::

   See the `k8s-bigip-ctlr reference documentation`_ for detailed information about iApp resources.


Deploy the iApp
---------------

#. Create a ConfigMap with the encoded data.

   .. literalinclude:: /kubernetes/config_examples/f5-resource-vs-iApp-example.configmap.yaml
      :caption: Example ConfigMap with F5 virtual server resource
      :linenos:

   :fonticon:`fa fa-download` :download:`f5-resource-vs-iApp-example.configmap.yaml </kubernetes/config_examples/f5-resource-vs-iApp-example.configmap.yaml>`

#. Upload the ConfigMap to the Kubernetes/OpenShift API server.

   .. code-block:: console
      :caption: kubectl

      kubectl create -f f5-resource-vs-iApp-example.configmap.yaml [--namespace=<service-namespace>]
      configmap "k8s.http" created

   .. code-block:: console
      :caption: openshift cli

      oc create -f f5-resource-vs-iApp-example.configmap.yaml [--namespace=<service-project>]
      configmap "k8s.http" created

#. Verify creation of the iApp and its related objects on the BIG-IP system.
   This is most easily done via the configuration utility:

   - Log in to the BIG-IP configuration utility.
   - Go to :menuselection:`iApps --> Application Services`.
   - Verify that a new item prefixed with the name of the Service appears in the list, in the correct partition.

.. important::

   If you see a :code:`traffic group configuration error`, please see :ref:`iapp traffic group` in the Troubleshooting documentation.

Delete iApp objects
-------------------

#. Remove the ConfigMap from the Kubernetes/OpenShift API server to delete the corresponding objects from the BIG-IP.

   .. code-block:: console
      :caption: kubectl

      kubectl delete configmap k8s.f5http
      configmap "k8s.f5http" deleted

   .. code-block:: console
      :caption: openshift cli

      oc delete configmap k8s.f5http
      configmap "k8s.f5http" deleted


#. Verify the iApp and its related objects no longer exist on the BIG-IP.

   - Log in to the BIG-IP configuration utility.
   - Go to :menuselection:`iApps --> Application Services`.
   - Verify that the item prefixed with the name of your Kubernetes Service no longer appears in the list for your partition.




