You can create RBAC resources in the project in which you will run your |kctlr|.
Each Controller that manages a device in a cluster or active-standby pair can use the same Service Account, Cluster Role, and Cluster Role Binding.

.. table:: Required RBAC Permissions

   +--------------+-----------------+-----------------------------------------+
   | API groups   | Resources       | Actions                                 |
   +==============+=================+=========================================+
   | ""           | endpoints,      | get, list, watch                        |
   |              | namespaces,     |                                         |
   |              | nodes,          |                                         |
   |              | routes,         |                                         |
   |              | services,       |                                         |
   |              | secrets         |                                         |
   +--------------+-----------------+-----------------------------------------+
   | "extensions" | ingresses       | get, list, watch                        |
   +--------------+-----------------+-----------------------------------------+
   | ""           | configmaps,     | get, list, watch, update, create, patch |
   |              | events          |                                         |
   +--------------+-----------------+-----------------------------------------+
   | "extensions" | ingresses/status| get, list, watch, update, create, patch |
   +--------------+-----------------+-----------------------------------------+

.. tip::

   Create the RBAC resources in the same Project (or namespace) as the |kctlr|, or in a Project the |kctlr| can access.

   If you need to be able to access the RBAC resources from all Projects, an OpenShift administrator should create them in the :code:`kube-system` namespace (:code:`-n kube-system`).

   In these cases, you can either:

   - use the Controller's default "watch all namespaces" setting (requires no additional configuration); or
   - set the Controller to watch both the :code:`kube-system` namespace and the Project's namespace.


#. Create a Service Account for the |kctlr|.

   .. parsed-literal::

      oc create serviceaccount bigip-ctlr [-n kube-system]
      serviceaccount "bigip-ctlr" created

#. Apply the **cluster-admin** Cluster Role to the BIG-IP Controller Service Account.

   .. parsed-literal::

      oc adm policy add-cluster-role-to-user cluster-admin -z bigip-ctlr [-n kube-system]

#. Create a `Cluster Role`_ and `Cluster Role Binding`_ with the required permissions.

   .. literalinclude:: /openshift/config_examples/f5-kctlr-openshift-clusterrole.yaml
      :emphasize-lines: 16


   :fonticon:`fa fa-download` :download:`f5-kctlr-openshift-clusterrole.yaml </openshift/config_examples/f5-kctlr-openshift-clusterrole.yaml>`

#. Upload the Cluster Role and Cluster Role Binding to the API server.

   .. parsed-literal::

      oc create -f f5-kctlr-openshift-clusterrole.yaml [-n kube-system]
      clusterrole "system:bigip-ctlr" created
      clusterrolebinding "bigip-ctlr-role" created


