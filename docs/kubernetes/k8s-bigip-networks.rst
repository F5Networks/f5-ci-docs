.. index::
   :pair: Kubernetes, BIG-IP
   :single: concept
   :triple: Kubernetes, networking, BIG-IP

.. _k8s-bigip-networks:

How the BIG-IP Controller handles network configurations in Kubernetes
======================================================================

The |kctlr-long| controller configures services on the BIG-IP device to expose applications inside your Kubernetes cluster to external users.
In certain deployments, the |kctlr| also handles some networking configurations on BIG-IP devices.

There are a number of options when it comes to connecting a BIG-IP device (physical or Virtual Edition) to a Kubernetes `Cluster Network`_, as noted below.
You can choose the one that best applies to your Kubernetes environment.

- OpenShift clusters using the default VXLAN overlay network.
- Kubernetes clusters where pods are directly addressable (like Calico BGP).
- Kubernetes clusters using an overlay with manual config (like VXLAN).
- All other Kubernetes clusters using NodePort.
.. Kubernetes clusters using Flannel VXLAN overlay network (since 1.2.0). Not available yet.

Overlay Networks
----------------

If using manual config:

SDN
```

If using `OpenShift SDN`_ in `OpenShift Origin`_:

- ``ovs-subnet``: BIG-IP can find all pods in the cluster; all pods can communicate with all other pods and services.
- ``ovs-multitenant``: Allows "project-level isolation for pods and services";
  BIG-IP can find all pods and services in the cluster when deployed in the ``default`` project (route domain 0). [#originsdn]_
- The BIG-IP device can allocate IP addresses for virtual servers and pool members from designated subnet(s).

.. seealso::

   Link to OpenShift feature parity page

Questions:
~~~~~~~~~~

- What BIG-IP pre-configs are required?
- Do we have to set up VLANs on BIG-IP with subnets allocated from the VXLAN overlay?
- How does SDN support work? Does the controller dynamically create VLANs on the BIG-IP when it discovers them? Or just routes?



Container Networking Providers
------------------------------

Directly addressable pods; policy-based networking; "works like the internet does"

Project Calico
``````````````

If using `Calico for Kubernetes`_:


Calico BGP https://docs.projectcalico.org/v2.4/usage/configuration/bgp

Questions:

- How does this work?
- What BIG-IP pre-configs are required?
- Do we have to set up VLANs on BIG-IP

Flannel
```````

see canal: https://github.com/projectcalico/canal

**future dev**

Kubernetes NodePort
-------------------

https://kubernetes.io/docs/concepts/architecture/nodes/


.. rubric:: Footnotes
.. [#originsdn] `OpenShift SDN <https://docs.openshift.org/1.4/architecture/additional_concepts/sdn.html#architecture-additional-concepts-sdn>`_ ; accessed 16 Aug 2017.



.. _Cluster Network: https://kubernetes.io/docs/concepts/cluster-administration/networking/
.. _OpenShift SDN: https://docs.openshift.org/1.4/architecture/additional_concepts/sdn.html
.. _Flannel: https://docs.openshift.org/1.4/architecture/additional_concepts/flannel.html
.. _Open vSwitch VXLAN network: https://kubernetes.io/docs/admin/ovs-networking/
.. _Calico for Kubernetes: https://docs.projectcalico.org/latest/getting-started/kubernetes/
