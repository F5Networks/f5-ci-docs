.. _troubleshoot-marathon:

Troubleshoot Your Marathon Deployments
======================================

|mctlr-long|
------------

|aspm-long|
-----------


|asp|
-----

"InsufficientPorts" Error
`````````````````````````

If the Service Port associated with an ASP instance cannot be allocated, the ASP will not deploy. Common reasons for port allocation failure include the specified port already being in use or out of range. Affected tasks in the Marathon queue will display an "InsufficientPorts" error.

.. rubric:: Solution:

Edit the Application definition and replace the service port with an available port in the correct range. See the Mesos `ports resource <http://mesos.apache.org/documentation/latest/attributes-resources/>`_ to see what ports are available in your cluster.


