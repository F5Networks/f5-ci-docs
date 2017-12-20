Troubleshoot Your Kubernetes Deployment
=======================================

.. toctree::
   :maxdepth: 1

How to get help
---------------

If the issue you're experiencing isn't covered here, try one of the following options:

- `Contact F5 Support`_ (valid support contract required).
- `Report a bug <https://github.com/F5Networks/k8s-bigip-ctlr/issues>`_ in the k8s-bigip-ctlr GitHub repo.
- `Join the F5 Cloud Solutions Slack team <https://f5cloudsolutions.herokuapp.com/>`_ and ask a question in the #cc-kubernetes channel.


General Kubernetes troubleshooting
----------------------------------

The following troubleshooting docs may help with Kubernetes-specific issues.

- `Kubernetes: Troubleshoot Applications <https://kubernetes.io/docs/tasks/debug-application-cluster/debug-application/>`_ :fonticon:`fa fa-external`
- `Kubernetes: Troubleshoot Clusters <https://kubernetes.io/docs/tasks/debug-application-cluster/debug-cluster/>`_ :fonticon:`fa fa-external`


.. _k8s-bigip-ctlr troubleshoot:

BIG-IP Controller troubleshooting
---------------------------------

.. hint::

   You can use `kubectl`_ commands to check the |kctlr| configurations using the command line.

   .. code-block:: console

      kubectl get pod -o yaml [--namespace=kube-system]          \\ Returns the Pod's YAML settings
      kubectl describe pod myBigIpCtlr [--namespace=kube-system] \\ Returns an information dump about the Pod you can use to troubleshoot specific issues

.. hint::

   When in doubt, restart the Controller.

   Just like your wifi at home, sometimes you just need to turn it off and turn it back on again. With the |kctlr|, you can do this by deleting the ``k8s-bigip-ctlr`` Pod. A new Pod deploys automatically, thanks to the `ReplicaSet`_.

   .. code-block:: console

      kubectl get pod --namespace=kube-system
      NAME                             READY     STATUS            RESTARTS   AGE
      k8s-bigip-ctlr-687734628-7fdds   0/1       CrashLoopBackoff  2          15d

      kubectl delete pod k8s-bigip-ctlr-687734628-7fdds --namespace=kube-system

.. _controller verify k8s:

I just deployed the Controller; how do I verify that it's running?
``````````````````````````````````````````````````````````````````

#. Find the name of the k8s-bigip-ctlr Pod.

   .. code-block:: console

      kubectl get pod --namespace=kube-system
      NAME                             READY     STATUS    RESTARTS   AGE
      k8s-bigip-ctlr-687734628-7fdds   1/1       Running   0          15d

#. Check the status of the Pod.

   .. code-block:: console

      Kubectl get pod k8s-bigip-ctlr-687734628-7fdds -o yaml --namespace=kube-system

   .. _troubleshoot openshift view-logs:

#. View the Controller logs.

   .. code-block:: console
      :caption: View the logs

      kubectl logs k8s-bigip-ctlr-687734628-7fdds --namespace=kube-system

   .. code-block:: console
      :caption: Follow the logs

      kubectl logs -f k8s-bigip-ctlr-687734628-7fdds --namespace=kube-system


   .. code-block:: console
      :caption: View logs for a container that isn't responding

      kubectl logs --previous k8s-bigip-ctlr-687734628-7fdds --namespace=kube-system


How do I set the log level?
~~~~~~~~~~~~~~~~~~~~~~~~~~~

To change the log level for the |kctlr|:

#. Annotate the :ref:`Deployment <k8s-bigip-ctlr-deployment>` for the |kctlr|.

   .. code-block:: console

      kubectl annotate k8s-bigip-ctlr.yaml "--log-level=DEBUG" --namespace=kube-system

#. Verify the Deployment updated successfully.

   .. code-block:: console

      kubectl describe deployment k8s-bigip-ctlr -o wide --namespace=kube-system

Why didn't the k8s-bigip-ctlr show up when I ran "get pods"?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you launched the |kctlr| in the ``--kube-system`` namespace, you should add the ``--namespace`` flag to your :command:`kubectl get` command.

.. code-block:: console

   kubectl get pod --namespace=kube-system
   kubectl get pod myBigIpCtlr --namespace=kube-system


-----------------------------------------

.. _bigip-config warning k8s:

.. include:: /_static/reuse/bigip-conf-overwrite.rst

-----------------------------------------


The BIG-IP pool members use the Kubernetes Node IPs instead of the Pod IPs
``````````````````````````````````````````````````````````````````````````

The |kctlr| uses node IPs when running in its default mode, ``nodeport``. See :ref:`Nodeport mode vs Cluster mode <kctlr modes>` for more information.

-----------------------------------------

