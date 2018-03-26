:product: BIG-IP Controller for Kubernetes
:type: task

.. _kctlr-per-svc-vs:

Attach Virtual Servers to Services
==================================

.. tip:: You can use F5 resources to attach custom BIG-IP virtual servers to Services in both Kubernetes and OpenShift.

Overview
--------

An :ref:`F5 Resource <k8s-f5-resources>` ConfigMap lets you expose an individual Service to external traffic.
Use an F5 resource if you need:

- a greater degree of flexibility and customization than that provided for :ref:`Ingresses <kctlr-ingress-config>`  and :ref:`Routes <kctlr-openshift-routes>`;
- to :ref:`deploy iApps <kctlr-deploy-iapps>`;
- L4 ingress (TCP or UDP);
- L7 ingress on non-standard ports (for example, 8080, 8443).

.. table:: Task summary

   =======  ===================================================================
   Step     Task
   =======  ===================================================================
   1.       :ref:`kctlr-create-vs`

   2.       :ref:`upload vs ConfigMap`

   3.       :ref:`verify bigip service objects created`
   =======  ===================================================================

.. _kctlr-create-vs:

Define a virtual server for a Service
-------------------------------------

#. Define the virtual server you want to create in an :ref:`F5 resource JSON blob <f5-resource-blob>`.
#. Include the JSON blob in the :code:`data` section of a Kubernetes `ConfigMap`_ resource.

.. _kctlr configmap example:

HTTP example
````````````

For example, if your Service looks like this:

.. code-block:: yaml

   apiVersion: v1
   kind: Service
   metadata:
     name: myService
     labels:
       app: myApp
   spec:
     ports:
     - protocol: TCP
       port: 80
       targetPort: 9376
     type: clusterIP

Your F5 resource ConfigMap might look like this:

.. literalinclude:: /kubernetes/config_examples/f5-resource-vs-example.configmap.yaml
   :lines: 1-7,9-15,23-34

:fonticon:`fa fa-download` :download:`f5-resource-vs-example.configmap.yaml </kubernetes/config_examples/f5-resource-vs-example.configmap.yaml>`

.. seealso::
   :class: sidebar

   See :ref:`kctlr-manage-bigip-objects` for information about :ref:`adding health monitors <k8s-service healthmonitor>`, :ref:`using IPAM to assign virtual server IP addresses <kctlr-ipam>`, and more.

- The :code:`backend.servicePort` property in the F5 resource matches the :code:`ports.port` property in the Service definition. The |kctlr| uses this to relate the Pod Node Ports and Endpoints to the BIG-IP virtual server.

- The :code:`ports.targetPort` setting is the Pod/Container port to which you want to send traffic.

- You can replace :code:`balance: round-robin` with any supported BIG-IP load balancing mode. [#lb]_

HTTPS example
`````````````

For an HTTPS virtual server, your ConfigMap for the same Service might look like this:

.. literalinclude:: /kubernetes/config_examples/f5-resource-configmap-https.yaml
   :lines: 1-14,22-36

:fonticon:`fa fa-download` :download:`f5-resource-configmap-https.yaml </kubernetes/config_examples/f5-resource-configmap-https.yaml>`

- You can define :code:`sslProfile.f5ProfileName` using any existing BIG-IP client SSL profile.

- To provide a list of SSL profiles, use :code:`sslProfile.f5ProfileNames`.

.. _upload vs ConfigMap:

Upload the ConfigMap to the API Server
--------------------------------------

.. tip::

   If you want to create both HTTP and HTTPS virtual servers (in other words, expose multiple ports) for the same Service, create an F5 resource ConfigMap for each port.
   You can pass the names of both YAML files in your :code:`apply` command or include both resources in a single manifest file.


Kubernetes
``````````

.. include:: /_static/reuse/kubectl-apply.rst

OpenShift
`````````

.. include:: /_static/reuse/oc-apply.rst

.. _verify bigip service objects created:

Verify changes on the BIG-IP system
-----------------------------------

.. include:: /_static/reuse/verify-bigip-objects.rst


.. _kctlr-downed-services:

Removing or replacing Services
------------------------------

If you remove the Service associated with an F5 resource ConfigMap from the API server, the |kctlr| will remove all BIG-IP objects associated with that Service.

If you remove a Service, you should also :ref:`delete the F5 Resource ConfigMap <kctlr-delete-objects>` associated with it.

When replacing a Service, you should create a new F5 resource ConfigMap that meets the new Service's needs.

.. rubric:: **Footnotes**
.. [#lb] The |kctlr| supports BIG-IP load balancing algorithms that do not require additional configuration parameters. You can view the full list of supported algorithms in the `f5-cccl schema <https://github.com/f5devcentral/f5-cccl/blob/03e22c4779ceb88f529337ade3ca31ddcd57e4c8/f5_cccl/schemas/cccl-ltm-api-schema.yml#L515>`_. See the `BIG-IP Local Traffic Management Basics user guide <https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/ltm-basics-13-0-0/4.html>`_ for information about each load balancing mode.
