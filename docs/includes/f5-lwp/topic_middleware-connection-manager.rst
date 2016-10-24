Connection Manager
~~~~~~~~~~~~~~~~~~

Overview
--------
This module is responsible for managing server connections which involves the following:

* Maintain a mapping of client to server connection
* Given a client connection, check if corresponding server connection exists; reuse connection if it already exists, else create a new one.
* Implement similar lookup in reverse direction (i.e., lookup client connection given server connection).
* Manage lifetime of server connection. Server connection is closed when:

    - client connection closes;
    - inactivity timeout fires.

Use Case
--------



Prerequisites
-------------

-
-
-


Caveats
-------

-
-
-


Configuration
-------------
.. comment:: explain applicable configuration PARAMETERS below

#.
#.
#.



Further Reading
---------------
.. comment:: provide links to relevant documentation (BIG-IP, other velcro projects, other docs in this project) here

.. seealso::

    * x
    * y
    * z