Why didn't the BIG-IP Controller create any objects on my BIG-IP?
`````````````````````````````````````````````````````````````````

Check the |kctlr| settings against those of the Service you want it to watch to make sure everything aligns correctly.

Do the namespaces match?
~~~~~~~~~~~~~~~~~~~~~~~~

By default, the |kctlr| watches all Kubernetes `Namespaces`_ (as of v1.3.0). If you do specify a Namespace to watch in the k8s-bigip-ctlr Deployment, make sure it matches that of the Kubernetes Resources you want to manage.

In the examples below, the Namespace in the Service doesn't match that provided in the sample Deployment. [#servicesrc]_

.. code-block:: yaml
   :caption: Sample Kubernetes Service
   :emphasize-lines: 4,5

   kind: Service
   apiVersion: v1
   metadata:
     name: hello
   namespace: test


.. code-block:: yaml
   :caption: Excerpt from a sample Deployment
   :emphasize-lines: 12-13

   apiVersion: extensions/v1beta1
   kind: Deployment
   metadata:
     name: k8s-bigip-ctlr-deployment
     namespace: kube-system
   ...
             args: [
               "--bigip-username=$(BIGIP_USERNAME)",
               "--bigip-password=$(BIGIP_PASSWORD)",
               "--bigip-url=10.190.24.171",
               "--bigip-partition=kubernetes",
               # THE LINE BELOW TELLS THE CONTROLLER WHAT NAMESPACE TO WATCH
               "--namespace=prod",
               ]
   ...


Are the Service name and port correct?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Make sure the name and port in your virtual server ConfigMap match those defined for the Service.

==============================   ==================================
Service field                    ConfigMap ``data.data.`` field
==============================   ==================================
metadata.name                    virtualServer.backend.serviceName
spec.ports.[port | targetPort]   virtualServer.backend.servicePort
==============================   ==================================

In the examples below, the servicePort and serviceName don't match the name and port in the example Service. [#servicesrc]_

.. code-block:: yaml
   :caption: Sample Kubernetes Service
   :emphasize-lines: 4,13

   kind: Service
   apiVersion: v1
   metadata:
     name: hello
   namespace: test
   spec:
     selector:
       app: hello
       tier: backend
     ports:
     - protocol: TCP
       port: 80
       targetPort: http

.. code-block:: yaml
   :caption: Excerpt from a sample virtual server ConfigMap
   :emphasize-lines: 10-11

   kind: ConfigMap
   apiVersion: v1
   ...
   data:
    schema: "f5schemadb://bigip-virtual-server_v0.1.4.json"
     data: |
       {
         "virtualServer": {
           "backend": {
             "servicePort": 8080,
             "serviceName": "helo",
           },
      ...
       }

.. [#servicesrc] *Example Service referenced from* `Connect a Front End to a Back End Using a Service <https://kubernetes.io/docs/tasks/access-application-cluster/connecting-frontend-backend/#creating-the-backend-service-object>`_

Do the service types match?
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The default type used for `Services`_ in Kubernetes is ``clusterIP``. The corresponding setting for the k8s-bigip-ctlr -- ``pool-member-type`` -- defaults to ``nodeport``.

**If you didn't specify a type** in the Service definition --OR-- a ``pool-member-type`` in the |kctlr| Deployment, you probably have a service type mismatch.

See :ref:`Nodeport mode vs Cluster mode <kctlr modes>` for more information about each service type and its recommended use.


.. _json troubleshoot k8s:

.. include:: /_static/reuse/controller-json-troubleshoot.rst

.. _schema troubleshoot k8s:

.. include:: /_static/reuse/schema-troubleshoot.rst

.. _bigip-partition troubleshoot k8s:

.. include:: /_static/reuse/bigip-partition-troubleshoot.rst

-----------------------------------------

Why didn't the |kctlr| create the pools/rules for my Ingress?
`````````````````````````````````````````````````````````````

When you create multiple rules in an Ingress that overlap, Kubernetes silently drops all but one of them. If you don't see all of the pools and/or rules you expect to see on the BIG-IP system, double-check your Ingress resource for redundant or overlapping settings.

For example, say you want to create a pool for your website's frontend app, with one (1) pool member for each of the Services comprising the app.

.. code-block:: yaml
   :caption: Good: 1 rule that includes both Services comprising the frontend app

   host: mysite.example.com
      path: /frontend
      - service: svc1
      - service: svc2

.. code-block:: yaml
   :caption: Bad: 2 rules that both attempt to route traffic for the frontend app

   host: mysite.example.com
      path: /frontend
      - service: svc1

   host: mysite.example.com
      path: /frontend
      - service: svc2

In the latter case, Kubernetes would drop one of the overlapping rules and the |kctlr| would only create one (1) pool member on the BIG-IP system.

-----------------------------------------

Why don't my Annotations work?
``````````````````````````````

Are you using Annotations recommended for a different `Kubernetes Ingress Controller`_ ?

**Annotations aren't universally applicable**. You should only use Annotations included in the list of `Ingress annotations`_ supported by the |kctlr|.

-----------------------------------------

.. _iapp traffic group:

Why did I see a traffic group error when I deployed my iApp?
````````````````````````````````````````````````````````````

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

