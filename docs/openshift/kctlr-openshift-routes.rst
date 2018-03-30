:product: BIG-IP Controller for Kubernetes
:type: task


.. _kctlr-openshift-routes:

Attach Virtual Servers to OpenShift Routes
==========================================

.. include:: /_static/reuse/k8s-version-added-1_2.rst

Overview
--------

As described in the OpenShift documentation, the IP address assigned to an `OpenShift Pod`_ is only accessible from within the cluster network. You can use the |kctlr| for OpenShift as a router to expose Services to external traffic.

When you use the |kctlr| as a `Router`_, you can

- create BIG-IP `Local Traffic Policies`_ for OpenShift Services;
- :ref:`use BIG-IP SSL profiles to secure Routes <route-TLS>`; and
- :ref:`add BIG-IP health monitors to Route resources <add health monitor to route>`.

.. attention::

   All Route resources share two virtual servers:

   - "ose-vserver" for HTTP traffic, and
   - "https-ose-vserver" for HTTPS traffic.

   The Controller assigns the names shown above by default. To set set custom names, define :code:`route-http-vserver` and :code:`route-https-vserver` in the |kctlr| :ref:`Deployment <openshift-bigip-ctlr-deployment>`.

.. table:: Task Summary

   =======  ===================================================================
   Step     Task
   =======  ===================================================================
   1.       :ref:`set up kctlr routes`

   2.       :ref:`create os route`

   3.       :ref:`route-TLS` (OPTIONAL)

   4.       :ref:`add health monitor to route` (OPTIONAL)

   5.       :ref:`deploy route resource`

   6.       :ref:`verify BIG-IP route objects`
   =======  ===================================================================

.. _set up kctlr routes:

Set up the BIG-IP Controller to manage Routes
---------------------------------------------

If you haven't already done so, add the |kctlr| `Route configuration parameters`_ to the |kctlr| Deployment:

.. literalinclude:: /openshift/config_examples/f5-kctlr-openshift-routes.yaml
   :linenos:
   :emphasize-lines: 47-56

.. _create os route:

Create an OpenShift Route Resource
----------------------------------

To use the BIG-IP device as an OpenShift Router, create a `Route Resource`_.
The |kctlr| supports use of the following Route Resource types:

- :ref:`unsecured`
- :ref:`edge`
- :ref:`passthrough`
- :ref:`reencrypt`

.. _unsecured:

Unsecured
`````````

.. literalinclude:: /openshift/config_examples/f5-openshift-unsecured-route.yaml
   :linenos:

:fonticon:`fa fa-download` :download:`f5-openshift-unsecured-route.yaml </openshift/config_examples/f5-openshift-unsecured-route.yaml>`

.. _edge:

Edge Termination
````````````````

.. literalinclude:: /openshift/config_examples/f5-openshift-edge-route.yaml
   :linenos:

:fonticon:`fa fa-download` :download:`f5-openshift-edge-route.yaml </openshift/config_examples/f5-openshift-edge-route.yaml>`

.. _passthrough:

Passthrough Termination
```````````````````````

.. literalinclude:: /openshift/config_examples/f5-openshift-passthrough-route.yaml
   :linenos:

:fonticon:`fa fa-download` :download:`f5-openshift-passthrough-route.yaml </openshift/config_examples/f5-openshift-passthrough-route.yaml>`

.. _reencrypt:

Re-encryption Termination
`````````````````````````

.. important:: The |kctlr| does not support path-based Routes for TLS re-encryption.

.. literalinclude:: /openshift/config_examples/f5-openshift-reencrypt-route.yaml
   :linenos:

:fonticon:`fa fa-download` :download:`f5-openshift-reencrypt-route.yaml </openshift/config_examples/f5-openshift-reencrypt-route.yaml>`

.. _attach bigip objects routes:

Attach BIG-IP objects to the Route virtual servers
--------------------------------------------------

Use the |kctlr| `Route annotations`_ to attach various types of BIG-IP objects to the virtual servers corresponding to OpenShift Routes.


.. _add health monitor to route:

Health monitors
```````````````

.. include:: /_static/reuse/k8s-version-added-1_3.rst

You can use the :code:`k8s-bigip-ctlr` `Route annotations`_ to update/add health monitors to OpenShift Routes.

#. Define the :code:`virtual-server.f5.com/health` annotation JSON blob.

#. Add the health monitor annotation to the Route Resource.

   .. code-block:: console
      :caption: Annotate an OpenShift Route using the cli

      oc annotate route myRoute virtual-server.f5.com/health='[{"path": "svc1.example.com/app1", "send": "HTTP GET /health/svc1", "interval": 5, "timeout": 10}]'

In the Route resource YAML file, the health monitor should look like this:

.. literalinclude:: /openshift/config_examples/f5-openshift-route-health-monitor.yaml
   :caption: Example Health Monitor in a Route resource
   :linenos:
   :emphasize-lines: 12-20

.. _route-TLS:

SSL Profiles
````````````

.. include:: /_static/reuse/k8s-version-added-1_3.rst

By default, the |kctlr| creates custom BIG-IP SSL Profiles using the certificates and keys defined in the Route resource.
You can also use an existing `BIG-IP SSL profile`_ to secure traffic for a Route.

- For a Client SSL profile, annotate the Route resource as shown below:

  .. code-block:: console

     oc annotate route <route_name> virtual-server.f5.com/clientssl=</BIG-IP-partition/SSL-profile-name>

- For a Server SSL profile, annotate the Route resource as shown below:

  .. code-block:: console

     oc annotate route <route_name> virtual-server.f5.com/serverssl=</BIG-IP-partition/SSL-profile-name>

.. note::

   - Each SSL profile applies to one Route.
   - The |kctlr| creates one client ssl and one server ssl profile for the HTTPS virtual server. These profiles -- "default-client-ssl" and "default-server-ssl" -- are the **default profiles used for SNI.**


.. _deploy route resource:

Upload the Route to the API server
----------------------------------

Use the :command:`oc apply` command to upload your Route resource to the OpenShift API server.

.. include:: /_static/reuse/oc-apply.rst


.. _verify BIG-IP route objects:

Verify creation of BIG-IP objects
---------------------------------

.. include:: /_static/reuse/verify-bigip-objects.rst

.. _delete vs route:

Delete the Route's virtual server
---------------------------------

If you want to remove the virtual server associated with a Route from the BIG-IP system, but **keep the Route**:

#. Remove the |kctlr| Annotations from the Route definition.
#. Update the OpenShift API server.

   .. include:: /_static/reuse/oc-apply.rst

.. seealso:: See :ref:`kctlr-manage-bigip-objects` for more information.

.. _OpenShift Pod: https://docs.openshift.com/enterprise/3.0/architecture/core_concepts/pods_and_services.html#pods
.. _Router: https://docs.openshift.com/enterprise/3.0/architecture/core_concepts/routes.html#routers
.. _OpenShift Service: https://docs.openshift.com/enterprise/3.0/architecture/core_concepts/pods_and_services.html#services
.. _Route Resource: https://docs.openshift.com/enterprise/3.0/architecture/core_concepts/routes.html
.. _TMSH Reference Guide: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/bigip-tmsh-reference-12-0-0.html
.. _BIG-IP Self IP address: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/tmos-routing-administration-13-0-0/5.html
