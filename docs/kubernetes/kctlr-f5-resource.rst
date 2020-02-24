:product: BIG-IP Controller for Kubernetes
:type: concept

.. _k8s-f5-resources:

F5 Resources Explained
======================

An F5 Resource is a specially-formatted JSON blob that defines a set of BIG-IP objects. In Kubernetes and OpenShift, you can include the F5 Resource in a `ConfigMap`_ to :ref:`kctlr-per-svc-vs`.

Creating a virtual server with an F5 Resource gives you the greatest degree of control over the objects that the |kctlr| ultimately creates on the BIG-IP system. If you only need to define a few basic settings, consider using an :ref:`Ingress resource <kctlr-ingress-config>` in Kubernetes or a :ref:`Route resource <kctlr-openshift-routes>` in OpenShift.

You can use an F5 Resource ConfigMap to create custom virtual servers for your Applications. For example:

- HTTP virtual servers that use non-standard ports;
- HTTP virtual servers that needs customization beyond the |kctlr| `Ingress annotations`_ ;
- virtual servers for TCP or UDP applications that require non-HTTP ingress.


.. _f5 resource properties:

F5 Resource properties
----------------------

The F5 resource is a JSON blob consisting of the properties shown in the table below.


.. table:: F5 Resource properties

   ======================= ======================================================== ===========
   Property                Description                                              Required
   ======================= ======================================================== ===========
   data                    A JSON object                                            Required
   ----------------------- -------------------------------------------------------- -----------
   - frontend              Defines BIG-IP objects.
   ----------------------- -------------------------------------------------------- -----------
   - backend               Identifies the Service you want to proxy.

                           Defines a BIG-IP health monitor(s) for the Service.
   ----------------------- -------------------------------------------------------- -----------
   f5type                  A :code:`label` property watched by the |kctlr|.         Required
   ----------------------- -------------------------------------------------------- -----------
   schema                  Tells the |kctlr| how to interpret the encoded data.     Required
   ======================= ======================================================== ===========

.. _f5 resource frontend:

Data.Frontend
`````````````

The :code:`data.frontend` property defines the objects you want to create on the BIG-IP system for a specific Service.
In this section, you can :ref:`define a custom virtual server <kctlr-per-svc-vs>` using the :code:`virtualServer` properties.

- `k8s-bigip-ctlr virtual server configuration parameters`_


.. _f5 resource backend:

Data.Backend
````````````

Use the :code:`data.backend` property to identify the `Kubernetes Service`_ that makes up the back end server pool.

.. tip:: You can also define BIG-IP health monitors in this section.


F5 type
```````

The :code:`f5type` is a Kubernetes Resource metadata label. Its usage differs depending on whether you're working in Kubernetes or OpenShift.

In Kubernetes, when used in an F5 Resource ConfigMap, the :code:`f5type` **value must be** :code:`virtual-server`.
This tells the |kctlr| that you want to create a virtual server on the BIG-IP device.

In OpenShift, when used in a Route Resource, you can use the :code:`f5type` label to identify which Routes you want the |kctlr| to watch.
When you deploy the Controller with the :code:`--route-label` setting, the |kctlr| watches the OpenShift API for Routes that contain the specified label. See :ref:`kctlr-openshift-routes` for more information.

.. _f5-schema:

F5 schema
`````````

The `F5 schema`_ defines the structure and formatting for the data defined in the F5 resource. The |kctlr| uses the schema version provided to validate the other inputs.

While all |kctlr| versions are backwards-compatible, using an older schema may limit Controller functionality.
Be sure to use the most recent schema version that corresponds with your Controller version to ensure access to the full feature set.

.. seealso:: See the :ref:`F5 schema compatibility table <schema-table>` for Controller-schema compatibility.

Example F5 Resources
--------------------

F5 Virtual Server ConfigMap
```````````````````````````

The example below creates an HTTP virtual server with a pool, pool member, and health monitor for the Service named "myService".
The |kctlr| will create the virtual server in the :code:`k8s` partition, which already exists on the BIG-IP system.

.. _f5-resource-blob:

.. literalinclude:: /kubernetes/config_examples/f5-resource-vs-example.configmap.yaml



