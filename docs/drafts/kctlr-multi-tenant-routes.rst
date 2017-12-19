
.. _openshift routes multi-tenant:

Multi-tenancy with Routes and Partitions in OpenShift
=====================================================



-------------------------------------------------------------------------------

Background


Route domains and administrative partitions:

- completely separate network environments
- common route domain for frontend network
- use virtual server on each tenant to connect to common route domain
- control access to tenants via virtual server connected to the common route domain

\

-------------------------------------------------------------------------------



.. _deploy kctlr multi-tenant partitions:

Run one k8s-bigip-ctlr instance per partition
---------------------------------------------

.. table:: Task table

   =======  ===================================================================
   Step     Task
   =======  ===================================================================
   1.       :ref:`kctlr create deployment multi-tenant`

   2.

   3.       ??

   4.       Verify object creation
   =======  ===================================================================

.. _create deployment partitions:

Create a Deployment
```````````````````

To launch one instance of the |kctlr| for each BIG-IP partition, take the steps below.

#. Define the desired number of |kctlr| instances as separate Deployments. Be sure to enter the name of the BIG-IP partition you want to manage in the "containr.arg" section of the Deployment.

   .. note::

      While it is possible to define multiple container instances in a single Deployment file, it isn't recommended. If you choose to do so, be aware that the instances will share the same ReplicaSet, run on the same Pod(s), and share Service Account permissions.

   .. literalinclude:: /kubernetes/config_examples/f5-k8s-bigip-ctlr_multi-tenant-deployment.yaml
      :linenos:
      :emphasize-lines: 31, 53

#. Upload the Deployment to the API server using :command:`kubectl apply` or :command:`oc apply`.

   .. code-block:: console

      kubectl apply -f f5-k8s-bigip-ctlr_multi-tenant-deployment.yaml


Create a front-end virtual server
`````````````````````````````````



.. _deploy kctlr multi-tenant namespaces:

Manage namespaces
-----------------

.. table:: Task table

   =======  ===================================================================
   Step     Task
   =======  ===================================================================
   1.       :ref:`multi-tenant deployment`

   2.

   3.       ??

   4.       Verify object creation
   =======  ===================================================================

In both Kubernetes and OpenShift, you can define the `global configuration parameters`_ for the |kctlr| in a Deployment.
To launch multiple instances of the |kctlr|, you can define multiple Deployments in a single YAML/JSON file.

.. _create deployment namespaces:

.. literalinclude:: /kubernetes/config_examples/f5-k8s-bigip-ctlr_image-secret.yaml
   :linenos:
   :emphasize-lines: 35
   :caption: Example Kubernetes Deployment manifest

When creating a Deployment, provide the name of the partition you want the |kctlr| to manage.

Deploy virtual servers
``````````````````````
