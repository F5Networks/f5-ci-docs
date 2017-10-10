The |kctlr| watches the Kubernetes API for resources that contain an F5 virtual server `Annotation`_.
The `Annotation`_ consists of a specially-formatted JSON blob defining the `k8s-bigip-ctlr virtual server configuration parameters`_.

When you add the :code:`virtual-server.f5.com` annotation to an :ref:`Ingress <kctlr-ingress-config>` or :ref:`Route <create os route>` resource, the |kctlr| creates a virtual server on the BIG-IP system with the settings you defined.
