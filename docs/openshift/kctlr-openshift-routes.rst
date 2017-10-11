.. _kctlr-openshift-routes:

Expose OpenShift Services to External Traffic using Routes
==========================================================

.. include:: /_static/reuse/k8s-version-added-1_2.rst

As described in the OpenShift documentation, the IP address assigned to an `OpenShift Pod`_ is only accessible from within the cluster network.

You can use the |kctlr-long| as a `Router`_ to:

- expose an `OpenShift Service`_ to external traffic via a BIG-IP virtual server;
- create BIG-IP `Local Traffic Policies`_ for OpenShift Services;
- :ref:`use BIG-IP SSL profiles to secure a Route <route-TLS>`; and
- :ref:`add a BIG-IP health monitor <add health monitor to route>` to a Route resource.

.. attention::

   All Route resources will share two virtual servers, "https-ose-vserver" for https traffic,
   and "ose-vserver" for http traffic. These are the default names of the virtual servers. You can
   change these names via the command line options.

   Allocate an external IP address for the virtual server *before* you set up the Route in OpenShift.

.. _create os route:

Create an OpenShift Route Resource
----------------------------------

Create a new `Route Resource`_.

.. _unsecured:

Unsecured
`````````

.. literalinclude:: /_static/config_examples/f5-openshift-unsecured-route.yaml
   :linenos:

:fonticon:`fa fa-download` :download:`f5-openshift-unsecured-route.yaml </_static/config_examples/f5-openshift-unsecured-route.yaml>`

.. _edge:

Edge Termination
````````````````

.. literalinclude:: /_static/config_examples/f5-openshift-edge-route.yaml
   :linenos:
   :emphasize-lines: 10-23

:fonticon:`fa fa-download` :download:`f5-openshift-edge-route.yaml </_static/config_examples/f5-openshift-edge-route.yaml>`

.. _passthrough:

Passthrough Termination
```````````````````````

.. literalinclude:: /_static/config_examples/f5-openshift-passthrough-route.yaml
   :linenos:
   :emphasize-lines: 10-11

:fonticon:`fa fa-download` :download:`f5-openshift-passthrough-route.yaml </_static/config_examples/f5-openshift-passthrough-route.yaml>`

.. _reencrypt:

Re-encryption Termination
`````````````````````````

.. literalinclude:: /_static/config_examples/f5-openshift-reencrypt-route.yaml
   :linenos:
   :emphasize-lines: 10-18

:fonticon:`fa fa-download` :download:`f5-openshift-reencrypt-route.yaml </_static/config_examples/f5-openshift-reencrypt-route.yaml>`

.. _route-TLS:

Use BIG-IP SSL Profiles to secure a Route
-----------------------------------------

By default, the controller creates custom BIG-IP SSL Profiles using 
the certificates and keys within the Route resource.

.. include:: /_static/reuse/k8s-version-added-1_3.rst

To instead use an existing `BIG-IP SSL profile`_ to secure traffic for a Route:


===   =========================================================================
1.    For a Client SSL profile, use the following annotation:

      :code:`virtual-server.f5.com/clientssl=<pre-existing-BIG-IP-profile-name>`

2.    For a Server SSL profile, use the following annotation:

      :code:`virtual-server.f5.com/serverssl=<pre-existing-BIG-IP-profile-name>`
===   =========================================================================

\

.. note:

These profiles apply to each individual Route. In addition to these, the controller creates one client ssl
and one server ssl profile for the https virtual server. These profiles are set as default for SNI. Their
names are "default-client-ssl" and "default-server-ssl". You can change these names via the command line
options.

.. _add health monitor to route:

Add a Health Monitor to a Route Resource
----------------------------------------

.. include:: /_static/reuse/k8s-version-added-1_3.rst

Use the :code:`virtual-server.f5.com/health` annotation with a JSON blob to create a BIG-IP health monitor for any OpenShift Route.

.. literalinclude:: /_static/config_examples/f5-openshift-route-health-monitor.yaml
   :caption: Health Monitor Example
   :linenos:
   :emphasize-lines: 5-14


.. _deploy route resource:

Deploy the Route Resource
-------------------------

Use :command:`oc create` to upload the Route Resource to the OpenShift API server.

.. code-block:: console

   oc create route -f <filename>.yaml
   route myRoute created

Verify creation of BIG-IP objects
---------------------------------

You can use TMOS or the BIG-IP configuration utility to verify that the |kctlr-long| created the requested BIG-IP objects for your Route.

To verify using the BIG-IP configuration utility:

#. Log in to the configuration utility at the management IP address (for example: :code:`https://10.190.25.225/tmui/login.jsp?`).
#. Select the correct partition from the :guilabel:`Partition` drop-down menu.
#. Go to :menuselection:`Local Traffic --> Virtual Servers` to view all virtual servers, pools, and pool members.
#. Go to :menuselection:`Local Traffic --> Policies` to view any new policies.

See the `TMSH Reference Guide`_ (PDF) for the relevant :command:`tmsh ltm` commands.



.. _OpenShift Pod: https://docs.openshift.com/enterprise/3.0/architecture/core_concepts/pods_and_services.html#pods
.. _Router: https://docs.openshift.com/enterprise/3.0/architecture/core_concepts/routes.html#routers
.. _OpenShift Service: https://docs.openshift.com/enterprise/3.0/architecture/core_concepts/pods_and_services.html#services
.. _Route Resource: https://docs.openshift.com/enterprise/3.0/architecture/core_concepts/routes.html
.. _TMSH Reference Guide: https://support.f5.com/kb/en-us/products/big-ip_ltm/manuals/product/bigip-tmsh-reference-12-0-0.html