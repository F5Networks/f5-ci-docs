Load Balancer Module
~~~~~~~~~~~~~~~~~~~~

This module queries the marathon-dns module for the current list of
servers and implements a load balancing algorithm to choose a back-end
server.

Features:

* Round-robin load balancing
* Collection of load balancing related statistics
