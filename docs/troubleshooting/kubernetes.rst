Troubleshoot Your Kubernetes Deployment
=======================================

BIG-IP Controller
-----------------

.. _iapp traffic group:

iApp traffic group configuration error
``````````````````````````````````````

When deploying an iApp with the |kctlr-long| and OpenShift, the iApp may create a virtual IP in the wrong traffic group. If this occurs, you will see an error message like that below.

.. code-block:: console

   Configuration error: Unable to to create virtual address (/kubernetes/127.0.0.2) as part of application
   (/k8s/default_k8s.http.app/default_k8s.http) because it matches the self ip (/Common/selfip.external)
   which uses a conflicting traffic group (/Common/traffic-group-local-only)

If you've seen this error, you can override or change the default traffic-group as follows:

- Set the specific traffic group you need in the ``iappOptions`` section of the virtual server F5 Resource definition.
- **Preferred** Set the desired traffic group as the default for the partition you want the |kctlr| to manage. This option doesn't require Kubernetes/OpenShift to know about BIG-IP traffic groups.

.. code-block:: javascript

   "trafficGroup": "/Common/traffic-group-local-only"
