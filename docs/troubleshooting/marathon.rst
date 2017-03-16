.. _troubleshoot-marathon:

Troubleshoot Your Marathon Deployment
=====================================

|asp|
-----

"InsufficientPorts" Error
`````````````````````````

If Apache Mesos can't allocate the Service Port associated with an ASP instance, the ASP won't deploy. Port allocation commonly fails because the specified port is either already in use or it's out of range. Affected tasks in the Marathon queue will display an "InsufficientPorts" error.

.. rubric:: Solution:

Edit the Application definition and replace the service port with an available port in the correct range. See the Apache Mesos `ports resource <http://mesos.apache.org/documentation/latest/attributes-resources/>`_ to see what ports are available in your cluster.


|aspm-long|
-----------

Coming soon!

|mctlr-long|
------------

Coming soon!
