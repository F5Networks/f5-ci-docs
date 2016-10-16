Using |fp| in Kubernetes
------------------------

|fp| can be deployed in a Kubernetes cluster to handle services within the Kubernetes cluster.
|fp| is deployed as a replacement for kube-proxy, and will optionally add enhanced processing to Kubernetes service traffic.


Configuring Services
````````````````````

Once installed, |fp| features can be configured on a service by adding a special annotation ``flowpoint.f5.com/config``

The value of this annotation should be a string containing a json object. The object is the same as for a virtual server, except for some properties.

.. topic:: Example Config value

    .. code-block:: yaml

        {
          "ip-protocol": "http",
          "load-balancing-mode": "round-robin",
          "flags" : {
            "x-forwarded-for": false,
            "x-served-by": true
          }
        }

When included in a service this object is a string.

.. topic:: Example Service 

    .. literalinclude:: ../static/example-service-flowpoint.yaml

    :download:`example-service-flowpoint.yaml <../static/example-service-flowpoint.yaml>`


Installing
``````````
|fp| in Kubernetes is composed of two parts. One privileged service that manages the iptables rules of the host, and the Flowpoint proxy to handle enhanced service traffic.


Replace kube-proxy
~~~~~~~~~~~~~~~~~~

In your Kubernetes cluster, replace the kube-proxy instance on every node with f5-kube-proxy, and setup a services configuration volume that |fp| will consume.

Assuming that kube-proxy is being run in a static pod, the new manifest file ``/etc/kubernetes/manifests/kube-proxy.yaml`` will look like the following.

.. topic:: Example Static Pod

    .. literalinclude:: ../static/example-kube-proxy-manifest.yaml
       :language: yaml

    :download:`example-kube-proxy-manifest.yaml <../static/example-kube-proxy-manifest.yaml>`



Run |fp| DaemonSet
~~~~~~~~~~~~~~~~~~

|fp| needs to be run on every node in the cluster, just like kube-proxy. This can be easily done with a DaemonSet, and a ConfigMap resource.

The global |fp| configuration is specified in a ConfigMap.
Note that the orchestration.kubernetes.config-file property points to a volume mounted by the |fp| DaemonSet spec

.. topic:: |fp| Config

    .. literalinclude:: ../static/example-flowpoint-configmap.yaml
       :language: yaml

    :download:`example-flowpoint-configmap.yaml <../static/example-flowpoint-configmap.yaml>`


The |fp| DaemonSet will ensure that a |fpp| instance is running on ever node in the Kubernetes cluster.
Note that it uses the ConfigMap to provide the config file, and that it mounts a volume that provides the service-ports.json config file at the path listed in the ConfigMap.

.. topic:: |fp| DaemonSet

    .. literalinclude:: ../static/example-flowpoint-daemonset.yaml
       :language: yaml

    :download:`example-flowpoint-daemonset.yaml <../static/example-flowpoint-daemonset.yaml>`

