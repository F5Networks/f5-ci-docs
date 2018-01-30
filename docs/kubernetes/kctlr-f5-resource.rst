:product: BIG-IP Controller for Kubernetes
:type: concept

.. _k8s-f5-resources:

F5 Resources Explained
======================

An F5 Resource is a specially-formatted JSON blob that defines a set of BIG-IP objects. In Kubernetes and OpenShift, you can include the F5 Resource in a `ConfigMap`_ to :ref:`kctlr-per-svc-vs`.

Creating a virtual server with an F5 Resource gives you the greatest degree of control over the objects that the |kctlr| ultimately creates on the BIG-IP system. If you only need to define a few basic settings, consider using an :ref:`Ingress resource <kctlr-ingress-config>` in Kubernetes or a :ref:`Route resource <kctlr-openshift-routes>` in OpenShift.

You can use an F5 Resource ConfigMap to create custom virtual servers for your Applications. For example:

- HTTP virtual servers that use non-standard ports;
- HTTP virtual servers that needs customization beyond the |kctlr| `Ingress annotations`_ (like iApps);
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
In this section, you can :ref:`define a custom virtual server <kctlr-per-svc-vs>` using the :code:`virtualServer` properties or :ref:`deploy an iApp <kctlr-deploy-iapps>` using the :code:`iApp` properties.

- `k8s-bigip-ctlr virtual server configuration parameters`_
- `k8s-bigip-ctlr iApp configuration parameters`_

The iApp configuration parameters include a set of customizable ``iappVariables`` parameters. These custom user-defined parameters must correspond to fields in the iApp template you want to launch. You can also define the `iApp pool member table`_ that the iApp creates on the BIG-IP system.

.. tip:: With the iApp configuration parameters, you can also deploy objects across BIG-IP modules (for example, ASM and LTM).

.. _f5 resource backend:

Data.Backend
````````````

Use the :code:`data.backend` property to identify the `Kubernetes Service`_ that makes up the back end server pool.

.. tip:: You can also define BIG-IP health monitors in this section.


F5 type
```````

The usage of the :code:`f5type` property differs depending on whether you're using it in Kubernetes or OpenShift.

- In an **F5 resource** ConfigMap, the :code:`f5type` value must be :code:`virtual-server`. This tells the |kctlr| that you want it to create a BIG-IP virtual server.

- In an **OpenShift Route resource**, the :code:`f5type` property functions as a :code:`route-label` filter.
  When you deploy the Controller with :code:`--route-label:true`, the |kctlr| watches the API for OpenShift Routes using the "f5type" label.
  This is useful when you're using multiple Controllers to manage traffic for different Applications and/or Projects within a single BIG-IP partition.

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

.. _f5-resource-iapp:

F5 iApp ConfigMap
`````````````````

The example below uses the |kctlr| to deploy the F5 iApp called :code:`f5.http`, which resides in the :code:`/Common` partition on the BIG-IP device.

.. literalinclude:: /kubernetes/config_examples/f5-resource-vs-iApp-example.configmap.yaml
