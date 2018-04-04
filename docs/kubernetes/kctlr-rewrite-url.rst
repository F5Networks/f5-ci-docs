:product: BIG-IP Controller for Kubernetes
:version: 1.5
:type: tutorial

.. _k8s url rewrite:

Rewrite URLs
============

Overview
--------

.. include:: /_static/reuse/k8s-version-added-1_5.rst

You can use the |kctlr| to rewrite URLs for Kubernetes Ingress resources and OpenShift Ingresses and Routes.

The Annotations are the same in both orchestration systems. The examples provided in this document are Kubernetes Ingress Resources. Their usage is no different in OpenShift Ingresses or Routes.

.. important::

   If you use both of the virtual-server.f5.com :code:`rewrite` Annotations for the same Service, the Controller applies them in the following order:

   #. :code:`app-root`
   #. :code:`target-url`

Usage
-----

You can add the :code:`rewrite` Annotations to any of the following resources:

- Kubernetes Ingress
- OpenShift Ingress
- OpenShift Route

.. seealso::

   - :ref:`create k8s ingress`
   - :ref:`create os route`

When using the Annotation(s) in a Single Service Ingress, Multi-Service Ingress, or Route resource, you can specify a **single value** in the annotation.

When using the Annotation(s) in a Multi-Service Ingress, you can specify a single value --OR-- **multiple, comma-separated** values.

Examples
--------

Rewrite App-Root
````````````````

.. sidebar:: Applies to:

   - Kubernetes Single-Service Ingress
   - Kubernetes Multi-Service Ingress
   - OpenShift Single-Service Ingress
   - OpenShift Multi-Service Ingress
   - OpenShift Route

Use the :code:`rewrite-app-root` Annotation to redirect requests for "/" to a different path.

.. code-block:: YAML
   :caption: Redirect "/" to "/home" for all traffic

   apiVersion: extensions/v1beta1
   kind: Ingress
   metadata:
     annotations:
       virtual-server.f5.com/rewrite-app-root: "/home"
     name: home
     namespace: default
   spec:
     rules:
     - http:
       paths:
       - backend:
           serviceName: http-svc
           servicePort: 80
           path: /home

.. code-block:: YAML
   :caption: Rewrite "/" to "/en" for traffic with host "docs.example.com"

   apiVersion: extensions/v1beta1
   kind: Ingress
   metadata:
     annotations:
       virtual-server.f5.com/rewrite-app-root: "docs.example.com=/en"
     name: docs-rewrite
     namespace: default
   spec:
     rules:
     - host: docs.example.com
       http:
         paths:
         - backend:
             serviceName: svc-docs
             servicePort: 80
             path: /docs-en
     - host: example.com
       http:
         paths:
         - backend:
             serviceName: svc-home
             servicePort: 80
             path: /home

.. code-block:: YAML
   :caption: Rewrite multiple paths in a single annotation

   apiVersion: extensions/v1beta1
   kind: Ingress
   metadata:
     annotations:
       virtual-server.f5.com/rewrite-app-root: "example.com=/home,docs.example.com=docs.example.com/en"
     name: photos-and-home
     namespace: default
   spec:
     rules:
     - host: example.com
       http:
         paths:
         - backend:
             serviceName: svc-home
             servicePort: 80
           path: /
     - host: docs.example.com
       http:
         paths:
         - backend:
             serviceName: svc-docs
             servicePort: 80
           path: /docs-en


Rewrite Target-URL
``````````````````

.. sidebar:: Applies to:

   - Kubernetes Multi-Service Ingress
   - OpenShift Multi-Service Ingress
   - OpenShift Route

Use the :code:`rewrite-target-url` Annotation to rewrite the exposed URL for a Service.
It can rewrite the :code:`host`, :code:`path`, or both to the specified target.

.. code-block:: YAML
   :caption: Rewrite URL for all traffic to old.example.com

   apiVersion: extensions/v1beta1
   kind: Ingress
   metadata:
     annotations:
       virtual-server.f5.com/rewrite-target-url: "new.example.com"
     name: rewrite-siteurl
     namespace: default
   spec:
     rules:
     - host: old.example.com
       http:
         paths:
         - backend:
             serviceName: new-svc
             servicePort: 80
             path: /my-site

.. code-block:: YAML
   :caption: Rewrite from a specific host and path to a different host and path

   apiVersion: extensions/v1beta1
   kind: Ingress
   metadata:
     annotations:
      virtual-server.f5.com/rewrite-target-url: "old.example.com/contact=new.example.com/about"
     name: rewrite-about
     namespace: default
   spec:
     rules:
     - host: old.example.com
       http:
         paths:
         - backend:
             serviceName: old-svc
             servicePort: 80
             path: /contact
   - host: old.example.com
       http:
         paths:
         - backend:
             serviceName: docs-svc
             servicePort: 80
             path: /docs

.. code-block:: YAML
   :caption: Rewrite multiple paths in a single annotation

   apiVersion: extensions/v1beta1
   kind: Ingress
   metadata:
     annotations:
       virtual-server.f5.com/rewrite-target-url: "old.example.com/contact=new.example.com/about,old.example.com/docs=new.example.com/docs"
     name: rewrite-about
     namespace: default
   spec:
     rules:
     - host: old.example.com
       http:
         paths:
         - backend:
             serviceName: old-svc
             servicePort: 80
             path: /contact
   - host: old.example.com
       http:
         paths:
         - backend:
             serviceName: docs-svc
             servicePort: 80
             path: /docs



