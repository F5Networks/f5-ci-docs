.. index::
   single: BIG-IP Controller; OpenShift; Route; F5 Router; BIG-IP

.. include:: /_static/reuse/k8s-version-added-1_2.rst

.. _kctlr-openshift-routes:

Expose OpenShift Services to External Traffic using Routes
==========================================================

Overview
--------

As described in the OpenShift documentation, the IP address assigned to an `OpenShift Pod`_ is only accessible from within the cluster network. You can use the |kctlr| for OpenShift as a router to expose Services to external traffic.

When you use the |kctlr| as a `Router`_, you can

- create BIG-IP `Local Traffic Policies`_ for OpenShift Services;
- :ref:`use BIG-IP SSL profiles to secure a Route <route-TLS>`; and
- :ref:`add a BIG-IP health monitor to a Route resource <add health monitor to route>`.

.. attention::

   - All Route resources share two virtual servers:

     - "ose-vserver" for HTTP traffic, and
     - "https-ose-vserver" for HTTPS traffic.

     These are the default names used for the virtual servers. You can set custom names for HTTP and HTTPS virtual servers using the :code:`route-http-vserver` and :code:`route-https-vserver` configuration parameters, respectively.

.. table:: Task table

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

Set up the |kctlr| to manage Routes
-----------------------------------

If you haven't already done so, add the |kctlr| `Route configuration parameters`_ to the |kctlr| Deployment:

.. literalinclude:: /openshift/config_examples/f5-kctlr-openshift-routes.yaml
   :linenos:
   :emphasize-lines: 47-56


.. _create os route:

Create a new OpenShift Route Resource
-------------------------------------

To use the BIG-IP device as an OpenShift Router, create a new `Route Resource`_. The |kctlr| supports use of the following Route Resource types:

- :ref:`unsecured`
- :ref:`edge`
- :ref:`passthrough`
- :ref:`reencrypt`

.. _unsecured:

Unsecured
`````````

.. todo:: Add one-line description of unsecured route

.. literalinclude:: /openshift/config_examples/f5-openshift-unsecured-route.yaml
   :linenos:

:fonticon:`fa fa-download` :download:`f5-openshift-unsecured-route.yaml </openshift/config_examples/f5-openshift-unsecured-route.yaml>`

.. _edge:

Edge Termination
````````````````

.. todo:: Add one-line description of edge-terminated route

.. literalinclude:: /openshift/config_examples/f5-openshift-edge-route.yaml
   :linenos:

:fonticon:`fa fa-download` :download:`f5-openshift-edge-route.yaml </openshift/config_examples/f5-openshift-edge-route.yaml>`

.. _passthrough:

Passthrough Termination
```````````````````````

.. todo:: Add one-line description of passthrough-termination route

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

#. Define the :code:`virtual-server.f5.com/health` annotation JSON blob using the |kctlr| supported `route annotations`_.

#. Add the health monitor annotation to the Route Resource.

   .. literalinclude:: /openshift/config_examples/f5-openshift-route-health-monitor.yaml
      :caption: Health Monitor Example
      :linenos:
      :emphasize-lines: 5-14

.. _route-TLS:

SSL Profiles
````````````

.. include:: /_static/reuse/k8s-version-added-1_3.rst

By default, the Controller creates custom BIG-IP SSL Profiles using the certificates and keys defined in the Route resource.
You can also use an existing `BIG-IP SSL profile`_ to secure traffic for a Route.

- For a Client SSL profile, annotate the Route resource as shown below:

  .. code-block:: console

     oc annotate route <route_name> virtual-server.f5.com/clientssl=<BIG-IP-SSL-profile-name>


- For a Server SSL profile, annotate the Route resource as shown below:

  .. code-block:: console

     oc annotate route <route_name> virtual-server.f5.com/serverssl=<BIG-IP-SSL-profile-name>

.. note::

   Each SSL profile applies to one (1) individual Route. In addition, the Controller creates one client ssl
   and one server ssl profile for the https virtual server, called "default-client-ssl" and "default-server-ssl".
   **These are the default profiles used for SNI.**


.. _deploy route resource:

Deploy the Route Resource
-------------------------

Use :command:`oc create` to upload the Route Resource to the OpenShift API server.

.. code-block:: console

   oc create route -f <filename>.yaml
   route myRoute created

.. _verify BIG-IP route objects:

Verify creation of BIG-IP objects
---------------------------------

You can use TMOS or the BIG-IP configuration utility to verify that the |kctlr| created the requested BIG-IP objects for your Route.

To verify using the BIG-IP configuration utility:

#. Log in to the configuration utility at the management IP address (for example: :code:`https://10.190.25.225/tmui/login.jsp?`).
#. Select the correct partition from the :guilabel:`Partition` drop-down menu.
#. Go to :menuselection:`Local Traffic --> Virtual Servers` to view all virtual servers, pools, and pool members.
#. Go to :menuselection:`Local Traffic --> Policies` to view all of the policies configured in the partition.

To verify using TMOS, see the `TMSH Reference Guide`_ (PDF) for the relevant :command:`tmsh` commands.



.. _OpenShift Pod: https://docs.openshift.com/enterprise/3.0/architecture/core_concepts/pods_and_services.html#pods
.. _Router: https://docs.openshift.com/enterprise/3.0/architecture/core_concepts/routes.html#routers
.. _OpenShift Service: https://docs.openshift.com/enterprise/3.0/architecture/core_concepts/pods_and_services.html#services
.. _Route Resource: https://docs.openshift.com/enterprise/3.0/architecture/core_concepts/routes.html
.. _TMSH Reference Guide: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/bigip-tmsh-reference-12-0-0.html
.. _BIG-IP Self IP address: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/tmos-routing-administration-13-0-0/5.html
