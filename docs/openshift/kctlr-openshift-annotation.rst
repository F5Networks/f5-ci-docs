:product: BIG-IP Controller for Kubernetes
:type: task

.. _kctlr-openshift-annotation:

OpenShift: Modifying a HOST IP address using annotations
========================================================

When a cluster member uses an unexpected **HOST** IP address, you can use **annotations** to modify the cluster member configuration. In this example, the cluster member **worker.example.net** should be using **HOST** IP address **172.16.1.20**.

.. code-block:: console
   :emphasize-lines: 4

   oc get hostsubnet
   NAME                  HOST                  HOST IP         SUBNET
   f5-bigip-node         f5-bigip-node         172.16.1.30     10.130.0.0/23
   worker.example.net    worker.example.net    192.168.1.20    10.129.0.0/23
   master.example.net    master.example.net    172.16.1.10     10.128.0.0/23

You can use this procedure to modify the **HOST** IP address of a cluster member using annotations.

#. Ensure the new IP address exists on one of the cluster member interfaces. 

   .. code-block:: console
      :emphasize-lines: 3

      ifconfig ens33    
      ens33: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
             inet 172.16.1.20  netmask 255.255.255.0  

#. Obtain the MAC address (ether) of the **tun0** interface.

   .. code-block:: console
      :emphasize-lines: 4

      ifconfig tun0
      tun0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1450
            inet 10.129.0.1  netmask 255.255.254.0
            ether aa:47:58:98:be:67 

#. Create a **HostSubnet** resource with annotations for the new IP and MAC addresses.

   .. code-block:: console
      :emphasize-lines: 6-7

      apiVersion: v1
      kind: HostSubnet
      metadata:
        name: worker.example.net
        annotations:
          flannel.alpha.coreos.com/public-ip: 172.16.1.20
          flannel.alpha.coreos.com/backend-data: '{"VtepMAC":"aa:47:58:98:be:67"}'

      host: worker.example.net
      hostIP: 172.16.1.20

#. Apply the **HostSubnet** resource using the :command:`oc apply` command.

   .. parsed-literal::

      oc apply -f worker-hostsubnet.yml
      hostsubnet.network.openshift.io/worker.example.net configured

#. Verify the cluster member **HOST** IP address is updated.

   .. code-block:: console
      :emphasize-lines: 4

      oc get hostsubnet
      NAME                  HOST                  HOST IP         SUBNET
      f5-bigip-node         f5-bigip-node         172.16.1.30     10.130.0.0/23
      worker.example.net    worker.example.net    172.16.1.20     10.129.0.0/23
      master.example.net    master.example.net    172.16.1.10     10.128.0.0/23


