:product: BIG-IP Controller for Kubernetes
:type: task


.. _kctlr-openshift-routes:

Attach Virtual Servers to OpenShift Routes
==========================================

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

            - :ref:`route existing virtual`

   2.       :ref:`create os route`

   3.       :ref:`deploy route resource`

   4.       :ref:`verify BIG-IP route objects`

   5.       :ref:`attach bigip objects routes`

            - :ref:`add health monitor to route`
            - :ref:`route-TLS`
            - :ref:`delete vs route`

   =======  ===================================================================


.. _route existing virtual:

Attach Routes to Existing BIG-IP Virtual Servers
------------------------------------------------

.. include:: /_static/reuse/k8s-version-added-1_5.rst

If you need to use BIG-IP system functionality that isn't natively supported by the |kctlr|, you can attach a Route to an existing BIG-IP virtual server.
Take the steps below **before** you deploy the |kctlr|.

**If you want the** |kctlr| **to create a new virtual server for your Route,** :ref:`skip to the Basic Deployment section <kctlr routes basic>`.

#. Create a virtual server in a BIG-IP partition that isn't already managed by a |kctlr| instance.

#. Customize the virtual server as needed. Be sure the settings applied don't conflict with those you want the Controller to apply for the Route.

#. In a TMOS shell, run the commands shown below to set the :code:`cccl-whitelist` metadata field. This field tells the Controller it should merge its configuration into the existing virtual instead of overwriting it.

   - Make sure you're in the correct partition (for example, :code:`user@(BIG-IP)(cfg-sync Standalone)(Active)(/myPartition)(tmos)`).
   - Replace "myVirtual" with the name of the virtual server on your BIG-IP device.

   .. parsed-literal::

      modify ltm virtual **myVirtual** metadata add { cccl-whitelist { value 1 }}


.. _set up kctlr routes:

Deploy the BIG-IP Controller
----------------------------

.. include:: /_static/reuse/kctlr-openshift-deployment-note.rst

.. _kctlr routes basic:

Basic Deployment
````````````````

Create a Kubernetes Deployment using valid YAML or JSON.
Define the |kctlr| `Route configuration parameters`_ as appropriate to suit your needs.

.. literalinclude:: /openshift/config_examples/f5-k8s-bigip-ctlr_openshift_routes.yaml
   :linenos:

:fonticon:`fa fa-download` :download:`f5-k8s-bigip-ctlr_openshift_routes.yaml </openshift/config_examples/f5-k8s-bigip-ctlr_openshift_routes.yaml>`

.. warning::

   Use caution when setting the :code:`--route-vserver-addr` and :ref:`specifying a BIG-IP SNAT pool <kctlr-openshift snat deploy>`.

   If you choose to set both options, make sure the IP address defined for the virtual server falls within the range of the selected SNAT pool.

.. _kctlr routes existing virtual:

Manage a Pre-Existing Virtual Server
````````````````````````````````````

Create a Kubernetes Deployment using valid YAML or JSON.

- Define the |kctlr| `Route configuration parameters`_ as appropriate to suit your needs.
- Provide the name of the BIG-IP virtual server to which you want to attach the Route to the |kctlr| Deployment. The config parameter to use depends on the type of virtual server (HTTP or HTTPS)

  - :code:`route-http-vserver` -- HTTP virtual server.
  - :code:`route-https-vserver` -- HTTPS virtual server.

.. rubric:: Example :code:`k8s-bigip-ctlr` args:

.. code-block:: YAML
   :emphasize-lines: 9

   args: [
         "--bigip-username=$(BIGIP_USERNAME)",
         "--bigip-password=$(BIGIP_PASSWORD)",
         "--bigip-url=10.10.10.10",
         "--bigip-partition=myPartition",
         "--pool-member-type=cluster",
         "--openshift-sdn-name=/Common/openshift_vxlan",
         "--manage-routes=true",
         "--route-http-vserver=myVirtual"
         ]

.. warning::

   When you attach an OpenShift Route to an existing BIG-IP virtual server, the |kctlr| attempts to merge its settings with the existing object configurations on the BIG-IP device. If conflicts occur, the Controller will attempt to replace the existing setting on the BIG-IP system with its own configuration. If the |kctlr| cannot create the requested objects, you can find the resulting error message in the |kctlr| logs.

   See :ref:`OpenShift troubleshooting <troubleshoot openshift view-logs>` for more information about viewing the Controller logs.


Upload the Deployment to the OpenShift API Server
`````````````````````````````````````````````````

Use the :command:`oc create` command to upload the Deployment to the OpenShift API server.

.. parsed-literal::

   oc create -f **f5-k8s-bigip-ctlr_openshift-sdn.yaml** **[-n kube-system]**
   deployment "k8s-bigip-ctlr" created

.. seealso:: See :ref:`upload openshift deployment` for additional information.

.. _create os route:

Create an OpenShift Route Resource
----------------------------------

To use the BIG-IP device as an OpenShift Router, add the |kctlr| `OpenShift Route Annotations`_ to a `Route Resource`_.
The |kctlr| supports the following types of Route Resource:

- :ref:`unsecured`
- :ref:`edge`
- :ref:`passthrough`
- :ref:`reencrypt`

.. _openshift url rewrite:

Rewrite URLs for Routes
```````````````````````

.. include:: /_static/reuse/k8s-version-added-1_5.rst

The |kctlr| can rewrite URLs for Routes. See :ref:`k8s url rewrite` for more information.

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

.. _deploy route resource:

Upload the Route to the OpenShift API server
--------------------------------------------

Use the :command:`oc apply` command to upload your Route resource to the OpenShift API server.

.. include:: /_static/reuse/oc-apply.rst


.. _verify BIG-IP route objects:

Verify creation of BIG-IP objects
---------------------------------

.. include:: /_static/reuse/verify-bigip-objects.rst


.. _attach bigip objects routes:

Manage BIG-IP objects for Routes
--------------------------------

Use the |kctlr| `Route annotations`_ to attach various types of BIG-IP objects to the virtual servers corresponding to OpenShift Routes.


.. _add health monitor to route:

Health monitors
```````````````

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

.. _delete vs route:

Delete a Route's virtual server
```````````````````````````````

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
